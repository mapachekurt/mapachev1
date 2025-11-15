"""
Customer Operations Team

This team handles customer operations team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.customersuccessdivision.agent_201 import agent_201
from app.agents.specialists.customersuccessdivision.agent_205 import agent_205
from app.agents.specialists.customersuccessdivision.agent_208 import agent_208
from app.agents.specialists.customersuccessdivision.agent_209 import agent_209
from app.agents.specialists.customersuccessdivision.agent_223 import agent_223
from app.agents.specialists.customersuccessdivision.agent_224 import agent_224
from app.agents.specialists.customersuccessdivision.agent_225 import agent_225
from app.agents.specialists.customersuccessdivision.agent_226 import agent_226
from app.agents.specialists.customersuccessdivision.agent_236 import agent_236
from app.agents.specialists.customersuccessdivision.agent_237 import agent_237


customeroperationsteam = LlmAgent(
    name="customer_operations_team",
    model="gemini-flash",
    description="Customer Operations Team",
    sub_agents=[agent_201, agent_205, agent_208, agent_209, agent_223, agent_224, agent_225, agent_226, agent_236, agent_237],
    instruction="""You are the Customer Operations Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 10 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
