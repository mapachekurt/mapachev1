"""
Dashboard definitions for agent observability visualization.

This module provides dashboard configurations in JSON format for various
monitoring platforms including Looker Studio, Grafana, and custom dashboards.
"""

import json
from typing import Any, Dict, List, Optional
from datetime import datetime


class DashboardDefinition:
    """
    Base class for dashboard definitions.

    Provides a structured way to define monitoring dashboards with panels,
    queries, and visualizations.

    Attributes:
        name: Dashboard name
        description: Dashboard description
        panels: List of dashboard panels
        refresh_interval: Auto-refresh interval in seconds
    """

    def __init__(
        self,
        name: str,
        description: str,
        refresh_interval: int = 30,
    ) -> None:
        """
        Initialize a dashboard definition.

        Args:
            name: Dashboard name
            description: Dashboard description
            refresh_interval: Auto-refresh interval in seconds
        """
        self.name = name
        self.description = description
        self.refresh_interval = refresh_interval
        self.panels: List[Dict[str, Any]] = []
        self.created_at = datetime.utcnow().isoformat()

    def add_panel(
        self,
        title: str,
        panel_type: str,
        query: str,
        visualization: str,
        position: Optional[Dict[str, int]] = None,
        **kwargs: Any,
    ) -> "DashboardDefinition":
        """
        Add a panel to the dashboard.

        Args:
            title: Panel title
            panel_type: Type of panel (metric, graph, table, heatmap, etc.)
            query: Query or metric expression
            visualization: Visualization type
            position: Optional position dict with x, y, w, h
            **kwargs: Additional panel configuration

        Returns:
            Self for method chaining
        """
        panel = {
            "title": title,
            "type": panel_type,
            "query": query,
            "visualization": visualization,
            "position": position or {"x": 0, "y": 0, "w": 6, "h": 4},
            **kwargs,
        }
        self.panels.append(panel)
        return self

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert dashboard to dictionary.

        Returns:
            Dictionary representation of the dashboard
        """
        return {
            "name": self.name,
            "description": self.description,
            "refresh_interval": self.refresh_interval,
            "created_at": self.created_at,
            "panels": self.panels,
        }

    def to_json(self, indent: int = 2) -> str:
        """
        Convert dashboard to JSON string.

        Args:
            indent: JSON indentation level

        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), indent=indent)


class AgentOverviewDashboard(DashboardDefinition):
    """Agent system overview dashboard with key metrics."""

    def __init__(self) -> None:
        """Initialize the agent overview dashboard."""
        super().__init__(
            name="Agent System Overview",
            description="High-level overview of agent system health and performance",
            refresh_interval=30,
        )
        self._build_panels()

    def _build_panels(self) -> None:
        """Build dashboard panels."""
        # Request rate panel
        self.add_panel(
            title="Request Rate",
            panel_type="time_series",
            query="rate(agent_system_requests_total[5m])",
            visualization="line_chart",
            position={"x": 0, "y": 0, "w": 6, "h": 4},
            unit="requests/sec",
            legend="bottom",
        )

        # Active requests gauge
        self.add_panel(
            title="Active Requests",
            panel_type="gauge",
            query="sum(agent_system_active_requests)",
            visualization="gauge",
            position={"x": 6, "y": 0, "w": 3, "h": 4},
            threshold_warning=50,
            threshold_critical=100,
        )

        # Error rate panel
        self.add_panel(
            title="Error Rate",
            panel_type="time_series",
            query="rate(agent_system_errors_total[5m])",
            visualization="line_chart",
            position={"x": 9, "y": 0, "w": 3, "h": 4},
            unit="errors/sec",
            color="red",
        )

        # Request duration histogram
        self.add_panel(
            title="Request Duration (p50, p95, p99)",
            panel_type="time_series",
            query=[
                "histogram_quantile(0.50, rate(agent_system_duration_seconds_bucket[5m]))",
                "histogram_quantile(0.95, rate(agent_system_duration_seconds_bucket[5m]))",
                "histogram_quantile(0.99, rate(agent_system_duration_seconds_bucket[5m]))",
            ],
            visualization="multi_line_chart",
            position={"x": 0, "y": 4, "w": 6, "h": 4},
            unit="seconds",
            legend="right",
        )

        # Success rate panel
        self.add_panel(
            title="Success Rate",
            panel_type="stat",
            query=(
                "sum(rate(agent_system_requests_total{status='success'}[5m])) / "
                "sum(rate(agent_system_requests_total[5m])) * 100"
            ),
            visualization="stat",
            position={"x": 6, "y": 4, "w": 3, "h": 4},
            unit="percent",
            threshold_warning=95,
            threshold_critical=90,
        )

        # Cost tracking panel
        self.add_panel(
            title="Hourly Cost (USD)",
            panel_type="time_series",
            query="rate(agent_system_cost_usd_total[1h])",
            visualization="area_chart",
            position={"x": 9, "y": 4, "w": 3, "h": 4},
            unit="USD/hour",
            color="green",
        )


