"""
Security, Legal & Compliance Division Coordinator

This coordinator manages security, legal & compliance division functions.
"""

from google.adk.agents import LlmAgent
from app.agents.teams.legalteam import legalteam
from app.agents.teams.cybersecurityteam import cybersecurityteam
from app.agents.teams.securityengineeringteam import securityengineeringteam
from app.agents.teams.complianceteam import complianceteam
from app.agents.teams.securitycomplianceteam import securitycomplianceteam


securitylegaldivision = LlmAgent(
    name="security_legal_compliance_division",
    model="gemini-2.0-flash-exp",
    description="Manages security, legal & compliance division functions",
    sub_agents=[legalteam, cybersecurityteam, securityengineeringteam, complianceteam, securitycomplianceteam],
    instruction="""You are the Security, Legal & Compliance Division coordinator.

Your role is to route requests to the appropriate team based on the nature of the request.

Available teams:
  - Legal Team: Legal Team
  - Cybersecurity Operations Team: Cybersecurity Operations Team
  - Security Engineering Team: Security Engineering Team
  - Regulatory Compliance Team: Regulatory Compliance Team
  - Security & Risk Compliance Team: Security & Risk Compliance Team

Routing Guidelines:
- Analyze the incoming request carefully
- Determine which team is best suited to handle it
- Route to the most specialized team when possible
- Escalate complex cross-team issues as needed
- Ensure high quality and timely responses

Always route to sub-agents. Do not attempt to answer requests directly."""
)
