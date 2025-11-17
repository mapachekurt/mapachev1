"""Memory Consolidation - Pruning, merging, and decay functions.

This module provides utilities for managing memory lifecycle, including
importance-based pruning, similar memory merging, and time-based decay
to optimize memory usage and maintain relevant information.
"""

import math
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Callable, Dict, List, Optional, Set, Tuple

from .vector_memory import MemoryVector, VectorMemory


@dataclass
class ConsolidationConfig:
    """Configuration for memory consolidation.

    Attributes:
        max_memories: Maximum number of memories to keep
        min_importance: Minimum importance threshold (0.0 to 1.0)
        decay_rate: Daily importance decay rate (0.0 to 1.0)
        merge_similarity_threshold: Similarity threshold for merging (0.0 to 1.0)
        access_boost: Importance boost per access
        time_decay_enabled: Whether to apply time-based decay
        merge_enabled: Whether to merge similar memories
    """

    max_memories: int = 10000
    min_importance: float = 0.1
    decay_rate: float = 0.01
    merge_similarity_threshold: float = 0.95
    access_boost: float = 0.05
    time_decay_enabled: bool = True
    merge_enabled: bool = True


class MemoryConsolidator:
    """
    Memory consolidation manager.

    Handles pruning, merging, and decay of memories to optimize
    storage and maintain relevant information.
    """

    def __init__(self, config: Optional[ConsolidationConfig] = None):
        """
        Initialize memory consolidator.

        Args:
            config: Optional consolidation configuration
        """
        self.config = config or ConsolidationConfig()

    def consolidate(
        self,
        vector_memory: VectorMemory,
        agent_id: Optional[str] = None,
    ) -> Dict[str, int]:
        """
        Run full consolidation process on memories.

        Args:
            vector_memory: VectorMemory instance to consolidate
            agent_id: Optional agent ID to filter consolidation

        Returns:
            Dictionary with consolidation statistics
        """
        stats = {
            "initial_count": vector_memory.get_memory_count(),
            "decayed": 0,
            "merged": 0,
            "pruned": 0,
        }

        # Apply time-based decay
        if self.config.time_decay_enabled:
            stats["decayed"] = self.apply_decay(vector_memory, agent_id)

        # Merge similar memories
        if self.config.merge_enabled:
            stats["merged"] = self.merge_similar_memories(vector_memory, agent_id)

        # Prune low-importance memories
        stats["pruned"] = self.prune_memories(vector_memory, agent_id)

        stats["final_count"] = vector_memory.get_memory_count()
        stats["total_removed"] = stats["merged"] + stats["pruned"]

        return stats

    def apply_decay(
        self,
        vector_memory: VectorMemory,
        agent_id: Optional[str] = None,
    ) -> int:
        """
        Apply time-based importance decay to memories.

        Older memories have their importance reduced based on age
        and access patterns.

        Args:
            vector_memory: VectorMemory instance
            agent_id: Optional agent ID to filter

        Returns:
            Number of memories that were decayed
        """
        now = datetime.utcnow()
        decayed_count = 0

        memories = (
            vector_memory.get_memories_by_agent(agent_id)
            if agent_id
            else list(vector_memory.memories.values())
        )

        for memory in memories:
            # Calculate age in days
            age_days = (now - memory.timestamp).total_seconds() / 86400.0

            # Calculate decay based on age
            decay_factor = math.exp(-self.config.decay_rate * age_days)

            # Boost importance based on access frequency
            access_boost = min(
                memory.access_count * self.config.access_boost,
                0.5,  # Cap at 0.5
            )

            # Calculate new importance
            new_importance = (memory.importance * decay_factor) + access_boost

            # Clamp to valid range
            new_importance = max(0.0, min(1.0, new_importance))

            if new_importance != memory.importance:
                memory.importance = new_importance
                decayed_count += 1

        return decayed_count

    def prune_memories(
        self,
        vector_memory: VectorMemory,
        agent_id: Optional[str] = None,
    ) -> int:
        """
        Remove low-importance memories and enforce max memory limit.

        Args:
            vector_memory: VectorMemory instance
            agent_id: Optional agent ID to filter

        Returns:
            Number of memories pruned
        """
        memories = (
            vector_memory.get_memories_by_agent(agent_id)
            if agent_id
            else list(vector_memory.memories.values())
        )

        pruned_count = 0

        # Prune memories below minimum importance
        for memory in memories:
            if memory.importance < self.config.min_importance:
                vector_memory.delete(memory.memory_id)
                pruned_count += 1

        # Enforce max memory limit
        if agent_id:
            remaining_memories = vector_memory.get_memories_by_agent(agent_id)
        else:
            remaining_memories = list(vector_memory.memories.values())

        if len(remaining_memories) > self.config.max_memories:
            # Sort by importance (ascending) and remove lowest
            remaining_memories.sort(key=lambda m: m.importance)
            to_remove = len(remaining_memories) - self.config.max_memories

            for i in range(to_remove):
                vector_memory.delete(remaining_memories[i].memory_id)
                pruned_count += 1

        return pruned_count

    def merge_similar_memories(
        self,
        vector_memory: VectorMemory,
        agent_id: Optional[str] = None,
    ) -> int:
        """
        Merge highly similar memories to reduce redundancy.

        Args:
            vector_memory: VectorMemory instance
            agent_id: Optional agent ID to filter

        Returns:
            Number of memories merged (removed)
        """
        memories = (
            vector_memory.get_memories_by_agent(agent_id)
            if agent_id
            else list(vector_memory.memories.values())
        )

        if len(memories) < 2:
            return 0

        merged_count = 0
        processed_ids: Set[str] = set()

        # Sort by timestamp (oldest first) to prefer keeping older memories
        memories.sort(key=lambda m: m.timestamp)

        for i, memory1 in enumerate(memories):
            if memory1.memory_id in processed_ids:
                continue

            for memory2 in memories[i + 1:]:
                if memory2.memory_id in processed_ids:
                    continue

                # Calculate similarity
                similarity = vector_memory._cosine_similarity(
                    memory1.embedding,
                    memory2.embedding,
                )

                # Merge if above threshold
                if similarity >= self.config.merge_similarity_threshold:
                    self._merge_memories(memory1, memory2)
                    vector_memory.delete(memory2.memory_id)
                    processed_ids.add(memory2.memory_id)
                    merged_count += 1

        return merged_count

    def _merge_memories(self, target: MemoryVector, source: MemoryVector) -> None:
        """
        Merge source memory into target memory.

        Args:
            target: Memory to merge into (kept)
            source: Memory to merge from (will be deleted)
        """
        # Update importance (take maximum)
        target.importance = max(target.importance, source.importance)

        # Combine access counts
        target.access_count += source.access_count

        # Update last accessed to most recent
        target.last_accessed = max(target.last_accessed, source.last_accessed)

        # Merge tags
        target.tags = list(set(target.tags + source.tags))

        # Merge metadata
        target.metadata.update(source.metadata)

        # Add merge info to metadata
        if "merged_from" not in target.metadata:
            target.metadata["merged_from"] = []
        target.metadata["merged_from"].append(source.memory_id)