class AgentPerformanceDashboard(DashboardDefinition):
    """Detailed agent performance metrics dashboard."""

    def __init__(self) -> None:
        """Initialize the agent performance dashboard."""
        super().__init__(
            name="Agent Performance Metrics",
            description="Detailed performance metrics for agent operations",
            refresh_interval=15,
        )
        self._build_panels()

    def _build_panels(self) -> None:
        """Build dashboard panels."""
        # Task duration by type
        self.add_panel(
            title="Task Duration by Type",
            panel_type="time_series",
            query="avg(agent_system_task_duration_seconds) by (task_type)",
            visualization="stacked_area",
            position={"x": 0, "y": 0, "w": 8, "h": 5},
            unit="seconds",
            legend="bottom",
        )

        # Request throughput by agent
        self.add_panel(
            title="Throughput by Agent",
            panel_type="bar_chart",
            query="sum(rate(agent_system_requests_total[5m])) by (agent_id)",
            visualization="horizontal_bar",
            position={"x": 8, "y": 0, "w": 4, "h": 5},
            unit="req/s",
        )

        # Memory usage
        self.add_panel(
            title="Memory Usage by Agent",
            panel_type="time_series",
            query="agent_system_memory_usage_bytes by (agent_id)",
            visualization="line_chart",
            position={"x": 0, "y": 5, "w": 6, "h": 4},
            unit="bytes",
            format="bytes",
        )

        # Queue depth
        self.add_panel(
            title="Queue Depth",
            panel_type="time_series",
            query="agent_system_queue_depth by (queue_name)",
            visualization="line_chart",
            position={"x": 6, "y": 5, "w": 6, "h": 4},
            unit="tasks",
        )

        # Response time heatmap
        self.add_panel(
            title="Response Time Distribution",
            panel_type="heatmap",
            query="rate(agent_system_response_time_seconds_bucket[5m])",
            visualization="heatmap",
            position={"x": 0, "y": 9, "w": 12, "h": 5},
            unit="seconds",
        )


