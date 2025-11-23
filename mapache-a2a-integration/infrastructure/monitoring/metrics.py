"""
Metrics Collection

Provides metrics collection for monitoring agent performance.
"""

import time
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from collections import defaultdict
from datetime import datetime
import threading


@dataclass
class MetricValue:
    """A single metric value"""
    value: float
    timestamp: datetime = field(default_factory=datetime.utcnow)
    labels: Dict[str, str] = field(default_factory=dict)


class MetricsCollector:
    """
    Collects and stores metrics for agents and services.

    Thread-safe metrics collection.
    """

    def __init__(self):
        self._counters: Dict[str, int] = defaultdict(int)
        self._gauges: Dict[str, float] = defaultdict(float)
        self._histograms: Dict[str, list] = defaultdict(list)
        self._lock = threading.Lock()

    def increment_counter(self, name: str, value: int = 1, labels: Dict[str, str] = None):
        """
        Increment a counter metric.

        Args:
            name: Metric name
            value: Value to increment by
            labels: Optional labels for the metric
        """
        with self._lock:
            key = self._make_key(name, labels)
            self._counters[key] += value

    def set_gauge(self, name: str, value: float, labels: Dict[str, str] = None):
        """
        Set a gauge metric.

        Args:
            name: Metric name
            value: Gauge value
            labels: Optional labels for the metric
        """
        with self._lock:
            key = self._make_key(name, labels)
            self._gauges[key] = value

    def record_histogram(self, name: str, value: float, labels: Dict[str, str] = None):
        """
        Record a value in a histogram.

        Args:
            name: Metric name
            value: Value to record
            labels: Optional labels for the metric
        """
        with self._lock:
            key = self._make_key(name, labels)
            self._histograms[key].append(value)

            # Keep only last 1000 values to prevent memory issues
            if len(self._histograms[key]) > 1000:
                self._histograms[key] = self._histograms[key][-1000:]

    def get_metrics(self) -> Dict[str, Any]:
        """
        Get all current metrics.

        Returns:
            Dictionary of all metrics
        """
        with self._lock:
            return {
                "counters": dict(self._counters),
                "gauges": dict(self._gauges),
                "histograms": {
                    name: {
                        "count": len(values),
                        "sum": sum(values),
                        "avg": sum(values) / len(values) if values else 0,
                        "min": min(values) if values else 0,
                        "max": max(values) if values else 0,
                    }
                    for name, values in self._histograms.items()
                },
            }

    def reset(self):
        """Reset all metrics"""
        with self._lock:
            self._counters.clear()
            self._gauges.clear()
            self._histograms.clear()

    @staticmethod
    def _make_key(name: str, labels: Optional[Dict[str, str]]) -> str:
        """Create a metric key from name and labels"""
        if not labels:
            return name

        label_str = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
        return f"{name}{{{label_str}}}"


# Global metrics collector
_global_collector = MetricsCollector()


def get_metrics_collector() -> MetricsCollector:
    """Get the global metrics collector"""
    return _global_collector


class Timer:
    """
    Context manager for timing operations.

    Example:
        with Timer("operation_name") as timer:
            # do something
            pass
        print(f"Operation took {timer.duration_ms}ms")
    """

    def __init__(self, name: str, collector: MetricsCollector = None, labels: Dict[str, str] = None):
        self.name = name
        self.collector = collector or get_metrics_collector()
        self.labels = labels or {}
        self.start_time = None
        self.end_time = None
        self.duration_ms = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        self.duration_ms = (self.end_time - self.start_time) * 1000

        # Record in histogram
        self.collector.record_histogram(
            f"{self.name}_duration_ms",
            self.duration_ms,
            self.labels
        )

        # Increment counter
        self.collector.increment_counter(
            f"{self.name}_total",
            labels=self.labels
        )

        # Increment error counter if exception occurred
        if exc_type is not None:
            self.collector.increment_counter(
                f"{self.name}_errors",
                labels={**self.labels, "error_type": exc_type.__name__}
            )


# Agent-specific metrics
def record_agent_message(
    agent_name: str,
    direction: str,
    success: bool = True,
    collector: MetricsCollector = None,
):
    """
    Record an agent message metric.

    Args:
        agent_name: Name of the agent
        direction: "sent" or "received"
        success: Whether the message was successful
        collector: Metrics collector to use
    """
    collector = collector or get_metrics_collector()

    collector.increment_counter(
        "agent_messages_total",
        labels={
            "agent": agent_name,
            "direction": direction,
            "status": "success" if success else "error",
        }
    )


def record_agent_discovery(
    agent_name: str,
    success: bool = True,
    collector: MetricsCollector = None,
):
    """
    Record an agent discovery metric.

    Args:
        agent_name: Name of the discovered agent
        success: Whether discovery was successful
        collector: Metrics collector to use
    """
    collector = collector or get_metrics_collector()

    collector.increment_counter(
        "agent_discoveries_total",
        labels={
            "agent": agent_name,
            "status": "success" if success else "error",
        }
    )


# Example usage
if __name__ == "__main__":
    collector = get_metrics_collector()

    # Counter example
    collector.increment_counter("requests_total", labels={"endpoint": "/agents"})
    collector.increment_counter("requests_total", labels={"endpoint": "/agents"})

    # Gauge example
    collector.set_gauge("active_connections", 42)

    # Histogram example
    collector.record_histogram("request_duration_ms", 125.5)
    collector.record_histogram("request_duration_ms", 200.0)

    # Timer example
    with Timer("database_query", collector):
        time.sleep(0.1)

    # Agent metrics
    record_agent_message("ceo", "sent", True)
    record_agent_discovery("cfo", True)

    # Get all metrics
    metrics = collector.get_metrics()
    print("Metrics:", metrics)
