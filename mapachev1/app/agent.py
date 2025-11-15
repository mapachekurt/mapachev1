"""
Root Orchestrator - Master Coordinator

This is the root orchestrator that routes requests to appropriate divisions.
"""

from google.adk.agents import LlmAgent
from app.agents.coordinators.executivestrategydivision import executivestrategydivision
from app.agents.coordinators.securitylegaldivision import securitylegaldivision
from app.agents.coordinators.technologyinfrastructuredivision import technologyinfrastructuredivision
from app.agents.coordinators.financeaccountingdivision import financeaccountingdivision
from app.agents.coordinators.peopleculturedivision import peopleculturedivision
from app.agents.coordinators.revenueoperationsdivision import revenueoperationsdivision
from app.agents.coordinators.engineeringproductdivision import engineeringproductdivision
from app.agents.coordinators.customersuccessdivision import customersuccessdivision
from app.agents.coordinators.operationssupplychaindivision import operationssupplychaindivision
from app.agents.coordinators.dataanalyticsdivision import dataanalyticsdivision
from app.agents.coordinators.integrationinnovationdivision import integrationinnovationdivision


root_orchestrator = LlmAgent(
    name="rootorchestrator",
    model="gemini-2.0-flash-exp",
    description="Master orchestrator that routes requests to appropriate divisions based on functional area. Analyzes incoming requests and delegates to the most appropriate division coordinator.",
    sub_agents=[executivestrategydivision, securitylegaldivision, technologyinfrastructuredivision, financeaccountingdivision, peopleculturedivision, revenueoperationsdivision, engineeringproductdivision, customersuccessdivision, operationssupplychaindivision, dataanalyticsdivision, integrationinnovationdivision],
    instruction="""You are the Root Orchestrator, the master coordinator of the entire organization.

Your role is to analyze incoming requests and route them to the appropriate division coordinator.

Available divisions:
  - Executive & Strategy Division: Manages executive & strategy division functions
  - Security, Legal & Compliance Division: Manages security, legal & compliance division functions
  - Technology Infrastructure Division: Manages technology infrastructure division functions
  - Finance & Accounting Division: Manages finance & accounting division functions
  - People & Culture Division: Manages people & culture division functions
  - Revenue Operations Division: Manages revenue operations division functions
  - Engineering & Product Division: Manages engineering & product division functions
  - Customer Success Division: Manages customer success division functions
  - Operations & Supply Chain Division: Manages operations & supply chain division functions
  - Data & Analytics Division: Manages data & analytics division functions
  - Integration & Innovation Division: Manages integration & innovation division functions

Routing Guidelines:
- Carefully analyze each request to understand its functional area
- Route to the most appropriate division based on the request type
- Consider cross-functional requests and route to the primary responsible division
- Balance load across divisions when multiple could handle a request
- Ensure all requests receive expert attention from the right division
- Track routing patterns to optimize future decisions

Always route to division coordinators. Do not attempt to answer requests directly.
You are a router and coordinator, not an executor."""
)

# Export for ADK
agent = root_orchestrator
app = root_orchestrator  # Alias for compatibility
