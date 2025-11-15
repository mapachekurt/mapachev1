"""
Data Architecture Team

This team handles data architecture team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.dataanalyticsdivision.agent_153 import agent_153
from app.agents.specialists.dataanalyticsdivision.agent_368 import agent_368
from app.agents.specialists.dataanalyticsdivision.agent_369 import agent_369
from app.agents.specialists.dataanalyticsdivision.agent_370 import agent_370


dataarchitectureteam = LlmAgent(
    name="data_architecture_team",
    model="gemini-flash",
    description="Data Architecture Team",
    sub_agents=[agent_153, agent_368, agent_369, agent_370],
    instruction="""You are the Data Architecture Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 4 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
