"""Memory Patterns - Experience Replay and Digital Twin patterns.

This module implements advanced memory patterns for agent learning
and simulation, including experience replay for learning from past
experiences and digital twin for maintaining agent state snapshots.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple
from uuid import uuid4
import random

from .session_memory import Session, SessionEntry
from .vector_memory import MemoryVector, VectorMemory


@dataclass
class Experience:
    """An experience record for experience replay.

    Attributes:
        experience_id: Unique identifier for this experience
        agent_id: ID of the agent that had this experience
        state: State before the action
        action: Action taken
        reward: Reward received
        next_state: State after the action
        done: Whether this was a terminal state
        timestamp: When this experience occurred
        metadata: Additional metadata
    """

    experience_id: str = field(default_factory=lambda: str(uuid4()))
    agent_id: str = ""
    state: Dict[str, Any] = field(default_factory=dict)
    action: Dict[str, Any] = field(default_factory=dict)
    reward: float = 0.0
    next_state: Dict[str, Any] = field(default_factory=dict)
    done: bool = False
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert experience to dictionary representation.

        Returns:
            Dictionary containing all experience fields
        """
        return {
            "experience_id": self.experience_id,
            "agent_id": self.agent_id,
            "state": self.state,
            "action": self.action,
            "reward": self.reward,
            "next_state": self.next_state,
            "done": self.done,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Experience":
        """Create experience from dictionary representation.

        Args:
            data: Dictionary containing experience fields

        Returns:
            Experience instance
        """
        return cls(
            experience_id=data.get("experience_id", str(uuid4())),
            agent_id=data.get("agent_id", ""),
            state=data.get("state", {}),
            action=data.get("action", {}),
            reward=data.get("reward", 0.0),
            next_state=data.get("next_state", {}),
            done=data.get("done", False),
            timestamp=datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else datetime.utcnow(),
            metadata=data.get("metadata", {}),
        )


class ExperienceReplayPattern:
    """
    Experience Replay Pattern for agent learning.

    Stores and samples past experiences to enable agents to learn
    from historical interactions. Useful for reinforcement learning
    and improving decision-making over time.
    """

    def __init__(
        self,
        max_experiences: int = 10000,
        batch_size: int = 32,
        priority_alpha: float = 0.6,
    ):
        """
        Initialize experience replay buffer.

        Args:
            max_experiences: Maximum number of experiences to store
            batch_size: Default batch size for sampling
            priority_alpha: Priority exponent for prioritized sampling (0=uniform)
        """
        self.max_experiences = max_experiences
        self.batch_size = batch_size
        self.priority_alpha = priority_alpha
        self.experiences: List[Experience] = []
        self.priorities: List[float] = []

    def add_experience(
        self,
        agent_id: str,
        state: Dict[str, Any],
        action: Dict[str, Any],
        reward: float,
        next_state: Dict[str, Any],
        done: bool = False,
        priority: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Add a new experience to the replay buffer.

        Args:
            agent_id: ID of the agent
            state: State before action
            action: Action taken
            reward: Reward received
            next_state: State after action
            done: Whether episode ended
            priority: Optional priority (defaults to max priority)
            metadata: Optional metadata

        Returns:
            experience_id: ID of the added experience
        """
        experience = Experience(
            agent_id=agent_id,
            state=state,
            action=action,
            reward=reward,
            next_state=next_state,
            done=done,
            metadata=metadata or {},
        )

        # Add to buffer
        if len(self.experiences) >= self.max_experiences:
            # Remove oldest experience
            self.experiences.pop(0)
            self.priorities.pop(0)

        self.experiences.append(experience)

        # Set priority (default to max priority for new experiences)
        if priority is None:
            priority = max(self.priorities) if self.priorities else 1.0

        self.priorities.append(priority)

        return experience.experience_id

    def sample_batch(
        self,
        batch_size: Optional[int] = None,
        agent_id: Optional[str] = None,
        use_priority: bool = True,
    ) -> List[Experience]:
        """
        Sample a batch of experiences for training.

        Args:
            batch_size: Size of batch (uses default if None)
            agent_id: Optional filter by agent ID
            use_priority: Whether to use priority-based sampling

        Returns:
            List of sampled experiences
        """
        batch_size = batch_size or self.batch_size

        # Filter by agent if specified
        if agent_id:
            candidate_indices = [
                i for i, exp in enumerate(self.experiences)
                if exp.agent_id == agent_id
            ]
        else:
            candidate_indices = list(range(len(self.experiences)))

        if not candidate_indices:
            return []

        # Sample based on priority or uniform
        sample_size = min(batch_size, len(candidate_indices))

        if use_priority and self.priority_alpha > 0:
            # Prioritized sampling
            candidate_priorities = [self.priorities[i] for i in candidate_indices]

            # Apply priority exponent
            priorities_alpha = [p ** self.priority_alpha for p in candidate_priorities]
            total_priority = sum(priorities_alpha)

            if total_priority > 0:
                probabilities = [p / total_priority for p in priorities_alpha]
                sampled_indices = random.choices(
                    candidate_indices,
                    weights=probabilities,
                    k=sample_size,
                )
            else:
                sampled_indices = random.sample(candidate_indices, sample_size)
        else:
            # Uniform sampling
            sampled_indices = random.sample(candidate_indices, sample_size)

        return [self.experiences[i] for i in sampled_indices]

    def update_priorities(
        self,
        experience_ids: List[str],
        priorities: List[float],
    ) -> int:
        """
        Update priorities for specific experiences.

        Useful after training to adjust priorities based on TD-error
        or other learning signals.

        Args:
            experience_ids: List of experience IDs
            priorities: Corresponding new priorities

        Returns:
            Number of priorities updated
        """
        updated = 0

        for exp_id, priority in zip(experience_ids, priorities):
            for i, exp in enumerate(self.experiences):
                if exp.experience_id == exp_id:
                    self.priorities[i] = priority
                    updated += 1
                    break

        return updated

    def get_experience(self, experience_id: str) -> Optional[Experience]:
        """
        Get a specific experience by ID.

        Args:
            experience_id: ID of the experience

        Returns:
            Experience or None if not found
        """
        for exp in self.experiences:
            if exp.experience_id == experience_id:
                return exp
        return None

    def get_recent_experiences(
        self,
        count: int,
        agent_id: Optional[str] = None,
    ) -> List[Experience]:
        """
        Get the most recent experiences.

        Args:
            count: Number of experiences to return
            agent_id: Optional filter by agent ID

        Returns:
            List of recent experiences
        """
        if agent_id:
            filtered = [exp for exp in self.experiences if exp.agent_id == agent_id]
        else:
            filtered = self.experiences

        return filtered[-count:]

    def get_high_reward_experiences(
        self,
        count: int,
        agent_id: Optional[str] = None,
    ) -> List[Experience]:
        """
        Get experiences with highest rewards.

        Args:
            count: Number of experiences to return
            agent_id: Optional filter by agent ID

        Returns:
            List of high-reward experiences
        """
        if agent_id:
            filtered = [exp for exp in self.experiences if exp.agent_id == agent_id]
        else:
            filtered = self.experiences

        sorted_experiences = sorted(filtered, key=lambda e: e.reward, reverse=True)
        return sorted_experiences[:count]

    def clear(self, agent_id: Optional[str] = None) -> int:
        """
        Clear experiences from buffer.

        Args:
            agent_id: Optional filter by agent ID (clears all if None)

        Returns:
            Number of experiences cleared
        """
        if agent_id:
            original_count = len(self.experiences)
            self.experiences = [
                exp for exp in self.experiences
                if exp.agent_id != agent_id
            ]
            self.priorities = self.priorities[:len(self.experiences)]
            return original_count - len(self.experiences)
        else:
            count = len(self.experiences)
            self.experiences.clear()
            self.priorities.clear()
            return count

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the replay buffer.

        Returns:
            Dictionary containing buffer statistics
        """
        if not self.experiences:
            return {
                "total_experiences": 0,
                "avg_reward": 0.0,
                "max_reward": 0.0,
                "min_reward": 0.0,
                "unique_agents": 0,
            }

        rewards = [exp.reward for exp in self.experiences]
        unique_agents = set(exp.agent_id for exp in self.experiences)

        return {
            "total_experiences": len(self.experiences),
            "avg_reward": sum(rewards) / len(rewards),
            "max_reward": max(rewards),
            "min_reward": min(rewards),
            "unique_agents": len(unique_agents),
            "capacity_usage": len(self.experiences) / self.max_experiences,
        }


@dataclass
class AgentSnapshot:
    """A snapshot of an agent's state at a point in time.

    Attributes:
        snapshot_id: Unique identifier for this snapshot
        agent_id: ID of the agent
        timestamp: When the snapshot was taken
        state: Agent's state data
        session: Optional session data
        memories: Optional memory data
        performance_metrics: Performance metrics at snapshot time
        metadata: Additional metadata
    """

    snapshot_id: str = field(default_factory=lambda: str(uuid4()))
    agent_id: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    state: Dict[str, Any] = field(default_factory=dict)
    session: Optional[Dict[str, Any]] = None
    memories: List[Dict[str, Any]] = field(default_factory=list)
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert snapshot to dictionary representation.

        Returns:
            Dictionary containing all snapshot fields
        """
        return {
            "snapshot_id": self.snapshot_id,
            "agent_id": self.agent_id,
            "timestamp": self.timestamp.isoformat(),
            "state": self.state,
            "session": self.session,
            "memories": self.memories,
            "performance_metrics": self.performance_metrics,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentSnapshot":
        """Create snapshot from dictionary representation.

        Args:
            data: Dictionary containing snapshot fields

        Returns:
            AgentSnapshot instance
        """
        return cls(
            snapshot_id=data.get("snapshot_id", str(uuid4())),
            agent_id=data.get("agent_id", ""),
            timestamp=datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else datetime.utcnow(),
            state=data.get("state", {}),
            session=data.get("session"),
            memories=data.get("memories", []),
            performance_metrics=data.get("performance_metrics", {}),
            metadata=data.get("metadata", {}),
        )


class DigitalTwinPattern:
    """
    Digital Twin Pattern for agent state management.

    Maintains snapshots of agent state over time, enabling state
    comparison, rollback, and what-if analysis.
    """

    def __init__(self, max_snapshots: int = 100):
        """
        Initialize digital twin manager.

        Args:
            max_snapshots: Maximum number of snapshots to keep per agent
        """
        self.max_snapshots = max_snapshots
        self.snapshots: Dict[str, List[AgentSnapshot]] = {}

    def capture_snapshot(
        self,
        agent_id: str,
        state: Dict[str, Any],
        session: Optional[Session] = None,
        vector_memory: Optional[VectorMemory] = None,
        performance_metrics: Optional[Dict[str, float]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Capture a snapshot of an agent's current state.

        Args:
            agent_id: ID of the agent
            state: Agent's current state
            session: Optional current session
            vector_memory: Optional vector memory instance
            performance_metrics: Optional performance metrics
            metadata: Optional metadata

        Returns:
            snapshot_id: ID of the created snapshot
        """
        # Prepare session data
        session_data = session.to_dict() if session else None

        # Prepare memory data
        memories_data = []
        if vector_memory:
            agent_memories = vector_memory.get_memories_by_agent(agent_id)
            memories_data = [m.to_dict() for m in agent_memories]

        snapshot = AgentSnapshot(
            agent_id=agent_id,
            state=state,
            session=session_data,
            memories=memories_data,
            performance_metrics=performance_metrics or {},
            metadata=metadata or {},
        )

        # Add to snapshots
        if agent_id not in self.snapshots:
            self.snapshots[agent_id] = []

        self.snapshots[agent_id].append(snapshot)

        # Enforce max snapshots limit
        if len(self.snapshots[agent_id]) > self.max_snapshots:
            self.snapshots[agent_id].pop(0)

        return snapshot.snapshot_id

    def get_snapshot(
        self,
        snapshot_id: str,
        agent_id: Optional[str] = None,
    ) -> Optional[AgentSnapshot]:
        """
        Retrieve a specific snapshot.

        Args:
            snapshot_id: ID of the snapshot
            agent_id: Optional agent ID for faster lookup

        Returns:
            AgentSnapshot or None if not found
        """
        if agent_id and agent_id in self.snapshots:
            for snapshot in self.snapshots[agent_id]:
                if snapshot.snapshot_id == snapshot_id:
                    return snapshot
        else:
            for snapshots_list in self.snapshots.values():
                for snapshot in snapshots_list:
                    if snapshot.snapshot_id == snapshot_id:
                        return snapshot

        return None

    def get_latest_snapshot(self, agent_id: str) -> Optional[AgentSnapshot]:
        """
        Get the most recent snapshot for an agent.

        Args:
            agent_id: ID of the agent

        Returns:
            AgentSnapshot or None if no snapshots exist
        """
        if agent_id in self.snapshots and self.snapshots[agent_id]:
            return self.snapshots[agent_id][-1]
        return None

    def get_snapshots_by_agent(
        self,
        agent_id: str,
        limit: Optional[int] = None,
    ) -> List[AgentSnapshot]:
        """
        Get all snapshots for an agent.

        Args:
            agent_id: ID of the agent
            limit: Optional limit on number of snapshots (most recent)

        Returns:
            List of snapshots
        """
        if agent_id not in self.snapshots:
            return []

        snapshots = self.snapshots[agent_id]

        if limit:
            return snapshots[-limit:]

        return snapshots

    def compare_snapshots(
        self,
        snapshot_id1: str,
        snapshot_id2: str,
    ) -> Dict[str, Any]:
        """
        Compare two snapshots to identify differences.

        Args:
            snapshot_id1: ID of first snapshot
            snapshot_id2: ID of second snapshot

        Returns:
            Dictionary containing comparison results
        """
        snapshot1 = self.get_snapshot(snapshot_id1)
        snapshot2 = self.get_snapshot(snapshot_id2)

        if not snapshot1 or not snapshot2:
            return {"error": "One or both snapshots not found"}

        comparison = {
            "time_difference_seconds": (
                snapshot2.timestamp - snapshot1.timestamp
            ).total_seconds(),
            "state_changed": snapshot1.state != snapshot2.state,
            "memory_count_change": len(snapshot2.memories) - len(snapshot1.memories),
            "performance_changes": {},
        }

        # Compare performance metrics
        for metric in set(snapshot1.performance_metrics.keys()) | set(snapshot2.performance_metrics.keys()):
            val1 = snapshot1.performance_metrics.get(metric, 0.0)
            val2 = snapshot2.performance_metrics.get(metric, 0.0)
            comparison["performance_changes"][metric] = {
                "before": val1,
                "after": val2,
                "change": val2 - val1,
            }

        return comparison

    def get_performance_trend(
        self,
        agent_id: str,
        metric: str,
    ) -> List[Tuple[datetime, float]]:
        """
        Get performance trend for a specific metric over time.

        Args:
            agent_id: ID of the agent
            metric: Name of the performance metric

        Returns:
            List of (timestamp, value) tuples
        """
        if agent_id not in self.snapshots:
            return []

        trend = []
        for snapshot in self.snapshots[agent_id]:
            if metric in snapshot.performance_metrics:
                trend.append((
                    snapshot.timestamp,
                    snapshot.performance_metrics[metric],
                ))

        return trend

    def delete_snapshots(
        self,
        agent_id: str,
        before_timestamp: Optional[datetime] = None,
    ) -> int:
        """
        Delete snapshots for an agent.

        Args:
            agent_id: ID of the agent
            before_timestamp: Optional cutoff (deletes snapshots before this time)

        Returns:
            Number of snapshots deleted
        """
        if agent_id not in self.snapshots:
            return 0

        if before_timestamp:
            original_count = len(self.snapshots[agent_id])
            self.snapshots[agent_id] = [
                s for s in self.snapshots[agent_id]
                if s.timestamp >= before_timestamp
            ]
            return original_count - len(self.snapshots[agent_id])
        else:
            count = len(self.snapshots[agent_id])
            del self.snapshots[agent_id]
            return count

    def export_snapshot(self, snapshot_id: str) -> Optional[str]:
        """
        Export a snapshot to JSON string.

        Args:
            snapshot_id: ID of the snapshot

        Returns:
            JSON string or None if not found
        """
        snapshot = self.get_snapshot(snapshot_id)
        if snapshot:
            return json.dumps(snapshot.to_dict(), indent=2)
        return None

    def import_snapshot(self, snapshot_json: str) -> Optional[str]:
        """
        Import a snapshot from JSON string.

        Args:
            snapshot_json: JSON string containing snapshot data

        Returns:
            snapshot_id if successful, None otherwise
        """
        try:
            data = json.loads(snapshot_json)
            snapshot = AgentSnapshot.from_dict(data)

            agent_id = snapshot.agent_id
            if agent_id not in self.snapshots:
                self.snapshots[agent_id] = []

            self.snapshots[agent_id].append(snapshot)

            # Enforce max snapshots limit
            if len(self.snapshots[agent_id]) > self.max_snapshots:
                self.snapshots[agent_id].pop(0)

            return snapshot.snapshot_id

        except (json.JSONDecodeError, KeyError):
            return None

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about stored snapshots.

        Returns:
            Dictionary containing snapshot statistics
        """
        total_snapshots = sum(len(snapshots) for snapshots in self.snapshots.values())
        total_agents = len(self.snapshots)

        return {
            "total_snapshots": total_snapshots,
            "total_agents": total_agents,
            "avg_snapshots_per_agent": total_snapshots / total_agents if total_agents > 0 else 0,
            "agents_with_snapshots": list(self.snapshots.keys()),
        }
