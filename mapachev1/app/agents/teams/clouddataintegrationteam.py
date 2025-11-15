"""
Cloud & Data Integration Team

This team handles cloud & data integration team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.integrationinnovationdivision.agent_436 import agent_436
from app.agents.specialists.integrationinnovationdivision.agent_437 import agent_437
from app.agents.specialists.integrationinnovationdivision.agent_438 import agent_438
from app.agents.specialists.integrationinnovationdivision.agent_439 import agent_439
from app.agents.specialists.integrationinnovationdivision.agent_440 import agent_440
from app.agents.specialists.integrationinnovationdivision.agent_476 import agent_476
from app.agents.specialists.integrationinnovationdivision.agent_477 import agent_477
from app.agents.specialists.integrationinnovationdivision.agent_478 import agent_478
from app.agents.specialists.integrationinnovationdivision.agent_479 import agent_479
from app.agents.specialists.integrationinnovationdivision.agent_480 import agent_480


clouddataintegrationteam = LlmAgent(
    name="cloud_data_integration_team",
    model="gemini-flash",
    description="Cloud & Data Integration Team",
    sub_agents=[agent_436, agent_437, agent_438, agent_439, agent_440, agent_476, agent_477, agent_478, agent_479, agent_480],
    instruction="""You are the Cloud & Data Integration Team coordinator.

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
