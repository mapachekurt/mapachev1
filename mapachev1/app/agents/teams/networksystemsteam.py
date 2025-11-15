"""
Network & Systems Team

This team handles network & systems team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.technologyinfrastructuredivision.agent_151 import agent_151
from app.agents.specialists.technologyinfrastructuredivision.agent_155 import agent_155
from app.agents.specialists.technologyinfrastructuredivision.agent_156 import agent_156
from app.agents.specialists.technologyinfrastructuredivision.agent_157 import agent_157
from app.agents.specialists.technologyinfrastructuredivision.agent_176 import agent_176
from app.agents.specialists.technologyinfrastructuredivision.agent_177 import agent_177
from app.agents.specialists.technologyinfrastructuredivision.agent_178 import agent_178
from app.agents.specialists.technologyinfrastructuredivision.agent_193 import agent_193
from app.agents.specialists.technologyinfrastructuredivision.agent_196 import agent_196
from app.agents.specialists.technologyinfrastructuredivision.agent_197 import agent_197
from app.agents.specialists.technologyinfrastructuredivision.agent_198 import agent_198
from app.agents.specialists.technologyinfrastructuredivision.agent_199 import agent_199
from app.agents.specialists.technologyinfrastructuredivision.agent_200 import agent_200


networksystemsteam = LlmAgent(
    name="network_systems_team",
    model="gemini-flash",
    description="Network & Systems Team",
    sub_agents=[agent_151, agent_155, agent_156, agent_157, agent_176, agent_177, agent_178, agent_193, agent_196, agent_197, agent_198, agent_199, agent_200],
    instruction="""You are the Network & Systems Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 13 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
