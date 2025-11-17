"""
Context Engineering for Intelligent Agents

Based on Google's 70-page Context Engineering whitepaper.

This package provides:
- Session management (one conversation, clear boundaries)
- Two-tier memory system (declarative + procedural)
- LLM-driven memory extraction
- Provenance tracking
- Intelligent context assembly
"""

from .session_manager import Session, SessionEvent, SessionState, SessionManager
from .memory_types import (
    MemoryType,
    DeclarativeMemory,
    ProceduralMemory,
    ContextMemorySystem,
)
from .memory_extraction import MemoryExtractor
from .provenance import MemoryProvenance, ProvenanceMemory
from .orchestrator import ContextOrchestrator

__version__ = "1.0.0"

__all__ = [
    # Session Management
    "Session",
    "SessionEvent",
    "SessionState",
    "SessionManager",
    # Memory Types
    "MemoryType",
    "DeclarativeMemory",
    "ProceduralMemory",
    "ContextMemorySystem",
    # Memory Extraction
    "MemoryExtractor",
    # Provenance
    "MemoryProvenance",
    "ProvenanceMemory",
    # Orchestration
    "ContextOrchestrator",
]
