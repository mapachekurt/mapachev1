"""Memory System - GAP #3 Implementation.

This module provides a comprehensive memory system for multi-agent systems,
including short-term session memory, long-term vector memory, memory
consolidation utilities, and advanced memory patterns.
"""

# Session Memory (Short-term)
from .session_memory import (
    Session,
    SessionEntry,
    SessionMemory,
)

# Vector Memory (Long-term)
from .vector_memory import (
    MemoryVector,
    SearchResult,
    SimpleEmbedding,
    VectorMemory,
)

# Memory Consolidation
from .consolidation import (
    ConsolidationConfig,
    MemoryConsolidator,
    calculate_importance_score,
    find_redundant_memories,
    apply_importance_boost,
    apply_importance_penalty,
    get_oldest_memories,
    get_least_accessed_memories,
    get_low_importance_memories,
    refresh_memory_importance,
)

# Memory Patterns
from .patterns import (
    Experience,
    ExperienceReplayPattern,
    AgentSnapshot,
    DigitalTwinPattern,
)

__all__ = [
    # Session Memory
    "Session",
    "SessionEntry",
    "SessionMemory",
    # Vector Memory
    "MemoryVector",
    "SearchResult",
    "SimpleEmbedding",
    "VectorMemory",
    # Consolidation
    "ConsolidationConfig",
    "MemoryConsolidator",
    "calculate_importance_score",
    "find_redundant_memories",
    "apply_importance_boost",
    "apply_importance_penalty",
    "get_oldest_memories",
    "get_least_accessed_memories",
    "get_low_importance_memories",
    "refresh_memory_importance",
    # Patterns
    "Experience",
    "ExperienceReplayPattern",
    "AgentSnapshot",
    "DigitalTwinPattern",
]
