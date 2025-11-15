"""
Customer Success Division Coordinator

This coordinator manages customer success division functions.
"""

from google.adk.agents import LlmAgent
from app.agents.teams.customersuccessteam import customersuccessteam
from app.agents.teams.customersupportteam import customersupportteam
from app.agents.teams.customeroperationsteam import customeroperationsteam
from app.agents.teams.customerengagementteam import customerengagementteam


customersuccessdivision = LlmAgent(
    name="customer_success_division",
    model="gemini-2.0-flash-exp",
    description="Manages customer success division functions",
    sub_agents=[customersuccessteam, customersupportteam, customeroperationsteam, customerengagementteam],
    instruction="""You are the Customer Success Division coordinator.

Your role is to route requests to the appropriate team based on the nature of the request.

Available teams:
  - Customer Success Team: Customer Success Team
  - Customer Support Team: Customer Support Team
  - Customer Operations Team: Customer Operations Team
  - Customer Engagement Team: Customer Engagement Team

Routing Guidelines:
- Analyze the incoming request carefully
- Determine which team is best suited to handle it
- Route to the most specialized team when possible
- Escalate complex cross-team issues as needed
- Ensure high quality and timely responses

Always route to sub-agents. Do not attempt to answer requests directly."""
)
