"""
Legal Team

This team handles legal team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.securitylegaldivision.agent_013 import agent_013
from app.agents.specialists.securitylegaldivision.agent_241 import agent_241
from app.agents.specialists.securitylegaldivision.agent_242 import agent_242
from app.agents.specialists.securitylegaldivision.agent_247 import agent_247
from app.agents.specialists.securitylegaldivision.agent_248 import agent_248
from app.agents.specialists.securitylegaldivision.agent_249 import agent_249
from app.agents.specialists.securitylegaldivision.agent_250 import agent_250
from app.agents.specialists.securitylegaldivision.agent_251 import agent_251
from app.agents.specialists.securitylegaldivision.agent_252 import agent_252
from app.agents.specialists.securitylegaldivision.agent_254 import agent_254
from app.agents.specialists.securitylegaldivision.agent_255 import agent_255
from app.agents.specialists.securitylegaldivision.agent_269 import agent_269
from app.agents.specialists.securitylegaldivision.agent_270 import agent_270
from app.agents.specialists.securitylegaldivision.agent_271 import agent_271
from app.agents.specialists.securitylegaldivision.agent_272 import agent_272
from app.agents.specialists.securitylegaldivision.agent_274 import agent_274
from app.agents.specialists.securitylegaldivision.agent_275 import agent_275
from app.agents.specialists.securitylegaldivision.agent_277 import agent_277
from app.agents.specialists.securitylegaldivision.agent_279 import agent_279
from app.agents.specialists.securitylegaldivision.agent_280 import agent_280


legalteam = LlmAgent(
    name="legal_team",
    model="gemini-flash",
    description="Legal Team",
    sub_agents=[agent_013, agent_241, agent_242, agent_247, agent_248, agent_249, agent_250, agent_251, agent_252, agent_254, agent_255, agent_269, agent_270, agent_271, agent_272, agent_274, agent_275, agent_277, agent_279, agent_280],
    instruction="""You are the Legal Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 20 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
