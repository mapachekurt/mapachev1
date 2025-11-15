"""
HR Operations Team

This team handles hr operations team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.peopleculturedivision.agent_044 import agent_044
from app.agents.specialists.peopleculturedivision.agent_053 import agent_053
from app.agents.specialists.peopleculturedivision.agent_055 import agent_055
from app.agents.specialists.peopleculturedivision.agent_056 import agent_056
from app.agents.specialists.peopleculturedivision.agent_057 import agent_057
from app.agents.specialists.peopleculturedivision.agent_059 import agent_059
from app.agents.specialists.peopleculturedivision.agent_060 import agent_060
from app.agents.specialists.peopleculturedivision.agent_387 import agent_387
from app.agents.specialists.peopleculturedivision.agent_393 import agent_393
from app.agents.specialists.peopleculturedivision.agent_448 import agent_448


hroperationsteam = LlmAgent(
    name="hr_operations_team",
    model="gemini-flash",
    description="HR Operations Team",
    sub_agents=[agent_044, agent_053, agent_055, agent_056, agent_057, agent_059, agent_060, agent_387, agent_393, agent_448],
    instruction="""You are the HR Operations Team coordinator.

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
