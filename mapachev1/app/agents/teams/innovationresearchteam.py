"""
Innovation & Research Team

This team handles innovation & research team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.integrationinnovationdivision.agent_481 import agent_481
from app.agents.specialists.integrationinnovationdivision.agent_484 import agent_484
from app.agents.specialists.integrationinnovationdivision.agent_485 import agent_485
from app.agents.specialists.integrationinnovationdivision.agent_486 import agent_486
from app.agents.specialists.integrationinnovationdivision.agent_488 import agent_488
from app.agents.specialists.integrationinnovationdivision.agent_489 import agent_489
from app.agents.specialists.integrationinnovationdivision.agent_490 import agent_490
from app.agents.specialists.integrationinnovationdivision.agent_491 import agent_491
from app.agents.specialists.integrationinnovationdivision.agent_492 import agent_492
from app.agents.specialists.integrationinnovationdivision.agent_493 import agent_493
from app.agents.specialists.integrationinnovationdivision.agent_494 import agent_494
from app.agents.specialists.integrationinnovationdivision.agent_495 import agent_495
from app.agents.specialists.integrationinnovationdivision.agent_496 import agent_496
from app.agents.specialists.integrationinnovationdivision.agent_497 import agent_497
from app.agents.specialists.integrationinnovationdivision.agent_498 import agent_498
from app.agents.specialists.integrationinnovationdivision.agent_499 import agent_499
from app.agents.specialists.integrationinnovationdivision.agent_501 import agent_501
from app.agents.specialists.integrationinnovationdivision.agent_502 import agent_502
from app.agents.specialists.integrationinnovationdivision.agent_503 import agent_503
from app.agents.specialists.integrationinnovationdivision.agent_504 import agent_504
from app.agents.specialists.integrationinnovationdivision.agent_505 import agent_505
from app.agents.specialists.integrationinnovationdivision.agent_506 import agent_506
from app.agents.specialists.integrationinnovationdivision.agent_507 import agent_507
from app.agents.specialists.integrationinnovationdivision.agent_508 import agent_508
from app.agents.specialists.integrationinnovationdivision.agent_509 import agent_509
from app.agents.specialists.integrationinnovationdivision.agent_510 import agent_510
from app.agents.specialists.integrationinnovationdivision.agent_511 import agent_511


innovationresearchteam = LlmAgent(
    name="innovation_research_team",
    model="gemini-flash",
    description="Innovation & Research Team",
    sub_agents=[agent_481, agent_484, agent_485, agent_486, agent_488, agent_489, agent_490, agent_491, agent_492, agent_493, agent_494, agent_495, agent_496, agent_497, agent_498, agent_499, agent_501, agent_502, agent_503, agent_504, agent_505, agent_506, agent_507, agent_508, agent_509, agent_510, agent_511],
    instruction="""You are the Innovation & Research Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 27 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
