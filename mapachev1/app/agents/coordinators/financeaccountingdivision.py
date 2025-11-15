"""
Finance & Accounting Division Coordinator

This coordinator manages finance & accounting division functions.
"""

from google.adk.agents import LlmAgent
from app.agents.teams.financialplanningteam import financialplanningteam
from app.agents.teams.taxtreasuryteam import taxtreasuryteam
from app.agents.teams.internalauditteam import internalauditteam
from app.agents.teams.accountingoperationsteam import accountingoperationsteam


financeaccountingdivision = LlmAgent(
    name="finance_accounting_division",
    model="gemini-2.0-flash-exp",
    description="Manages finance & accounting division functions",
    sub_agents=[financialplanningteam, taxtreasuryteam, internalauditteam, accountingoperationsteam],
    instruction="""You are the Finance & Accounting Division coordinator.

Your role is to route requests to the appropriate team based on the nature of the request.

Available teams:
  - Financial Planning & Analysis Team: Financial Planning & Analysis Team
  - Tax & Treasury Team: Tax & Treasury Team
  - Internal Audit Team: Internal Audit Team
  - Accounting Operations Team: Accounting Operations Team

Routing Guidelines:
- Analyze the incoming request carefully
- Determine which team is best suited to handle it
- Route to the most specialized team when possible
- Escalate complex cross-team issues as needed
- Ensure high quality and timely responses

Always route to sub-agents. Do not attempt to answer requests directly."""
)
