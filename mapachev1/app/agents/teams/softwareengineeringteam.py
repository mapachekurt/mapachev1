"""
Software Engineering Team

This team handles software engineering team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.engineeringproductdivision.agent_144 import agent_144
from app.agents.specialists.engineeringproductdivision.agent_281 import agent_281
from app.agents.specialists.engineeringproductdivision.agent_287 import agent_287
from app.agents.specialists.engineeringproductdivision.agent_288 import agent_288
from app.agents.specialists.engineeringproductdivision.agent_289 import agent_289
from app.agents.specialists.engineeringproductdivision.agent_290 import agent_290
from app.agents.specialists.engineeringproductdivision.agent_291 import agent_291
from app.agents.specialists.engineeringproductdivision.agent_292 import agent_292
from app.agents.specialists.engineeringproductdivision.agent_293 import agent_293
from app.agents.specialists.engineeringproductdivision.agent_294 import agent_294
from app.agents.specialists.engineeringproductdivision.agent_295 import agent_295
from app.agents.specialists.engineeringproductdivision.agent_296 import agent_296
from app.agents.specialists.engineeringproductdivision.agent_297 import agent_297


softwareengineeringteam = LlmAgent(
    name="software_engineering_team",
    model="gemini-flash",
    description="Software Engineering Team",
    sub_agents=[agent_144, agent_281, agent_287, agent_288, agent_289, agent_290, agent_291, agent_292, agent_293, agent_294, agent_295, agent_296, agent_297],
    instruction="""You are the Software Engineering Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 13 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
