"""
CRM & Sales Integration Team

This team handles crm & sales integration team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.integrationinnovationdivision.agent_421 import agent_421
from app.agents.specialists.integrationinnovationdivision.agent_431 import agent_431
from app.agents.specialists.integrationinnovationdivision.agent_432 import agent_432


crmsalesintegrationteam = LlmAgent(
    name="crm_sales_integration_team",
    model="gemini-flash",
    description="CRM & Sales Integration Team",
    sub_agents=[agent_421, agent_431, agent_432],
    instruction="""You are the CRM & Sales Integration Team coordinator.

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
