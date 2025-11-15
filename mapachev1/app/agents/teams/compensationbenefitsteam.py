"""
Compensation & Benefits Team

This team handles compensation & benefits team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.peopleculturedivision.agent_042 import agent_042
from app.agents.specialists.peopleculturedivision.agent_051 import agent_051
from app.agents.specialists.peopleculturedivision.agent_052 import agent_052


compensationbenefitsteam = LlmAgent(
    name="compensation_benefits_team",
    model="gemini-flash",
    description="Compensation & Benefits Team",
    sub_agents=[agent_042, agent_051, agent_052],
    instruction="""You are the Compensation & Benefits Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 3 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
