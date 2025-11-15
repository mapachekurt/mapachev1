"""
Business Intelligence Team

This team handles business intelligence team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.dataanalyticsdivision.agent_351 import agent_351
from app.agents.specialists.dataanalyticsdivision.agent_352 import agent_352
from app.agents.specialists.dataanalyticsdivision.agent_353 import agent_353
from app.agents.specialists.dataanalyticsdivision.agent_354 import agent_354
from app.agents.specialists.dataanalyticsdivision.agent_355 import agent_355
from app.agents.specialists.dataanalyticsdivision.agent_358 import agent_358
from app.agents.specialists.dataanalyticsdivision.agent_359 import agent_359
from app.agents.specialists.dataanalyticsdivision.agent_360 import agent_360


businessintelligenceteam = LlmAgent(
    name="business_intelligence_team",
    model="gemini-flash",
    description="Business Intelligence Team",
    sub_agents=[agent_351, agent_352, agent_353, agent_354, agent_355, agent_358, agent_359, agent_360],
    instruction="""You are the Business Intelligence Team coordinator.

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
