"""
Collaboration Integration Team

This team handles collaboration integration team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.integrationinnovationdivision.agent_427 import agent_427
from app.agents.specialists.integrationinnovationdivision.agent_428 import agent_428
from app.agents.specialists.integrationinnovationdivision.agent_429 import agent_429
from app.agents.specialists.integrationinnovationdivision.agent_430 import agent_430


collaborationintegrationteam = LlmAgent(
    name="collaboration_integration_team",
    model="gemini-flash",
    description="Collaboration Integration Team",
    sub_agents=[agent_427, agent_428, agent_429, agent_430],
    instruction="""You are the Collaboration Integration Team coordinator.

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
