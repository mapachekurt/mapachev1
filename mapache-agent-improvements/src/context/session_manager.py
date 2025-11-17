"""
Session Management: One conversation with clear start and end.

Key Concepts:
- Session = one task (debugging, planning, analysis)
- Sessions end but memories persist
- Clear lifecycle: start → interact → close
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid


@dataclass
class SessionEvent:
    """Single event within a session."""
    event_type: str  # "user_message", "agent_response", "tool_call", "observation"
    timestamp: datetime
    data: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_type": self.event_type,
            "timestamp": self.timestamp.isoformat(),
            "data": self.data,
            "metadata": self.metadata
        }


@dataclass
class SessionState:
    """Accumulated state within a session."""
    conversation_history: List[SessionEvent] = field(default_factory=list)
    active_context: Dict[str, Any] = field(default_factory=dict)
    extracted_intents: List[str] = field(default_factory=list)
    tools_used: List[str] = field(default_factory=list)
    cost_accumulated: float = 0.0

    def add_event(self, event: SessionEvent) -> None:
        """Add event to history."""
        self.conversation_history.append(event)

    def get_recent_context(self, limit: int = 10) -> List[SessionEvent]:
        """Get recent conversation context."""
        return self.conversation_history[-limit:]


class Session:
    """
    One conversation session with clear boundaries.

    Examples:
    - Debugging a specific bug = one session
    - Planning a project = one session
    - Analyzing Q3 revenue = one session

    Power move: Sessions close but memories persist.
    """

    def __init__(
        self,
        user_id: str,
        agent_id: str,
        task_type: str,
        session_id: Optional[str] = None
    ):
        self.session_id = session_id or str(uuid.uuid4())
        self.user_id = user_id
        self.agent_id = agent_id
        self.task_type = task_type
        self.state = SessionState()
        self.started_at = datetime.utcnow()
        self.ended_at: Optional[datetime] = None
        self.status = "active"

    def add_user_message(self, message: str, metadata: Optional[Dict] = None) -> None:
        """Add user message to session."""
        event = SessionEvent(
            event_type="user_message",
            timestamp=datetime.utcnow(),
            data={"message": message},
            metadata=metadata or {}
        )
        self.state.add_event(event)

        # Extract intent
        intent = self._extract_intent(message)
        if intent:
            self.state.extracted_intents.append(intent)

    def add_agent_response(self, response: str, metadata: Optional[Dict] = None) -> None:
        """Add agent response to session."""
        event = SessionEvent(
            event_type="agent_response",
            timestamp=datetime.utcnow(),
            data={"response": response},
            metadata=metadata or {}
        )
        self.state.add_event(event)

    def add_tool_call(self, tool_name: str, result: Any, metadata: Optional[Dict] = None) -> None:
        """Record tool usage."""
        event = SessionEvent(
            event_type="tool_call",
            timestamp=datetime.utcnow(),
            data={"tool": tool_name, "result": result},
            metadata=metadata or {}
        )
        self.state.add_event(event)

        if tool_name not in self.state.tools_used:
            self.state.tools_used.append(tool_name)

    def update_cost(self, cost: float) -> None:
        """Track session cost."""
        self.state.cost_accumulated += cost

    def close(self) -> Dict[str, Any]:
        """Close session and return summary.

        Session ends but learnings will be extracted and persisted
        separately by MemoryExtractor.
        """
        self.ended_at = datetime.utcnow()
        self.status = "closed"

        duration = (self.ended_at - self.started_at).total_seconds()

        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "agent_id": self.agent_id,
            "task_type": self.task_type,
            "duration_seconds": duration,
            "events_count": len(self.state.conversation_history),
            "tools_used": self.state.tools_used,
            "intents": self.state.extracted_intents,
            "cost_usd": self.state.cost_accumulated,
            "started_at": self.started_at.isoformat(),
            "ended_at": self.ended_at.isoformat()
        }

    def _extract_intent(self, message: str) -> Optional[str]:
        """Simple intent extraction (can be enhanced with LLM)."""
        message_lower = message.lower()

        if any(word in message_lower for word in ["analyze", "analysis", "review"]):
            return "analysis"
        elif any(word in message_lower for word in ["debug", "error", "fix", "bug"]):
            return "debugging"
        elif any(word in message_lower for word in ["create", "build", "generate"]):
            return "creation"
        elif any(word in message_lower for word in ["plan", "design", "architect"]):
            return "planning"

        return "general_query"

    def to_dict(self) -> Dict[str, Any]:
        """Serialize session to dict."""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "agent_id": self.agent_id,
            "task_type": self.task_type,
            "status": self.status,
            "started_at": self.started_at.isoformat(),
            "ended_at": self.ended_at.isoformat() if self.ended_at else None,
            "state": {
                "events": [e.to_dict() for e in self.state.conversation_history],
                "intents": self.state.extracted_intents,
                "tools_used": self.state.tools_used,
                "cost": self.state.cost_accumulated
            }
        }


class SessionManager:
    """Manage multiple sessions across agents and users."""

    def __init__(self):
        self.active_sessions: Dict[str, Session] = {}
        self.session_history: List[Dict[str, Any]] = []

    def create_session(
        self,
        user_id: str,
        agent_id: str,
        task_type: str
    ) -> Session:
        """Create and track new session."""
        session = Session(user_id, agent_id, task_type)
        self.active_sessions[session.session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[Session]:
        """Retrieve active session."""
        return self.active_sessions.get(session_id)

    def close_session(self, session_id: str) -> Dict[str, Any]:
        """Close session and move to history."""
        session = self.active_sessions.pop(session_id, None)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        summary = session.close()
        self.session_history.append(summary)
        return summary

    def get_user_sessions(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent sessions for a user."""
        user_sessions = [
            s for s in self.session_history
            if s["user_id"] == user_id
        ]
        return sorted(
            user_sessions,
            key=lambda s: s["ended_at"],
            reverse=True
        )[:limit]
