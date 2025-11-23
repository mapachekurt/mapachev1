"""
CEO Agent - Chief Executive Officer

This agent serves as the CEO and coordinates with the leadership team.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from agents.core import BaseA2AAgent, AgentConfig, RemoteAgent


class CEOAgent(BaseA2AAgent):
    """
    CEO Agent - Coordinates with the leadership team
    """

    def __init__(self):
        """Initialize the CEO agent"""
        config = AgentConfig(
            name="ceo",
            description="Chief Executive Officer responsible for overall company strategy, vision, and leadership",
            role="Chief Executive Officer",
            department="executive",
            skills=[
                "strategic_planning",
                "executive_leadership",
                "decision_making",
                "stakeholder_management",
                "vision_setting",
            ],
            tools=[],
            reports_to=None,
            manages=["cfo", "cto", "cmo", "coo", "chro"],
            model="gemini-2.0-flash-exp",
            tags=["executive", "leadership", "c-suite"],
        )

        super().__init__(config)

        # Leadership team remote agents (will be connected when agents are deployed)
        self.leadership_team = {}

    def connect_to_leadership_team(self):
        """
        Connect to the leadership team members.

        This method discovers and connects to CFO, CTO, CMO, COO, and CHRO.
        """
        leadership_roles = ["cfo", "cto", "cmo", "coo", "chro"]

        for role in leadership_roles:
            try:
                remote_agent = RemoteAgent(role)
                self.leadership_team[role] = remote_agent
                print(f"Connected to {role.upper()}")
            except Exception as e:
                print(f"Could not connect to {role.upper()}: {e}")

    def delegate_to_cfo(self, task: str):
        """Delegate financial tasks to CFO"""
        if "cfo" in self.leadership_team:
            return self.leadership_team["cfo"].send_message(task)
        else:
            return {"error": "CFO not connected"}

    def delegate_to_cto(self, task: str):
        """Delegate technology tasks to CTO"""
        if "cto" in self.leadership_team:
            return self.leadership_team["cto"].send_message(task)
        else:
            return {"error": "CTO not connected"}

    def delegate_to_cmo(self, task: str):
        """Delegate marketing tasks to CMO"""
        if "cmo" in self.leadership_team:
            return self.leadership_team["cmo"].send_message(task)
        else:
            return {"error": "CMO not connected"}

    def delegate_to_coo(self, task: str):
        """Delegate operations tasks to COO"""
        if "coo" in self.leadership_team:
            return self.leadership_team["coo"].send_message(task)
        else:
            return {"error": "COO not connected"}

    def delegate_to_chro(self, task: str):
        """Delegate HR tasks to CHRO"""
        if "chro" in self.leadership_team:
            return self.leadership_team["chro"].send_message(task)
        else:
            return {"error": "CHRO not connected"}


# Create the agent instance
agent = CEOAgent()


if __name__ == "__main__":
    print(f"CEO Agent: {agent}")
    print(f"Agent Card: {agent.get_agent_card()}")
