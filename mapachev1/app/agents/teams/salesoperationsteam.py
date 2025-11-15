"""
Sales Operations Team

This team handles sales operations team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.revenueoperationsdivision.agent_078 import agent_078
from app.agents.specialists.revenueoperationsdivision.agent_079 import agent_079
from app.agents.specialists.revenueoperationsdivision.agent_080 import agent_080
from app.agents.specialists.revenueoperationsdivision.agent_091 import agent_091
from app.agents.specialists.revenueoperationsdivision.agent_092 import agent_092
from app.agents.specialists.revenueoperationsdivision.agent_093 import agent_093
from app.agents.specialists.revenueoperationsdivision.agent_094 import agent_094
from app.agents.specialists.revenueoperationsdivision.agent_095 import agent_095
from app.agents.specialists.revenueoperationsdivision.agent_096 import agent_096


salesoperationsteam = LlmAgent(
    name="sales_operations_team",
    model="gemini-flash",
    description="Sales Operations Team",
    sub_agents=[agent_078, agent_079, agent_080, agent_091, agent_092, agent_093, agent_094, agent_095, agent_096],
    instruction="""You are the Sales Operations Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 9 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
