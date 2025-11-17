"""
Example usage of production operations deployment strategies.

This module demonstrates how to use blue-green deployments, canary deployments,
rollback management, and smoke tests in a production environment.
"""

import asyncio
from src.deployment import (
    BlueGreenDeployment,
    CanaryDeployment,
    RollbackManager,
    RollbackReason,
    SmokeTests,
)


async def example_blue_green_deployment():
    """
    Example: Blue-Green deployment with zero downtime.

    Demonstrates deploying a new version using blue-green strategy,
    which maintains two identical environments and swaps traffic.
    """
    print("=" * 60)
    print("EXAMPLE 1: Blue-Green Deployment")
    print("=" * 60)

    # Initialize blue-green deployment
    deployment = BlueGreenDeployment(
        health_check_interval=2.0,
        health_check_threshold=3,
        monitoring_duration=10.0,
    )

    # Show initial status
    status = deployment.get_deployment_status()
    print(f"\nInitial State:")
    print(f"  Active: {status['active_environment']}")
    print(f"  Blue: {status['blue']['version']} ({status['blue']['status']})")
    print(f"  Green: {status['green']['version']} ({status['green']['status']})")

    # Deploy new version
    print("\nDeploying version 1.2.0...")
    result = await deployment.deploy("1.2.0")

    if result.success:
        print(f"✓ Deployment succeeded in {result.duration_seconds:.2f}s")
        print(f"  Health checks: {result.health_checks_passed} passed, {result.health_checks_failed} failed")
    else:
        print(f"✗ Deployment failed: {result.message}")

    # Show final status
    status = deployment.get_deployment_status()
    print(f"\nFinal State:")
    print(f"  Active: {status['active_environment']}")
    print(f"  Blue: {status['blue']['version']} ({status['blue']['status']}, {status['blue']['traffic_percentage']}% traffic)")
    print(f"  Green: {status['green']['version']} ({status['green']['status']}, {status['green']['traffic_percentage']}% traffic)")


async def example_canary_deployment():
    """
    Example: Canary deployment with gradual rollout.

    Demonstrates deploying a new version using canary strategy,
    which gradually increases traffic while monitoring metrics.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Canary Deployment")
    print("=" * 60)

    # Initialize canary deployment
    canary = CanaryDeployment(
        stable_version="1.1.0",
        traffic_steps=[10, 25, 50, 100],
        validation_duration=5.0,
    )

    # Show initial status
    status = canary.get_deployment_status()
    print(f"\nInitial State:")
    print(f"  Stable version: {status['stable_version']}")
    print(f"  Traffic: {status['traffic']['stable_percentage']}% stable, {status['traffic']['canary_percentage']}% canary")

    # Deploy new version
    print("\nDeploying version 1.2.0 with canary rollout...")
    result = await canary.deploy("1.2.0")

    if result.success:
        print(f"✓ Canary deployment succeeded in {result.duration_seconds:.2f}s")
        print(f"  Phases completed: {result.phases_completed}/{result.total_phases}")
        print(f"  Final traffic: {result.final_canary_percentage}% to new version")
    else:
        print(f"✗ Canary deployment failed: {result.message}")
        print(f"  Failed at: {result.final_canary_percentage}% canary traffic")

    # Show metrics comparison
    status = canary.get_deployment_status()
    print(f"\nFinal State:")
    print(f"  Stable version: {status['stable_version']}")
    if status['baseline_metrics'] and status['canary_metrics']:
        print(f"  Baseline error rate: {status['baseline_metrics']['error_rate']:.4f}")
        print(f"  Canary error rate: {status['canary_metrics']['error_rate']:.4f}")


async def example_rollback_scenario():
    """
    Example: Automated rollback on deployment failure.

    Demonstrates using the rollback manager to recover from
    a failed deployment by routing traffic back to stable version.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Automated Rollback")
    print("=" * 60)

    # Initialize rollback manager
    manager = RollbackManager(
        current_version="1.2.0",
        previous_version="1.1.0",
    )

    # Simulate an active deployment
    manager.add_active_deployment(
        "deploy-123",
        "canary",
        "1.2.0",
        {"started_at": "2025-11-17T10:00:00"},
    )

    # Show initial status
    status = manager.get_rollback_status()
    print(f"\nInitial State:")
    print(f"  Current version: {status['current_version']}")
    print(f"  Active deployments: {status['active_deployments_count']}")

    # Perform rollback due to health check failure
    print("\nPerforming rollback due to health check failure...")
    result = await manager.rollback(reason=RollbackReason.HEALTH_CHECK_FAILURE)

    if result.success:
        print(f"✓ Rollback succeeded in {result.rollback_duration:.2f}s")
        print(f"  Rolled back from {result.previous_version} to {result.target_version}")
        print(f"  Steps completed: {len(result.steps_completed)}")
        for step in result.steps_completed:
            print(f"    ✓ {step}")
    else:
        print(f"✗ Rollback failed: {result.message}")
        if result.steps_failed:
            print(f"  Failed steps:")
            for step in result.steps_failed:
                print(f"    ✗ {step}")

    # Show final status
    status = manager.get_rollback_status()
    print(f"\nFinal State:")
    print(f"  Current version: {status['current_version']}")
    print(f"  Active deployments: {status['active_deployments_count']}")
    print(f"  Rollback history: {status['rollback_history_count']} operations")


