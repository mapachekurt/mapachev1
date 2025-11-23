"""
Golden Task Executor - Runs golden tasks and collects results.

This module executes golden tasks against agents and validates outputs
against acceptance criteria.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
import asyncio
import time

from .golden_tasks import GoldenTask, AcceptanceCriterion
from .validator import OutputValidator


@dataclass
class TaskResult:
    """Result of executing a golden task."""

    task_id: str
    agent_id: str
    task_name: str
    passed: bool
    execution_time_ms: float
    cost_usd: float
    output: Any
    validation_results: Dict[str, bool] = field(default_factory=dict)
    error: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Convert task result to dictionary."""
        return {
            "task_id": self.task_id,
            "agent_id": self.agent_id,
            "task_name": self.task_name,
            "passed": self.passed,
            "execution_time_ms": self.execution_time_ms,
            "cost_usd": self.cost_usd,
            "output": self.output,
            "validation_results": self.validation_results,
            "error": self.error,
            "timestamp": self.timestamp,
        }


@dataclass
class ExecutionReport:
    """Report of golden task execution."""

    total_tasks: int
    passed_tasks: int
    failed_tasks: int
    total_execution_time_ms: float
    total_cost_usd: float
    pass_rate: float
    task_results: List[TaskResult]
    generated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary."""
        return {
            "total_tasks": self.total_tasks,
            "passed_tasks": self.passed_tasks,
            "failed_tasks": self.failed_tasks,
            "total_execution_time_ms": self.total_execution_time_ms,
            "total_cost_usd": self.total_cost_usd,
            "pass_rate": self.pass_rate,
            "task_results": [result.to_dict() for result in self.task_results],
            "generated_at": self.generated_at,
        }


class GoldenTaskExecutor:
    """
    Executor for golden tasks.

    Runs golden tasks against agents and validates outputs.
    """

    def __init__(self, validator: Optional[OutputValidator] = None):
        """
        Initialize executor.

        Args:
            validator: Optional custom validator (default: OutputValidator)
        """
        self.validator = validator or OutputValidator()

    async def execute_task(
        self,
        task: GoldenTask,
        agent_function: Callable[[Dict[str, Any]], Any],
        timeout_override: Optional[int] = None,
    ) -> TaskResult:
        """
        Execute a single golden task.

        Args:
            task: Golden task to execute
            agent_function: Agent function to call with input_data
            timeout_override: Optional timeout override in milliseconds

        Returns:
            TaskResult: Result of task execution
        """
        start_time = time.time()
        timeout_ms = timeout_override or task.timeout_ms
        timeout_seconds = timeout_ms / 1000.0

        try:
            # Execute agent with timeout
            output = await asyncio.wait_for(
                self._run_agent(agent_function, task.input_data),
                timeout=timeout_seconds,
            )

            # Calculate execution time
            execution_time_ms = (time.time() - start_time) * 1000

            # Validate output against acceptance criteria
            validation_results = {}
            all_passed = True

            for criterion in task.acceptance_criteria:
                # Extract the value to validate from output
                actual_value = self._extract_value(output, criterion.name)

                # Validate using criterion
                passed = self.validator.validate_criterion(
                    criterion=criterion,
                    actual_value=actual_value,
                    expected_value=criterion.expected_value,
                )

                validation_results[criterion.name] = passed
                if not passed:
                    all_passed = False

            # Estimate cost (placeholder - should integrate with actual cost tracking)
            cost_usd = self._estimate_cost(output)

            # Check cost limit
            if cost_usd > task.max_cost_usd:
                all_passed = False
                validation_results["cost_check"] = False

            return TaskResult(
                task_id=task.task_id,
                agent_id=task.agent_id,
                task_name=task.name,
                passed=all_passed,
                execution_time_ms=execution_time_ms,
                cost_usd=cost_usd,
                output=output,
                validation_results=validation_results,
            )

        except asyncio.TimeoutError:
            execution_time_ms = (time.time() - start_time) * 1000
            return TaskResult(
                task_id=task.task_id,
                agent_id=task.agent_id,
                task_name=task.name,
                passed=False,
                execution_time_ms=execution_time_ms,
                cost_usd=0.0,
                output=None,
                error=f"Task exceeded timeout of {timeout_ms}ms",
            )

        except Exception as e:
            execution_time_ms = (time.time() - start_time) * 1000
            return TaskResult(
                task_id=task.task_id,
                agent_id=task.agent_id,
                task_name=task.name,
                passed=False,
                execution_time_ms=execution_time_ms,
                cost_usd=0.0,
                output=None,
                error=str(e),
            )

    async def _run_agent(
        self, agent_function: Callable, input_data: Dict[str, Any]
    ) -> Any:
        """Run agent function (handles both sync and async)."""
        result = agent_function(input_data)
        if asyncio.iscoroutine(result):
            return await result
        return result

    def _extract_value(self, output: Any, key: str) -> Any:
        """Extract value from output using key."""
        if isinstance(output, dict):
            # Support nested keys with dot notation
            keys = key.split(".")
            value = output
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    return None
            return value
        return output

    def _estimate_cost(self, output: Any) -> float:
        """
        Estimate cost of execution.

        This is a placeholder - in production, this should integrate
        with actual cost tracking from the LLM API.
        """
        # Simple heuristic based on output size
        if isinstance(output, str):
            token_count = len(output.split())
        elif isinstance(output, dict):
            token_count = len(str(output).split())
        else:
            token_count = 100

        # Assume average cost of $0.0001 per 1k tokens
        return (token_count / 1000) * 0.0001

    async def execute_all_tasks(
        self,
        tasks: List[GoldenTask],
        agent_function: Callable[[Dict[str, Any]], Any],
        parallel: bool = True,
    ) -> List[TaskResult]:
        """
        Execute multiple golden tasks.

        Args:
            tasks: List of golden tasks to execute
            agent_function: Agent function to call
            parallel: Whether to execute tasks in parallel

        Returns:
            List[TaskResult]: Results for all tasks
        """
        if parallel:
            # Execute all tasks concurrently
            results = await asyncio.gather(
                *[self.execute_task(task, agent_function) for task in tasks],
                return_exceptions=True,
            )

            # Convert exceptions to failed results
            final_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    task = tasks[i]
                    final_results.append(
                        TaskResult(
                            task_id=task.task_id,
                            agent_id=task.agent_id,
                            task_name=task.name,
                            passed=False,
                            execution_time_ms=0.0,
                            cost_usd=0.0,
                            output=None,
                            error=str(result),
                        )
                    )
                else:
                    final_results.append(result)

            return final_results
        else:
            # Execute tasks sequentially
            results = []
            for task in tasks:
                result = await self.execute_task(task, agent_function)
                results.append(result)

            return results

    def generate_report(self, results: List[TaskResult]) -> ExecutionReport:
        """
        Generate execution report from task results.

        Args:
            results: List of task results

        Returns:
            ExecutionReport: Comprehensive execution report
        """
        total_tasks = len(results)
        passed_tasks = sum(1 for r in results if r.passed)
        failed_tasks = total_tasks - passed_tasks

        total_execution_time_ms = sum(r.execution_time_ms for r in results)
        total_cost_usd = sum(r.cost_usd for r in results)

        pass_rate = passed_tasks / total_tasks if total_tasks > 0 else 0.0

        return ExecutionReport(
            total_tasks=total_tasks,
            passed_tasks=passed_tasks,
            failed_tasks=failed_tasks,
            total_execution_time_ms=total_execution_time_ms,
            total_cost_usd=total_cost_usd,
            pass_rate=pass_rate,
            task_results=results,
        )

    async def execute_and_report(
        self,
        tasks: List[GoldenTask],
        agent_function: Callable[[Dict[str, Any]], Any],
        parallel: bool = True,
    ) -> ExecutionReport:
        """
        Execute tasks and generate report in one call.

        Args:
            tasks: List of golden tasks
            agent_function: Agent function to call
            parallel: Whether to execute in parallel

        Returns:
            ExecutionReport: Comprehensive execution report
        """
        results = await self.execute_all_tasks(tasks, agent_function, parallel)
        return self.generate_report(results)
