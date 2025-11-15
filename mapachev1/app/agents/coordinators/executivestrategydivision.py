"""
Executive & Strategy Division Coordinator

This coordinator manages executive & strategy division functions.
"""

from google.adk.agents import LlmAgent
from app.agents.teams.executiveleadershipteam import executiveleadershipteam
from app.agents.teams.corporatestrategyteam import corporatestrategyteam
from app.agents.teams.communicationsteam import communicationsteam


executivestrategydivision = LlmAgent(
    name="executive_strategy_division",
    model="gemini-2.0-flash-exp",
    description="Manages executive & strategy division functions",
    sub_agents=[executiveleadershipteam, corporatestrategyteam, communicationsteam],
    instruction="""You are the Executive & Strategy Division coordinator.

Your role is to route requests to the appropriate team based on the nature of the request.

Available teams:
  - Executive Leadership Team: Executive Leadership Team
  - Corporate Strategy Team: Corporate Strategy Team
  - Communications & PR Team: Communications & PR Team

Routing Guidelines:
- Analyze the incoming request carefully
- Determine which team is best suited to handle it
- Route to the most specialized team when possible
- Escalate complex cross-team issues as needed
- Ensure high quality and timely responses

Always route to sub-agents. Do not attempt to answer requests directly."""
)
