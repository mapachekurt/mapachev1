"""
Executive Leadership Team

This team handles executive leadership team.
"""

from google.adk.agents import LlmAgent
from app.agents.specialists.executivestrategydivision.agent_001 import agent_001
from app.agents.specialists.executivestrategydivision.agent_002 import agent_002
from app.agents.specialists.executivestrategydivision.agent_003 import agent_003
from app.agents.specialists.executivestrategydivision.agent_004 import agent_004
from app.agents.specialists.executivestrategydivision.agent_005 import agent_005
from app.agents.specialists.executivestrategydivision.agent_006 import agent_006
from app.agents.specialists.executivestrategydivision.agent_007 import agent_007
from app.agents.specialists.executivestrategydivision.agent_008 import agent_008
from app.agents.specialists.executivestrategydivision.agent_009 import agent_009
from app.agents.specialists.executivestrategydivision.agent_010 import agent_010
from app.agents.specialists.executivestrategydivision.agent_011 import agent_011
from app.agents.specialists.executivestrategydivision.agent_012 import agent_012
from app.agents.specialists.executivestrategydivision.agent_014 import agent_014
from app.agents.specialists.executivestrategydivision.agent_015 import agent_015
from app.agents.specialists.executivestrategydivision.agent_026 import agent_026
from app.agents.specialists.executivestrategydivision.agent_027 import agent_027
from app.agents.specialists.executivestrategydivision.agent_028 import agent_028
from app.agents.specialists.executivestrategydivision.agent_029 import agent_029
from app.agents.specialists.executivestrategydivision.agent_032 import agent_032
from app.agents.specialists.executivestrategydivision.agent_033 import agent_033
from app.agents.specialists.executivestrategydivision.agent_045 import agent_045
from app.agents.specialists.executivestrategydivision.agent_046 import agent_046
from app.agents.specialists.executivestrategydivision.agent_047 import agent_047
from app.agents.specialists.executivestrategydivision.agent_048 import agent_048
from app.agents.specialists.executivestrategydivision.agent_049 import agent_049
from app.agents.specialists.executivestrategydivision.agent_065 import agent_065
from app.agents.specialists.executivestrategydivision.agent_066 import agent_066
from app.agents.specialists.executivestrategydivision.agent_067 import agent_067
from app.agents.specialists.executivestrategydivision.agent_068 import agent_068
from app.agents.specialists.executivestrategydivision.agent_069 import agent_069
from app.agents.specialists.executivestrategydivision.agent_070 import agent_070
from app.agents.specialists.executivestrategydivision.agent_099 import agent_099
from app.agents.specialists.executivestrategydivision.agent_105 import agent_105
from app.agents.specialists.executivestrategydivision.agent_106 import agent_106
from app.agents.specialists.executivestrategydivision.agent_107 import agent_107
from app.agents.specialists.executivestrategydivision.agent_108 import agent_108
from app.agents.specialists.executivestrategydivision.agent_109 import agent_109
from app.agents.specialists.executivestrategydivision.agent_119 import agent_119
from app.agents.specialists.executivestrategydivision.agent_120 import agent_120
from app.agents.specialists.executivestrategydivision.agent_129 import agent_129
from app.agents.specialists.executivestrategydivision.agent_131 import agent_131
from app.agents.specialists.executivestrategydivision.agent_145 import agent_145
from app.agents.specialists.executivestrategydivision.agent_146 import agent_146
from app.agents.specialists.executivestrategydivision.agent_147 import agent_147
from app.agents.specialists.executivestrategydivision.agent_148 import agent_148
from app.agents.specialists.executivestrategydivision.agent_149 import agent_149
from app.agents.specialists.executivestrategydivision.agent_190 import agent_190
from app.agents.specialists.executivestrategydivision.agent_202 import agent_202
from app.agents.specialists.executivestrategydivision.agent_203 import agent_203
from app.agents.specialists.executivestrategydivision.agent_204 import agent_204
from app.agents.specialists.executivestrategydivision.agent_234 import agent_234
from app.agents.specialists.executivestrategydivision.agent_238 import agent_238
from app.agents.specialists.executivestrategydivision.agent_240 import agent_240
from app.agents.specialists.executivestrategydivision.agent_243 import agent_243
from app.agents.specialists.executivestrategydivision.agent_244 import agent_244
from app.agents.specialists.executivestrategydivision.agent_245 import agent_245
from app.agents.specialists.executivestrategydivision.agent_246 import agent_246
from app.agents.specialists.executivestrategydivision.agent_276 import agent_276
from app.agents.specialists.executivestrategydivision.agent_278 import agent_278
from app.agents.specialists.executivestrategydivision.agent_284 import agent_284
from app.agents.specialists.executivestrategydivision.agent_285 import agent_285
from app.agents.specialists.executivestrategydivision.agent_286 import agent_286
from app.agents.specialists.executivestrategydivision.agent_342 import agent_342
from app.agents.specialists.executivestrategydivision.agent_343 import agent_343
from app.agents.specialists.executivestrategydivision.agent_344 import agent_344
from app.agents.specialists.executivestrategydivision.agent_382 import agent_382
from app.agents.specialists.executivestrategydivision.agent_383 import agent_383
from app.agents.specialists.executivestrategydivision.agent_384 import agent_384
from app.agents.specialists.executivestrategydivision.agent_426 import agent_426
from app.agents.specialists.executivestrategydivision.agent_482 import agent_482
from app.agents.specialists.executivestrategydivision.agent_483 import agent_483


executiveleadershipteam = LlmAgent(
    name="executive_leadership_team",
    model="gemini-flash",
    description="Executive Leadership Team",
    sub_agents=[agent_001, agent_002, agent_003, agent_004, agent_005, agent_006, agent_007, agent_008, agent_009, agent_010, agent_011, agent_012, agent_014, agent_015, agent_026, agent_027, agent_028, agent_029, agent_032, agent_033, agent_045, agent_046, agent_047, agent_048, agent_049, agent_065, agent_066, agent_067, agent_068, agent_069, agent_070, agent_099, agent_105, agent_106, agent_107, agent_108, agent_109, agent_119, agent_120, agent_129, agent_131, agent_145, agent_146, agent_147, agent_148, agent_149, agent_190, agent_202, agent_203, agent_204, agent_234, agent_238, agent_240, agent_243, agent_244, agent_245, agent_246, agent_276, agent_278, agent_284, agent_285, agent_286, agent_342, agent_343, agent_344, agent_382, agent_383, agent_384, agent_426, agent_482, agent_483],
    instruction="""You are the Executive Leadership Team coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: 71 specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available."""
)
