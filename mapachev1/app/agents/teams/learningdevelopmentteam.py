"""
Learning & Development Team

This team handles learning & development team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.peopleculturedivision.agent_043 import agent_043
from app.agents.specialists.peopleculturedivision.agent_054 import agent_054
from app.agents.specialists.peopleculturedivision.agent_058 import agent_058


learningdevelopmentteam = LlmAgent(
    name="learning_development_team",
    model="gemini-flash",
    description="Learning & Development Team",
    sub_agents=[agent_043, agent_054, agent_058],
    instruction="""You are the Learning & Development Team coordinator.

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
