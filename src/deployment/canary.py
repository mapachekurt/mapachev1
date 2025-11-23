"""
Canary deployment strategy for gradual rollout.

This module provides a CanaryDeployment class that enables gradual rollouts
by routing a small percentage of traffic to the new version and progressively
increasing it based on metrics validation.
"""

import asyncio
import time
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


class CanaryPhase(Enum):
    """Phase of canary deployment."""
    INITIAL = "initial"
    SCALING = "scaling"
    VALIDATING = "validating"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLING_BACK = "rolling_back"


@dataclass
class TrafficConfig:
    """Traffic routing configuration."""
    stable_percentage: int
    canary_percentage: int

    def __post_init__(self) -> None:
        """Validate traffic percentages."""
        total = self.stable_percentage + self.canary_percentage
        if total != 100:
            raise ValueError(f"Traffic percentages must sum to 100, got {total}")


@dataclass
class MetricsSnapshot:
    """Snapshot of deployment metrics."""
    timestamp: datetime
    error_rate: float
    avg_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    request_rate: float
    success_rate: float
    cpu_usage_percent: float
    memory_usage_percent: float


@dataclass
class CanaryDeploymentResult:
    """Result of a canary deployment operation."""
    success: bool
    version: str
    duration_seconds: float
    message: str
    final_canary_percentage: int
    phases_completed: int
    total_phases: int
    metrics_passed: bool
    metadata: Dict[str, Any] = field(default_factory=dict)


