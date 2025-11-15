"""
Data Engineering Team

This team handles data engineering team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.dataanalyticsdivision.agent_315 import agent_315
from app.agents.specialists.dataanalyticsdivision.agent_316 import agent_316
from app.agents.specialists.dataanalyticsdivision.agent_349 import agent_349
from app.agents.specialists.dataanalyticsdivision.agent_350 import agent_350
from app.agents.specialists.dataanalyticsdivision.agent_371 import agent_371
from app.agents.specialists.dataanalyticsdivision.agent_372 import agent_372
from app.agents.specialists.dataanalyticsdivision.agent_373 import agent_373
from app.agents.specialists.dataanalyticsdivision.agent_374 import agent_374


dataengineeringteam = LlmAgent(
    name="data_engineering_team",
    model="gemini-flash",
    description="Data Engineering Team",
    sub_agents=[agent_315, agent_316, agent_349, agent_350, agent_371, agent_372, agent_373, agent_374],
    instruction="""You are the Data Engineering Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 8 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
