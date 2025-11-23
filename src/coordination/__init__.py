"""Agent Coordination Module.

This module provides coordination primitives, communication protocols, and
orchestration patterns for multi-agent systems.
"""

from .a2a_protocol import A2AMessage, MessageType
from .message_broker import MessageBroker
from .orchestration_patterns import (
    HierarchicalPattern,
    OrchestrationPattern,
    OrchestrationResult,
    PeerToPeerPattern,
    PipelinePattern,
)
from .primitives import Barrier, Queue, Semaphore

__all__ = [
    # Protocol
    "A2AMessage",
    "MessageType",
    # Broker
    "MessageBroker",
    # Orchestration
    "OrchestrationPattern",
    "OrchestrationResult",
    "HierarchicalPattern",
    "PipelinePattern",
    "PeerToPeerPattern",
    # Primitives
    "Semaphore",
    "Barrier",
    "Queue",
]
