"""
Cloud & Infrastructure Team

This team handles cloud & infrastructure team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.technologyinfrastructuredivision.agent_141 import agent_141
from app.agents.specialists.technologyinfrastructuredivision.agent_142 import agent_142
from app.agents.specialists.technologyinfrastructuredivision.agent_150 import agent_150
from app.agents.specialists.technologyinfrastructuredivision.agent_154 import agent_154
from app.agents.specialists.technologyinfrastructuredivision.agent_160 import agent_160
from app.agents.specialists.technologyinfrastructuredivision.agent_179 import agent_179
from app.agents.specialists.technologyinfrastructuredivision.agent_180 import agent_180
from app.agents.specialists.technologyinfrastructuredivision.agent_188 import agent_188


cloudinfrastructureteam = LlmAgent(
    name="cloud_infrastructure_team",
    model="gemini-flash",
    description="Cloud & Infrastructure Team",
    sub_agents=[agent_141, agent_142, agent_150, agent_154, agent_160, agent_179, agent_180, agent_188],
    instruction="""You are the Cloud & Infrastructure Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 8 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
