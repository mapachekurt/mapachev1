"""
Logistics & Warehouse Team

This team handles logistics & warehouse team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.operationssupplychaindivision.agent_103 import agent_103
from app.agents.specialists.operationssupplychaindivision.agent_111 import agent_111
from app.agents.specialists.operationssupplychaindivision.agent_112 import agent_112
from app.agents.specialists.operationssupplychaindivision.agent_117 import agent_117
from app.agents.specialists.operationssupplychaindivision.agent_127 import agent_127
from app.agents.specialists.operationssupplychaindivision.agent_128 import agent_128
from app.agents.specialists.operationssupplychaindivision.agent_130 import agent_130
from app.agents.specialists.operationssupplychaindivision.agent_132 import agent_132
from app.agents.specialists.operationssupplychaindivision.agent_133 import agent_133
from app.agents.specialists.operationssupplychaindivision.agent_134 import agent_134
from app.agents.specialists.operationssupplychaindivision.agent_261 import agent_261


logisticswarehouseteam = LlmAgent(
    name="logistics_warehouse_team",
    model="gemini-flash",
    description="Logistics & Warehouse Team",
    sub_agents=[agent_103, agent_111, agent_112, agent_117, agent_127, agent_128, agent_130, agent_132, agent_133, agent_134, agent_261],
    instruction="""You are the Logistics & Warehouse Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 11 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
