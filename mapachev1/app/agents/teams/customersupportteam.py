"""
Customer Support Team

This team handles customer support team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.customersuccessdivision.agent_206 import agent_206
from app.agents.specialists.customersuccessdivision.agent_210 import agent_210
from app.agents.specialists.customersuccessdivision.agent_211 import agent_211
from app.agents.specialists.customersuccessdivision.agent_212 import agent_212
from app.agents.specialists.customersuccessdivision.agent_213 import agent_213
from app.agents.specialists.customersuccessdivision.agent_214 import agent_214
from app.agents.specialists.customersuccessdivision.agent_215 import agent_215
from app.agents.specialists.customersuccessdivision.agent_216 import agent_216
from app.agents.specialists.customersuccessdivision.agent_217 import agent_217
from app.agents.specialists.customersuccessdivision.agent_218 import agent_218
from app.agents.specialists.customersuccessdivision.agent_273 import agent_273


customersupportteam = LlmAgent(
    name="customer_support_team",
    model="gemini-flash",
    description="Customer Support Team",
    sub_agents=[agent_206, agent_210, agent_211, agent_212, agent_213, agent_214, agent_215, agent_216, agent_217, agent_218, agent_273],
    instruction="""You are the Customer Support Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 11 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
