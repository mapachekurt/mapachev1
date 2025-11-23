"""Agent-to-Agent (A2A) Communication Protocol.

This module defines the core message types and structures for agent-to-agent
communication in the Mapache multi-agent system.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from uuid import uuid4


class MessageType(Enum):
    """Enumeration of A2A message types."""

    # Basic communication
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"

    # Task coordination
    TASK_ASSIGNMENT = "task_assignment"
    TASK_ACCEPTANCE = "task_acceptance"
    TASK_REJECTION = "task_rejection"
    TASK_PROGRESS = "task_progress"
    TASK_COMPLETION = "task_completion"
    TASK_FAILURE = "task_failure"

    # Resource coordination
    RESOURCE_REQUEST = "resource_request"
    RESOURCE_GRANT = "resource_grant"
    RESOURCE_DENY = "resource_deny"
    RESOURCE_RELEASE = "resource_release"

    # Synchronization
    SYNC_BARRIER = "sync_barrier"
    SYNC_READY = "sync_ready"
    SYNC_PROCEED = "sync_proceed"

    # Control messages
    HEARTBEAT = "heartbeat"
    SHUTDOWN = "shutdown"
    ERROR = "error"


@dataclass
class A2AMessage:
    """Agent-to-Agent message structure.

    Attributes:
        message_id: Unique identifier for this message
        conversation_id: Identifier for the conversation/thread this message belongs to
        from_agent_id: ID of the sending agent
        to_agent_id: ID of the receiving agent (None for broadcast)
        message_type: Type of message being sent
        payload: Message content (arbitrary data)
        timestamp: When the message was created
        priority: Message priority (0-10, higher is more important)
        requires_response: Whether this message expects a response
        correlation_id: ID of the message this responds to (if applicable)
        metadata: Additional metadata for the message
    """

    message_id: str = field(default_factory=lambda: str(uuid4()))
    conversation_id: str = field(default_factory=lambda: str(uuid4()))
    from_agent_id: str = ""
    to_agent_id: Optional[str] = None
    message_type: MessageType = MessageType.NOTIFICATION
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    priority: int = 5
    requires_response: bool = False
    correlation_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary representation.

        Returns:
            Dictionary containing all message fields
        """
        return {
            "message_id": self.message_id,
            "conversation_id": self.conversation_id,
            "from_agent_id": self.from_agent_id,
            "to_agent_id": self.to_agent_id,
            "message_type": self.message_type.value,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat(),
            "priority": self.priority,
            "requires_response": self.requires_response,
            "correlation_id": self.correlation_id,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "A2AMessage":
        """Create message from dictionary representation.

        Args:
            data: Dictionary containing message fields

        Returns:
            A2AMessage instance
        """
        return cls(
            message_id=data.get("message_id", str(uuid4())),
            conversation_id=data.get("conversation_id", str(uuid4())),
            from_agent_id=data.get("from_agent_id", ""),
            to_agent_id=data.get("to_agent_id"),
            message_type=MessageType(data.get("message_type", "notification")),
            payload=data.get("payload", {}),
            timestamp=datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else datetime.utcnow(),
            priority=data.get("priority", 5),
            requires_response=data.get("requires_response", False),
            correlation_id=data.get("correlation_id"),
            metadata=data.get("metadata", {}),
        )

    def create_response(
        self,
        from_agent_id: str,
        payload: Dict[str, Any],
        message_type: MessageType = MessageType.RESPONSE,
    ) -> "A2AMessage":
        """Create a response message to this message.

        Args:
            from_agent_id: ID of the agent sending the response
            payload: Response payload
            message_type: Type of response message

        Returns:
            New A2AMessage instance configured as a response
        """
        return A2AMessage(
            conversation_id=self.conversation_id,
            from_agent_id=from_agent_id,
            to_agent_id=self.from_agent_id,
            message_type=message_type,
            payload=payload,
            correlation_id=self.message_id,
            priority=self.priority,
        )

    def __repr__(self) -> str:
        """String representation of the message."""
        return (
            f"A2AMessage(id={self.message_id[:8]}..., "
            f"type={self.message_type.value}, "
            f"from={self.from_agent_id}, "
            f"to={self.to_agent_id})"
        )
