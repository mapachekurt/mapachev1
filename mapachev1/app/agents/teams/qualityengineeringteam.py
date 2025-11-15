"""
Quality Engineering Team

This team handles qa engineers, test automation, and software quality assurance.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.engineeringproductdivision.agent_298 import agent_298
from app.agents.specialists.engineeringproductdivision.agent_299 import agent_299
from app.agents.specialists.engineeringproductdivision.agent_300 import agent_300


qualityengineeringteam = LlmAgent(
    name="quality_engineering_team",
    model="gemini-flash",
    description="QA engineers, test automation, and software quality assurance",
    sub_agents=[agent_298, agent_299, agent_300],
    instruction="""You are the Quality Engineering Team coordinator.

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
