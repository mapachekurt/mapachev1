"""
Blue-Green deployment strategy for zero-downtime deployments.

This module provides a BlueGreenDeployment class that enables zero-downtime
deployments by maintaining two identical production environments (blue and green)
and switching traffic between them.
"""

import asyncio
import time
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


class DeploymentEnvironment(Enum):
    """Deployment environment color designation."""
    BLUE = "blue"
    GREEN = "green"


class DeploymentStatus(Enum):
    """Status of a deployment."""
    IDLE = "idle"
    DEPLOYING = "deploying"
    STAGING = "staging"
    MONITORING = "monitoring"
    LIVE = "live"
    FAILED = "failed"
    ROLLING_BACK = "rolling_back"


@dataclass
class EnvironmentState:
    """State of a deployment environment."""
    name: DeploymentEnvironment
    status: DeploymentStatus
    version: str = "0.0.0"
    deployed_at: Optional[datetime] = None
    health_score: float = 1.0
    traffic_percentage: int = 0
    endpoint_url: str = ""
    instances: List[Dict[str, Any]] = field(default_factory=list)
    metrics: Dict[str, float] = field(default_factory=dict)


@dataclass
class DeploymentResult:
    """Result of a deployment operation."""
    success: bool
    environment: DeploymentEnvironment
    version: str
    duration_seconds: float
    message: str
    health_checks_passed: int = 0
    health_checks_failed: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


