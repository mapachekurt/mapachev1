"""Session Memory - Short-term memory storage using Redis.

This module provides short-term memory capabilities for agent sessions,
storing conversation history, context, and temporary state using Redis
with fakeredis support for testing without external dependencies.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from uuid import uuid4

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

try:
    import fakeredis
    FAKEREDIS_AVAILABLE = True
except ImportError:
    FAKEREDIS_AVAILABLE = False


@dataclass
class SessionEntry:
    """Entry in a session's conversation history.

    Attributes:
        entry_id: Unique identifier for this entry
        role: Role of the participant (user, agent, system)
        content: Content of the message or action
        timestamp: When this entry was created
        metadata: Additional metadata for the entry
    """

    entry_id: str = field(default_factory=lambda: str(uuid4()))
    role: str = "agent"
    content: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert entry to dictionary representation.

        Returns:
            Dictionary containing all entry fields
        """
        return {
            "entry_id": self.entry_id,
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SessionEntry":
        """Create entry from dictionary representation.

        Args:
            data: Dictionary containing entry fields

        Returns:
            SessionEntry instance
        """
        return cls(
            entry_id=data.get("entry_id", str(uuid4())),
            role=data.get("role", "agent"),
            content=data.get("content", ""),
            timestamp=datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else datetime.utcnow(),
            metadata=data.get("metadata", {}),
        )


@dataclass
class Session:
    """Agent session with conversation history and context.

    Attributes:
        session_id: Unique identifier for this session
        agent_id: ID of the agent owning this session
        created_at: When the session was created
        last_accessed: When the session was last accessed
        history: List of conversation entries
        context: Session context data
        metadata: Additional session metadata
    """

    session_id: str = field(default_factory=lambda: str(uuid4()))
    agent_id: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_accessed: datetime = field(default_factory=datetime.utcnow)
    history: List[SessionEntry] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary representation.

        Returns:
            Dictionary containing all session fields
        """
        return {
            "session_id": self.session_id,
            "agent_id": self.agent_id,
            "created_at": self.created_at.isoformat(),
            "last_accessed": self.last_accessed.isoformat(),
            "history": [entry.to_dict() for entry in self.history],
            "context": self.context,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Session":
        """Create session from dictionary representation.

        Args:
            data: Dictionary containing session fields

        Returns:
            Session instance
        """
        return cls(
            session_id=data.get("session_id", str(uuid4())),
            agent_id=data.get("agent_id", ""),
            created_at=datetime.fromisoformat(data["created_at"]) if "created_at" in data else datetime.utcnow(),
            last_accessed=datetime.fromisoformat(data["last_accessed"]) if "last_accessed" in data else datetime.utcnow(),
            history=[SessionEntry.from_dict(e) for e in data.get("history", [])],
            context=data.get("context", {}),
            metadata=data.get("metadata", {}),
        )


class SessionMemory:
    """
    Short-term memory storage using Redis.

    Manages agent session data including conversation history, context,
    and temporary state. Uses fakeredis for testing without external
    Redis dependencies.
    """

    def __init__(
        self,
        redis_client: Optional[Any] = None,
        use_fakeredis: bool = True,
        ttl_seconds: int = 3600,
        max_history_length: int = 100,
    ):
        """
        Initialize session memory.

        Args:
            redis_client: Optional Redis client (will create fakeredis if None)
            use_fakeredis: Whether to use fakeredis for in-memory storage
            ttl_seconds: Default TTL for sessions in seconds
            max_history_length: Maximum number of history entries to keep
        """
        self.ttl_seconds = ttl_seconds
        self.max_history_length = max_history_length

        if redis_client is not None:
            self.redis = redis_client
        elif use_fakeredis and FAKEREDIS_AVAILABLE:
            self.redis = fakeredis.FakeRedis(decode_responses=True)
        elif REDIS_AVAILABLE:
            # Fallback to real Redis
            self.redis = redis.Redis(decode_responses=True)
        else:
            # In-memory fallback if neither is available
            self.redis = None
            self._memory_store: Dict[str, str] = {}

    def _set(self, key: str, value: str, ex: Optional[int] = None) -> None:
        """Set a key-value pair in storage.

        Args:
            key: Storage key
            value: String value to store
            ex: Optional expiration in seconds
        """
        if self.redis is not None:
            self.redis.set(key, value, ex=ex)
        else:
            self._memory_store[key] = value

    def _get(self, key: str) -> Optional[str]:
        """Get a value from storage.

        Args:
            key: Storage key

        Returns:
            Stored value or None if not found
        """
        if self.redis is not None:
            return self.redis.get(key)
        else:
            return self._memory_store.get(key)

    def _delete(self, key: str) -> None:
        """Delete a key from storage.

        Args:
            key: Storage key to delete
        """
        if self.redis is not None:
            self.redis.delete(key)
        else:
            self._memory_store.pop(key, None)

    def _keys(self, pattern: str) -> List[str]:
        """Get keys matching a pattern.

        Args:
            pattern: Key pattern (e.g., "session:*")

        Returns:
            List of matching keys
        """
        if self.redis is not None:
            keys = self.redis.keys(pattern)
            # Handle both bytes and str returns from different redis versions
            return [k.decode() if isinstance(k, bytes) else k for k in keys]
        else:
            import fnmatch
            return [k for k in self._memory_store.keys() if fnmatch.fnmatch(k, pattern)]

    def store_session(self, session: Session, ttl_override: Optional[int] = None) -> None:
        """
        Store a session in memory.

        Args:
            session: Session to store
            ttl_override: Optional TTL override in seconds
        """
        session.last_accessed = datetime.utcnow()
        key = f"session:{session.session_id}"
        value = json.dumps(session.to_dict())
        ttl = ttl_override if ttl_override is not None else self.ttl_seconds
        self._set(key, value, ex=ttl)

    def get_session(self, session_id: str) -> Optional[Session]:
        """
        Retrieve a session from memory.

        Args:
            session_id: ID of the session to retrieve

        Returns:
            Session instance or None if not found
        """
        key = f"session:{session_id}"
        value = self._get(key)

        if value is None:
            return None

        try:
            data = json.loads(value)
            session = Session.from_dict(data)

            # Update last accessed time
            session.last_accessed = datetime.utcnow()
            self.store_session(session)

            return session
        except (json.JSONDecodeError, KeyError) as e:
            # Invalid session data
            return None

    def delete_session(self, session_id: str) -> None:
        """
        Delete a session from memory.

        Args:
            session_id: ID of the session to delete
        """
        key = f"session:{session_id}"
        self._delete(key)

    def append_to_history(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Append an entry to a session's history.

        Args:
            session_id: ID of the session
            role: Role of the participant (user, agent, system)
            content: Content of the message
            metadata: Optional metadata for the entry

        Returns:
            True if successful, False if session not found
        """
        session = self.get_session(session_id)
        if session is None:
            return False

        entry = SessionEntry(
            role=role,
            content=content,
            metadata=metadata or {},
        )

        session.history.append(entry)

        # Trim history if it exceeds max length
        if len(session.history) > self.max_history_length:
            session.history = session.history[-self.max_history_length:]

        self.store_session(session)
        return True

    def update_context(
        self,
        session_id: str,
        context_updates: Dict[str, Any],
    ) -> bool:
        """
        Update session context.

        Args:
            session_id: ID of the session
            context_updates: Dictionary of context updates to merge

        Returns:
            True if successful, False if session not found
        """
        session = self.get_session(session_id)
        if session is None:
            return False

        session.context.update(context_updates)
        self.store_session(session)
        return True

    def get_sessions_by_agent(self, agent_id: str) -> List[Session]:
        """
        Get all sessions for a specific agent.

        Args:
            agent_id: ID of the agent

        Returns:
            List of sessions belonging to the agent
        """
        sessions = []
        keys = self._keys("session:*")

        for key in keys:
            value = self._get(key)
            if value:
                try:
                    data = json.loads(value)
                    if data.get("agent_id") == agent_id:
                        sessions.append(Session.from_dict(data))
                except (json.JSONDecodeError, KeyError):
                    continue

        return sessions

    def cleanup_expired_sessions(self, max_age_seconds: Optional[int] = None) -> int:
        """
        Clean up expired sessions based on last access time.

        Args:
            max_age_seconds: Maximum age in seconds (defaults to ttl_seconds)

        Returns:
            Number of sessions cleaned up
        """
        max_age = max_age_seconds if max_age_seconds is not None else self.ttl_seconds
        cutoff_time = datetime.utcnow() - timedelta(seconds=max_age)

        cleaned = 0
        keys = self._keys("session:*")

        for key in keys:
            value = self._get(key)
            if value:
                try:
                    data = json.loads(value)
                    last_accessed = datetime.fromisoformat(data["last_accessed"])

                    if last_accessed < cutoff_time:
                        self._delete(key)
                        cleaned += 1
                except (json.JSONDecodeError, KeyError):
                    # Invalid data, clean it up
                    self._delete(key)
                    cleaned += 1

        return cleaned

    def get_session_count(self) -> int:
        """
        Get the total number of active sessions.

        Returns:
            Number of sessions in storage
        """
        keys = self._keys("session:*")
        return len(keys)
