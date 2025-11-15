"""
Security Engineering Team

This team handles security engineering team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.securitylegaldivision.agent_152 import agent_152
from app.agents.specialists.securitylegaldivision.agent_318 import agent_318
from app.agents.specialists.securitylegaldivision.agent_389 import agent_389
from app.agents.specialists.securitylegaldivision.agent_390 import agent_390
from app.agents.specialists.securitylegaldivision.agent_409 import agent_409
from app.agents.specialists.securitylegaldivision.agent_410 import agent_410
from app.agents.specialists.securitylegaldivision.agent_411 import agent_411
from app.agents.specialists.securitylegaldivision.agent_412 import agent_412
from app.agents.specialists.securitylegaldivision.agent_413 import agent_413
from app.agents.specialists.securitylegaldivision.agent_414 import agent_414
from app.agents.specialists.securitylegaldivision.agent_415 import agent_415
from app.agents.specialists.securitylegaldivision.agent_416 import agent_416


securityengineeringteam = LlmAgent(
    name="security_engineering_team",
    model="gemini-flash",
    description="Security Engineering Team",
    sub_agents=[agent_152, agent_318, agent_389, agent_390, agent_409, agent_410, agent_411, agent_412, agent_413, agent_414, agent_415, agent_416],
    instruction="""You are the Security Engineering Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 12 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
