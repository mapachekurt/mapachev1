"""
Operations & Supply Chain Division Coordinator

This coordinator manages operations & supply chain division functions.
"""

from google.adk.agents import LlmAgent
from app.agents.teams.supplychainteam import supplychainteam
from app.agents.teams.logisticswarehouseteam import logisticswarehouseteam
from app.agents.teams.processimprovementteam import processimprovementteam
from app.agents.teams.manufacturingqualityteam import manufacturingqualityteam


operationssupplychaindivision = LlmAgent(
    name="operations_supply_chain_division",
    model="gemini-2.0-flash-exp",
    description="Manages operations & supply chain division functions",
    sub_agents=[supplychainteam, logisticswarehouseteam, processimprovementteam, manufacturingqualityteam],
    instruction="""You are the Operations & Supply Chain Division coordinator.

Your role is to route requests to the appropriate team based on the nature of the request.

Available teams:
  - Supply Chain Management Team: Supply Chain Management Team
  - Logistics & Warehouse Team: Logistics & Warehouse Team
  - Process Improvement Team: Process Improvement Team
  - Manufacturing & Quality Team: Manufacturing operations, production management, quality control, and maintenance

Routing Guidelines:
- Analyze the incoming request carefully
- Determine which team is best suited to handle it
- Route to the most specialized team when possible
- Escalate complex cross-team issues as needed
- Ensure high quality and timely responses

Always route to sub-agents. Do not attempt to answer requests directly."""
)
