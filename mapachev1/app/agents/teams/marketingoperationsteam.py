"""
Marketing Operations Team

This team handles marketing operations team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.revenueoperationsdivision.agent_075 import agent_075


marketingoperationsteam = LlmAgent(
    name="marketing_operations_team",
    model="gemini-flash",
    description="Marketing Operations Team",
    sub_agents=[agent_075],
    instruction="""You are the Marketing Operations Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 1 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
