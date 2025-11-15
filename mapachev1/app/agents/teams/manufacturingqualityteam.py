"""
Manufacturing & Quality Team

This team handles manufacturing operations, production management, quality control, and maintenance.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.operationssupplychaindivision.agent_102 import agent_102
from app.agents.specialists.operationssupplychaindivision.agent_104 import agent_104
from app.agents.specialists.operationssupplychaindivision.agent_113 import agent_113
from app.agents.specialists.operationssupplychaindivision.agent_114 import agent_114
from app.agents.specialists.operationssupplychaindivision.agent_121 import agent_121
from app.agents.specialists.operationssupplychaindivision.agent_122 import agent_122
from app.agents.specialists.operationssupplychaindivision.agent_123 import agent_123
from app.agents.specialists.operationssupplychaindivision.agent_135 import agent_135
from app.agents.specialists.operationssupplychaindivision.agent_138 import agent_138


manufacturingqualityteam = LlmAgent(
    name="manufacturing_quality_team",
    model="gemini-flash",
    description="Manufacturing operations, production management, quality control, and maintenance",
    sub_agents=[agent_102, agent_104, agent_113, agent_114, agent_121, agent_122, agent_123, agent_135, agent_138],
    instruction="""You are the Manufacturing & Quality Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 9 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
