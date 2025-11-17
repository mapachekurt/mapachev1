"""
Two-Tier Memory System: Declarative + Procedural

Declarative Memory = Facts and preferences (static data)
- "I prefer Python over JavaScript"
- "Working hours 6-11 AM Germany time"
- "Use Stoic philosophy principles"

Procedural Memory = How you work (dynamic behavior patterns)
- "Kurt debugs by checking logs first"
- "Kurt starts projects with comprehensive specs"
- "Kurt values systematic thinking"
"""

from typing import Dict, Any, List, Optional
from enum import Enum
from datetime import datetime
import uuid


class MemoryType(Enum):
    """Type of memory."""
    DECLARATIVE = "declarative"
    PROCEDURAL = "procedural"


class DeclarativeMemory:
    """
    Static facts and preferences about the user.

    This is what the agent KNOWS about you.
    """

    def __init__(self):
        self.facts: Dict[str, Dict[str, Any]] = {}

    def store_fact(
        self,
        key: str,
        value: Any,
        confidence: float = 1.0,
        source_session: Optional[str] = None
    ) -> None:
        """Store a declarative fact."""
        self.facts[key] = {
            "value": value,
            "confidence": confidence,
            "source_session": source_session,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "verification_count": 1
        }

    def update_fact(
        self,
        key: str,
        new_value: Any,
        confidence: float,
        source_session: Optional[str] = None
    ) -> None:
        """Update existing fact or create if doesn't exist."""
        if key in self.facts:
            existing = self.facts[key]

            # Higher confidence wins
            if confidence > existing["confidence"]:
                existing["value"] = new_value
                existing["confidence"] = confidence
                existing["updated_at"] = datetime.utcnow().isoformat()

            # Increment verification count
            existing["verification_count"] += 1
        else:
            self.store_fact(key, new_value, confidence, source_session)

    def get_fact(self, key: str) -> Optional[Any]:
        """Retrieve a specific fact."""
        fact = self.facts.get(key)
        return fact["value"] if fact else None

    def get_all_facts(self, min_confidence: float = 0.5) -> Dict[str, Any]:
        """Get all facts above confidence threshold."""
        return {
            k: v["value"]
            for k, v in self.facts.items()
            if v["confidence"] >= min_confidence
        }

    def search_facts(self, query: str) -> List[Dict[str, Any]]:
        """Simple text search through facts."""
        query_lower = query.lower()
        results = []

        for key, fact in self.facts.items():
            if query_lower in key.lower() or query_lower in str(fact["value"]).lower():
                results.append({
                    "key": key,
                    **fact
                })

        return results


class ProceduralMemory:
    """
    Behavioral patterns and working style.

    This is HOW the user works, decides, communicates.
    """

    def __init__(self):
        self.patterns: List[Dict[str, Any]] = []

    def store_pattern(
        self,
        pattern_type: str,
        description: str,
        examples: List[str],
        confidence: float = 1.0,
        source_sessions: Optional[List[str]] = None
    ) -> str:
        """Store a procedural pattern."""
        pattern_id = str(uuid.uuid4())

        pattern = {
            "id": pattern_id,
            "type": pattern_type,
            "description": description,
            "examples": examples,
            "confidence": confidence,
            "source_sessions": source_sessions or [],
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "usage_count": 0
        }

        self.patterns.append(pattern)
        return pattern_id

    def update_pattern(
        self,
        pattern_id: str,
        new_examples: Optional[List[str]] = None,
        confidence_delta: float = 0.0
    ) -> None:
        """Update existing pattern."""
        for pattern in self.patterns:
            if pattern["id"] == pattern_id:
                if new_examples:
                    pattern["examples"].extend(new_examples)

                pattern["confidence"] = max(0.0, min(1.0, pattern["confidence"] + confidence_delta))
                pattern["updated_at"] = datetime.utcnow().isoformat()
                pattern["usage_count"] += 1
                break

    def get_patterns(
        self,
        pattern_type: Optional[str] = None,
        min_confidence: float = 0.5
    ) -> List[Dict[str, Any]]:
        """Retrieve patterns, optionally filtered."""
        patterns = self.patterns

        # Filter by type
        if pattern_type:
            patterns = [p for p in patterns if p["type"] == pattern_type]

        # Filter by confidence
        patterns = [p for p in patterns if p["confidence"] >= min_confidence]

        # Sort by confidence and usage
        patterns = sorted(
            patterns,
            key=lambda p: (p["confidence"], p["usage_count"]),
            reverse=True
        )

        return patterns

    def search_relevant_patterns(
        self,
        current_task: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Find patterns relevant to current task."""
        task_lower = current_task.lower()
        scored_patterns = []

        for pattern in self.patterns:
            # Simple relevance scoring
            score = 0.0

            # Check if pattern type matches task
            if pattern["type"] in task_lower:
                score += 0.5

            # Check if description is relevant
            if any(word in pattern["description"].lower() for word in task_lower.split()):
                score += 0.3

            # Weight by confidence
            score *= pattern["confidence"]

            if score > 0:
                scored_patterns.append({
                    "pattern": pattern,
                    "relevance_score": score
                })

        # Sort by relevance
        scored_patterns.sort(key=lambda x: x["relevance_score"], reverse=True)

        return [sp["pattern"] for sp in scored_patterns[:limit]]


class ContextMemorySystem:
    """
    Combined memory system for context engineering.

    Integrates declarative and procedural memory for full user understanding.
    """

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.declarative = DeclarativeMemory()
        self.procedural = ProceduralMemory()

    def get_proactive_context(self) -> Dict[str, Any]:
        """
        Get MUST-HAVE context for every request.

        Proactive = Always included (Push):
        - User's core preferences
        - Active project context
        - Safety information
        - Essential facts
        """
        return {
            "user_id": self.user_id,
            "declarative_facts": self.declarative.get_all_facts(min_confidence=0.7),
            "key_patterns": self.procedural.get_patterns(min_confidence=0.8)
        }

    def get_reactive_context(
        self,
        current_task: str,
        limit: int = 5
    ) -> Dict[str, Any]:
        """
        Get ON-DEMAND context via semantic search.

        Reactive = Retrieved when relevant (Pull):
        - Historical patterns (only when task-relevant)
        - Past project details (only when referenced)
        - Specific procedural knowledge (only when needed)
        """
        return {
            "relevant_patterns": self.procedural.search_relevant_patterns(current_task, limit),
            "task_specific_facts": self.declarative.search_facts(current_task)
        }

    def get_full_context(
        self,
        current_task: str,
        max_tokens: int = 4000
    ) -> Dict[str, Any]:
        """Assemble complete context for a query."""
        proactive = self.get_proactive_context()
        reactive = self.get_reactive_context(current_task)

        # Estimate tokens (rough: 1 token ≈ 4 chars)
        context = {"proactive": proactive, "reactive": reactive}
        tokens_used = len(str(context)) // 4

        # If over budget, trim reactive context
        if tokens_used > max_tokens:
            # Keep proactive, trim reactive
            trim_amount = len(reactive["relevant_patterns"]) // 2
            context["reactive"]["relevant_patterns"] = reactive["relevant_patterns"][:trim_amount]

        return context
