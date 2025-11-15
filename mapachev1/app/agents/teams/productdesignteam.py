"""
Product Design Team

This team handles product design team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.engineeringproductdivision.agent_305 import agent_305
from app.agents.specialists.engineeringproductdivision.agent_306 import agent_306
from app.agents.specialists.engineeringproductdivision.agent_307 import agent_307
from app.agents.specialists.engineeringproductdivision.agent_308 import agent_308
from app.agents.specialists.engineeringproductdivision.agent_309 import agent_309
from app.agents.specialists.engineeringproductdivision.agent_319 import agent_319
from app.agents.specialists.engineeringproductdivision.agent_331 import agent_331
from app.agents.specialists.engineeringproductdivision.agent_446 import agent_446
from app.agents.specialists.engineeringproductdivision.agent_447 import agent_447


productdesignteam = LlmAgent(
    name="product_design_team",
    model="gemini-flash",
    description="Product Design Team",
    sub_agents=[agent_305, agent_306, agent_307, agent_308, agent_309, agent_319, agent_331, agent_446, agent_447],
    instruction="""You are the Product Design Team coordinator.

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
