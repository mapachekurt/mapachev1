"""
Revenue Operations Division Coordinator

This coordinator manages revenue operations division functions.
"""

from google.adk.agents import LlmAgent
from app.agents.teams.enterprisesalesteam import enterprisesalesteam
from app.agents.teams.growthmarketingteam import growthmarketingteam
from app.agents.teams.brandproductmarketingteam import brandproductmarketingteam
from app.agents.teams.marketingoperationsteam import marketingoperationsteam
from app.agents.teams.salesoperationsteam import salesoperationsteam


revenueoperationsdivision = LlmAgent(
    name="revenue_operations_division",
    model="gemini-2.0-flash-exp",
    description="Manages revenue operations division functions",
    sub_agents=[enterprisesalesteam, growthmarketingteam, brandproductmarketingteam, marketingoperationsteam, salesoperationsteam],
    instruction="""You are the Revenue Operations Division coordinator.

Your role is to route requests to the appropriate team based on the nature of the request.

Available teams:
  - Enterprise Sales Team: Enterprise Sales Team
  - Growth Marketing Team: Growth Marketing Team
  - Brand & Product Marketing Team: Brand & Product Marketing Team
  - Marketing Operations Team: Marketing Operations Team
  - Sales Operations Team: Sales Operations Team

Routing Guidelines:
- Analyze the incoming request carefully
- Determine which team is best suited to handle it
- Route to the most specialized team when possible
- Escalate complex cross-team issues as needed
- Ensure high quality and timely responses

Always route to sub-agents. Do not attempt to answer requests directly."""
)
