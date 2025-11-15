"""
API & Integration Engineering Team

This team handles api & integration engineering team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.integrationinnovationdivision.agent_187 import agent_187
from app.agents.specialists.integrationinnovationdivision.agent_189 import agent_189
from app.agents.specialists.integrationinnovationdivision.agent_191 import agent_191
from app.agents.specialists.integrationinnovationdivision.agent_323 import agent_323


apiintegrationteam = LlmAgent(
    name="api_integration_engineering_team",
    model="gemini-flash",
    description="API & Integration Engineering Team",
    sub_agents=[agent_187, agent_189, agent_191, agent_323],
    instruction="""You are the API & Integration Engineering Team coordinator.

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
