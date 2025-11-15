"""
Enterprise Integration Team

This team handles enterprise integration team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.integrationinnovationdivision.agent_422 import agent_422
from app.agents.specialists.integrationinnovationdivision.agent_423 import agent_423
from app.agents.specialists.integrationinnovationdivision.agent_424 import agent_424
from app.agents.specialists.integrationinnovationdivision.agent_425 import agent_425


enterpriseintegrationteam = LlmAgent(
    name="enterprise_integration_team",
    model="gemini-flash",
    description="Enterprise Integration Team",
    sub_agents=[agent_422, agent_423, agent_424, agent_425],
    instruction="""You are the Enterprise Integration Team coordinator.

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
