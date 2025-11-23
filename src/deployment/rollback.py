"""
Automated rollback management for deployments.

This module provides a RollbackManager class that handles automated rollback
of failed deployments, including stopping deployments, routing traffic back
to stable versions, and cleaning up failed resources.
"""

import asyncio
import time
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


class RollbackStatus(Enum):
    """Status of a rollback operation."""
    IDLE = "idle"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


class RollbackReason(Enum):
    """Reason for rollback."""
    MANUAL = "manual"
    HEALTH_CHECK_FAILURE = "health_check_failure"
    METRICS_DEGRADATION = "metrics_degradation"
    DEPLOYMENT_TIMEOUT = "deployment_timeout"
    ERROR_THRESHOLD_EXCEEDED = "error_threshold_exceeded"
    RESOURCE_EXHAUSTION = "resource_exhaustion"


@dataclass
class DeploymentSnapshot:
    """Snapshot of deployment state before rollback."""
    version: str
    timestamp: datetime
    instances: List[Dict[str, Any]]
    traffic_config: Dict[str, int]
    health_score: float
    metrics: Dict[str, Any]


@dataclass
class RollbackResult:
    """Result of a rollback operation."""
    success: bool
    reason: RollbackReason
    rollback_duration: float
    previous_version: str
    target_version: str
    message: str
    steps_completed: List[str]
    steps_failed: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