async def example_smoke_tests():
    """
    Example: Post-deployment smoke tests.

    Demonstrates running comprehensive smoke tests after deployment
    to validate system functionality.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Smoke Tests")
    print("=" * 60)

    # Initialize smoke tests
    smoke = SmokeTests(
        endpoint_url="http://api.example.com",
        timeout=10.0,
        fail_fast=False,
    )

    # Run all smoke tests
    print("\nRunning smoke tests...")
    result = await smoke.run_all()

    print(f"\nTest Results:")
    print(f"  Total: {result.total_tests}")
    print(f"  Passed: {result.passed}")
    print(f"  Failed: {result.failed}")
    print(f"  Skipped: {result.skipped}")
    print(f"  Duration: {result.duration_seconds:.2f}s")
    print(f"  Overall: {'✓ SUCCESS' if result.success else '✗ FAILURE'}")

    # Show individual test results
    print(f"\nDetailed Results:")
    for test in result.test_results:
        status_symbol = "✓" if test.status.value == "passed" else "✗"
        print(f"  {status_symbol} {test.test_name} ({test.severity.value}): {test.message}")
        if test.error:
            print(f"      Error: {test.error}")


async def example_complete_deployment_pipeline():
    """
    Example: Complete deployment pipeline with all components.

    Demonstrates a full deployment workflow including:
    1. Blue-green deployment
    2. Smoke tests
    3. Rollback on failure
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Complete Deployment Pipeline")
    print("=" * 60)

    # Initialize components
    deployment = BlueGreenDeployment(monitoring_duration=5.0)
    smoke = SmokeTests(endpoint_url="http://api.example.com")
    rollback = RollbackManager(current_version="1.1.0", previous_version="1.0.0")

    # Register deployment
    rollback.add_active_deployment("deploy-456", "blue-green", "1.2.0")

    # Step 1: Deploy new version
    print("\n[1/3] Deploying version 1.2.0...")
    deploy_result = await deployment.deploy("1.2.0")

    if not deploy_result.success:
        print(f"✗ Deployment failed: {deploy_result.message}")
        print("\nInitiating rollback...")
        rollback_result = await rollback.rollback(reason=RollbackReason.DEPLOYMENT_TIMEOUT)
        print(f"Rollback: {rollback_result.message}")
        return

    print(f"✓ Deployment succeeded")

    # Step 2: Run smoke tests
    print("\n[2/3] Running smoke tests...")
    smoke_result = await smoke.run_all()
    print(f"Tests: {smoke_result.passed}/{smoke_result.total_tests} passed")

    if not smoke_result.success:
        print(f"✗ Smoke tests failed")
        print("\nInitiating rollback due to test failures...")
        rollback_result = await rollback.rollback(reason=RollbackReason.HEALTH_CHECK_FAILURE)
        print(f"Rollback: {rollback_result.message}")
        return

    print(f"✓ Smoke tests passed")

    # Step 3: Complete deployment
    print("\n[3/3] Finalizing deployment...")
    rollback.remove_active_deployment("deploy-456")
    rollback.current_version = "1.2.0"
    print("✓ Deployment complete!")

    # Show final summary
    print("\n" + "=" * 60)
    print("DEPLOYMENT SUMMARY")
    print("=" * 60)
    print(f"  Version deployed: 1.2.0")
    print(f"  Deployment time: {deploy_result.duration_seconds:.2f}s")
    print(f"  Tests passed: {smoke_result.passed}/{smoke_result.total_tests}")
    print(f"  Status: SUCCESS")


async def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("PRODUCTION OPERATIONS - DEPLOYMENT EXAMPLES")
    print("=" * 60)

    # Run individual examples
    await example_blue_green_deployment()
    await example_canary_deployment()
    await example_rollback_scenario()
    await example_smoke_tests()

    # Run complete pipeline
    await example_complete_deployment_pipeline()

    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
