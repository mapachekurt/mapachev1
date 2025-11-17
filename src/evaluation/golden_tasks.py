"""
Golden Tasks - Benchmark tests for agent evaluation.

This module provides the core evaluation framework for testing agent quality
and preventing regressions in production systems.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
import yaml
from pathlib import Path


class ValidationMode(Enum):
    """Validation modes for acceptance criteria."""

    EXACT_MATCH = "exact_match"
    REGEX = "regex"
    SIMILARITY = "similarity"
    CUSTOM = "custom"


@dataclass
class AcceptanceCriterion:
    """Single acceptance criterion for a golden task."""

    name: str
    validation_mode: ValidationMode
    expected_value: Any = None
    threshold: float = 0.0
    custom_validator: Optional[callable] = None

    def __post_init__(self):
        """Convert string validation mode to enum."""
        if isinstance(self.validation_mode, str):
            self.validation_mode = ValidationMode(self.validation_mode)

    def validate(self, actual_value: Any) -> bool:
        """
        Validate actual value against criterion.

        Args:
            actual_value: The value to validate

        Returns:
            bool: True if validation passes
        """
        if self.validation_mode == ValidationMode.EXACT_MATCH:
            return actual_value == self.expected_value

        elif self.validation_mode == ValidationMode.REGEX:
            import re
            pattern = str(self.expected_value)
            return bool(re.match(pattern, str(actual_value)))

        elif self.validation_mode == ValidationMode.SIMILARITY:
            # Simple similarity check (can be enhanced with embeddings)
            similarity = self._compute_similarity(str(actual_value), str(self.expected_value))
            return similarity >= self.threshold

        elif self.validation_mode == ValidationMode.CUSTOM:
            if self.custom_validator is None:
                raise ValueError("Custom validator function required for CUSTOM mode")
            return self.custom_validator(actual_value, self.expected_value)

        return False

    def _compute_similarity(self, text1: str, text2: str) -> float:
        """
        Compute simple similarity between two strings.

        For production, this should use embeddings and cosine similarity.
        This is a simple placeholder implementation.
        """
        # Simple word overlap similarity
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))

        return intersection / union if union > 0 else 0.0


@dataclass
class GoldenTask:
    """
    A golden task represents a benchmark test for an agent.

    Golden tasks are used to ensure agent quality and prevent regressions.
    """

    task_id: str
    agent_id: str
    name: str
    description: str
    input_data: Dict[str, Any]
    expected_output: Dict[str, Any]
    acceptance_criteria: List[AcceptanceCriterion]
    timeout_ms: int = 30000
    max_cost_usd: float = 0.10
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert golden task to dictionary."""
        return {
            "task_id": self.task_id,
            "agent_id": self.agent_id,
            "name": self.name,
            "description": self.description,
            "input_data": self.input_data,
            "expected_output": self.expected_output,
            "acceptance_criteria": [
                {
                    "name": criterion.name,
                    "validation_mode": criterion.validation_mode.value,
                    "expected_value": criterion.expected_value,
                    "threshold": criterion.threshold,
                }
                for criterion in self.acceptance_criteria
            ],
            "timeout_ms": self.timeout_ms,
            "max_cost_usd": self.max_cost_usd,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GoldenTask":
        """Create golden task from dictionary."""
        # Convert acceptance criteria
        acceptance_criteria = [
            AcceptanceCriterion(
                name=criterion["name"],
                validation_mode=criterion["validation_mode"],
                expected_value=criterion.get("expected_value"),
                threshold=criterion.get("threshold", 0.0),
            )
            for criterion in data.get("acceptance_criteria", [])
        ]

        return cls(
            task_id=data["task_id"],
            agent_id=data["agent_id"],
            name=data["name"],
            description=data["description"],
            input_data=data["input_data"],
            expected_output=data["expected_output"],
            acceptance_criteria=acceptance_criteria,
            timeout_ms=data.get("timeout_ms", 30000),
            max_cost_usd=data.get("max_cost_usd", 0.10),
            metadata=data.get("metadata", {}),
        )


class GoldenTaskRegistry:
    """Registry for managing golden tasks."""

    def __init__(self):
        self.tasks: Dict[str, List[GoldenTask]] = {}

    def register(self, task: GoldenTask) -> None:
        """Register a golden task for an agent."""
        if task.agent_id not in self.tasks:
            self.tasks[task.agent_id] = []

        self.tasks[task.agent_id].append(task)

    def get_tasks(self, agent_id: str) -> List[GoldenTask]:
        """Get all golden tasks for an agent."""
        return self.tasks.get(agent_id, [])

    def get_task(self, task_id: str) -> Optional[GoldenTask]:
        """Get a specific golden task by ID."""
        for agent_tasks in self.tasks.values():
            for task in agent_tasks:
                if task.task_id == task_id:
                    return task
        return None

    def get_all_tasks(self) -> List[GoldenTask]:
        """Get all golden tasks across all agents."""
        all_tasks = []
        for agent_tasks in self.tasks.values():
            all_tasks.extend(agent_tasks)
        return all_tasks

    def load_from_yaml(self, yaml_path: str) -> None:
        """
        Load golden tasks from YAML configuration file.

        Args:
            yaml_path: Path to YAML file with golden tasks
        """
        path = Path(yaml_path)
        if not path.exists():
            raise FileNotFoundError(f"YAML file not found: {yaml_path}")

        with open(path, 'r') as f:
            data = yaml.safe_load(f)

        if not data:
            return

        for agent_id, tasks_data in data.items():
            for task_data in tasks_data:
                task_data["agent_id"] = agent_id
                task = GoldenTask.from_dict(task_data)
                self.register(task)

    def save_to_yaml(self, yaml_path: str) -> None:
        """
        Save golden tasks to YAML configuration file.

        Args:
            yaml_path: Path to save YAML file
        """
        # Group tasks by agent_id
        data = {}
        for agent_id, tasks in self.tasks.items():
            data[agent_id] = [task.to_dict() for task in tasks]

        path = Path(yaml_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    def count_tasks(self) -> int:
        """Get total count of golden tasks."""
        return sum(len(tasks) for tasks in self.tasks.values())

    def count_agents(self) -> int:
        """Get count of agents with golden tasks."""
        return len(self.tasks)
