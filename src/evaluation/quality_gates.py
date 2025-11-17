"""
Quality Gates - Automated quality checks for agent deployments.

This module provides quality gates to ensure agents meet requirements
before moving between environments (dev → staging → production).
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import json


class GateType(Enum):
    """Types of quality gates."""

    DEV_TO_STAGING = "dev_to_staging"
    STAGING_TO_PROD = "staging_to_prod"
    PROD_MONITORING = "prod_monitoring"


@dataclass
class GateRequirement:
    """Single requirement for a quality gate."""

    name: str
    description: str
    required: bool = True
    threshold: Optional[float] = None
    actual_value: Optional[Any] = None
    passed: bool = False


@dataclass
class QualityGate:
    """
    Quality gate with multiple requirements.

    Quality gates prevent low-quality agents from reaching production.
    """

    gate_type: GateType
    requirements: List[GateRequirement]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Convert string gate type to enum."""
        if isinstance(self.gate_type, str):
            self.gate_type = GateType(self.gate_type)

    def check_requirement(self, name: str, actual_value: Any) -> bool:
        """
        Check if a requirement passes.

        Args:
            name: Requirement name
            actual_value: Actual value to check

        Returns:
            bool: True if requirement passes
        """
        requirement = self._get_requirement(name)
        if not requirement:
            raise ValueError(f"Requirement not found: {name}")

        requirement.actual_value = actual_value

        # Check based on requirement type
        if requirement.threshold is not None:
            # Numeric comparison
            if isinstance(actual_value, (int, float)):
                requirement.passed = actual_value >= requirement.threshold
            else:
                requirement.passed = False
        elif isinstance(actual_value, bool):
            # Boolean check
            requirement.passed = actual_value
        else:
            # Existence check
            requirement.passed = actual_value is not None

        return requirement.passed

    def _get_requirement(self, name: str) -> Optional[GateRequirement]:
        """Get requirement by name."""
        for req in self.requirements:
            if req.name == name:
                return req
        return None

    def evaluate(self) -> bool:
        """
        Evaluate if the gate passes.

        Returns:
            bool: True if all required requirements pass
        """
        for requirement in self.requirements:
            if requirement.required and not requirement.passed:
                return False
        return True

    def get_results(self) -> Dict[str, Any]:
        """Get gate evaluation results."""
        return {
            "gate_type": self.gate_type.value,
            "passed": self.evaluate(),
            "requirements": [
                {
                    "name": req.name,
                    "description": req.description,
                    "required": req.required,
                    "threshold": req.threshold,
                    "actual_value": req.actual_value,
                    "passed": req.passed,
                }
                for req in self.requirements
            ],
            "metadata": self.metadata,
            "evaluated_at": datetime.utcnow().isoformat(),
        }

    @classmethod
    def create_dev_to_staging_gate(cls) -> "QualityGate":
        """
        Create a dev-to-staging quality gate.

        Requirements:
        - Golden task pass rate >= 80%
        - Has evaluation framework
        - Has unit tests
        - Documentation complete
        """
        requirements = [
            GateRequirement(
                name="golden_task_pass_rate",
                description="Golden task pass rate >= 80%",
                required=True,
                threshold=0.80,
            ),
            GateRequirement(
                name="has_evaluation",
                description="Has evaluation framework implemented",
                required=True,
            ),
            GateRequirement(
                name="has_unit_tests",
                description="Has unit tests with coverage",
                required=True,
            ),
            GateRequirement(
                name="documentation_complete",
                description="Documentation is complete",
                required=True,
            ),
        ]
        return cls(gate_type=GateType.DEV_TO_STAGING, requirements=requirements)

    @classmethod
    def create_staging_to_prod_gate(cls) -> "QualityGate":
        """
        Create a staging-to-production quality gate.

        Requirements:
        - Golden task pass rate >= 95%
        - Load test passed
        - Cost per request <= $0.10
        - P95 latency <= 5000ms
        - Has rollback plan
        - Has monitoring
        """
        requirements = [
            GateRequirement(
                name="golden_task_pass_rate",
                description="Golden task pass rate >= 95%",
                required=True,
                threshold=0.95,
            ),
            GateRequirement(
                name="load_test_passed",
                description="Load testing passed successfully",
                required=True,
            ),
            GateRequirement(
                name="cost_per_request",
                description="Average cost per request <= $0.10",
                required=True,
                threshold=0.10,
            ),
            GateRequirement(
                name="p95_latency_ms",
                description="P95 latency <= 5000ms",
                required=True,
                threshold=5000.0,
            ),
            GateRequirement(
                name="has_rollback_plan",
                description="Rollback plan documented and tested",
                required=True,
            ),
            GateRequirement(
                name="has_monitoring",
                description="Monitoring and alerting configured",
                required=True,
            ),
        ]
        return cls(gate_type=GateType.STAGING_TO_PROD, requirements=requirements)

    @classmethod
    def create_prod_monitoring_gate(cls) -> "QualityGate":
        """
        Create a production monitoring quality gate.

        Requirements:
        - Success rate >= 99%
        - Error rate <= 1%
        - Cost deviation <= 20%
        - Human feedback score >= 4.0
        """
        requirements = [
            GateRequirement(
                name="success_rate",
                description="Success rate >= 99%",
                required=True,
                threshold=0.99,
            ),
            GateRequirement(
                name="error_rate",
                description="Error rate <= 1%",
                required=True,
                threshold=0.01,
            ),
            GateRequirement(
                name="cost_deviation",
                description="Cost deviation from baseline <= 20%",
                required=True,
                threshold=0.20,
            ),
            GateRequirement(
                name="human_feedback_score",
                description="Average human feedback score >= 4.0/5.0",
                required=False,
                threshold=4.0,
            ),
        ]
        return cls(gate_type=GateType.PROD_MONITORING, requirements=requirements)


