"""
Internal Audit Team

This team handles internal audit team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.financeaccountingdivision.agent_025 import agent_025
from app.agents.specialists.financeaccountingdivision.agent_036 import agent_036


internalauditteam = LlmAgent(
    name="internal_audit_team",
    model="gemini-flash",
    description="Internal Audit Team",
    sub_agents=[agent_025, agent_036],
    instruction="""You are the Internal Audit Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 2 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
