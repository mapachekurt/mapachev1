"""
Corporate Strategy Team

This team handles corporate strategy team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.executivestrategydivision.agent_016 import agent_016
from app.agents.specialists.executivestrategydivision.agent_500 import agent_500


corporatestrategyteam = LlmAgent(
    name="corporate_strategy_team",
    model="gemini-flash",
    description="Corporate Strategy Team",
    sub_agents=[agent_016, agent_500],
    instruction="""You are the Corporate Strategy Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 2 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