def calculate_importance_score(
    memory: MemoryVector,
    recency_weight: float = 0.3,
    frequency_weight: float = 0.3,
    base_importance_weight: float = 0.4,
) -> float:
    """
    Calculate composite importance score for a memory.

    Combines recency, access frequency, and base importance into
    a single score.

    Args:
        memory: Memory to score
        recency_weight: Weight for recency component (0.0 to 1.0)
        frequency_weight: Weight for frequency component (0.0 to 1.0)
        base_importance_weight: Weight for base importance (0.0 to 1.0)

    Returns:
        Composite importance score (0.0 to 1.0)
    """
    # Normalize weights
    total_weight = recency_weight + frequency_weight + base_importance_weight
    recency_weight /= total_weight
    frequency_weight /= total_weight
    base_importance_weight /= total_weight

    # Calculate recency score (exponential decay)
    now = datetime.utcnow()
    age_hours = (now - memory.last_accessed).total_seconds() / 3600.0
    recency_score = math.exp(-age_hours / 168.0)  # Half-life of 1 week

    # Calculate frequency score (logarithmic)
    frequency_score = math.log(memory.access_count + 1) / math.log(100)
    frequency_score = min(1.0, frequency_score)

    # Combine scores
    composite_score = (
        recency_weight * recency_score +
        frequency_weight * frequency_score +
        base_importance_weight * memory.importance
    )

    return min(1.0, max(0.0, composite_score))


