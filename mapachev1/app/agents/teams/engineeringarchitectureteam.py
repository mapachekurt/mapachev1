"""
Engineering Architecture Team

This team handles engineering architecture team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.engineeringproductdivision.agent_097 import agent_097
from app.agents.specialists.engineeringproductdivision.agent_310 import agent_310
from app.agents.specialists.engineeringproductdivision.agent_311 import agent_311
from app.agents.specialists.engineeringproductdivision.agent_312 import agent_312


engineeringarchitectureteam = LlmAgent(
    name="engineering_architecture_team",
    model="gemini-flash",
    description="Engineering Architecture Team",
    sub_agents=[agent_097, agent_310, agent_311, agent_312],
    instruction="""You are the Engineering Architecture Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 4 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
