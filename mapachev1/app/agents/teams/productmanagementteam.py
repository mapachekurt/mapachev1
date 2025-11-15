"""
Product Management Team

This team handles product management team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.engineeringproductdivision.agent_019 import agent_019
from app.agents.specialists.engineeringproductdivision.agent_233 import agent_233
from app.agents.specialists.engineeringproductdivision.agent_282 import agent_282
from app.agents.specialists.engineeringproductdivision.agent_301 import agent_301
from app.agents.specialists.engineeringproductdivision.agent_302 import agent_302
from app.agents.specialists.engineeringproductdivision.agent_303 import agent_303
from app.agents.specialists.engineeringproductdivision.agent_304 import agent_304


productmanagementteam = LlmAgent(
    name="product_management_team",
    model="gemini-flash",
    description="Product Management Team",
    sub_agents=[agent_019, agent_233, agent_282, agent_301, agent_302, agent_303, agent_304],
    instruction="""You are the Product Management Team coordinator.

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
