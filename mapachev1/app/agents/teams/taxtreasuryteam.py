"""
Tax & Treasury Team

This team handles tax & treasury team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.financeaccountingdivision.agent_023 import agent_023
from app.agents.specialists.financeaccountingdivision.agent_024 import agent_024
from app.agents.specialists.financeaccountingdivision.agent_034 import agent_034
from app.agents.specialists.financeaccountingdivision.agent_035 import agent_035


taxtreasuryteam = LlmAgent(
    name="tax_treasury_team",
    model="gemini-flash",
    description="Tax & Treasury Team",
    sub_agents=[agent_023, agent_024, agent_034, agent_035],
    instruction="""You are the Tax & Treasury Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 4 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
