"""
Brand & Product Marketing Team

This team handles brand & product marketing team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.revenueoperationsdivision.agent_063 import agent_063
from app.agents.specialists.revenueoperationsdivision.agent_064 import agent_064
from app.agents.specialists.revenueoperationsdivision.agent_073 import agent_073
from app.agents.specialists.revenueoperationsdivision.agent_074 import agent_074
from app.agents.specialists.revenueoperationsdivision.agent_085 import agent_085
from app.agents.specialists.revenueoperationsdivision.agent_086 import agent_086


brandproductmarketingteam = LlmAgent(
    name="brand_product_marketing_team",
    model="gemini-flash",
    description="Brand & Product Marketing Team",
    sub_agents=[agent_063, agent_064, agent_073, agent_074, agent_085, agent_086],
    instruction="""You are the Brand & Product Marketing Team coordinator.

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
