"""
Talent Acquisition Team

This team handles talent acquisition team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.peopleculturedivision.agent_041 import agent_041
from app.agents.specialists.peopleculturedivision.agent_050 import agent_050


talentacquisitionteam = LlmAgent(
    name="talent_acquisition_team",
    model="gemini-flash",
    description="Talent Acquisition Team",
    sub_agents=[agent_041, agent_050],
    instruction="""You are the Talent Acquisition Team coordinator.

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