class CanaryDeployment:
    """
    Canary deployment strategy for gradual rollout.

    Gradually routes traffic to a new version while monitoring metrics to
    ensure the deployment is stable. Traffic is progressively shifted from
    the stable version to the canary version in configurable steps.

    Attributes:
        stable_version: Currently stable/production version
        canary_version: New version being deployed
        current_traffic: Current traffic routing configuration
        phase: Current deployment phase
        baseline_metrics: Metrics from stable version
        canary_metrics: Metrics from canary version

    Example:
        >>> canary = CanaryDeployment(
        ...     stable_version="1.0.0",
        ...     traffic_steps=[10, 25, 50, 75, 100]
        ... )
        >>> result = await canary.deploy("1.1.0")
        >>> if result.success:
        ...     print(f"Deployed {result.version} successfully")
    """

    def __init__(
        self,
        stable_version: str = "1.0.0",
        traffic_steps: Optional[List[int]] = None,
        validation_duration: float = 30.0,
        metrics_threshold: Optional[Dict[str, float]] = None,
    ) -> None:
        """
        Initialize CanaryDeployment.

        Args:
            stable_version: Current stable version identifier
            traffic_steps: List of canary traffic percentages to progress through
            validation_duration: Seconds to validate at each step
            metrics_threshold: Thresholds for metrics degradation
        """
        self.stable_version = stable_version
        self.canary_version: Optional[str] = None
        self.traffic_steps = traffic_steps or [5, 10, 25, 50, 100]
        self.validation_duration = validation_duration

        # Default metrics thresholds
        self.metrics_threshold = metrics_threshold or {
            "error_rate_increase": 0.05,  # 5% increase in errors
            "latency_increase": 0.20,  # 20% increase in latency
            "success_rate_decrease": 0.05,  # 5% decrease in success rate
        }

        # Current state
        self.current_traffic = TrafficConfig(stable_percentage=100, canary_percentage=0)
        self.phase = CanaryPhase.INITIAL
        self.current_step = 0

        # Metrics tracking
        self.baseline_metrics: Optional[MetricsSnapshot] = None
        self.canary_metrics: Optional[MetricsSnapshot] = None
        self._metrics_history: List[MetricsSnapshot] = []
        self._deployment_history: List[CanaryDeploymentResult] = []

    async def deploy(
        self,
        version: str,
        config: Optional[Dict[str, Any]] = None,
    ) -> CanaryDeploymentResult:
        """
        Deploy a new version using canary strategy.

        Gradually increases traffic to the canary version while monitoring
        metrics at each step. Rolls back if metrics degrade beyond thresholds.

        Args:
            version: Version string to deploy
            config: Optional deployment configuration

        Returns:
            CanaryDeploymentResult with deployment outcome

        Example:
            >>> canary = CanaryDeployment(stable_version="1.0.0")
            >>> result = await canary.deploy("1.1.0")
            >>> print(f"Final canary traffic: {result.final_canary_percentage}%")
        """
        start_time = time.time()
        config = config or {}

        self.canary_version = version
        self.phase = CanaryPhase.INITIAL
        self.current_step = 0

        phases_completed = 0
        total_phases = len(self.traffic_steps)

        try:
            # Get baseline metrics from stable version
            self.baseline_metrics = await self.get_baseline_metrics()

            # Deploy canary instances
            await self._deploy_canary_instances(version, config)

            # Progress through traffic steps
            self.phase = CanaryPhase.SCALING

            for step_idx, canary_percentage in enumerate(self.traffic_steps):
                self.current_step = step_idx

                # Route traffic to canary
                await self.route_traffic(
                    canary_percentage=canary_percentage,
                    stable_percentage=100 - canary_percentage,
                )

                # Validate metrics at this step
                self.phase = CanaryPhase.VALIDATING
                validation_result = await self._validate_canary_metrics()

                if not validation_result["passed"]:
                    # Metrics degraded, rollback
                    self.phase = CanaryPhase.FAILED
                    duration = time.time() - start_time

                    result = CanaryDeploymentResult(
                        success=False,
                        version=version,
                        duration_seconds=duration,
                        message=f"Deployment failed at {canary_percentage}% traffic: {validation_result['reason']}",
                        final_canary_percentage=canary_percentage,
                        phases_completed=phases_completed,
                        total_phases=total_phases,
                        metrics_passed=False,
                        metadata={
                            "failed_step": canary_percentage,
                            "validation_result": validation_result,
                            "config": config,
                        },
                    )
                    self._deployment_history.append(result)
                    return result

                phases_completed += 1
                self.phase = CanaryPhase.SCALING

            # All steps passed, deployment complete
            self.phase = CanaryPhase.COMPLETED
            self.stable_version = version
            self.canary_version = None

            duration = time.time() - start_time
            result = CanaryDeploymentResult(
                success=True,
                version=version,
                duration_seconds=duration,
                message=f"Canary deployment completed successfully through {total_phases} phases",
                final_canary_percentage=100,
                phases_completed=phases_completed,
                total_phases=total_phases,
                metrics_passed=True,
                metadata={
                    "traffic_steps": self.traffic_steps,
                    "validation_duration": self.validation_duration,
                    "config": config,
                },
            )
            self._deployment_history.append(result)
            return result

        except Exception as e:
            self.phase = CanaryPhase.FAILED
            duration = time.time() - start_time

            result = CanaryDeploymentResult(
                success=False,
                version=version,
                duration_seconds=duration,
                message=f"Deployment error: {str(e)}",
                final_canary_percentage=self.current_traffic.canary_percentage,
                phases_completed=phases_completed,
                total_phases=total_phases,
                metrics_passed=False,
                metadata={"error": str(e), "config": config},
            )
            self._deployment_history.append(result)
            return result

    async def route_traffic(
        self,
        canary_percentage: int,
        stable_percentage: int,
    ) -> None:
        """
        Route traffic between stable and canary versions.

        Updates the traffic routing configuration to split traffic between
        the stable and canary versions according to the specified percentages.

        Args:
            canary_percentage: Percentage of traffic to route to canary
            stable_percentage: Percentage of traffic to route to stable

        Raises:
            ValueError: If percentages don't sum to 100

        Example:
            >>> await canary.route_traffic(canary_percentage=25, stable_percentage=75)
        """
        # Validate percentages
        total = canary_percentage + stable_percentage
        if total != 100:
            raise ValueError(f"Traffic percentages must sum to 100, got {total}")

        # Simulate traffic routing update
        await asyncio.sleep(0.5)  # Simulate load balancer update

        # Update configuration
        self.current_traffic = TrafficConfig(
            stable_percentage=stable_percentage,
            canary_percentage=canary_percentage,
        )

    async def get_baseline_metrics(self) -> MetricsSnapshot:
        """
        Collect baseline metrics from the stable version.

        Captures current performance metrics from the stable version to
        serve as a baseline for comparing canary version performance.

        Returns:
            MetricsSnapshot with baseline metrics

        Example:
            >>> baseline = await canary.get_baseline_metrics()
            >>> print(f"Baseline error rate: {baseline.error_rate}")
        """
        # Simulate metrics collection
        await asyncio.sleep(0.5)

        import random
        baseline = MetricsSnapshot(
            timestamp=datetime.now(),
            error_rate=random.uniform(0.001, 0.01),  # 0.1% - 1% errors
            avg_latency_ms=random.uniform(50, 100),
            p95_latency_ms=random.uniform(100, 200),
            p99_latency_ms=random.uniform(200, 400),
            request_rate=random.uniform(100, 1000),
            success_rate=random.uniform(0.99, 0.999),
            cpu_usage_percent=random.uniform(30, 60),
            memory_usage_percent=random.uniform(40, 70),
        )

        self._metrics_history.append(baseline)
        return baseline

    async def metrics_degraded(
        self,
        baseline: MetricsSnapshot,
        current: MetricsSnapshot,
    ) -> Dict[str, Any]:
        """
        Check if metrics have degraded beyond acceptable thresholds.

        Compares current metrics against baseline to determine if there
        has been unacceptable degradation in performance.

        Args:
            baseline: Baseline metrics snapshot
            current: Current metrics snapshot

        Returns:
            Dictionary with degradation analysis

        Example:
            >>> baseline = await canary.get_baseline_metrics()
            >>> await canary.route_traffic(10, 90)
            >>> current = await canary.get_baseline_metrics()
            >>> degradation = await canary.metrics_degraded(baseline, current)
            >>> if degradation['degraded']:
            ...     print(f"Reason: {degradation['reason']}")
        """
        # Simulate analysis delay
        await asyncio.sleep(0.1)

        issues = []
        degraded = False

        # Check error rate increase
        error_rate_increase = (current.error_rate - baseline.error_rate) / max(baseline.error_rate, 0.001)
        if error_rate_increase > self.metrics_threshold["error_rate_increase"]:
            issues.append(f"Error rate increased by {error_rate_increase:.1%}")
            degraded = True

        # Check latency increase
        latency_increase = (current.avg_latency_ms - baseline.avg_latency_ms) / baseline.avg_latency_ms
        if latency_increase > self.metrics_threshold["latency_increase"]:
            issues.append(f"Latency increased by {latency_increase:.1%}")
            degraded = True

        # Check success rate decrease
        success_rate_decrease = baseline.success_rate - current.success_rate
        if success_rate_decrease > self.metrics_threshold["success_rate_decrease"]:
            issues.append(f"Success rate decreased by {success_rate_decrease:.1%}")
            degraded = True

        return {
            "degraded": degraded,
            "issues": issues,
            "metrics_comparison": {
                "error_rate": {
                    "baseline": baseline.error_rate,
                    "current": current.error_rate,
                    "change_percent": error_rate_increase * 100,
                },
                "avg_latency_ms": {
                    "baseline": baseline.avg_latency_ms,
                    "current": current.avg_latency_ms,
                    "change_percent": latency_increase * 100,
                },
                "success_rate": {
                    "baseline": baseline.success_rate,
                    "current": current.success_rate,
                    "change": success_rate_decrease,
                },
            },
        }

    async def _deploy_canary_instances(
        self,
        version: str,
        config: Dict[str, Any],
    ) -> None:
        """
        Deploy canary instances.

        Args:
            version: Version to deploy
            config: Deployment configuration
        """
        # Simulate canary deployment
        deployment_steps = [
            "Creating canary service",
            "Pulling container image",
            "Starting canary instances",
            "Configuring health checks",
            "Registering with load balancer",
        ]

        for step in deployment_steps:
            await asyncio.sleep(0.3)

    async def _validate_canary_metrics(self) -> Dict[str, Any]:
        """
        Validate canary metrics at current traffic level.

        Returns:
            Validation result dictionary
        """
        # Wait for metrics to stabilize
        await asyncio.sleep(self.validation_duration)

        # Collect canary metrics
        self.canary_metrics = await self._collect_canary_metrics()

        if not self.baseline_metrics:
            return {
                "passed": False,
                "reason": "No baseline metrics available",
            }

        # Check for degradation
        degradation = await self.metrics_degraded(
            self.baseline_metrics,
            self.canary_metrics,
        )

        if degradation["degraded"]:
            return {
                "passed": False,
                "reason": ", ".join(degradation["issues"]),
                "degradation": degradation,
            }

        return {
            "passed": True,
            "reason": "All metrics within acceptable thresholds",
            "degradation": degradation,
        }

    async def _collect_canary_metrics(self) -> MetricsSnapshot:
        """
        Collect metrics from canary version.

        Returns:
            MetricsSnapshot with canary metrics
        """
        # Simulate metrics collection
        await asyncio.sleep(0.3)

        import random

        # Simulate mostly good metrics with occasional degradation
        if self.baseline_metrics:
            # Base canary metrics on baseline with some variation
            metrics = MetricsSnapshot(
                timestamp=datetime.now(),
                error_rate=self.baseline_metrics.error_rate * random.uniform(0.8, 1.15),
                avg_latency_ms=self.baseline_metrics.avg_latency_ms * random.uniform(0.9, 1.15),
                p95_latency_ms=self.baseline_metrics.p95_latency_ms * random.uniform(0.9, 1.15),
                p99_latency_ms=self.baseline_metrics.p99_latency_ms * random.uniform(0.9, 1.15),
                request_rate=self.baseline_metrics.request_rate * (self.current_traffic.canary_percentage / 100),
                success_rate=max(0.95, self.baseline_metrics.success_rate * random.uniform(0.99, 1.0)),
                cpu_usage_percent=random.uniform(30, 70),
                memory_usage_percent=random.uniform(40, 75),
            )
        else:
            # Fallback metrics
            metrics = MetricsSnapshot(
                timestamp=datetime.now(),
                error_rate=random.uniform(0.001, 0.01),
                avg_latency_ms=random.uniform(50, 100),
                p95_latency_ms=random.uniform(100, 200),
                p99_latency_ms=random.uniform(200, 400),
                request_rate=random.uniform(10, 100),
                success_rate=random.uniform(0.99, 0.999),
                cpu_usage_percent=random.uniform(30, 60),
                memory_usage_percent=random.uniform(40, 70),
            )

        self._metrics_history.append(metrics)
        return metrics

    def get_deployment_status(self) -> Dict[str, Any]:
        """
        Get current deployment status.

        Returns:
            Status dictionary with current state

        Example:
            >>> status = canary.get_deployment_status()
            >>> print(f"Phase: {status['phase']}")
            >>> print(f"Canary traffic: {status['traffic']['canary_percentage']}%")
        """
        return {
            "phase": self.phase.value,
            "stable_version": self.stable_version,
            "canary_version": self.canary_version,
            "current_step": self.current_step,
            "total_steps": len(self.traffic_steps),
            "traffic": {
                "stable_percentage": self.current_traffic.stable_percentage,
                "canary_percentage": self.current_traffic.canary_percentage,
            },
            "baseline_metrics": {
                "error_rate": self.baseline_metrics.error_rate if self.baseline_metrics else None,
                "avg_latency_ms": self.baseline_metrics.avg_latency_ms if self.baseline_metrics else None,
                "success_rate": self.baseline_metrics.success_rate if self.baseline_metrics else None,
            } if self.baseline_metrics else None,
            "canary_metrics": {
                "error_rate": self.canary_metrics.error_rate if self.canary_metrics else None,
                "avg_latency_ms": self.canary_metrics.avg_latency_ms if self.canary_metrics else None,
                "success_rate": self.canary_metrics.success_rate if self.canary_metrics else None,
            } if self.canary_metrics else None,
            "metrics_history_count": len(self._metrics_history),
            "deployment_history_count": len(self._deployment_history),
        }

    def get_deployment_history(self) -> List[Dict[str, Any]]:
        """
        Get deployment history.

        Returns:
            List of deployment results
        """
        return [
            {
                "success": result.success,
                "version": result.version,
                "duration_seconds": result.duration_seconds,
                "message": result.message,
                "final_canary_percentage": result.final_canary_percentage,
                "phases_completed": result.phases_completed,
                "total_phases": result.total_phases,
                "metrics_passed": result.metrics_passed,
            }
            for result in self._deployment_history
        ]

    def get_metrics_history(self) -> List[Dict[str, Any]]:
        """
        Get metrics history.

        Returns:
            List of metrics snapshots
        """
        return [
            {
                "timestamp": snapshot.timestamp.isoformat(),
                "error_rate": snapshot.error_rate,
                "avg_latency_ms": snapshot.avg_latency_ms,
                "p95_latency_ms": snapshot.p95_latency_ms,
                "p99_latency_ms": snapshot.p99_latency_ms,
                "request_rate": snapshot.request_rate,
                "success_rate": snapshot.success_rate,
                "cpu_usage_percent": snapshot.cpu_usage_percent,
                "memory_usage_percent": snapshot.memory_usage_percent,
            }
            for snapshot in self._metrics_history
        ]
