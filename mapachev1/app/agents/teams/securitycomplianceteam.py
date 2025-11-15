"""
Security & Risk Compliance Team

This team handles security & risk compliance team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.securitylegaldivision.agent_388 import agent_388
from app.agents.specialists.securitylegaldivision.agent_401 import agent_401
from app.agents.specialists.securitylegaldivision.agent_402 import agent_402
from app.agents.specialists.securitylegaldivision.agent_403 import agent_403
from app.agents.specialists.securitylegaldivision.agent_404 import agent_404
from app.agents.specialists.securitylegaldivision.agent_405 import agent_405
from app.agents.specialists.securitylegaldivision.agent_406 import agent_406
from app.agents.specialists.securitylegaldivision.agent_407 import agent_407
from app.agents.specialists.securitylegaldivision.agent_408 import agent_408
from app.agents.specialists.securitylegaldivision.agent_417 import agent_417
from app.agents.specialists.securitylegaldivision.agent_418 import agent_418
from app.agents.specialists.securitylegaldivision.agent_419 import agent_419
from app.agents.specialists.securitylegaldivision.agent_420 import agent_420


securitycomplianceteam = LlmAgent(
    name="security_risk_compliance_team",
    model="gemini-flash",
    description="Security & Risk Compliance Team",
    sub_agents=[agent_388, agent_401, agent_402, agent_403, agent_404, agent_405, agent_406, agent_407, agent_408, agent_417, agent_418, agent_419, agent_420],
    instruction="""You are the Security & Risk Compliance Team coordinator.

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
