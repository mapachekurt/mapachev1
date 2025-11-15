"""
Integration & Innovation Division Coordinator

This coordinator manages integration & innovation division functions.
"""

from google.adk.agents import LlmAgent
from app.agents.teams.apiintegrationteam import apiintegrationteam
from app.agents.teams.crmsalesintegrationteam import crmsalesintegrationteam
from app.agents.teams.enterpriseintegrationteam import enterpriseintegrationteam
from app.agents.teams.collaborationintegrationteam import collaborationintegrationteam
from app.agents.teams.supportproductivityintegrationteam import supportproductivityintegrationteam
from app.agents.teams.clouddataintegrationteam import clouddataintegrationteam
from app.agents.teams.commercemarketingintegrationteam import commercemarketingintegrationteam
from app.agents.teams.hrdocumentintegrationteam import hrdocumentintegrationteam
from app.agents.teams.communicationanalyticsintegrationteam import communicationanalyticsintegrationteam
from app.agents.teams.monitoringopsintegrationteam import monitoringopsintegrationteam
from app.agents.teams.innovationresearchteam import innovationresearchteam


integrationinnovationdivision = LlmAgent(
    name="integration_innovation_division",
    model="gemini-2.0-flash-exp",
    description="Manages integration & innovation division functions",
    sub_agents=[apiintegrationteam, crmsalesintegrationteam, enterpriseintegrationteam, collaborationintegrationteam, supportproductivityintegrationteam, clouddataintegrationteam, commercemarketingintegrationteam, hrdocumentintegrationteam, communicationanalyticsintegrationteam, monitoringopsintegrationteam, innovationresearchteam],
    instruction="""You are the Integration & Innovation Division coordinator.

Your role is to route requests to the appropriate team based on the nature of the request.

Available teams:
  - API & Integration Engineering Team: API & Integration Engineering Team
  - CRM & Sales Integration Team: CRM & Sales Integration Team
  - Enterprise Integration Team: Enterprise Integration Team
  - Collaboration Integration Team: Collaboration Integration Team
  - Support & Productivity Integration Team: Support & Productivity Integration Team
  - Cloud & Data Integration Team: Cloud & Data Integration Team
  - Commerce & Marketing Integration Team: Commerce & Marketing Integration Team
  - HR & Document Integration Team: HR & Document Integration Team
  - Communication & Analytics Integration Team: Communication & Analytics Integration Team
  - Monitoring & Ops Integration Team: Monitoring & Ops Integration Team
  - Innovation & Research Team: Innovation & Research Team

Routing Guidelines:
- Analyze the incoming request carefully
- Determine which team is best suited to handle it
- Route to the most specialized team when possible
- Escalate complex cross-team issues as needed
- Ensure high quality and timely responses

Always route to sub-agents. Do not attempt to answer requests directly."""
)
