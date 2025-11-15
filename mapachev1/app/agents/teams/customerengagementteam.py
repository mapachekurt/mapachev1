"""
Customer Engagement Team

This team handles customer engagement team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.customersuccessdivision.agent_227 import agent_227
from app.agents.specialists.customersuccessdivision.agent_230 import agent_230
from app.agents.specialists.customersuccessdivision.agent_231 import agent_231
from app.agents.specialists.customersuccessdivision.agent_232 import agent_232
from app.agents.specialists.customersuccessdivision.agent_235 import agent_235
from app.agents.specialists.customersuccessdivision.agent_239 import agent_239


customerengagementteam = LlmAgent(
    name="customer_engagement_team",
    model="gemini-flash",
    description="Customer Engagement Team",
    sub_agents=[agent_227, agent_230, agent_231, agent_232, agent_235, agent_239],
    instruction="""You are the Customer Engagement Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 6 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
