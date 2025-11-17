"""
CFO Agent - Chief Financial Officer

This agent manages all financial operations and reports to the CEO.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from agents.core import BaseA2AAgent, AgentConfig, RemoteAgent


class CFOAgent(BaseA2AAgent):
    """
    CFO Agent - Manages financial operations
    """

    def __init__(self):
        """Initialize the CFO agent"""
        config = AgentConfig(
            name="cfo",
            description="Chief Financial Officer responsible for financial planning, analysis, and reporting",
            role="Chief Financial Officer",
            department="finance",
            skills=[
                "financial_planning",
                "budget_management",
                "investor_relations",
                "financial_reporting",
                "risk_management",
            ],
            tools=[],
            reports_to="ceo",
            manages=["controller", "vp_fp_and_a", "treasurer"],
            model="gemini-2.0-flash-exp",
            tags=["finance", "leadership", "c-suite"],
        )

        super().__init__(config)

        # Finance team remote agents
        self.finance_team = {}

    def connect_to_finance_team(self):
        """Connect to the finance team members"""
        finance_roles = ["controller", "vp_fp_and_a", "treasurer"]

        for role in finance_roles:
            try:
                remote_agent = RemoteAgent(role)
                self.finance_team[role] = remote_agent
                print(f"Connected to {role}")
            except Exception as e:
                print(f"Could not connect to {role}: {e}")

    def delegate_to_controller(self, task: str):
        """Delegate accounting tasks to Controller"""
        if "controller" in self.finance_team:
            return self.finance_team["controller"].send_message(task)
        else:
            return {"error": "Controller not connected"}

    def delegate_to_fp_and_a(self, task: str):
        """Delegate FP&A tasks"""
        if "vp_fp_and_a" in self.finance_team:
            return self.finance_team["vp_fp_and_a"].send_message(task)
        else:
            return {"error": "VP FP&A not connected"}


# Create the agent instance
agent = CFOAgent()


if __name__ == "__main__":
    print(f"CFO Agent: {agent}")
    print(f"Agent Card: {agent.get_agent_card()}")
