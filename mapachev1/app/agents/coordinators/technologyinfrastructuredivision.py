"""
Technology Infrastructure Division Coordinator

This coordinator manages technology infrastructure division functions.
"""

from google.adk.agents import LlmAgent
from app.agents.teams.itservicemanagementteam import itservicemanagementteam
from app.agents.teams.cloudinfrastructureteam import cloudinfrastructureteam
from app.agents.teams.networksystemsteam import networksystemsteam
from app.agents.teams.devopssreteam import devopssreteam


technologyinfrastructuredivision = LlmAgent(
    name="technology_infrastructure_division",
    model="gemini-2.0-flash-exp",
    description="Manages technology infrastructure division functions",
    sub_agents=[itservicemanagementteam, cloudinfrastructureteam, networksystemsteam, devopssreteam],
    instruction="""You are the Technology Infrastructure Division coordinator.

Your role is to route requests to the appropriate team based on the nature of the request.

Available teams:
  - IT Service Management Team: IT Service Management Team
  - Cloud & Infrastructure Team: Cloud & Infrastructure Team
  - Network & Systems Team: Network & Systems Team
  - DevOps & SRE Team: DevOps & SRE Team

Routing Guidelines:
- Analyze the incoming request carefully
- Determine which team is best suited to handle it
- Route to the most specialized team when possible
- Escalate complex cross-team issues as needed
- Ensure high quality and timely responses

Always route to sub-agents. Do not attempt to answer requests directly."""
)