class RollbackManager:
    """
    Automated rollback management for deployments.

    Handles the complete rollback process including stopping failed deployments,
    routing traffic back to stable versions, and cleaning up failed resources.
    Maintains rollback history and deployment snapshots for recovery.

    Attributes:
        current_version: Currently deployed version
        previous_version: Previous stable version
        rollback_status: Current status of rollback operations
        deployment_snapshots: Historical deployment states
        rollback_history: History of rollback operations

    Example:
        >>> manager = RollbackManager(current_version="1.2.0", previous_version="1.1.0")
        >>> result = await manager.rollback(reason=RollbackReason.HEALTH_CHECK_FAILURE)
        >>> if result.success:
        ...     print(f"Rolled back to {result.target_version}")
    """

    def __init__(
        self,
        current_version: str = "1.0.0",
        previous_version: str = "0.9.0",
        max_snapshots: int = 10,
        rollback_timeout: float = 300.0,
    ) -> None:
        """
        Initialize RollbackManager.

        Args:
            current_version: Currently deployed version
            previous_version: Previous stable version to rollback to
            max_snapshots: Maximum deployment snapshots to maintain
            rollback_timeout: Maximum time for rollback operation in seconds
        """
        self.current_version = current_version
        self.previous_version = previous_version
        self.max_snapshots = max_snapshots
        self.rollback_timeout = rollback_timeout

        # State tracking
        self.rollback_status = RollbackStatus.IDLE
        self._deployment_snapshots: List[DeploymentSnapshot] = []
        self._rollback_history: List[RollbackResult] = []
        self._active_deployments: Dict[str, Dict[str, Any]] = {}

    async def rollback(
        self,
        reason: RollbackReason,
        target_version: Optional[str] = None,
        force: bool = False,
    ) -> RollbackResult:
        """
        Perform a complete rollback operation.

        Orchestrates the full rollback process:
        1. Stop current deployments
        2. Route all traffic to previous stable version
        3. Cleanup failed deployment resources
        4. Verify rollback success

        Args:
            reason: Reason for initiating rollback
            target_version: Specific version to rollback to (uses previous if None)
            force: Force rollback even if current deployment appears healthy

        Returns:
            RollbackResult with outcome details

        Example:
            >>> manager = RollbackManager("1.2.0", "1.1.0")
            >>> result = await manager.rollback(
            ...     reason=RollbackReason.METRICS_DEGRADATION
            ... )
            >>> print(f"Rollback: {result.message}")
        """
        start_time = time.time()
        target_version = target_version or self.previous_version

        steps_completed: List[str] = []
        steps_failed: List[str] = []

        if self.rollback_status == RollbackStatus.IN_PROGRESS:
            return RollbackResult(
                success=False,
                reason=reason,
                rollback_duration=0,
                previous_version=self.current_version,
                target_version=target_version,
                message="Rollback already in progress",
                steps_completed=[],
                steps_failed=["Concurrent rollback detected"],
            )

        self.rollback_status = RollbackStatus.IN_PROGRESS

        try:
            # Step 1: Create snapshot of current state
            snapshot = await self._create_snapshot()
            self._add_snapshot(snapshot)
            steps_completed.append("Created deployment snapshot")

            # Step 2: Stop current deployments
            stop_result = await self.stop_deployments()
            if stop_result["success"]:
                steps_completed.append(f"Stopped {stop_result['deployments_stopped']} deployments")
            else:
                steps_failed.append(f"Failed to stop deployments: {stop_result['error']}")
                if not force:
                    raise Exception("Failed to stop deployments")

            # Step 3: Route all traffic to stable version
            traffic_result = await self.route_all_traffic(target_version)
            if traffic_result["success"]:
                steps_completed.append(f"Routed traffic to {target_version}")
            else:
                steps_failed.append(f"Failed to route traffic: {traffic_result['error']}")
                if not force:
                    raise Exception("Failed to route traffic")

            # Step 4: Cleanup failed deployment
            cleanup_result = await self.cleanup_failed_deployment(self.current_version)
            if cleanup_result["success"]:
                steps_completed.append(f"Cleaned up {cleanup_result['resources_cleaned']} resources")
            else:
                steps_failed.append(f"Cleanup failed: {cleanup_result['error']}")
                # Don't fail rollback if cleanup fails

            # Step 5: Verify rollback
            verification_result = await self._verify_rollback(target_version)
            if verification_result["healthy"]:
                steps_completed.append("Verified rollback health")
            else:
                steps_failed.append("Health verification failed")

            # Update versions
            self.previous_version = self.current_version
            self.current_version = target_version

            # Determine overall success
            critical_failures = any("traffic" in step.lower() for step in steps_failed)
            success = not critical_failures

            if success:
                self.rollback_status = RollbackStatus.COMPLETED
            else:
                self.rollback_status = RollbackStatus.PARTIAL

            duration = time.time() - start_time
            result = RollbackResult(
                success=success,
                reason=reason,
                rollback_duration=duration,
                previous_version=snapshot.version,
                target_version=target_version,
                message=f"Rollback {'completed' if success else 'partially completed'} in {duration:.2f}s",
                steps_completed=steps_completed,
                steps_failed=steps_failed,
                metadata={
                    "snapshot": {
                        "version": snapshot.version,
                        "timestamp": snapshot.timestamp.isoformat(),
                        "health_score": snapshot.health_score,
                    },
                    "verification": verification_result,
                    "force": force,
                },
            )

            self._rollback_history.append(result)
            return result

        except Exception as e:
            self.rollback_status = RollbackStatus.FAILED
            duration = time.time() - start_time

            result = RollbackResult(
                success=False,
                reason=reason,
                rollback_duration=duration,
                previous_version=self.current_version,
                target_version=target_version,
                message=f"Rollback failed: {str(e)}",
                steps_completed=steps_completed,
                steps_failed=steps_failed + [str(e)],
                metadata={"error": str(e), "force": force},
            )

            self._rollback_history.append(result)
            return result

    async def stop_deployments(self) -> Dict[str, Any]:
        """
        Stop all active deployments.

        Gracefully stops all in-progress deployments, including canary
        deployments, blue-green swaps, and rolling updates.

        Returns:
            Dictionary with stop operation results

        Example:
            >>> result = await manager.stop_deployments()
            >>> if result['success']:
            ...     print(f"Stopped {result['deployments_stopped']} deployments")
        """
        try:
            deployments_stopped = 0
            stopped_deployments = []

            # Simulate stopping active deployments
            for deployment_id, deployment in list(self._active_deployments.items()):
                # Simulate stop operation
                await asyncio.sleep(0.3)

                deployment["status"] = "stopped"
                deployment["stopped_at"] = datetime.now()
                deployments_stopped += 1
                stopped_deployments.append({
                    "id": deployment_id,
                    "type": deployment.get("type", "unknown"),
                    "version": deployment.get("version", "unknown"),
                })

                # Remove from active deployments
                del self._active_deployments[deployment_id]

            return {
                "success": True,
                "deployments_stopped": deployments_stopped,
                "stopped_deployments": stopped_deployments,
                "message": f"Successfully stopped {deployments_stopped} deployments",
            }

        except Exception as e:
            return {
                "success": False,
                "deployments_stopped": 0,
                "error": str(e),
                "message": f"Failed to stop deployments: {str(e)}",
            }

    async def route_all_traffic(self, target_version: str) -> Dict[str, Any]:
        """
        Route all traffic to the target version.

        Updates load balancers, service meshes, and routing rules to direct
        100% of traffic to the specified version.

        Args:
            target_version: Version to route traffic to

        Returns:
            Dictionary with routing operation results

        Example:
            >>> result = await manager.route_all_traffic("1.1.0")
            >>> if result['success']:
            ...     print(f"All traffic routed to {target_version}")
        """
        try:
            # Simulate traffic routing steps
            routing_steps = [
                "Updating load balancer configuration",
                "Updating service mesh rules",
                "Flushing DNS cache",
                "Verifying routing rules",
            ]

            for step in routing_steps:
                await asyncio.sleep(0.3)

            return {
                "success": True,
                "target_version": target_version,
                "traffic_percentage": 100,
                "routing_steps_completed": len(routing_steps),
                "message": f"Successfully routed all traffic to {target_version}",
            }

        except Exception as e:
            return {
                "success": False,
                "target_version": target_version,
                "error": str(e),
                "message": f"Failed to route traffic: {str(e)}",
            }

    async def cleanup_failed_deployment(self, version: str) -> Dict[str, Any]:
        """
        Clean up resources from a failed deployment.

        Removes instances, containers, services, and other resources
        associated with a failed deployment version.

        Args:
            version: Version to clean up

        Returns:
            Dictionary with cleanup operation results

        Example:
            >>> result = await manager.cleanup_failed_deployment("1.2.0")
            >>> print(f"Cleaned {result['resources_cleaned']} resources")
        """
        try:
            resources_cleaned = 0
            cleaned_resources = []

            # Simulate resource cleanup
            resource_types = [
                "container_instances",
                "service_definitions",
                "configuration_maps",
                "secrets",
                "network_policies",
            ]

            for resource_type in resource_types:
                await asyncio.sleep(0.2)

                # Simulate finding and cleaning resources
                import random
                count = random.randint(1, 5)
                resources_cleaned += count

                cleaned_resources.append({
                    "type": resource_type,
                    "count": count,
                    "version": version,
                })

            return {
                "success": True,
                "version": version,
                "resources_cleaned": resources_cleaned,
                "cleaned_resources": cleaned_resources,
                "message": f"Successfully cleaned {resources_cleaned} resources for version {version}",
            }

        except Exception as e:
            return {
                "success": False,
                "version": version,
                "resources_cleaned": 0,
                "error": str(e),
                "message": f"Cleanup failed: {str(e)}",
            }

    async def _create_snapshot(self) -> DeploymentSnapshot:
        """
        Create a snapshot of current deployment state.

        Returns:
            DeploymentSnapshot with current state
        """
        await asyncio.sleep(0.2)

        import random
        return DeploymentSnapshot(
            version=self.current_version,
            timestamp=datetime.now(),
            instances=[
                {
                    "id": f"instance-{i}",
                    "status": "running",
                    "version": self.current_version,
                }
                for i in range(random.randint(2, 6))
            ],
            traffic_config={
                "current": 100,
                "canary": 0,
            },
            health_score=random.uniform(0.7, 1.0),
            metrics={
                "error_rate": random.uniform(0.01, 0.1),
                "avg_latency_ms": random.uniform(100, 500),
                "request_rate": random.uniform(100, 1000),
            },
        )

    def _add_snapshot(self, snapshot: DeploymentSnapshot) -> None:
        """
        Add a snapshot to history, maintaining max_snapshots limit.

        Args:
            snapshot: Snapshot to add
        """
        self._deployment_snapshots.append(snapshot)

        # Maintain size limit
        if len(self._deployment_snapshots) > self.max_snapshots:
            self._deployment_snapshots = self._deployment_snapshots[-self.max_snapshots:]

    async def _verify_rollback(self, target_version: str) -> Dict[str, Any]:
        """
        Verify rollback was successful.

        Args:
            target_version: Version that should now be active

        Returns:
            Verification results
        """
        # Simulate health checks
        await asyncio.sleep(1.0)

        import random
        healthy = random.random() > 0.1  # 90% success rate

        return {
            "healthy": healthy,
            "version": target_version,
            "health_score": random.uniform(0.9, 1.0) if healthy else random.uniform(0.5, 0.8),
            "checks_passed": random.randint(8, 10) if healthy else random.randint(5, 7),
            "checks_total": 10,
        }

    def add_active_deployment(
        self,
        deployment_id: str,
        deployment_type: str,
        version: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Register an active deployment for tracking.

        Args:
            deployment_id: Unique deployment identifier
            deployment_type: Type of deployment (canary, blue-green, etc.)
            version: Version being deployed
            metadata: Additional deployment metadata

        Example:
            >>> manager.add_active_deployment(
            ...     "deploy-123",
            ...     "canary",
            ...     "1.2.0"
            ... )
        """
        self._active_deployments[deployment_id] = {
            "id": deployment_id,
            "type": deployment_type,
            "version": version,
            "started_at": datetime.now(),
            "status": "active",
            "metadata": metadata or {},
        }

    def remove_active_deployment(self, deployment_id: str) -> bool:
        """
        Remove a deployment from active tracking.

        Args:
            deployment_id: Deployment identifier to remove

        Returns:
            True if deployment was found and removed
        """
        if deployment_id in self._active_deployments:
            del self._active_deployments[deployment_id]
            return True
        return False

    def get_rollback_status(self) -> Dict[str, Any]:
        """
        Get current rollback manager status.

        Returns:
            Status dictionary

        Example:
            >>> status = manager.get_rollback_status()
            >>> print(f"Status: {status['rollback_status']}")
            >>> print(f"Current version: {status['current_version']}")
        """
        return {
            "rollback_status": self.rollback_status.value,
            "current_version": self.current_version,
            "previous_version": self.previous_version,
            "active_deployments_count": len(self._active_deployments),
            "active_deployments": [
                {
                    "id": dep["id"],
                    "type": dep["type"],
                    "version": dep["version"],
                    "status": dep["status"],
                }
                for dep in self._active_deployments.values()
            ],
            "snapshots_count": len(self._deployment_snapshots),
            "rollback_history_count": len(self._rollback_history),
        }

    def get_rollback_history(self) -> List[Dict[str, Any]]:
        """
        Get rollback history.

        Returns:
            List of rollback results

        Example:
            >>> history = manager.get_rollback_history()
            >>> for rollback in history:
            ...     print(f"{rollback['target_version']}: {rollback['message']}")
        """
        return [
            {
                "success": result.success,
                "reason": result.reason.value,
                "rollback_duration": result.rollback_duration,
                "previous_version": result.previous_version,
                "target_version": result.target_version,
                "message": result.message,
                "steps_completed": result.steps_completed,
                "steps_failed": result.steps_failed,
            }
            for result in self._rollback_history
        ]

    def get_deployment_snapshots(self) -> List[Dict[str, Any]]:
        """
        Get deployment snapshots history.

        Returns:
            List of deployment snapshots

        Example:
            >>> snapshots = manager.get_deployment_snapshots()
            >>> for snapshot in snapshots:
            ...     print(f"{snapshot['version']} @ {snapshot['timestamp']}")
        """
        return [
            {
                "version": snapshot.version,
                "timestamp": snapshot.timestamp.isoformat(),
                "instances_count": len(snapshot.instances),
                "traffic_config": snapshot.traffic_config,
                "health_score": snapshot.health_score,
                "metrics": snapshot.metrics,
            }
            for snapshot in self._deployment_snapshots
        ]

    async def quick_rollback(self) -> RollbackResult:
        """
        Perform a quick rollback to previous version.

        Convenience method for common rollback scenario.

        Returns:
            RollbackResult with outcome

        Example:
            >>> result = await manager.quick_rollback()
            >>> if result.success:
            ...     print("Quick rollback successful")
        """
        return await self.rollback(
            reason=RollbackReason.MANUAL,
            target_version=self.previous_version,
            force=False,
        )
