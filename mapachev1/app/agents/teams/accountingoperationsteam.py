"""
Accounting Operations Team

This team handles accounting operations team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.financeaccountingdivision.agent_022 import agent_022
from app.agents.specialists.financeaccountingdivision.agent_037 import agent_037
from app.agents.specialists.financeaccountingdivision.agent_038 import agent_038
from app.agents.specialists.financeaccountingdivision.agent_039 import agent_039
from app.agents.specialists.financeaccountingdivision.agent_040 import agent_040


accountingoperationsteam = LlmAgent(
    name="accounting_operations_team",
    model="gemini-flash",
    description="Accounting Operations Team",
    sub_agents=[agent_022, agent_037, agent_038, agent_039, agent_040],
    instruction="""You are the Accounting Operations Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 5 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
