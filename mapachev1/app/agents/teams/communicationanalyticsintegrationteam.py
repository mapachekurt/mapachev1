"""
Communication & Analytics Integration Team

This team handles communication & analytics integration team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.integrationinnovationdivision.agent_461 import agent_461
from app.agents.specialists.integrationinnovationdivision.agent_462 import agent_462
from app.agents.specialists.integrationinnovationdivision.agent_463 import agent_463
from app.agents.specialists.integrationinnovationdivision.agent_464 import agent_464
from app.agents.specialists.integrationinnovationdivision.agent_465 import agent_465
from app.agents.specialists.integrationinnovationdivision.agent_466 import agent_466
from app.agents.specialists.integrationinnovationdivision.agent_467 import agent_467
from app.agents.specialists.integrationinnovationdivision.agent_468 import agent_468
from app.agents.specialists.integrationinnovationdivision.agent_469 import agent_469
from app.agents.specialists.integrationinnovationdivision.agent_470 import agent_470


communicationanalyticsintegrationteam = LlmAgent(
    name="communication_analytics_integration_team",
    model="gemini-flash",
    description="Communication & Analytics Integration Team",
    sub_agents=[agent_461, agent_462, agent_463, agent_464, agent_465, agent_466, agent_467, agent_468, agent_469, agent_470],
    instruction="""You are the Communication & Analytics Integration Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 10 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
