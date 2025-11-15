"""
Support & Productivity Integration Team

This team handles support & productivity integration team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.integrationinnovationdivision.agent_433 import agent_433
from app.agents.specialists.integrationinnovationdivision.agent_434 import agent_434
from app.agents.specialists.integrationinnovationdivision.agent_435 import agent_435
from app.agents.specialists.integrationinnovationdivision.agent_455 import agent_455
from app.agents.specialists.integrationinnovationdivision.agent_456 import agent_456
from app.agents.specialists.integrationinnovationdivision.agent_457 import agent_457
from app.agents.specialists.integrationinnovationdivision.agent_458 import agent_458
from app.agents.specialists.integrationinnovationdivision.agent_459 import agent_459
from app.agents.specialists.integrationinnovationdivision.agent_460 import agent_460


supportproductivityintegrationteam = LlmAgent(
    name="support_productivity_integration_team",
    model="gemini-flash",
    description="Support & Productivity Integration Team",
    sub_agents=[agent_433, agent_434, agent_435, agent_455, agent_456, agent_457, agent_458, agent_459, agent_460],
    instruction="""You are the Support & Productivity Integration Team coordinator.

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
