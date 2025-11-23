"""
Unit tests for the evaluation framework.

Tests golden tasks, quality gates, executor, and validator.
"""

import pytest
import asyncio
import tempfile
from pathlib import Path
from unittest.mock import Mock, AsyncMock

from src.evaluation.golden_tasks import (
    GoldenTask,
    AcceptanceCriterion,
    ValidationMode,
    GoldenTaskRegistry,
)
from src.evaluation.quality_gates import (
    QualityGate,
    GateType,
    GateRequirement,
    GateOverride,
    GateManager,
)
from src.evaluation.executor import (
    GoldenTaskExecutor,
    TaskResult,
    ExecutionReport,
)
from src.evaluation.validator import (
    OutputValidator,
    ErrorCategory,
    ValidationError,
    validate_json_structure,
    validate_financial_metrics,
)


# ===== Golden Tasks Tests =====


class TestAcceptanceCriterion:
    """Test AcceptanceCriterion class."""

    def test_exact_match_validation(self):
        """Test exact match validation mode."""
        criterion = AcceptanceCriterion(
            name="status",
            validation_mode=ValidationMode.EXACT_MATCH,
            expected_value="success",
        )

        assert criterion.validate("success") is True
        assert criterion.validate("failure") is False

    def test_regex_validation(self):
        """Test regex validation mode."""
        criterion = AcceptanceCriterion(
            name="email",
            validation_mode=ValidationMode.REGEX,
            expected_value=r"^[\w\.-]+@[\w\.-]+\.\w+$",
        )

        assert criterion.validate("user@example.com") is True
        assert criterion.validate("invalid-email") is False

    def test_similarity_validation(self):
        """Test similarity validation mode."""
        criterion = AcceptanceCriterion(
            name="description",
            validation_mode=ValidationMode.SIMILARITY,
            expected_value="The quick brown fox jumps over the lazy dog",
            threshold=0.5,
        )

        assert criterion.validate("The quick brown fox jumps") is True
        assert criterion.validate("Completely different text") is False

    def test_custom_validation(self):
        """Test custom validation mode."""

        def custom_validator(actual, expected):
            return actual > expected

        criterion = AcceptanceCriterion(
            name="revenue",
            validation_mode=ValidationMode.CUSTOM,
            expected_value=1000,
            custom_validator=custom_validator,
        )

        assert criterion.validate(1500) is True
        assert criterion.validate(500) is False

    def test_string_to_enum_conversion(self):
        """Test that string validation_mode is converted to enum."""
        criterion = AcceptanceCriterion(
            name="test",
            validation_mode="exact_match",
            expected_value="value",
        )

        assert isinstance(criterion.validation_mode, ValidationMode)
        assert criterion.validation_mode == ValidationMode.EXACT_MATCH


class TestGoldenTask:
    """Test GoldenTask class."""

    def test_golden_task_creation(self):
        """Test creating a golden task."""
        criteria = [
            AcceptanceCriterion(
                name="revenue_growth",
                validation_mode=ValidationMode.EXACT_MATCH,
                expected_value=True,
            )
        ]

        task = GoldenTask(
            task_id="test-001",
            agent_id="financial_analyst",
            name="Q3 Revenue Analysis",
            description="Analyze Q3 revenue trends",
            input_data={"quarter": "Q3", "year": 2024},
            expected_output={"revenue_growth": True},
            acceptance_criteria=criteria,
            timeout_ms=5000,
            max_cost_usd=0.10,
        )

        assert task.task_id == "test-001"
        assert task.agent_id == "financial_analyst"
        assert len(task.acceptance_criteria) == 1

    def test_golden_task_to_dict(self):
        """Test converting golden task to dictionary."""
        criteria = [
            AcceptanceCriterion(
                name="status",
                validation_mode=ValidationMode.EXACT_MATCH,
                expected_value="success",
            )
        ]

        task = GoldenTask(
            task_id="test-001",
            agent_id="test_agent",
            name="Test Task",
            description="Test description",
            input_data={"key": "value"},
            expected_output={"status": "success"},
            acceptance_criteria=criteria,
        )

        task_dict = task.to_dict()

        assert task_dict["task_id"] == "test-001"
        assert task_dict["agent_id"] == "test_agent"
        assert len(task_dict["acceptance_criteria"]) == 1

    def test_golden_task_from_dict(self):
        """Test creating golden task from dictionary."""
        data = {
            "task_id": "test-001",
            "agent_id": "test_agent",
            "name": "Test Task",
            "description": "Test description",
            "input_data": {"key": "value"},
            "expected_output": {"status": "success"},
            "acceptance_criteria": [
                {
                    "name": "status",
                    "validation_mode": "exact_match",
                    "expected_value": "success",
                }
            ],
        }

        task = GoldenTask.from_dict(data)

        assert task.task_id == "test-001"
        assert task.agent_id == "test_agent"
        assert len(task.acceptance_criteria) == 1


