"""
LLM-Driven Memory Extraction: AI generates its own memories.

This is Google's breakthrough: Automated intelligence extraction.

Process:
1. Extract - LLM identifies information worth remembering
2. Consolidate - Merge new memories with existing
3. Load - Store in memory system
"""

from typing import Dict, Any, List, Optional
import json


class MemoryExtractor:
    """
    Extract memories from sessions using LLM.

    The LLM drives memory creation itself - no manual rules.
    """

    async def extract_from_session(
        self,
        session: Any,  # Session type
        llm: Any
    ) -> Dict[str, Any]:
        """
        Step 1: Extract signal from noise.

        LLM analyzes conversation and identifies:
        - Declarative facts worth remembering
        - Procedural patterns observed
        """
        conversation = self._format_conversation(session)

        prompt = f"""
Analyze this conversation session and extract memories worth persisting.

Session Details:
- Task Type: {session.task_type}
- Duration: {(session.ended_at - session.started_at).total_seconds() if session.ended_at else 0} seconds
- Events: {len(session.state.conversation_history)}

Conversation:
{conversation}

Extract two types of memories:

1. DECLARATIVE MEMORIES (facts, preferences, context):
   - What facts did you learn about the user?
   - What preferences were expressed?
   - What context is important?

2. PROCEDURAL MEMORIES (patterns, behaviors, style):
   - How does the user work?
   - What patterns did you observe?
   - What is their communication/decision style?

Output JSON:
{{
    "declarative": [
        {{"key": "preference_name", "value": "preference_value", "confidence": 0.0-1.0, "reason": "why confident"}}
    ],
    "procedural": [
        {{"type": "pattern_type", "description": "pattern description", "examples": ["example1"], "confidence": 0.0-1.0}}
    ]
}}

Be selective. Only extract memories that are:
- Clearly stated or strongly implied
- Likely to be relevant in future interactions
- Not contradictory or ambiguous
"""

        # Call LLM to extract memories
        response = await self._call_llm(llm, prompt)

        try:
            memories = json.loads(response)
        except json.JSONDecodeError:
            # Fallback: extract from markdown code block
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0]
                memories = json.loads(json_str)
            else:
                memories = {"declarative": [], "procedural": []}

        return memories

    async def consolidate_memories(
        self,
        new_memories: Dict[str, Any],
        memory_system: Any,  # ContextMemorySystem type
        session_id: str
    ) -> Dict[str, Any]:
        """
        Step 2: Consolidate - merge new with existing.

        Examples of consolidation:
        - Previous: "User at mid-size company"
        - New: "200+ developers"
        - Updated: "User at large company (200+ devs)"

        - Previous: "User debugs reactively"
        - New: "User checks logs before code"
        - Updated: Pattern strengthened with new example
        """
        stats = {
            "declarative_added": 0,
            "declarative_updated": 0,
            "procedural_added": 0,
            "procedural_updated": 0
        }

        # Process declarative memories
        for memory in new_memories.get("declarative", []):
            key = memory["key"]
            value = memory["value"]
            confidence = memory["confidence"]

            existing = memory_system.declarative.get_fact(key)

            if existing:
                # Update existing fact
                memory_system.declarative.update_fact(
                    key, value, confidence, session_id
                )
                stats["declarative_updated"] += 1
            else:
                # Store new fact
                memory_system.declarative.store_fact(
                    key, value, confidence, session_id
                )
                stats["declarative_added"] += 1

        # Process procedural memories
        for memory in new_memories.get("procedural", []):
            pattern_type = memory["type"]
            description = memory["description"]
            examples = memory.get("examples", [])
            confidence = memory["confidence"]

            # Check for similar existing patterns
            existing_patterns = memory_system.procedural.get_patterns(pattern_type)
            similar = self._find_similar_pattern(description, existing_patterns)

            if similar:
                # Update existing pattern
                memory_system.procedural.update_pattern(
                    similar["id"],
                    new_examples=examples,
                    confidence_delta=0.1  # Reinforce with new evidence
                )
                stats["procedural_updated"] += 1
            else:
                # Store new pattern
                memory_system.procedural.store_pattern(
                    pattern_type, description, examples, confidence, [session_id]
                )
                stats["procedural_added"] += 1

        return stats

    def _format_conversation(self, session: Any) -> str:
        """Format conversation history for LLM."""
        lines = []
        for event in session.state.conversation_history:
            if event.event_type == "user_message":
                lines.append(f"User: {event.data.get('message', '')}")
            elif event.event_type == "agent_response":
                lines.append(f"Agent: {event.data.get('response', '')}")
            elif event.event_type == "tool_call":
                lines.append(f"Tool: {event.data.get('tool', '')} → {event.data.get('result', '')}")

        return "\n".join(lines)

    async def _call_llm(self, llm: Any, prompt: str) -> str:
        """Call LLM (mock mode supported)."""
        # In production, this would call actual LLM
        # For now, return mock response for testing
        return json.dumps({
            "declarative": [],
            "procedural": []
        })

    def _find_similar_pattern(
        self,
        description: str,
        existing_patterns: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """Find similar existing pattern."""
        desc_lower = description.lower()

        for pattern in existing_patterns:
            # Simple similarity: check for keyword overlap
            pattern_desc = pattern["description"].lower()
            common_words = set(desc_lower.split()) & set(pattern_desc.split())

            if len(common_words) >= 3:  # At least 3 words in common
                return pattern

        return None
