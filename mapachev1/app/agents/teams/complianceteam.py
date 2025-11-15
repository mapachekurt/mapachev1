"""
Regulatory Compliance Team

This team handles regulatory compliance team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.securitylegaldivision.agent_253 import agent_253
from app.agents.specialists.securitylegaldivision.agent_256 import agent_256
from app.agents.specialists.securitylegaldivision.agent_257 import agent_257
from app.agents.specialists.securitylegaldivision.agent_258 import agent_258
from app.agents.specialists.securitylegaldivision.agent_259 import agent_259
from app.agents.specialists.securitylegaldivision.agent_260 import agent_260
from app.agents.specialists.securitylegaldivision.agent_262 import agent_262
from app.agents.specialists.securitylegaldivision.agent_263 import agent_263
from app.agents.specialists.securitylegaldivision.agent_264 import agent_264
from app.agents.specialists.securitylegaldivision.agent_265 import agent_265
from app.agents.specialists.securitylegaldivision.agent_266 import agent_266
from app.agents.specialists.securitylegaldivision.agent_267 import agent_267
from app.agents.specialists.securitylegaldivision.agent_268 import agent_268


complianceteam = LlmAgent(
    name="regulatory_compliance_team",
    model="gemini-flash",
    description="Regulatory Compliance Team",
    sub_agents=[agent_253, agent_256, agent_257, agent_258, agent_259, agent_260, agent_262, agent_263, agent_264, agent_265, agent_266, agent_267, agent_268],
    instruction="""You are the Regulatory Compliance Team coordinator.

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
