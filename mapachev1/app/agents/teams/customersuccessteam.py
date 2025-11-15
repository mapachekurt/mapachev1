"""
Customer Success Team

This team handles customer success team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.customersuccessdivision.agent_100 import agent_100
from app.agents.specialists.customersuccessdivision.agent_207 import agent_207
from app.agents.specialists.customersuccessdivision.agent_219 import agent_219
from app.agents.specialists.customersuccessdivision.agent_220 import agent_220
from app.agents.specialists.customersuccessdivision.agent_221 import agent_221
from app.agents.specialists.customersuccessdivision.agent_222 import agent_222
from app.agents.specialists.customersuccessdivision.agent_228 import agent_228
from app.agents.specialists.customersuccessdivision.agent_229 import agent_229


customersuccessteam = LlmAgent(
    name="customer_success_team",
    model="gemini-flash",
    description="Customer Success Team",
    sub_agents=[agent_100, agent_207, agent_219, agent_220, agent_221, agent_222, agent_228, agent_229],
    instruction="""You are the Customer Success Team coordinator.

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
