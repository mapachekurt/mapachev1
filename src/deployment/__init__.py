"""
Production Operations deployment strategies and testing.

This module provides production-ready deployment strategies including:
- Blue-Green deployments for zero-downtime releases
- Canary deployments for gradual rollouts with metrics validation
- Automated rollback management for deployment failures
- Comprehensive smoke tests for post-deployment validation
"""

from .blue_green import (
    BlueGreenDeployment,
    DeploymentEnvironment,
    DeploymentStatus,
    EnvironmentState,
    DeploymentResult,
)

from .canary import (
    CanaryDeployment,
    CanaryPhase,
    TrafficConfig,
    MetricsSnapshot,
    CanaryDeploymentResult,
)

from .rollback import (
    RollbackManager,
    RollbackStatus,
    RollbackReason,
    DeploymentSnapshot,
    RollbackResult,
)

from .smoke_tests import (
    SmokeTests,
    TestStatus,
    TestSeverity,
    TestResult,
    SmokeTestSuite,
)

__all__ = [
    # Blue-Green Deployment
    "BlueGreenDeployment",
    "DeploymentEnvironment",
    "DeploymentStatus",
    "EnvironmentState",
    "DeploymentResult",
    # Canary Deployment
    "CanaryDeployment",
    "CanaryPhase",
    "TrafficConfig",
    "MetricsSnapshot",
    "CanaryDeploymentResult",
    # Rollback Management
    "RollbackManager",
    "RollbackStatus",
    "RollbackReason",
    "DeploymentSnapshot",
    "RollbackResult",
    # Smoke Tests
    "SmokeTests",
    "TestStatus",
    "TestSeverity",
    "TestResult",
    "SmokeTestSuite",
]
