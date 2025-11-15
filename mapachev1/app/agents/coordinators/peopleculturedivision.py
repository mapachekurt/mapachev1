"""
People & Culture Division Coordinator

This coordinator manages people & culture division functions.
"""

from google.adk.agents import LlmAgent
from app.agents.teams.talentacquisitionteam import talentacquisitionteam
from app.agents.teams.compensationbenefitsteam import compensationbenefitsteam
from app.agents.teams.learningdevelopmentteam import learningdevelopmentteam
from app.agents.teams.hroperationsteam import hroperationsteam


peopleculturedivision = LlmAgent(
    name="people_culture_division",
    model="gemini-2.0-flash-exp",
    description="Manages people & culture division functions",
    sub_agents=[talentacquisitionteam, compensationbenefitsteam, learningdevelopmentteam, hroperationsteam],
    instruction="""You are the People & Culture Division coordinator.

Your role is to route requests to the appropriate team based on the nature of the request.

Available teams:
  - Talent Acquisition Team: Talent Acquisition Team
  - Compensation & Benefits Team: Compensation & Benefits Team
  - Learning & Development Team: Learning & Development Team
  - HR Operations Team: HR Operations Team

Routing Guidelines:
- Analyze the incoming request carefully
- Determine which team is best suited to handle it
- Route to the most specialized team when possible
- Escalate complex cross-team issues as needed
- Ensure high quality and timely responses

Always route to sub-agents. Do not attempt to answer requests directly."""
)
