"""
Analytics Specialist Team

This team handles analytics specialist team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.dataanalyticsdivision.agent_356 import agent_356
from app.agents.specialists.dataanalyticsdivision.agent_357 import agent_357
from app.agents.specialists.dataanalyticsdivision.agent_376 import agent_376
from app.agents.specialists.dataanalyticsdivision.agent_377 import agent_377
from app.agents.specialists.dataanalyticsdivision.agent_378 import agent_378
from app.agents.specialists.dataanalyticsdivision.agent_379 import agent_379
from app.agents.specialists.dataanalyticsdivision.agent_380 import agent_380


analyticsspecialistteam = LlmAgent(
    name="analytics_specialist_team",
    model="gemini-flash",
    description="Analytics Specialist Team",
    sub_agents=[agent_356, agent_357, agent_376, agent_377, agent_378, agent_379, agent_380],
    instruction="""You are the Analytics Specialist Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 7 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