class BlueGreenDeployment:
    """
    Blue-Green deployment strategy for zero-downtime deployments.

    Maintains two identical production environments and switches traffic between
    them to enable zero-downtime deployments. This implementation uses mock
    deployments without requiring actual cloud resources.

    Attributes:
        blue: State of the blue environment
        green: State of the green environment
        active_environment: Currently active environment receiving traffic
        monitoring_enabled: Whether deployment monitoring is active
        health_check_interval: Seconds between health checks
        health_check_threshold: Required successful health checks

    Example:
        >>> deployment = BlueGreenDeployment()
        >>> result = await deployment.deploy("1.2.3")
        >>> if result.success:
        ...     await deployment.swap_endpoints()
    """

    def __init__(
        self,
        health_check_interval: float = 5.0,
        health_check_threshold: int = 3,
        monitoring_duration: float = 30.0,
    ) -> None:
        """
        Initialize BlueGreenDeployment.

        Args:
            health_check_interval: Seconds between health checks
            health_check_threshold: Required successful health checks before swap
            monitoring_duration: Seconds to monitor after swap
        """
        self.blue = EnvironmentState(
            name=DeploymentEnvironment.BLUE,
            status=DeploymentStatus.LIVE,
            version="1.0.0",
            endpoint_url="http://blue.example.com",
            traffic_percentage=100,
        )
        self.green = EnvironmentState(
            name=DeploymentEnvironment.GREEN,
            status=DeploymentStatus.IDLE,
            version="0.0.0",
            endpoint_url="http://green.example.com",
            traffic_percentage=0,
        )

        # Blue is initially active
        self.active_environment = DeploymentEnvironment.BLUE
        self.monitoring_enabled = False
        self.health_check_interval = health_check_interval
        self.health_check_threshold = health_check_threshold
        self.monitoring_duration = monitoring_duration
        self._deployment_history: List[DeploymentResult] = []

    def get_inactive_environment(self) -> EnvironmentState:
        """
        Get the currently inactive environment.

        Returns:
            The inactive environment state
        """
        if self.active_environment == DeploymentEnvironment.BLUE:
            return self.green
        return self.blue

    def get_active_environment(self) -> EnvironmentState:
        """
        Get the currently active environment.

        Returns:
            The active environment state
        """
        if self.active_environment == DeploymentEnvironment.BLUE:
            return self.blue
        return self.green

    async def deploy(
        self,
        version: str,
        config: Optional[Dict[str, Any]] = None,
    ) -> DeploymentResult:
        """
        Deploy a new version using blue-green strategy.

        This method orchestrates the full deployment process:
        1. Deploy to inactive environment (staging)
        2. Run health checks
        3. Monitor the deployment
        4. Swap endpoints if healthy

        Args:
            version: Version string to deploy
            config: Optional deployment configuration

        Returns:
            DeploymentResult with deployment outcome

        Example:
            >>> deployment = BlueGreenDeployment()
            >>> result = await deployment.deploy("1.2.3")
            >>> print(f"Deployed {result.version}: {result.message}")
        """
        start_time = time.time()
        config = config or {}

        # Step 1: Deploy to staging (inactive environment)
        staging_result = await self.deploy_to_staging(version, config)
        if not staging_result.success:
            return staging_result

        # Step 2: Monitor the deployment
        monitoring_result = await self.monitor_deployment(
            staging_result.environment,
            duration=self.monitoring_duration,
        )
        if not monitoring_result.success:
            return monitoring_result

        # Step 3: Swap endpoints
        swap_result = await self.swap_endpoints()

        duration = time.time() - start_time
        result = DeploymentResult(
            success=swap_result.success,
            environment=staging_result.environment,
            version=version,
            duration_seconds=duration,
            message=f"Blue-green deployment {'succeeded' if swap_result.success else 'failed'}",
            health_checks_passed=monitoring_result.health_checks_passed,
            health_checks_failed=monitoring_result.health_checks_failed,
            metadata={
                "staging_duration": staging_result.duration_seconds,
                "monitoring_duration": monitoring_result.duration_seconds,
                "swap_duration": swap_result.duration_seconds,
                "config": config,
            },
        )

        self._deployment_history.append(result)
        return result

    async def deploy_to_staging(
        self,
        version: str,
        config: Optional[Dict[str, Any]] = None,
    ) -> DeploymentResult:
        """
        Deploy to the inactive (staging) environment.

        Simulates deploying the application to the inactive environment
        without affecting live traffic.

        Args:
            version: Version string to deploy
            config: Optional deployment configuration

        Returns:
            DeploymentResult with staging deployment outcome

        Example:
            >>> result = await deployment.deploy_to_staging("1.2.3")
            >>> if result.success:
            ...     print(f"Staged version {result.version}")
        """
        start_time = time.time()
        config = config or {}

        inactive = self.get_inactive_environment()
        inactive.status = DeploymentStatus.DEPLOYING

        # Simulate deployment steps
        deployment_steps = [
            "Pulling container image",
            "Updating configuration",
            "Starting new instances",
            "Running database migrations",
            "Warming up caches",
        ]

        try:
            for step in deployment_steps:
                # Simulate deployment step
                await asyncio.sleep(0.5)  # Simulate work

            # Update environment state
            inactive.version = version
            inactive.deployed_at = datetime.now()
            inactive.status = DeploymentStatus.STAGING
            inactive.health_score = 1.0
            inactive.instances = [
                {
                    "id": f"{inactive.name.value}-instance-{i}",
                    "status": "healthy",
                    "version": version,
                }
                for i in range(config.get("instance_count", 3))
            ]

            duration = time.time() - start_time
            return DeploymentResult(
                success=True,
                environment=inactive.name,
                version=version,
                duration_seconds=duration,
                message=f"Successfully deployed {version} to {inactive.name.value} environment",
                metadata={
                    "steps_completed": len(deployment_steps),
                    "instances": len(inactive.instances),
                },
            )

        except Exception as e:
            inactive.status = DeploymentStatus.FAILED
            duration = time.time() - start_time
            return DeploymentResult(
                success=False,
                environment=inactive.name,
                version=version,
                duration_seconds=duration,
                message=f"Deployment failed: {str(e)}",
                metadata={"error": str(e)},
            )

    async def swap_endpoints(self) -> DeploymentResult:
        """
        Swap the active and inactive environments.

        Switches all production traffic from the current active environment
        to the staged environment. This is the critical moment where the
        new version goes live.

        Returns:
            DeploymentResult with swap outcome

        Example:
            >>> result = await deployment.swap_endpoints()
            >>> if result.success:
            ...     print(f"Traffic now routing to {result.environment.value}")
        """
        start_time = time.time()

        inactive = self.get_inactive_environment()
        active = self.get_active_environment()

        # Verify inactive environment is ready
        if inactive.status != DeploymentStatus.STAGING:
            return DeploymentResult(
                success=False,
                environment=inactive.name,
                version=inactive.version,
                duration_seconds=0,
                message=f"Cannot swap: {inactive.name.value} is not in staging state",
            )

        if inactive.health_score < 0.9:
            return DeploymentResult(
                success=False,
                environment=inactive.name,
                version=inactive.version,
                duration_seconds=0,
                message=f"Cannot swap: {inactive.name.value} health score too low",
            )

        try:
            # Simulate endpoint swap steps
            await asyncio.sleep(0.5)  # Update load balancer
            await asyncio.sleep(0.3)  # Update DNS
            await asyncio.sleep(0.2)  # Update routing rules

            # Perform the swap
            old_active = self.active_environment
            self.active_environment = inactive.name

            # Update traffic routing
            inactive.traffic_percentage = 100
            inactive.status = DeploymentStatus.LIVE

            active.traffic_percentage = 0
            active.status = DeploymentStatus.IDLE

            duration = time.time() - start_time
            return DeploymentResult(
                success=True,
                environment=inactive.name,
                version=inactive.version,
                duration_seconds=duration,
                message=f"Successfully swapped from {old_active.value} to {inactive.name.value}",
                metadata={
                    "old_environment": old_active.value,
                    "new_environment": inactive.name.value,
                    "old_version": active.version,
                    "new_version": inactive.version,
                },
            )

        except Exception as e:
            duration = time.time() - start_time
            return DeploymentResult(
                success=False,
                environment=inactive.name,
                version=inactive.version,
                duration_seconds=duration,
                message=f"Swap failed: {str(e)}",
                metadata={"error": str(e)},
            )

    async def monitor_deployment(
        self,
        environment: DeploymentEnvironment,
        duration: Optional[float] = None,
    ) -> DeploymentResult:
        """
        Monitor a deployment environment for health and stability.

        Continuously monitors the specified environment, running health checks
        and collecting metrics to ensure the deployment is stable before
        allowing traffic to be routed to it.

        Args:
            environment: Environment to monitor
            duration: Monitoring duration in seconds (uses default if None)

        Returns:
            DeploymentResult with monitoring outcome

        Example:
            >>> result = await deployment.monitor_deployment(
            ...     DeploymentEnvironment.GREEN,
            ...     duration=60.0
            ... )
            >>> print(f"Health checks passed: {result.health_checks_passed}")
        """
        start_time = time.time()
        duration = duration or self.monitoring_duration

        env = self.blue if environment == DeploymentEnvironment.BLUE else self.green

        if env.status not in [DeploymentStatus.STAGING, DeploymentStatus.LIVE]:
            return DeploymentResult(
                success=False,
                environment=environment,
                version=env.version,
                duration_seconds=0,
                message=f"Cannot monitor: {environment.value} is in {env.status.value} state",
            )

        env.status = DeploymentStatus.MONITORING
        self.monitoring_enabled = True

        health_checks_passed = 0
        health_checks_failed = 0
        checks_performed = 0

        try:
            end_time = start_time + duration

            while time.time() < end_time:
                # Perform health check
                health_check_result = await self._perform_health_check(env)
                checks_performed += 1

                if health_check_result["healthy"]:
                    health_checks_passed += 1
                else:
                    health_checks_failed += 1

                # Update health score (running average)
                success_rate = health_checks_passed / checks_performed
                env.health_score = success_rate

                # Check if we've failed too many checks
                if health_checks_failed > self.health_check_threshold:
                    env.status = DeploymentStatus.FAILED
                    return DeploymentResult(
                        success=False,
                        environment=environment,
                        version=env.version,
                        duration_seconds=time.time() - start_time,
                        message=f"Monitoring failed: too many failed health checks ({health_checks_failed})",
                        health_checks_passed=health_checks_passed,
                        health_checks_failed=health_checks_failed,
                    )

                # Collect metrics
                env.metrics = await self._collect_metrics(env)

                # Wait before next check
                await asyncio.sleep(self.health_check_interval)

            # Monitoring completed successfully
            self.monitoring_enabled = False
            env.status = DeploymentStatus.STAGING

            elapsed = time.time() - start_time
            return DeploymentResult(
                success=True,
                environment=environment,
                version=env.version,
                duration_seconds=elapsed,
                message=f"Monitoring completed: {health_checks_passed}/{checks_performed} checks passed",
                health_checks_passed=health_checks_passed,
                health_checks_failed=health_checks_failed,
                metadata={
                    "checks_performed": checks_performed,
                    "health_score": env.health_score,
                    "metrics": env.metrics,
                },
            )

        except Exception as e:
            self.monitoring_enabled = False
            env.status = DeploymentStatus.FAILED
            return DeploymentResult(
                success=False,
                environment=environment,
                version=env.version,
                duration_seconds=time.time() - start_time,
                message=f"Monitoring error: {str(e)}",
                health_checks_passed=health_checks_passed,
                health_checks_failed=health_checks_failed,
                metadata={"error": str(e)},
            )

    async def _perform_health_check(
        self,
        env: EnvironmentState,
    ) -> Dict[str, Any]:
        """
        Perform a health check on an environment.

        Args:
            env: Environment to check

        Returns:
            Health check result dictionary
        """
        # Simulate health check (mock implementation)
        await asyncio.sleep(0.1)

        # Simulate occasional failures (5% failure rate)
        import random
        healthy = random.random() > 0.05

        return {
            "healthy": healthy,
            "timestamp": datetime.now().isoformat(),
            "response_time_ms": random.uniform(10, 100),
            "instances_healthy": len([i for i in env.instances if i["status"] == "healthy"]),
            "instances_total": len(env.instances),
        }

    async def _collect_metrics(
        self,
        env: EnvironmentState,
    ) -> Dict[str, float]:
        """
        Collect metrics from an environment.

        Args:
            env: Environment to collect from

        Returns:
            Metrics dictionary
        """
        # Simulate metrics collection (mock implementation)
        await asyncio.sleep(0.05)

        import random
        return {
            "request_rate": random.uniform(100, 1000),
            "error_rate": random.uniform(0, 0.05),
            "avg_response_time_ms": random.uniform(50, 200),
            "cpu_usage_percent": random.uniform(20, 80),
            "memory_usage_percent": random.uniform(30, 70),
            "active_connections": random.uniform(10, 100),
        }

    def get_deployment_status(self) -> Dict[str, Any]:
        """
        Get current deployment status.

        Returns:
            Status dictionary with both environments

        Example:
            >>> status = deployment.get_deployment_status()
            >>> print(f"Active: {status['active_environment']}")
            >>> print(f"Blue: {status['blue']['version']}")
        """
        return {
            "active_environment": self.active_environment.value,
            "monitoring_enabled": self.monitoring_enabled,
            "blue": {
                "status": self.blue.status.value,
                "version": self.blue.version,
                "traffic_percentage": self.blue.traffic_percentage,
                "health_score": self.blue.health_score,
                "instances": len(self.blue.instances),
            },
            "green": {
                "status": self.green.status.value,
                "version": self.green.version,
                "traffic_percentage": self.green.traffic_percentage,
                "health_score": self.green.health_score,
                "instances": len(self.green.instances),
            },
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
                "environment": result.environment.value,
                "version": result.version,
                "duration_seconds": result.duration_seconds,
                "message": result.message,
                "health_checks_passed": result.health_checks_passed,
                "health_checks_failed": result.health_checks_failed,
            }
            for result in self._deployment_history
        ]
