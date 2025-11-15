"""
Engineering & Product Division Coordinator

This coordinator manages engineering & product division functions.
"""

from google.adk.agents import LlmAgent
from app.agents.teams.engineeringarchitectureteam import engineeringarchitectureteam
from app.agents.teams.productmanagementteam import productmanagementteam
from app.agents.teams.softwareengineeringteam import softwareengineeringteam
from app.agents.teams.productdesignteam import productdesignteam
from app.agents.teams.specializedengineeringteam import specializedengineeringteam
from app.agents.teams.qualityengineeringteam import qualityengineeringteam


engineeringproductdivision = LlmAgent(
    name="engineering_product_division",
    model="gemini-2.0-flash-exp",
    description="Manages engineering & product division functions",
    sub_agents=[engineeringarchitectureteam, productmanagementteam, softwareengineeringteam, productdesignteam, specializedengineeringteam, qualityengineeringteam],
    instruction="""You are the Engineering & Product Division coordinator.

Your role is to route requests to the appropriate team based on the nature of the request.

Available teams:
  - Engineering Architecture Team: Engineering Architecture Team
  - Product Management Team: Product Management Team
  - Software Engineering Team: Software Engineering Team
  - Product Design Team: Product Design Team
  - Specialized Engineering Team: Specialized Engineering Team
  - Quality Engineering Team: QA engineers, test automation, and software quality assurance

Routing Guidelines:
- Analyze the incoming request carefully
- Determine which team is best suited to handle it
- Route to the most specialized team when possible
- Escalate complex cross-team issues as needed
- Ensure high quality and timely responses

Always route to sub-agents. Do not attempt to answer requests directly."""
)