class TestGoldenTaskRegistry:
    """Test GoldenTaskRegistry class."""

    def test_register_task(self):
        """Test registering a golden task."""
        registry = GoldenTaskRegistry()

        task = GoldenTask(
            task_id="test-001",
            agent_id="test_agent",
            name="Test Task",
            description="Test",
            input_data={},
            expected_output={},
            acceptance_criteria=[],
        )

        registry.register(task)

        assert len(registry.get_tasks("test_agent")) == 1
        assert registry.count_tasks() == 1

    def test_get_tasks_by_agent(self):
        """Test getting tasks for specific agent."""
        registry = GoldenTaskRegistry()

        task1 = GoldenTask(
            task_id="test-001",
            agent_id="agent1",
            name="Task 1",
            description="Test",
            input_data={},
            expected_output={},
            acceptance_criteria=[],
        )

        task2 = GoldenTask(
            task_id="test-002",
            agent_id="agent2",
            name="Task 2",
            description="Test",
            input_data={},
            expected_output={},
            acceptance_criteria=[],
        )

        registry.register(task1)
        registry.register(task2)

        assert len(registry.get_tasks("agent1")) == 1
        assert len(registry.get_tasks("agent2")) == 1

    def test_get_task_by_id(self):
        """Test getting task by ID."""
        registry = GoldenTaskRegistry()

        task = GoldenTask(
            task_id="test-001",
            agent_id="test_agent",
            name="Test Task",
            description="Test",
            input_data={},
            expected_output={},
            acceptance_criteria=[],
        )

        registry.register(task)

        retrieved = registry.get_task("test-001")
        assert retrieved is not None
        assert retrieved.task_id == "test-001"

    def test_load_from_yaml(self):
        """Test loading tasks from YAML file."""
        registry = GoldenTaskRegistry()

        yaml_content = """
financial_analyst:
  - task_id: fa-001
    name: Q3 Revenue Analysis
    description: Analyze revenue
    input_data:
      quarter: Q3
      year: 2024
    expected_output:
      revenue_growth: true
    acceptance_criteria:
      - name: revenue_growth
        validation_mode: exact_match
        expected_value: true
        threshold: 0.0
"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            yaml_path = f.name

        try:
            registry.load_from_yaml(yaml_path)

            assert registry.count_tasks() == 1
            assert registry.count_agents() == 1

            tasks = registry.get_tasks("financial_analyst")
            assert len(tasks) == 1
            assert tasks[0].task_id == "fa-001"
        finally:
            Path(yaml_path).unlink()


# ===== Quality Gates Tests =====


class TestQualityGate:
    """Test QualityGate class."""

    def test_create_dev_to_staging_gate(self):
        """Test creating dev-to-staging quality gate."""
        gate = QualityGate.create_dev_to_staging_gate()

        assert gate.gate_type == GateType.DEV_TO_STAGING
        assert len(gate.requirements) == 4

    def test_create_staging_to_prod_gate(self):
        """Test creating staging-to-production quality gate."""
        gate = QualityGate.create_staging_to_prod_gate()

        assert gate.gate_type == GateType.STAGING_TO_PROD
        assert len(gate.requirements) == 6

    def test_create_prod_monitoring_gate(self):
        """Test creating production monitoring quality gate."""
        gate = QualityGate.create_prod_monitoring_gate()

        assert gate.gate_type == GateType.PROD_MONITORING
        assert len(gate.requirements) == 4

    def test_check_requirement(self):
        """Test checking individual requirement."""
        gate = QualityGate(
            gate_type=GateType.DEV_TO_STAGING,
            requirements=[
                GateRequirement(
                    name="pass_rate",
                    description="Pass rate >= 80%",
                    threshold=0.8,
                )
            ],
        )

        assert gate.check_requirement("pass_rate", 0.85) is True
        assert gate.check_requirement("pass_rate", 0.75) is False

    def test_evaluate_gate(self):
        """Test evaluating entire gate."""
        gate = QualityGate(
            gate_type=GateType.DEV_TO_STAGING,
            requirements=[
                GateRequirement(
                    name="req1",
                    description="Test",
                    required=True,
                    threshold=0.8,
                ),
                GateRequirement(
                    name="req2",
                    description="Test",
                    required=True,
                    threshold=0.9,
                ),
            ],
        )

        gate.check_requirement("req1", 0.85)
        gate.check_requirement("req2", 0.95)

        assert gate.evaluate() is True

    def test_evaluate_gate_failure(self):
        """Test gate evaluation failure."""
        gate = QualityGate(
            gate_type=GateType.DEV_TO_STAGING,
            requirements=[
                GateRequirement(
                    name="req1",
                    description="Test",
                    required=True,
                    threshold=0.8,
                ),
            ],
        )

        gate.check_requirement("req1", 0.70)

        assert gate.evaluate() is False


class TestGateManager:
    """Test GateManager class."""

    def test_register_override(self):
        """Test registering a manual override."""
        manager = GateManager()

        override = manager.register_override(
            gate_type=GateType.DEV_TO_STAGING,
            requirement_name="golden_task_pass_rate",
            reason="Emergency hotfix",
            overridden_by="admin",
        )

        assert override is not None
        assert len(manager.overrides) == 1

    def test_has_override(self):
        """Test checking for override."""
        manager = GateManager()

        manager.register_override(
            gate_type=GateType.DEV_TO_STAGING,
            requirement_name="golden_task_pass_rate",
            reason="Emergency hotfix",
            overridden_by="admin",
        )

        assert manager.has_override(GateType.DEV_TO_STAGING, "golden_task_pass_rate") is True
        assert manager.has_override(GateType.DEV_TO_STAGING, "other_requirement") is False

    def test_evaluate_with_overrides(self):
        """Test evaluating gate with overrides."""
        manager = GateManager()
        gate = QualityGate(
            gate_type=GateType.DEV_TO_STAGING,
            requirements=[
                GateRequirement(
                    name="pass_rate",
                    description="Test",
                    required=True,
                    threshold=0.8,
                ),
            ],
        )

        # Fail the requirement
        gate.check_requirement("pass_rate", 0.70)

        # Should fail without override
        assert gate.evaluate() is False

        # Register override
        manager.register_override(
            gate_type=GateType.DEV_TO_STAGING,
            requirement_name="pass_rate",
            reason="Emergency",
            overridden_by="admin",
        )

        # Should pass with override
        results = manager.evaluate_with_overrides(gate)
        assert results["passed"] is True


# ===== Executor Tests =====


class TestGoldenTaskExecutor:
    """Test GoldenTaskExecutor class."""

    @pytest.mark.asyncio
    async def test_execute_task_success(self):
        """Test successful task execution."""
        executor = GoldenTaskExecutor()

        async def mock_agent(input_data):
            return {"status": "success"}

        task = GoldenTask(
            task_id="test-001",
            agent_id="test_agent",
            name="Test Task",
            description="Test",
            input_data={"key": "value"},
            expected_output={"status": "success"},
            acceptance_criteria=[
                AcceptanceCriterion(
                    name="status",
                    validation_mode=ValidationMode.EXACT_MATCH,
                    expected_value="success",
                )
            ],
        )

        result = await executor.execute_task(task, mock_agent)

        assert result.passed is True
        assert result.error is None
        assert result.task_id == "test-001"

    @pytest.mark.asyncio
    async def test_execute_task_timeout(self):
        """Test task execution timeout."""
        executor = GoldenTaskExecutor()

        async def slow_agent(input_data):
            await asyncio.sleep(10)
            return {"status": "success"}

        task = GoldenTask(
            task_id="test-001",
            agent_id="test_agent",
            name="Test Task",
            description="Test",
            input_data={"key": "value"},
            expected_output={"status": "success"},
            acceptance_criteria=[],
            timeout_ms=100,  # 100ms timeout
        )

        result = await executor.execute_task(task, slow_agent)

        assert result.passed is False
        assert "timeout" in result.error.lower()

    @pytest.mark.asyncio
    async def test_execute_task_failure(self):
        """Test task execution with validation failure."""
        executor = GoldenTaskExecutor()

        async def mock_agent(input_data):
            return {"status": "failure"}

        task = GoldenTask(
            task_id="test-001",
            agent_id="test_agent",
            name="Test Task",
            description="Test",
            input_data={"key": "value"},
            expected_output={"status": "success"},
            acceptance_criteria=[
                AcceptanceCriterion(
                    name="status",
                    validation_mode=ValidationMode.EXACT_MATCH,
                    expected_value="success",
                )
            ],
        )

        result = await executor.execute_task(task, mock_agent)

        assert result.passed is False
        assert result.validation_results["status"] is False

    @pytest.mark.asyncio
    async def test_execute_all_tasks_parallel(self):
        """Test executing multiple tasks in parallel."""
        executor = GoldenTaskExecutor()

        async def mock_agent(input_data):
            return {"status": "success"}

        tasks = [
            GoldenTask(
                task_id=f"test-{i:03d}",
                agent_id="test_agent",
                name=f"Test Task {i}",
                description="Test",
                input_data={"key": "value"},
                expected_output={"status": "success"},
                acceptance_criteria=[
                    AcceptanceCriterion(
                        name="status",
                        validation_mode=ValidationMode.EXACT_MATCH,
                        expected_value="success",
                    )
                ],
            )
            for i in range(5)
        ]

        results = await executor.execute_all_tasks(tasks, mock_agent, parallel=True)

        assert len(results) == 5
        assert all(r.passed for r in results)

    @pytest.mark.asyncio
    async def test_generate_report(self):
        """Test generating execution report."""
        executor = GoldenTaskExecutor()

        results = [
            TaskResult(
                task_id=f"test-{i:03d}",
                agent_id="test_agent",
                task_name=f"Task {i}",
                passed=(i % 2 == 0),  # Alternate pass/fail
                execution_time_ms=100.0,
                cost_usd=0.01,
                output={},
            )
            for i in range(10)
        ]

        report = executor.generate_report(results)

        assert report.total_tasks == 10
        assert report.passed_tasks == 5
        assert report.failed_tasks == 5
        assert report.pass_rate == 0.5


# ===== Validator Tests =====


class TestOutputValidator:
    """Test OutputValidator class."""

    def test_validate_exact_match(self):
        """Test exact match validation."""
        validator = OutputValidator()

        assert validator.validate_exact_match("test", "test") is True
        assert validator.validate_exact_match("test", "other") is False

    def test_validate_regex(self):
        """Test regex validation."""
        validator = OutputValidator()

        assert validator.validate_regex("test123", r"test\d+") is True
        assert validator.validate_regex("test", r"test\d+") is False

    def test_validate_similarity(self):
        """Test similarity validation."""
        validator = OutputValidator()

        assert validator.validate_similarity(
            "The quick brown fox",
            "The quick brown fox jumps",
            threshold=0.6,
        ) is True

        assert validator.validate_similarity(
            "Completely different",
            "The quick brown fox",
            threshold=0.6,
        ) is False

    def test_register_custom_validator(self):
        """Test registering custom validator."""
        validator = OutputValidator()

        def custom_validator(actual, expected):
            return actual > expected

        validator.register_custom_validator("greater_than", custom_validator)

        assert validator.validate_custom(10, 5, "greater_than") is True
        assert validator.validate_custom(5, 10, "greater_than") is False

    def test_validate_numeric_range(self):
        """Test numeric range validation."""
        validator = OutputValidator()

        assert validator.validate_numeric_range(50, 0, 100) is True
        assert validator.validate_numeric_range(150, 0, 100) is False

    def test_validate_list_contains(self):
        """Test list contains validation."""
        validator = OutputValidator()

        assert validator.validate_list_contains([1, 2, 3, 4], [2, 3]) is True
        assert validator.validate_list_contains([1, 2, 3], [4, 5]) is False

    def test_validate_dict_has_keys(self):
        """Test dictionary has keys validation."""
        validator = OutputValidator()

        assert validator.validate_dict_has_keys({"a": 1, "b": 2, "c": 3}, ["a", "b"]) is True
        assert validator.validate_dict_has_keys({"a": 1, "b": 2}, ["c"]) is False

    def test_categorize_error(self):
        """Test error categorization."""
        validator = OutputValidator()

        assert validator.categorize_error(Exception("timeout error")) == ErrorCategory.TIMEOUT
        assert validator.categorize_error(Exception("cost exceeded")) == ErrorCategory.COST_EXCEEDED
        assert validator.categorize_error(Exception("format error")) == ErrorCategory.FORMAT_ERROR


class TestCustomValidators:
    """Test custom validator functions."""

    def test_validate_json_structure(self):
        """Test JSON structure validation."""
        actual = {"name": "John", "age": 30}
        expected_structure = {"name": str, "age": int}

        assert validate_json_structure(actual, expected_structure) is True

    def test_validate_financial_metrics(self):
        """Test financial metrics validation with tolerance."""
        actual = {"revenue": 1000, "profit": 200}
        expected = {"revenue": 1020, "profit": 205}

        assert validate_financial_metrics(actual, expected) is True

    def test_validate_financial_metrics_failure(self):
        """Test financial metrics validation failure."""
        actual = {"revenue": 1000, "profit": 200}
        expected = {"revenue": 2000, "profit": 400}  # Too far off

        assert validate_financial_metrics(actual, expected) is False
