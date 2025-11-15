"""
Cybersecurity Operations Team

This team handles cybersecurity operations team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.securitylegaldivision.agent_143 import agent_143
from app.agents.specialists.securitylegaldivision.agent_381 import agent_381
from app.agents.specialists.securitylegaldivision.agent_385 import agent_385
from app.agents.specialists.securitylegaldivision.agent_386 import agent_386
from app.agents.specialists.securitylegaldivision.agent_391 import agent_391
from app.agents.specialists.securitylegaldivision.agent_392 import agent_392
from app.agents.specialists.securitylegaldivision.agent_394 import agent_394
from app.agents.specialists.securitylegaldivision.agent_395 import agent_395
from app.agents.specialists.securitylegaldivision.agent_396 import agent_396
from app.agents.specialists.securitylegaldivision.agent_397 import agent_397
from app.agents.specialists.securitylegaldivision.agent_398 import agent_398
from app.agents.specialists.securitylegaldivision.agent_399 import agent_399
from app.agents.specialists.securitylegaldivision.agent_400 import agent_400


cybersecurityteam = LlmAgent(
    name="cybersecurity_operations_team",
    model="gemini-flash",
    description="Cybersecurity Operations Team",
    sub_agents=[agent_143, agent_381, agent_385, agent_386, agent_391, agent_392, agent_394, agent_395, agent_396, agent_397, agent_398, agent_399, agent_400],
    instruction="""You are the Cybersecurity Operations Team coordinator.

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
