"""
Data Science Team

This team handles data science team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.dataanalyticsdivision.agent_341 import agent_341
from app.agents.specialists.dataanalyticsdivision.agent_345 import agent_345
from app.agents.specialists.dataanalyticsdivision.agent_346 import agent_346
from app.agents.specialists.dataanalyticsdivision.agent_347 import agent_347
from app.agents.specialists.dataanalyticsdivision.agent_348 import agent_348
from app.agents.specialists.dataanalyticsdivision.agent_375 import agent_375


datascienceteam = LlmAgent(
    name="data_science_team",
    model="gemini-flash",
    description="Data Science Team",
    sub_agents=[agent_341, agent_345, agent_346, agent_347, agent_348, agent_375],
    instruction="""You are the Data Science Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 6 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
