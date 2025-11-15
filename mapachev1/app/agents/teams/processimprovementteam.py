"""
Process Improvement Team

This team handles process improvement team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.operationssupplychaindivision.agent_124 import agent_124
from app.agents.specialists.operationssupplychaindivision.agent_125 import agent_125
from app.agents.specialists.operationssupplychaindivision.agent_136 import agent_136
from app.agents.specialists.operationssupplychaindivision.agent_137 import agent_137
from app.agents.specialists.operationssupplychaindivision.agent_139 import agent_139
from app.agents.specialists.operationssupplychaindivision.agent_140 import agent_140
from app.agents.specialists.operationssupplychaindivision.agent_487 import agent_487


processimprovementteam = LlmAgent(
    name="process_improvement_team",
    model="gemini-flash",
    description="Process Improvement Team",
    sub_agents=[agent_124, agent_125, agent_136, agent_137, agent_139, agent_140, agent_487],
    instruction="""You are the Process Improvement Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 7 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