def find_redundant_memories(
    vector_memory: VectorMemory,
    agent_id: Optional[str] = None,
    similarity_threshold: float = 0.9,
) -> List[Tuple[str, str, float]]:
    """
    Find pairs of highly similar (redundant) memories.

    Args:
        vector_memory: VectorMemory instance
        agent_id: Optional agent ID to filter
        similarity_threshold: Minimum similarity to be considered redundant

    Returns:
        List of tuples (memory_id1, memory_id2, similarity)
    """
    memories = (
        vector_memory.get_memories_by_agent(agent_id)
        if agent_id
        else list(vector_memory.memories.values())
    )

    redundant_pairs = []

    for i, memory1 in enumerate(memories):
        for memory2 in memories[i + 1:]:
            similarity = vector_memory._cosine_similarity(
                memory1.embedding,
                memory2.embedding,
            )

            if similarity >= similarity_threshold:
                redundant_pairs.append((
                    memory1.memory_id,
                    memory2.memory_id,
                    similarity,
                ))

    return redundant_pairs


def apply_importance_boost(
    memory: MemoryVector,
    boost_amount: float = 0.1,
    max_importance: float = 1.0,
) -> float:
    """
    Boost the importance of a memory (e.g., after access or validation).

    Args:
        memory: Memory to boost
        boost_amount: Amount to boost importance by
        max_importance: Maximum importance value

    Returns:
        New importance value
    """
    new_importance = min(max_importance, memory.importance + boost_amount)
    memory.importance = new_importance
    return new_importance


def apply_importance_penalty(
    memory: MemoryVector,
    penalty_amount: float = 0.1,
    min_importance: float = 0.0,
) -> float:
    """
    Reduce the importance of a memory (e.g., after errors or contradictions).

    Args:
        memory: Memory to penalize
        penalty_amount: Amount to reduce importance by
        min_importance: Minimum importance value

    Returns:
        New importance value
    """
    new_importance = max(min_importance, memory.importance - penalty_amount)
    memory.importance = new_importance
    return new_importance


def get_oldest_memories(
    vector_memory: VectorMemory,
    agent_id: Optional[str] = None,
    count: int = 10,
) -> List[MemoryVector]:
    """
    Get the oldest memories.

    Args:
        vector_memory: VectorMemory instance
        agent_id: Optional agent ID to filter
        count: Number of memories to return

    Returns:
        List of oldest memories
    """
    memories = (
        vector_memory.get_memories_by_agent(agent_id)
        if agent_id
        else list(vector_memory.memories.values())
    )

    memories.sort(key=lambda m: m.timestamp)
    return memories[:count]


def get_least_accessed_memories(
    vector_memory: VectorMemory,
    agent_id: Optional[str] = None,
    count: int = 10,
) -> List[MemoryVector]:
    """
    Get the least accessed memories.

    Args:
        vector_memory: VectorMemory instance
        agent_id: Optional agent ID to filter
        count: Number of memories to return

    Returns:
        List of least accessed memories
    """
    memories = (
        vector_memory.get_memories_by_agent(agent_id)
        if agent_id
        else list(vector_memory.memories.values())
    )

    memories.sort(key=lambda m: m.access_count)
    return memories[:count]


def get_low_importance_memories(
    vector_memory: VectorMemory,
    agent_id: Optional[str] = None,
    threshold: float = 0.3,
) -> List[MemoryVector]:
    """
    Get memories below an importance threshold.

    Args:
        vector_memory: VectorMemory instance
        agent_id: Optional agent ID to filter
        threshold: Importance threshold

    Returns:
        List of low importance memories
    """
    memories = (
        vector_memory.get_memories_by_agent(agent_id)
        if agent_id
        else list(vector_memory.memories.values())
    )

    return [m for m in memories if m.importance < threshold]


def refresh_memory_importance(
    vector_memory: VectorMemory,
    agent_id: Optional[str] = None,
    recency_weight: float = 0.3,
    frequency_weight: float = 0.3,
    base_importance_weight: float = 0.4,
) -> int:
    """
    Recalculate importance scores for all memories.

    Args:
        vector_memory: VectorMemory instance
        agent_id: Optional agent ID to filter
        recency_weight: Weight for recency component
        frequency_weight: Weight for frequency component
        base_importance_weight: Weight for base importance

    Returns:
        Number of memories updated
    """
    memories = (
        vector_memory.get_memories_by_agent(agent_id)
        if agent_id
        else list(vector_memory.memories.values())
    )

    updated_count = 0

    for memory in memories:
        old_importance = memory.importance
        new_importance = calculate_importance_score(
            memory,
            recency_weight,
            frequency_weight,
            base_importance_weight,
        )

        if old_importance != new_importance:
            memory.importance = new_importance
            updated_count += 1

    return updated_count
