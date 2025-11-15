"""
Data & Analytics Division Coordinator

This coordinator manages data & analytics division functions.
"""

from google.adk.agents import LlmAgent
from app.agents.teams.dataarchitectureteam import dataarchitectureteam
from app.agents.teams.dataengineeringteam import dataengineeringteam
from app.agents.teams.datascienceteam import datascienceteam
from app.agents.teams.businessintelligenceteam import businessintelligenceteam
from app.agents.teams.datagovernanceteam import datagovernanceteam
from app.agents.teams.analyticsspecialistteam import analyticsspecialistteam


dataanalyticsdivision = LlmAgent(
    name="data_analytics_division",
    model="gemini-2.0-flash-exp",
    description="Manages data & analytics division functions",
    sub_agents=[dataarchitectureteam, dataengineeringteam, datascienceteam, businessintelligenceteam, datagovernanceteam, analyticsspecialistteam],
    instruction="""You are the Data & Analytics Division coordinator.

Your role is to route requests to the appropriate team based on the nature of the request.

Available teams:
  - Data Architecture Team: Data Architecture Team
  - Data Engineering Team: Data Engineering Team
  - Data Science Team: Data Science Team
  - Business Intelligence Team: Business Intelligence Team
  - Data Governance Team: Data Governance Team
  - Analytics Specialist Team: Analytics Specialist Team

Routing Guidelines:
- Analyze the incoming request carefully
- Determine which team is best suited to handle it
- Route to the most specialized team when possible
- Escalate complex cross-team issues as needed
- Ensure high quality and timely responses

Always route to sub-agents. Do not attempt to answer requests directly."""
)
