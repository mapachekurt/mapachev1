"""
HR & Document Integration Team

This team handles hr & document integration team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.integrationinnovationdivision.agent_449 import agent_449
from app.agents.specialists.integrationinnovationdivision.agent_450 import agent_450
from app.agents.specialists.integrationinnovationdivision.agent_451 import agent_451
from app.agents.specialists.integrationinnovationdivision.agent_452 import agent_452
from app.agents.specialists.integrationinnovationdivision.agent_453 import agent_453
from app.agents.specialists.integrationinnovationdivision.agent_454 import agent_454


hrdocumentintegrationteam = LlmAgent(
    name="hr_document_integration_team",
    model="gemini-flash",
    description="HR & Document Integration Team",
    sub_agents=[agent_449, agent_450, agent_451, agent_452, agent_453, agent_454],
    instruction="""You are the HR & Document Integration Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 6 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
