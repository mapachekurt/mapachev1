"""
Memory Provenance: Trust layer for debugging.

Not just WHAT you remember, but:
- WHERE it came from (source session)
- WHEN it was created/updated
- HOW CERTAIN you are (confidence)
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class MemoryProvenance:
    """
    Metadata for every memory.

    Enables debugging: "Why did agent suggest wrong restaurant?"
    Answer: "Vegan preference stored but confidence=0.3 (mentioned once, might be joke)"
    """

    source_session_id: str
    created_at: datetime
    updated_at: datetime
    confidence: float  # 0.0-1.0
    verification_count: int  # Times confirmed
    contradiction_count: int  # Times contradicted

    def increase_confidence(self) -> None:
        """Memory was confirmed again."""
        self.verification_count += 1
        # Confidence increases but caps at 1.0
        self.confidence = min(1.0, self.confidence + 0.1)
        self.updated_at = datetime.utcnow()

    def decrease_confidence(self) -> None:
        """Memory was contradicted."""
        self.contradiction_count += 1
        # Confidence decreases but floors at 0.0
        self.confidence = max(0.0, self.confidence - 0.2)
        self.updated_at = datetime.utcnow()

    def should_expire(
        self,
        max_age_days: int = 90,
        min_confidence: float = 0.3
    ) -> bool:
        """Check if memory should be removed."""
        age_days = (datetime.utcnow() - self.updated_at).days

        # Expire if both old AND low confidence
        return age_days > max_age_days and self.confidence < min_confidence

    def debug_info(self) -> Dict[str, Any]:
        """Get debugging information."""
        return {
            "source": f"Session {self.source_session_id}",
            "age_days": (datetime.utcnow() - self.created_at).days,
            "last_updated_days": (datetime.utcnow() - self.updated_at).days,
            "confidence": f"{self.confidence:.2f}",
            "verifications": self.verification_count,
            "contradictions": self.contradiction_count,
            "should_expire": self.should_expire()
        }


class ProvenanceMemory:
    """Memory with full provenance tracking."""

    def __init__(
        self,
        memory_id: str,
        memory_type: Any,  # MemoryType enum
        content: Dict[str, Any],
        provenance: MemoryProvenance
    ):
        self.memory_id = memory_id
        self.memory_type = memory_type
        self.content = content
        self.provenance = provenance

    def verify(self) -> None:
        """Confirm this memory is correct."""
        self.provenance.increase_confidence()

    def contradict(self) -> None:
        """Mark this memory as incorrect."""
        self.provenance.decrease_confidence()

    def to_dict(self) -> Dict[str, Any]:
        """Serialize with provenance."""
        return {
            "memory_id": self.memory_id,
            "type": self.memory_type.value if hasattr(self.memory_type, 'value') else str(self.memory_type),
            "content": self.content,
            "provenance": {
                "source_session": self.provenance.source_session_id,
                "created_at": self.provenance.created_at.isoformat(),
                "updated_at": self.provenance.updated_at.isoformat(),
                "confidence": self.provenance.confidence,
                "verifications": self.provenance.verification_count,
                "contradictions": self.provenance.contradiction_count
            }
        }

    def debug_report(self) -> str:
        """Human-readable debug report."""
        debug = self.provenance.debug_info()

        return f"""
Memory: {self.memory_id}
Type: {self.memory_type.value if hasattr(self.memory_type, 'value') else str(self.memory_type)}
Content: {self.content}

Provenance:
- Source: {debug['source']}
- Age: {debug['age_days']} days
- Last Updated: {debug['last_updated_days']} days ago
- Confidence: {debug['confidence']}
- Verified: {debug['verifications']} times
- Contradicted: {debug['contradictions']} times
- Expires: {debug['should_expire']}
"""
