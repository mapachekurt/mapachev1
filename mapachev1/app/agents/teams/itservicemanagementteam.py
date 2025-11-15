"""
IT Service Management Team

This team handles it service management team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.technologyinfrastructuredivision.agent_020 import agent_020
from app.agents.specialists.technologyinfrastructuredivision.agent_161 import agent_161
from app.agents.specialists.technologyinfrastructuredivision.agent_162 import agent_162
from app.agents.specialists.technologyinfrastructuredivision.agent_163 import agent_163
from app.agents.specialists.technologyinfrastructuredivision.agent_164 import agent_164
from app.agents.specialists.technologyinfrastructuredivision.agent_165 import agent_165
from app.agents.specialists.technologyinfrastructuredivision.agent_166 import agent_166
from app.agents.specialists.technologyinfrastructuredivision.agent_167 import agent_167
from app.agents.specialists.technologyinfrastructuredivision.agent_168 import agent_168
from app.agents.specialists.technologyinfrastructuredivision.agent_169 import agent_169
from app.agents.specialists.technologyinfrastructuredivision.agent_170 import agent_170
from app.agents.specialists.technologyinfrastructuredivision.agent_172 import agent_172
from app.agents.specialists.technologyinfrastructuredivision.agent_173 import agent_173
from app.agents.specialists.technologyinfrastructuredivision.agent_174 import agent_174
from app.agents.specialists.technologyinfrastructuredivision.agent_175 import agent_175
from app.agents.specialists.technologyinfrastructuredivision.agent_192 import agent_192
from app.agents.specialists.technologyinfrastructuredivision.agent_194 import agent_194
from app.agents.specialists.technologyinfrastructuredivision.agent_195 import agent_195


itservicemanagementteam = LlmAgent(
    name="it_service_management_team",
    model="gemini-flash",
    description="IT Service Management Team",
    sub_agents=[agent_020, agent_161, agent_162, agent_163, agent_164, agent_165, agent_166, agent_167, agent_168, agent_169, agent_170, agent_172, agent_173, agent_174, agent_175, agent_192, agent_194, agent_195],
    instruction="""You are the IT Service Management Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 18 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
