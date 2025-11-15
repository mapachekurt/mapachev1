"""
Commerce & Marketing Integration Team

This team handles commerce & marketing integration team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.integrationinnovationdivision.agent_441 import agent_441
from app.agents.specialists.integrationinnovationdivision.agent_442 import agent_442
from app.agents.specialists.integrationinnovationdivision.agent_443 import agent_443
from app.agents.specialists.integrationinnovationdivision.agent_444 import agent_444
from app.agents.specialists.integrationinnovationdivision.agent_445 import agent_445


commercemarketingintegrationteam = LlmAgent(
    name="commerce_marketing_integration_team",
    model="gemini-flash",
    description="Commerce & Marketing Integration Team",
    sub_agents=[agent_441, agent_442, agent_443, agent_444, agent_445],
    instruction="""You are the Commerce & Marketing Integration Team coordinator.

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
