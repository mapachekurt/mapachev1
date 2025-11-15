"""
DevOps & SRE Team

This team handles devops & sre team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.technologyinfrastructuredivision.agent_158 import agent_158
from app.agents.specialists.technologyinfrastructuredivision.agent_159 import agent_159
from app.agents.specialists.technologyinfrastructuredivision.agent_171 import agent_171
from app.agents.specialists.technologyinfrastructuredivision.agent_181 import agent_181
from app.agents.specialists.technologyinfrastructuredivision.agent_182 import agent_182
from app.agents.specialists.technologyinfrastructuredivision.agent_183 import agent_183
from app.agents.specialists.technologyinfrastructuredivision.agent_184 import agent_184
from app.agents.specialists.technologyinfrastructuredivision.agent_185 import agent_185
from app.agents.specialists.technologyinfrastructuredivision.agent_186 import agent_186


devopssreteam = LlmAgent(
    name="devops_sre_team",
    model="gemini-flash",
    description="DevOps & SRE Team",
    sub_agents=[agent_158, agent_159, agent_171, agent_181, agent_182, agent_183, agent_184, agent_185, agent_186],
    instruction="""You are the DevOps & SRE Team coordinator.

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