class LLMMetricsDashboard(DashboardDefinition):
    """Dashboard for LLM-specific metrics and costs."""

    def __init__(self) -> None:
        """Initialize the LLM metrics dashboard."""
        super().__init__(
            name="LLM Metrics & Costs",
            description="LLM usage, token consumption, and cost tracking",
            refresh_interval=60,
        )
        self._build_panels()

    def _build_panels(self) -> None:
        """Build dashboard panels."""
        # Token consumption by model
        self.add_panel(
            title="Token Consumption by Model",
            panel_type="time_series",
            query="sum(rate(agent_system_llm_tokens_total[1h])) by (model)",
            visualization="stacked_area",
            position={"x": 0, "y": 0, "w": 8, "h": 5},
            unit="tokens/hour",
            legend="bottom",
        )

        # Cost by model
        self.add_panel(
            title="Cost by Model (Last 24h)",
            panel_type="pie_chart",
            query="sum(increase(agent_system_cost_usd_total{cost_type='llm'}[24h])) by (model)",
            visualization="donut",
            position={"x": 8, "y": 0, "w": 4, "h": 5},
            unit="USD",
        )

        # Prompt vs completion tokens
        self.add_panel(
            title="Prompt vs Completion Tokens",
            panel_type="time_series",
            query=[
                "sum(rate(agent_system_llm_tokens_total{token_type='prompt'}[5m]))",
                "sum(rate(agent_system_llm_tokens_total{token_type='completion'}[5m]))",
            ],
            visualization="area_chart",
            position={"x": 0, "y": 5, "w": 6, "h": 4},
            unit="tokens/sec",
            legend="right",
        )

        # Cost trend
        self.add_panel(
            title="Daily Cost Trend",
            panel_type="time_series",
            query="sum(increase(agent_system_cost_usd_total[24h]))",
            visualization="line_chart",
            position={"x": 6, "y": 5, "w": 6, "h": 4},
            unit="USD/day",
        )

        # Top agents by cost
        self.add_panel(
            title="Top 10 Agents by Cost",
            panel_type="table",
            query="topk(10, sum(agent_system_cost_usd_total) by (agent_id))",
            visualization="table",
            position={"x": 0, "y": 9, "w": 12, "h": 4},
            columns=["Agent ID", "Total Cost (USD)", "Trend"],
        )


class ErrorAnalysisDashboard(DashboardDefinition):
    """Dashboard for error tracking and analysis."""

    def __init__(self) -> None:
        """Initialize the error analysis dashboard."""
        super().__init__(
            name="Error Analysis",
            description="Error tracking, analysis, and debugging",
            refresh_interval=30,
        )
        self._build_panels()

    def _build_panels(self) -> None:
        """Build dashboard panels."""
        # Error rate over time
        self.add_panel(
            title="Error Rate",
            panel_type="time_series",
            query="sum(rate(agent_system_errors_total[5m])) by (error_type)",
            visualization="line_chart",
            position={"x": 0, "y": 0, "w": 8, "h": 5},
            unit="errors/sec",
            alert_threshold=1.0,
        )

        # Error distribution
        self.add_panel(
            title="Error Distribution by Type",
            panel_type="pie_chart",
            query="sum(agent_system_errors_total) by (error_type)",
            visualization="pie",
            position={"x": 8, "y": 0, "w": 4, "h": 5},
        )

        # Failed requests by agent
        self.add_panel(
            title="Failed Requests by Agent",
            panel_type="bar_chart",
            query="sum(agent_system_requests_total{status='error'}) by (agent_id)",
            visualization="horizontal_bar",
            position={"x": 0, "y": 5, "w": 6, "h": 4},
            unit="failures",
        )

        # Error spike detection
        self.add_panel(
            title="Error Spike Detection",
            panel_type="time_series",
            query=(
                "increase(agent_system_errors_total[5m]) > "
                "avg_over_time(increase(agent_system_errors_total[5m])[1h:5m]) * 2"
            ),
            visualization="threshold_line",
            position={"x": 6, "y": 5, "w": 6, "h": 4},
            alert_on_anomaly=True,
        )

        # Recent errors table
        self.add_panel(
            title="Recent Errors (Last 1h)",
            panel_type="log_panel",
            query="error_logs{level='error', time_range='1h'}",
            visualization="logs",
            position={"x": 0, "y": 9, "w": 12, "h": 6},
            max_lines=100,
        )


# Pre-defined dashboard configurations
DASHBOARD_CONFIGS: Dict[str, DashboardDefinition] = {
    "overview": AgentOverviewDashboard(),
    "performance": AgentPerformanceDashboard(),
    "llm_metrics": LLMMetricsDashboard(),
    "error_analysis": ErrorAnalysisDashboard(),
}


def get_dashboard(name: str) -> Optional[DashboardDefinition]:
    """
    Get a pre-defined dashboard by name.

    Args:
        name: Dashboard name (overview, performance, llm_metrics, error_analysis)

    Returns:
        DashboardDefinition instance or None if not found

    Example:
        >>> dashboard = get_dashboard("overview")
        >>> json_config = dashboard.to_json()
    """
    return DASHBOARD_CONFIGS.get(name)


