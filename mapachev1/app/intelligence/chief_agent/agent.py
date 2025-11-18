"""Chief Agent for opportunity synthesis and project creation."""

import logging
from datetime import datetime
from typing import Any

import vertexai
from google.cloud import firestore
from vertexai.generative_models import (
    FunctionDeclaration,
    GenerativeModel,
    Tool,
    GenerationConfig,
)

from ..utils.config import config
from .tools import linear_tool, slack_tool

logger = logging.getLogger(__name__)


class ChiefAgent:
    """Chief Agent for daily intelligence briefing."""

    SYNTHESIS_PROMPT = """You are the Chief Intelligence Officer for Mapache, an AI company building agents and automation solutions.

Your task: Analyze recent discoveries and identify the top 5 strategic opportunities for Mapache.

For each opportunity:
1. Synthesize insights from multiple related discoveries
2. Identify strategic value and business impact
3. Create a complete Linear project specification with:
   - Clear, actionable title
   - Comprehensive description
   - Technical requirements
   - Acceptance criteria
   - Rollback plan
   - Priority level (low/medium/high/urgent)

Then create a daily briefing summary for the team.

You have access to these tools:
- create_linear_project: Create a Linear project for an opportunity
- send_slack_briefing: Send the daily briefing to Slack

Process:
1. Review all discoveries with relevance_score >= 70
2. Group related discoveries by topic/theme
3. Identify top 5 strategic opportunities
4. Create Linear project for each opportunity (use create_linear_project)
5. Send comprehensive briefing to Slack (use send_slack_briefing)

Recent discoveries are provided below.
"""

    def __init__(self) -> None:
        """Initialize the Chief Agent."""
        # Initialize Vertex AI
        vertexai.init(
            project=config.gcp.project_id,
            location=config.gcp.location,
        )

        # Initialize Firestore
        self.db = firestore.Client(project=config.gcp.project_id)

        # Define tools
        create_project_func = FunctionDeclaration(
            name="create_linear_project",
            description="Create a Linear project for a strategic opportunity",
            parameters={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Project title (clear and actionable)",
                    },
                    "description": {
                        "type": "string",
                        "description": "Comprehensive project description",
                    },
                    "technical_requirements": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of technical requirements",
                    },
                    "acceptance_criteria": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of acceptance criteria",
                    },
                    "rollback_plan": {
                        "type": "string",
                        "description": "Plan for rolling back changes if needed",
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high", "urgent"],
                        "description": "Priority level",
                    },
                },
                "required": [
                    "title",
                    "description",
                    "technical_requirements",
                    "acceptance_criteria",
                    "rollback_plan",
                ],
            },
        )

        send_briefing_func = FunctionDeclaration(
            name="send_slack_briefing",
            description="Send daily intelligence briefing to Slack",
            parameters={
                "type": "object",
                "properties": {
                    "summary": {
                        "type": "string",
                        "description": "Brief summary of today's intelligence (2-3 sentences)",
                    },
                    "top_opportunities": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string"},
                                "description": {"type": "string"},
                                "relevance_score": {"type": "number"},
                            },
                        },
                        "description": "Top 5 opportunities identified",
                    },
                },
                "required": ["summary", "top_opportunities"],
            },
        )

        # Create tools
        tools = Tool(
            function_declarations=[create_project_func, send_briefing_func],
        )

        # Initialize Gemini model with tools
        self.model = GenerativeModel(
            config.gemini.model,
            tools=[tools],
        )

    def fetch_recent_discoveries(self, min_relevance: int = 70) -> list[dict[str, Any]]:
        """Fetch recent discoveries from Firestore.

        Args:
            min_relevance: Minimum relevance score

        Returns:
            List of discovery documents
        """
        try:
            # Query Firestore for recent discoveries with high relevance
            discoveries_ref = self.db.collection(config.firestore.discoveries_collection)

            # Get discoveries from last 24 hours with relevance >= min_relevance
            query = discoveries_ref.where(
                "relevance_score", ">=", min_relevance
            ).order_by("analyzed_at", direction=firestore.Query.DESCENDING).limit(50)

            discoveries = []
            for doc in query.stream():
                data = doc.to_dict()
                data["id"] = doc.id
                discoveries.append(data)

            logger.info(f"Fetched {len(discoveries)} recent discoveries")
            return discoveries

        except Exception as e:
            logger.error(f"Error fetching discoveries: {e}", exc_info=True)
            return []

    def format_discoveries_context(self, discoveries: list[dict[str, Any]]) -> str:
        """Format discoveries for model context.

        Args:
            discoveries: List of discoveries

        Returns:
            Formatted context string
        """
        context = "# Recent Discoveries\n\n"

        for i, disc in enumerate(discoveries[:20], 1):  # Limit to top 20
            context += f"## Discovery {i}\n"
            context += f"**Title:** {disc.get('title', 'Untitled')}\n"
            context += f"**Source:** {disc.get('source', 'unknown')}\n"
            context += f"**Relevance Score:** {disc.get('relevance_score', 0)}/100\n"
            context += f"**Strategic Value:** {disc.get('strategic_value', '')}\n"
            context += f"**Key Insights:**\n"
            for insight in disc.get("key_insights", []):
                context += f"  - {insight}\n"
            context += f"**Action Items:**\n"
            for action in disc.get("action_items", []):
                context += f"  - {action}\n"
            context += f"**Tags:** {', '.join(disc.get('tags', []))}\n"
            context += f"**URL:** {disc.get('url', '')}\n\n"

        return context

    def execute_tool_call(self, function_call: Any) -> dict[str, Any]:
        """Execute a tool call.

        Args:
            function_call: Function call from model

        Returns:
            Tool execution result
        """
        function_name = function_call.name
        args = dict(function_call.args)

        logger.info(f"Executing tool: {function_name}")

        if function_name == "create_linear_project":
            return linear_tool.create_project(**args)
        elif function_name == "send_slack_briefing":
            # Add metadata
            args["date"] = datetime.utcnow()
            args["total_discoveries"] = self.total_discoveries
            args["relevant_discoveries"] = self.relevant_discoveries
            args["projects_created"] = self.projects_created
            return slack_tool.send_briefing(**args)
        else:
            logger.error(f"Unknown tool: {function_name}")
            return {"success": False, "error": f"Unknown tool: {function_name}"}

    def run_daily_briefing(self) -> dict[str, Any]:
        """Run the daily intelligence briefing.

        Returns:
            Briefing summary
        """
        logger.info("Starting daily intelligence briefing...")

        try:
            # Fetch recent discoveries
            discoveries = self.fetch_recent_discoveries(
                min_relevance=config.gemini.project_threshold
            )

            self.total_discoveries = len(discoveries)
            self.relevant_discoveries = len(
                [d for d in discoveries if d.get("relevance_score", 0) >= 70]
            )
            self.projects_created = []

            if not discoveries:
                logger.warning("No relevant discoveries found")
                return {
                    "status": "no_discoveries",
                    "message": "No relevant discoveries found",
                }

            # Format context
            context = self.format_discoveries_context(discoveries)

            # Generate with model (multi-turn for tool use)
            full_prompt = f"{self.SYNTHESIS_PROMPT}\n\n{context}"

            generation_config = GenerationConfig(
                temperature=0.7,
                max_output_tokens=4096,
            )

            chat = self.model.start_chat()
            response = chat.send_message(full_prompt, generation_config=generation_config)

            # Handle tool calls
            max_turns = 10
            turn_count = 0

            while turn_count < max_turns:
                turn_count += 1

                # Check if model wants to call a tool
                if not response.candidates[0].content.parts:
                    break

                function_calls = [
                    part.function_call
                    for part in response.candidates[0].content.parts
                    if hasattr(part, "function_call")
                ]

                if not function_calls:
                    # No more tool calls, we're done
                    break

                # Execute tool calls
                for function_call in function_calls:
                    result = self.execute_tool_call(function_call)

                    # Track created projects
                    if function_call.name == "create_linear_project" and result.get("success"):
                        self.projects_created.append({
                            "identifier": result.get("project_identifier", ""),
                            "url": result.get("project_url", ""),
                            "title": function_call.args.get("title", ""),
                        })

                    # Send result back to model
                    response = chat.send_message(
                        f"Tool {function_call.name} result: {result}",
                        generation_config=generation_config,
                    )

            logger.info(
                f"Daily briefing complete. Created {len(self.projects_created)} projects."
            )

            return {
                "status": "success",
                "discoveries_analyzed": len(discoveries),
                "projects_created": len(self.projects_created),
                "project_urls": [p["url"] for p in self.projects_created],
            }

        except Exception as e:
            logger.error(f"Error running daily briefing: {e}", exc_info=True)
            return {"status": "error", "error": str(e)}


# Singleton instance
chief_agent = ChiefAgent()
