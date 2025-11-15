"""
Communications & PR Team

This team handles communications & pr team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.executivestrategydivision.agent_017 import agent_017
from app.agents.specialists.executivestrategydivision.agent_018 import agent_018
from app.agents.specialists.executivestrategydivision.agent_087 import agent_087


communicationsteam = LlmAgent(
    name="communications_pr_team",
    model="gemini-flash",
    description="Communications & PR Team",
    sub_agents=[agent_017, agent_018, agent_087],
    instruction="""You are the Communications & PR Team coordinator.

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