@dataclass
class GateOverride:
    """Manual override for quality gate requirements."""

    gate_type: GateType
    requirement_name: str
    reason: str
    overridden_by: str
    overridden_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    approval_required: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert override to dictionary."""
        return {
            "gate_type": self.gate_type.value if isinstance(self.gate_type, GateType) else self.gate_type,
            "requirement_name": self.requirement_name,
            "reason": self.reason,
            "overridden_by": self.overridden_by,
            "overridden_at": self.overridden_at,
            "approval_required": self.approval_required,
        }

    def save_to_file(self, file_path: str) -> None:
        """Save override to audit log file."""
        with open(file_path, 'a') as f:
            json.dump(self.to_dict(), f)
            f.write('\n')


class GateManager:
    """Manager for quality gates and overrides."""

    def __init__(self):
        self.overrides: List[GateOverride] = []

    def register_override(
        self,
        gate_type: GateType,
        requirement_name: str,
        reason: str,
        overridden_by: str,
    ) -> GateOverride:
        """
        Register a manual override for a quality gate requirement.

        Args:
            gate_type: Type of gate
            requirement_name: Name of requirement to override
            reason: Reason for override
            overridden_by: User who approved override

        Returns:
            GateOverride: The registered override
        """
        override = GateOverride(
            gate_type=gate_type,
            requirement_name=requirement_name,
            reason=reason,
            overridden_by=overridden_by,
        )
        self.overrides.append(override)
        return override

    def has_override(self, gate_type: GateType, requirement_name: str) -> bool:
        """Check if a requirement has an active override."""
        for override in self.overrides:
            if (
                override.gate_type == gate_type
                and override.requirement_name == requirement_name
            ):
                return True
        return False

    def evaluate_with_overrides(self, gate: QualityGate) -> Dict[str, Any]:
        """
        Evaluate gate with consideration for overrides.

        Args:
            gate: Quality gate to evaluate

        Returns:
            dict: Evaluation results with override information
        """
        results = gate.get_results()

        # Check for overrides
        overridden_requirements = []
        for req in gate.requirements:
            if not req.passed and self.has_override(gate.gate_type, req.name):
                overridden_requirements.append(req.name)

        # Update pass status if all failures are overridden
        if overridden_requirements:
            all_failures_overridden = all(
                req.passed or req.name in overridden_requirements
                for req in gate.requirements
                if req.required
            )
            results["passed"] = all_failures_overridden
            results["overridden_requirements"] = overridden_requirements

        return results
