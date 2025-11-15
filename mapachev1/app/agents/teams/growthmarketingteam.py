"""
Growth Marketing Team

This team handles growth marketing team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.revenueoperationsdivision.agent_062 import agent_062
from app.agents.specialists.revenueoperationsdivision.agent_072 import agent_072
from app.agents.specialists.revenueoperationsdivision.agent_076 import agent_076
from app.agents.specialists.revenueoperationsdivision.agent_077 import agent_077
from app.agents.specialists.revenueoperationsdivision.agent_081 import agent_081
from app.agents.specialists.revenueoperationsdivision.agent_082 import agent_082
from app.agents.specialists.revenueoperationsdivision.agent_083 import agent_083
from app.agents.specialists.revenueoperationsdivision.agent_084 import agent_084
from app.agents.specialists.revenueoperationsdivision.agent_088 import agent_088
from app.agents.specialists.revenueoperationsdivision.agent_089 import agent_089
from app.agents.specialists.revenueoperationsdivision.agent_090 import agent_090
from app.agents.specialists.revenueoperationsdivision.agent_116 import agent_116


growthmarketingteam = LlmAgent(
    name="growth_marketing_team",
    model="gemini-flash",
    description="Growth Marketing Team",
    sub_agents=[agent_062, agent_072, agent_076, agent_077, agent_081, agent_082, agent_083, agent_084, agent_088, agent_089, agent_090, agent_116],
    instruction="""You are the Growth Marketing Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 12 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
