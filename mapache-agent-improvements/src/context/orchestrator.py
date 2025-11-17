"""
Context Assembly Orchestration: Everything working together.

For each query (in milliseconds):
1. Parse intent
2. Retrieve memories (proactive + reactive)
3. Fetch external knowledge (RAG)
4. Call tools for real-time data
5. Assemble optimal context
6. Generate response with full awareness
7. Extract new memories
"""

import time
from typing import Dict, Any, Optional


class ContextOrchestrator:
    """
    Orchestrate full context assembly pipeline.

    This is where all components work together seamlessly.
    """

    def __init__(
        self,
        memory_system: Any,  # ContextMemorySystem
        memory_extractor: Any,  # MemoryExtractor
        rag_system: Optional[Any] = None,
        tool_system: Optional[Any] = None
    ):
        self.memory_system = memory_system
        self.memory_extractor = memory_extractor
        self.rag_system = rag_system
        self.tool_system = tool_system

    async def process_query(
        self,
        user_id: str,
        agent_id: str,
        query: str,
        session: Any,  # Session
        llm: Any
    ) -> Dict[str, Any]:
        """
        Full context assembly and response generation.

        This is the main entry point that ties everything together.
        """
        start_time = time.time()

        # Step 1: Parse intent
        intent = self._parse_intent(query)

        # Step 2: Retrieve memories (proactive + reactive)
        memories = self.memory_system.get_full_context(query)

        # Step 3: Fetch external knowledge (RAG) - if available
        external_knowledge = []
        if self.rag_system:
            external_knowledge = await self.rag_system.retrieve(query, limit=5)

        # Step 4: Call tools for real-time data - if needed
        tool_outputs = {}
        if self.tool_system and self._needs_tools(intent):
            tool_outputs = await self._call_relevant_tools(intent, query)

        # Step 5: Assemble optimal context
        full_context = {
            "user_id": user_id,
            "agent_id": agent_id,
            "query": query,
            "intent": intent,
            "memories": memories,
            "external_knowledge": external_knowledge,
            "tool_outputs": tool_outputs,
            "session_context": {
                "session_id": session.session_id,
                "task_type": session.task_type,
                "recent_history": [
                    e.to_dict() for e in session.state.get_recent_context(limit=5)
                ]
            }
        }

        # Step 6: Generate response with full awareness
        response = await self._generate_response(llm, full_context)

        # Record in session
        session.add_user_message(query)
        session.add_agent_response(response["text"])

        # Step 7: Extract new memories (async, after response)
        # This happens in background after session closes

        duration_ms = (time.time() - start_time) * 1000

        return {
            "response": response["text"],
            "context_used": full_context,
            "intent": intent,
            "duration_ms": duration_ms,
            "cost_usd": response.get("cost", 0.0)
        }

    def _parse_intent(self, query: str) -> str:
        """Parse user intent (simplified)."""
        query_lower = query.lower()

        if any(word in query_lower for word in ["analyze", "analysis", "review"]):
            return "analysis"
        elif any(word in query_lower for word in ["debug", "error", "fix"]):
            return "debugging"
        elif any(word in query_lower for word in ["create", "build", "generate"]):
            return "creation"
        elif any(word in query_lower for word in ["explain", "what", "how", "why"]):
            return "information"

        return "general"

    def _needs_tools(self, intent: str) -> bool:
        """Determine if tools are needed for this intent."""
        return intent in ["creation", "debugging", "analysis"]

    async def _call_relevant_tools(
        self,
        intent: str,
        query: str
    ) -> Dict[str, Any]:
        """Call appropriate tools based on intent."""
        if not self.tool_system:
            return {}

        # Route to relevant tools
        tools_to_call = []

        if intent == "debugging":
            tools_to_call = ["log_viewer", "error_tracker"]
        elif intent == "analysis":
            tools_to_call = ["data_fetcher", "metrics_calculator"]
        elif intent == "creation":
            tools_to_call = ["code_generator", "file_writer"]

        results = {}
        for tool in tools_to_call:
            try:
                result = await self.tool_system.call(tool, query)
                results[tool] = result
            except Exception as e:
                results[tool] = {"error": str(e)}

        return results

    async def _generate_response(
        self,
        llm: Any,
        full_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate response with full context."""
        prompt = self._build_prompt(full_context)

        # In production, call actual LLM
        # For testing, return mock response
        return {
            "text": f"Response to: {full_context['query']}",
            "cost": 0.0
        }

    def _build_prompt(self, context: Dict[str, Any]) -> str:
        """Build LLM prompt with full context."""
        memories = context["memories"]

        return f"""
You are an AI assistant with full context about this user.

USER CONTEXT (Always remember):
{self._format_memories(memories.get("proactive", {}))}

RELEVANT PATTERNS FOR THIS TASK:
{self._format_memories(memories.get("reactive", {}))}

CURRENT QUERY:
{context["query"]}

INTENT: {context["intent"]}

EXTERNAL KNOWLEDGE:
{context.get("external_knowledge", [])}

REAL-TIME DATA:
{context.get("tool_outputs", {})}

RECENT CONVERSATION:
{self._format_history(context["session_context"]["recent_history"])}

Generate a response that:
1. Leverages all user context (preferences, patterns, history)
2. Addresses the specific query
3. Matches the user's communication style
4. Is personalized based on what you know about them
"""

    def _format_memories(self, memories: Dict[str, Any]) -> str:
        """Format memories for prompt."""
        if not memories:
            return "None"

        lines = []
        for key, value in memories.items():
            lines.append(f"- {key}: {value}")

        return "\n".join(lines) if lines else "None"

    def _format_history(self, history: list) -> str:
        """Format conversation history."""
        if not history:
            return "None"

        lines = []
        for event in history:
            event_type = event["event_type"]
            if event_type == "user_message":
                lines.append(f"User: {event['data'].get('message', '')}")
            elif event_type == "agent_response":
                lines.append(f"Agent: {event['data'].get('response', '')}")

        return "\n".join(lines) if lines else "None"
