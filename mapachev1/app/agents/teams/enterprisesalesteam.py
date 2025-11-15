"""
Enterprise Sales Team

This team handles enterprise sales team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.revenueoperationsdivision.agent_061 import agent_061
from app.agents.specialists.revenueoperationsdivision.agent_071 import agent_071
from app.agents.specialists.revenueoperationsdivision.agent_098 import agent_098


enterprisesalesteam = LlmAgent(
    name="enterprise_sales_team",
    model="gemini-flash",
    description="Enterprise Sales Team",
    sub_agents=[agent_061, agent_071, agent_098],
    instruction="""You are the Enterprise Sales Team coordinator.

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
