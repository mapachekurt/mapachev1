"""
Specialized Engineering Team

This team handles specialized engineering team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.engineeringproductdivision.agent_283 import agent_283
from app.agents.specialists.engineeringproductdivision.agent_313 import agent_313
from app.agents.specialists.engineeringproductdivision.agent_314 import agent_314
from app.agents.specialists.engineeringproductdivision.agent_317 import agent_317
from app.agents.specialists.engineeringproductdivision.agent_320 import agent_320
from app.agents.specialists.engineeringproductdivision.agent_321 import agent_321
from app.agents.specialists.engineeringproductdivision.agent_322 import agent_322
from app.agents.specialists.engineeringproductdivision.agent_324 import agent_324
from app.agents.specialists.engineeringproductdivision.agent_325 import agent_325
from app.agents.specialists.engineeringproductdivision.agent_326 import agent_326
from app.agents.specialists.engineeringproductdivision.agent_327 import agent_327
from app.agents.specialists.engineeringproductdivision.agent_328 import agent_328
from app.agents.specialists.engineeringproductdivision.agent_329 import agent_329
from app.agents.specialists.engineeringproductdivision.agent_330 import agent_330
from app.agents.specialists.engineeringproductdivision.agent_332 import agent_332
from app.agents.specialists.engineeringproductdivision.agent_333 import agent_333
from app.agents.specialists.engineeringproductdivision.agent_334 import agent_334
from app.agents.specialists.engineeringproductdivision.agent_335 import agent_335
from app.agents.specialists.engineeringproductdivision.agent_336 import agent_336
from app.agents.specialists.engineeringproductdivision.agent_337 import agent_337
from app.agents.specialists.engineeringproductdivision.agent_338 import agent_338
from app.agents.specialists.engineeringproductdivision.agent_339 import agent_339
from app.agents.specialists.engineeringproductdivision.agent_340 import agent_340


specializedengineeringteam = LlmAgent(
    name="specialized_engineering_team",
    model="gemini-flash",
    description="Specialized Engineering Team",
    sub_agents=[agent_283, agent_313, agent_314, agent_317, agent_320, agent_321, agent_322, agent_324, agent_325, agent_326, agent_327, agent_328, agent_329, agent_330, agent_332, agent_333, agent_334, agent_335, agent_336, agent_337, agent_338, agent_339, agent_340],
    instruction="""You are the Specialized Engineering Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 23 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
