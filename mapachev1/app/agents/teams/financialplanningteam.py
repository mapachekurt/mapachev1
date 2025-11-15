"""
Financial Planning & Analysis Team

This team handles financial planning & analysis team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.financeaccountingdivision.agent_021 import agent_021
from app.agents.specialists.financeaccountingdivision.agent_030 import agent_030
from app.agents.specialists.financeaccountingdivision.agent_031 import agent_031


financialplanningteam = LlmAgent(
    name="financial_planning_analysis_team",
    model="gemini-flash",
    description="Financial Planning & Analysis Team",
    sub_agents=[agent_021, agent_030, agent_031],
    instruction="""You are the Financial Planning & Analysis Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 3 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
