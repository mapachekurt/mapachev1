"""
Agent 098: Inside Sales Rep
Role: Inside Sales Rep - Remote Sales Execution
Tier: Sales Operations
"""


class InsideSalesRepAgent:
    """
    Inside Sales Rep Agent - Remote sales and pipeline development
    Manages inside sales activities, prospecting, and deal closure
    """

    def __init__(self):
        self.agent_id = "agent_098"
        self.role = "Inside Sales Rep"
        self.tier = "Sales Operations"
        self.department = "Marketing & Sales Support"
        self.responsibilities = [
            "Inbound lead qualification and follow-up",
            "Outbound prospecting and cold calling",
            "Sales pipeline development and management",
            "Product demonstrations and presentations",
            "Proposal development and negotiation",
            "Deal closure and contract execution",
            "CRM data hygiene and activity tracking",
            "Sales quota attainment and forecasting"
        ]
        self.integrations = [
            "Salesforce CRM",
            "Outreach",
            "ZoomInfo",
            "LinkedIn Sales Navigator"
        ]

    def execute(self, task=None):
        """
        Execute inside sales tasks
        """
        if task:
            return f"Inside Sales Rep executing: {task}"
        return "Inside Sales Rep standing by for sales execution directives"

    def qualify_leads(self):
        """
        Qualify and nurture sales leads
        """
        return "Qualifying inbound leads and developing opportunities"

    def prospect_accounts(self):
        """
        Prospect new accounts and generate pipeline
        """
        return "Prospecting target accounts and generating pipeline"

    def close_deals(self):
        """
        Close sales opportunities and manage contracts
        """
        return "Closing sales deals and executing contracts"
