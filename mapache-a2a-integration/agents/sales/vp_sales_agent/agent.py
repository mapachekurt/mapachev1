"""
VP Sales Agent

This agent manages the sales organization.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from agents.core import BaseA2AAgent, AgentConfig, RemoteAgent


class VPSalesAgent(BaseA2AAgent):
    """
    VP Sales Agent - Manages sales organization
    """

    def __init__(self):
        """Initialize the VP Sales agent"""
        config = AgentConfig(
            name="vp_sales",
            description="VP of Sales responsible for revenue generation and sales team management",
            role="VP of Sales",
            department="sales",
            skills=[
                "sales_leadership",
                "revenue_management",
                "sales_strategy",
                "team_building",
                "forecasting",
            ],
            tools=[],
            reports_to="ceo",
            manages=["sales_director_1", "sales_director_2", "sales_director_3"],
            model="gemini-2.0-flash-exp",
            tags=["sales", "leadership", "revenue"],
        )

        super().__init__(config)

        self.sales_team = {}

    def connect_to_sales_team(self):
        """Connect to the sales team"""
        sales_roles = ["sales_director_1", "sales_director_2", "sales_director_3", "director_sales_ops"]

        for role in sales_roles:
            try:
                remote_agent = RemoteAgent(role)
                self.sales_team[role] = remote_agent
                print(f"Connected to {role}")
            except Exception as e:
                print(f"Could not connect to {role}: {e}")


# Create the agent instance
agent = VPSalesAgent()


if __name__ == "__main__":
    print(f"VP Sales Agent: {agent}")
