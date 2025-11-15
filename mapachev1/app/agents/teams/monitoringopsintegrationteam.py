"""
Monitoring & Ops Integration Team

This team handles monitoring & ops integration team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.integrationinnovationdivision.agent_471 import agent_471
from app.agents.specialists.integrationinnovationdivision.agent_472 import agent_472
from app.agents.specialists.integrationinnovationdivision.agent_473 import agent_473
from app.agents.specialists.integrationinnovationdivision.agent_474 import agent_474
from app.agents.specialists.integrationinnovationdivision.agent_475 import agent_475


monitoringopsintegrationteam = LlmAgent(
    name="monitoring_ops_integration_team",
    model="gemini-flash",
    description="Monitoring & Ops Integration Team",
    sub_agents=[agent_471, agent_472, agent_473, agent_474, agent_475],
    instruction="""You are the Monitoring & Ops Integration Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 5 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
