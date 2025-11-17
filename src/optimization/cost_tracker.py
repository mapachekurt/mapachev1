"""Cost tracking system for LLM usage across agents, users, and tasks.

This module provides the CostTracker class which tracks and analyzes
costs associated with LLM usage for budgeting and optimization.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
from enum import Enum
import json


class CostCategory(Enum):
    """Categories of costs to track."""

    LLM_API = "llm_api"
    EMBEDDING = "embedding"
    STORAGE = "storage"
    COMPUTE = "compute"
    OTHER = "other"


@dataclass
class CostRecord:
    """Record of a cost event."""

    timestamp: datetime
    category: CostCategory
    amount: float
    agent_id: Optional[str] = None
    user_id: Optional[str] = None
    task_id: Optional[str] = None
    model_name: Optional[str] = None
    tokens_used: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CostSummary:
    """Summary of costs for a specific dimension."""

    total_cost: float
    total_tokens: int
    request_count: int
    average_cost_per_request: float
    cost_by_category: Dict[str, float]
    cost_by_model: Dict[str, float]
    period_start: datetime
    period_end: datetime


@dataclass
class BudgetAlert:
    """Alert for budget threshold exceeded."""

    dimension: str  # agent_id, user_id, or task_id
    identifier: str
    current_cost: float
    budget_limit: float
    threshold_percentage: float
    timestamp: datetime


class CostTracker:
    """Track and analyze costs for LLM usage across dimensions.

    This tracker maintains detailed cost records and provides analytics
    for agents, users, tasks, and time periods to support cost optimization
    and budget management.
    """

    def __init__(
        self,
        enable_alerts: bool = True,
        default_budget_period_days: int = 30
    ) -> None:
        """Initialize the cost tracker.

        Args:
            enable_alerts: Whether to generate budget alerts
            default_budget_period_days: Default period for budget calculations
        """
        self._records: List[CostRecord] = []
        self._budgets: Dict[str, Dict[str, float]] = {
            "agent": {},
            "user": {},
            "task": {},
            "global": {}
        }
        self._enable_alerts = enable_alerts
        self._default_budget_period_days = default_budget_period_days
        self._alerts: List[BudgetAlert] = []

        # Model pricing (cost per 1K tokens)
        self._model_pricing: Dict[str, Tuple[float, float]] = {
            # (input_cost, output_cost) per 1K tokens
            "gpt-4": (0.03, 0.06),
            "gpt-4-turbo": (0.01, 0.03),
            "gpt-3.5-turbo": (0.0015, 0.002),
            "claude-3-opus": (0.015, 0.075),
            "claude-3-sonnet": (0.003, 0.015),
            "claude-3-haiku": (0.00025, 0.00125),
            "local-slm": (0.0, 0.0)
        }

    def record(
        self,
        amount: float,
        category: CostCategory = CostCategory.LLM_API,
        agent_id: Optional[str] = None,
        user_id: Optional[str] = None,
        task_id: Optional[str] = None,
        model_name: Optional[str] = None,
        tokens_used: int = 0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> CostRecord:
        """Record a cost event.

        Args:
            amount: Cost amount in dollars
            category: Category of cost
            agent_id: Optional agent identifier
            user_id: Optional user identifier
            task_id: Optional task identifier
            model_name: Optional model name
            tokens_used: Number of tokens used
            metadata: Optional additional metadata

        Returns:
            Created CostRecord
        """
        metadata = metadata or {}

        record = CostRecord(
            timestamp=datetime.now(),
            category=category,
            amount=amount,
            agent_id=agent_id,
            user_id=user_id,
            task_id=task_id,
            model_name=model_name,
            tokens_used=tokens_used,
            metadata=metadata
        )

        self._records.append(record)

        # Check budgets and generate alerts
        if self._enable_alerts:
            self._check_budgets(record)

        return record

    def record_llm_call(
        self,
        model_name: str,
        input_tokens: int,
        output_tokens: int,
        agent_id: Optional[str] = None,
        user_id: Optional[str] = None,
        task_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> CostRecord:
        """Record an LLM API call with automatic cost calculation.

        Args:
            model_name: Name of the model used
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            agent_id: Optional agent identifier
            user_id: Optional user identifier
            task_id: Optional task identifier
            metadata: Optional additional metadata

        Returns:
            Created CostRecord
        """
        # Calculate cost based on model pricing
        if model_name in self._model_pricing:
            input_cost_per_1k, output_cost_per_1k = self._model_pricing[model_name]
            input_cost = (input_tokens / 1000) * input_cost_per_1k
            output_cost = (output_tokens / 1000) * output_cost_per_1k
            total_cost = input_cost + output_cost
        else:
            # Unknown model, use conservative estimate
            total_cost = ((input_tokens + output_tokens) / 1000) * 0.01

        metadata = metadata or {}
        metadata.update({
            "input_tokens": input_tokens,
            "output_tokens": output_tokens
        })

        return self.record(
            amount=total_cost,
            category=CostCategory.LLM_API,
            agent_id=agent_id,
            user_id=user_id,
            task_id=task_id,
            model_name=model_name,
            tokens_used=input_tokens + output_tokens,
            metadata=metadata
        )

    def get_stats(
        self,
        agent_id: Optional[str] = None,
        user_id: Optional[str] = None,
        task_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        category: Optional[CostCategory] = None
    ) -> CostSummary:
        """Get cost statistics for specified filters.

        Args:
            agent_id: Filter by agent ID
            user_id: Filter by user ID
            task_id: Filter by task ID
            start_time: Start of time period
            end_time: End of time period
            category: Filter by cost category

        Returns:
            CostSummary with aggregated statistics
        """
        # Filter records
        filtered_records = self._filter_records(
            agent_id=agent_id,
            user_id=user_id,
            task_id=task_id,
            start_time=start_time,
            end_time=end_time,
            category=category
        )

        if not filtered_records:
            return CostSummary(
                total_cost=0.0,
                total_tokens=0,
                request_count=0,
                average_cost_per_request=0.0,
                cost_by_category={},
                cost_by_model={},
                period_start=start_time or datetime.now(),
                period_end=end_time or datetime.now()
            )

        # Calculate aggregates
        total_cost = sum(r.amount for r in filtered_records)
        total_tokens = sum(r.tokens_used for r in filtered_records)
        request_count = len(filtered_records)
        avg_cost = total_cost / request_count if request_count > 0 else 0.0

        # Group by category
        cost_by_category: Dict[str, float] = defaultdict(float)
        for record in filtered_records:
            cost_by_category[record.category.value] += record.amount

        # Group by model
        cost_by_model: Dict[str, float] = defaultdict(float)
        for record in filtered_records:
            if record.model_name:
                cost_by_model[record.model_name] += record.amount

        return CostSummary(
            total_cost=round(total_cost, 4),
            total_tokens=total_tokens,
            request_count=request_count,
            average_cost_per_request=round(avg_cost, 4),
            cost_by_category=dict(cost_by_category),
            cost_by_model=dict(cost_by_model),
            period_start=start_time or filtered_records[0].timestamp,
            period_end=end_time or filtered_records[-1].timestamp
        )

    def get_agent_stats(self, agent_id: str, days: int = 30) -> CostSummary:
        """Get cost statistics for a specific agent.

        Args:
            agent_id: Agent identifier
            days: Number of days to include

        Returns:
            CostSummary for the agent
        """
        start_time = datetime.now() - timedelta(days=days)
        return self.get_stats(agent_id=agent_id, start_time=start_time)

    def get_user_stats(self, user_id: str, days: int = 30) -> CostSummary:
        """Get cost statistics for a specific user.

        Args:
            user_id: User identifier
            days: Number of days to include

        Returns:
            CostSummary for the user
        """
        start_time = datetime.now() - timedelta(days=days)
        return self.get_stats(user_id=user_id, start_time=start_time)

    def get_task_stats(self, task_id: str) -> CostSummary:
        """Get cost statistics for a specific task.

        Args:
            task_id: Task identifier

        Returns:
            CostSummary for the task
        """
        return self.get_stats(task_id=task_id)

    def set_budget(
        self,
        limit: float,
        dimension: str = "global",
        identifier: Optional[str] = None,
        period_days: Optional[int] = None
    ) -> None:
        """Set a budget limit.

        Args:
            limit: Budget limit in dollars
            dimension: Budget dimension (agent, user, task, global)
            identifier: Specific identifier for the dimension
            period_days: Budget period in days
        """
        if dimension not in self._budgets:
            self._budgets[dimension] = {}

        key = identifier if identifier else "default"
        self._budgets[dimension][key] = limit

    def get_budget_status(
        self,
        dimension: str = "global",
        identifier: Optional[str] = None,
        days: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get budget status for a dimension.

        Args:
            dimension: Budget dimension (agent, user, task, global)
            identifier: Specific identifier for the dimension
            days: Number of days to include in calculation

        Returns:
            Dictionary with budget status information
        """
        days = days or self._default_budget_period_days
        start_time = datetime.now() - timedelta(days=days)

        # Get current spending
        if dimension == "agent":
            stats = self.get_stats(agent_id=identifier, start_time=start_time)
        elif dimension == "user":
            stats = self.get_stats(user_id=identifier, start_time=start_time)
        elif dimension == "task":
            stats = self.get_stats(task_id=identifier)
        else:
            stats = self.get_stats(start_time=start_time)

        current_spending = stats.total_cost

        # Get budget limit
        key = identifier if identifier else "default"
        budget_limit = self._budgets.get(dimension, {}).get(key, 0.0)

        # Calculate status
        if budget_limit > 0:
            percentage_used = (current_spending / budget_limit) * 100
            remaining = budget_limit - current_spending
        else:
            percentage_used = 0.0
            remaining = 0.0

        return {
            "dimension": dimension,
            "identifier": identifier,
            "current_spending": round(current_spending, 4),
            "budget_limit": budget_limit,
            "remaining": round(remaining, 4),
            "percentage_used": round(percentage_used, 2),
            "period_days": days,
            "is_over_budget": current_spending > budget_limit if budget_limit > 0 else False
        }

    def get_top_spenders(
        self,
        dimension: str = "agent",
        limit: int = 10,
        days: int = 30
    ) -> List[Tuple[str, float]]:
        """Get top spenders for a dimension.

        Args:
            dimension: Dimension to analyze (agent, user, task)
            limit: Maximum number of results
            days: Number of days to include

        Returns:
            List of (identifier, total_cost) tuples sorted by cost
        """
        start_time = datetime.now() - timedelta(days=days)
        filtered_records = self._filter_records(start_time=start_time)

        # Aggregate by dimension
        costs: Dict[str, float] = defaultdict(float)
        for record in filtered_records:
            if dimension == "agent" and record.agent_id:
                costs[record.agent_id] += record.amount
            elif dimension == "user" and record.user_id:
                costs[record.user_id] += record.amount
            elif dimension == "task" and record.task_id:
                costs[record.task_id] += record.amount

        # Sort and limit
        sorted_costs = sorted(costs.items(), key=lambda x: x[1], reverse=True)
        return sorted_costs[:limit]

    def get_cost_trends(
        self,
        days: int = 30,
        granularity: str = "daily"
    ) -> Dict[str, List[Tuple[datetime, float]]]:
        """Get cost trends over time.

        Args:
            days: Number of days to include
            granularity: Granularity of data points (hourly, daily, weekly)

        Returns:
            Dictionary mapping categories to (timestamp, cost) lists
        """
        start_time = datetime.now() - timedelta(days=days)
        filtered_records = self._filter_records(start_time=start_time)

        # Group by time period and category
        trends: Dict[str, Dict[datetime, float]] = defaultdict(lambda: defaultdict(float))

        for record in filtered_records:
            # Round timestamp to granularity
            if granularity == "hourly":
                period = record.timestamp.replace(minute=0, second=0, microsecond=0)
            elif granularity == "daily":
                period = record.timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
            elif granularity == "weekly":
                days_since_monday = record.timestamp.weekday()
                period = (record.timestamp - timedelta(days=days_since_monday)).replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
            else:
                period = record.timestamp

            trends[record.category.value][period] += record.amount

        # Convert to sorted lists
        result = {}
        for category, period_costs in trends.items():
            sorted_periods = sorted(period_costs.items())
            result[category] = sorted_periods

        return result

    def get_alerts(self, clear: bool = False) -> List[BudgetAlert]:
        """Get budget alerts.

        Args:
            clear: Whether to clear alerts after retrieving

        Returns:
            List of BudgetAlert objects
        """
        alerts = self._alerts.copy()
        if clear:
            self._alerts.clear()
        return alerts

    def export_records(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        format: str = "json"
    ) -> str:
        """Export cost records.

        Args:
            start_time: Start of time period
            end_time: End of time period
            format: Export format (json, csv)

        Returns:
            Serialized cost records
        """
        filtered_records = self._filter_records(
            start_time=start_time,
            end_time=end_time
        )

        if format == "json":
            records_data = []
            for record in filtered_records:
                record_dict = {
                    "timestamp": record.timestamp.isoformat(),
                    "category": record.category.value,
                    "amount": record.amount,
                    "agent_id": record.agent_id,
                    "user_id": record.user_id,
                    "task_id": record.task_id,
                    "model_name": record.model_name,
                    "tokens_used": record.tokens_used,
                    "metadata": record.metadata
                }
                records_data.append(record_dict)

            return json.dumps(records_data, indent=2)
        else:
            raise ValueError(f"Unsupported export format: {format}")

    def _filter_records(
        self,
        agent_id: Optional[str] = None,
        user_id: Optional[str] = None,
        task_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        category: Optional[CostCategory] = None
    ) -> List[CostRecord]:
        """Filter cost records by criteria.

        Args:
            agent_id: Filter by agent ID
            user_id: Filter by user ID
            task_id: Filter by task ID
            start_time: Start of time period
            end_time: End of time period
            category: Filter by cost category

        Returns:
            Filtered list of CostRecord objects
        """
        filtered = self._records

        if agent_id:
            filtered = [r for r in filtered if r.agent_id == agent_id]

        if user_id:
            filtered = [r for r in filtered if r.user_id == user_id]

        if task_id:
            filtered = [r for r in filtered if r.task_id == task_id]

        if start_time:
            filtered = [r for r in filtered if r.timestamp >= start_time]

        if end_time:
            filtered = [r for r in filtered if r.timestamp <= end_time]

        if category:
            filtered = [r for r in filtered if r.category == category]

        return filtered

    def _check_budgets(self, record: CostRecord) -> None:
        """Check if any budgets are exceeded and generate alerts.

        Args:
            record: Most recent cost record
        """
        alert_thresholds = [0.8, 0.9, 1.0]  # 80%, 90%, 100%

        # Check agent budget
        if record.agent_id and "agent" in self._budgets:
            if record.agent_id in self._budgets["agent"]:
                self._check_dimension_budget(
                    "agent",
                    record.agent_id,
                    alert_thresholds
                )

        # Check user budget
        if record.user_id and "user" in self._budgets:
            if record.user_id in self._budgets["user"]:
                self._check_dimension_budget(
                    "user",
                    record.user_id,
                    alert_thresholds
                )

        # Check global budget
        if "global" in self._budgets and "default" in self._budgets["global"]:
            self._check_dimension_budget(
                "global",
                "default",
                alert_thresholds
            )

    def _check_dimension_budget(
        self,
        dimension: str,
        identifier: str,
        thresholds: List[float]
    ) -> None:
        """Check budget for a specific dimension and generate alerts.

        Args:
            dimension: Budget dimension
            identifier: Dimension identifier
            thresholds: List of threshold percentages to check
        """
        status = self.get_budget_status(dimension, identifier)
        percentage_used = status["percentage_used"] / 100

        for threshold in thresholds:
            if percentage_used >= threshold:
                # Check if we already alerted for this threshold
                existing_alert = any(
                    alert.dimension == dimension and
                    alert.identifier == identifier and
                    abs(alert.threshold_percentage - threshold) < 0.01
                    for alert in self._alerts
                )

                if not existing_alert:
                    alert = BudgetAlert(
                        dimension=dimension,
                        identifier=identifier,
                        current_cost=status["current_spending"],
                        budget_limit=status["budget_limit"],
                        threshold_percentage=threshold * 100,
                        timestamp=datetime.now()
                    )
                    self._alerts.append(alert)

    def add_model_pricing(
        self,
        model_name: str,
        input_cost_per_1k: float,
        output_cost_per_1k: float
    ) -> None:
        """Add or update pricing for a model.

        Args:
            model_name: Name of the model
            input_cost_per_1k: Cost per 1K input tokens
            output_cost_per_1k: Cost per 1K output tokens
        """
        self._model_pricing[model_name] = (input_cost_per_1k, output_cost_per_1k)