def get_all_dashboards() -> Dict[str, DashboardDefinition]:
    """
    Get all pre-defined dashboards.

    Returns:
        Dictionary of dashboard name to DashboardDefinition

    Example:
        >>> dashboards = get_all_dashboards()
        >>> for name, dashboard in dashboards.items():
        ...     print(f"{name}: {dashboard.description}")
    """
    return DASHBOARD_CONFIGS.copy()


def export_dashboard_json(dashboard: DashboardDefinition, file_path: str) -> None:
    """
    Export a dashboard definition to a JSON file.

    Args:
        dashboard: DashboardDefinition instance
        file_path: Path to write JSON file

    Example:
        >>> dashboard = get_dashboard("overview")
        >>> export_dashboard_json(dashboard, "/tmp/overview_dashboard.json")
    """
    with open(file_path, "w") as f:
        f.write(dashboard.to_json())


def create_looker_studio_config() -> Dict[str, Any]:
    """
    Create a Looker Studio compatible configuration.

    Returns:
        Dictionary with Looker Studio dashboard configuration

    Example:
        >>> config = create_looker_studio_config()
        >>> # Import into Looker Studio
    """
    return {
        "version": "1.0",
        "platform": "looker_studio",
        "data_sources": [
            {
                "id": "prometheus",
                "type": "prometheus",
                "connection": {
                    "url": "http://prometheus:9090",
                    "auth_type": "none",
                },
            },
            {
                "id": "logs",
                "type": "bigquery",
                "connection": {
                    "project_id": "agent-project",
                    "dataset": "agent_logs",
                },
            },
        ],
        "dashboards": [
            {
                "name": dashboard.name,
                "description": dashboard.description,
                "config": dashboard.to_dict(),
            }
            for dashboard in DASHBOARD_CONFIGS.values()
        ],
    }


def create_grafana_config() -> Dict[str, Any]:
    """
    Create a Grafana-compatible dashboard configuration.

    Returns:
        Dictionary with Grafana dashboard configuration

    Example:
        >>> config = create_grafana_config()
        >>> # Import into Grafana via API or UI
    """
    grafana_dashboards = []

    for name, dashboard in DASHBOARD_CONFIGS.items():
        grafana_panels = []
        for idx, panel in enumerate(dashboard.panels):
            grafana_panel = {
                "id": idx + 1,
                "title": panel["title"],
                "type": panel["visualization"],
                "targets": [
                    {
                        "expr": panel["query"] if isinstance(panel["query"], str) else panel["query"][0],
                        "legendFormat": panel.get("legend", ""),
                    }
                ],
                "gridPos": {
                    "x": panel["position"]["x"],
                    "y": panel["position"]["y"],
                    "w": panel["position"]["w"],
                    "h": panel["position"]["h"],
                },
            }
            grafana_panels.append(grafana_panel)

        grafana_dashboards.append({
            "dashboard": {
                "title": dashboard.name,
                "description": dashboard.description,
                "tags": ["agent", "observability"],
                "timezone": "utc",
                "refresh": f"{dashboard.refresh_interval}s",
                "panels": grafana_panels,
            }
        })

    return {
        "apiVersion": 1,
        "dashboards": grafana_dashboards,
    }


# Example usage and templates
if __name__ == "__main__":
    # Print all dashboard configurations
    print("Available Dashboards:")
    print("=" * 80)

    for name, dashboard in get_all_dashboards().items():
        print(f"\n{dashboard.name}")
        print(f"  Description: {dashboard.description}")
        print(f"  Panels: {len(dashboard.panels)}")
        print(f"  Refresh: {dashboard.refresh_interval}s")

    # Export overview dashboard
    overview = get_dashboard("overview")
    if overview:
        print("\n" + "=" * 80)
        print("Overview Dashboard JSON:")
        print(overview.to_json())
