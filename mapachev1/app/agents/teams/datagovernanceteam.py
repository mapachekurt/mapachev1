"""
Data Governance Team

This team handles data governance team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.dataanalyticsdivision.agent_361 import agent_361
from app.agents.specialists.dataanalyticsdivision.agent_362 import agent_362
from app.agents.specialists.dataanalyticsdivision.agent_363 import agent_363
from app.agents.specialists.dataanalyticsdivision.agent_364 import agent_364
from app.agents.specialists.dataanalyticsdivision.agent_365 import agent_365
from app.agents.specialists.dataanalyticsdivision.agent_366 import agent_366
from app.agents.specialists.dataanalyticsdivision.agent_367 import agent_367


datagovernanceteam = LlmAgent(
    name="data_governance_team",
    model="gemini-flash",
    description="Data Governance Team",
    sub_agents=[agent_361, agent_362, agent_363, agent_364, agent_365, agent_366, agent_367],
    instruction="""You are the Data Governance Team coordinator.

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
