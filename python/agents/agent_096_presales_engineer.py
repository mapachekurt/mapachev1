"""
Agent 096: Presales Engineer
Role: Presales Engineer - Technical Sales Support
Tier: Sales Operations
"""


class PresalesEngineerAgent:
    """
    Presales Engineer Agent - Technical sales support and demonstrations
    Manages technical sales activities, product demos, and proof of concepts
    """

    def __init__(self):
        self.agent_id = "agent_096"
        self.role = "Presales Engineer"
        self.tier = "Sales Operations"
        self.department = "Marketing & Sales Support"
        self.responsibilities = [
            "Product demonstrations and presentations",
            "Technical discovery and requirements gathering",
            "Proof of concept design and execution",
            "Technical proposal development",
            "Customer technical objection handling",
            "Solution architecture and design",
            "RFP technical response coordination",
            "Sales team technical enablement"
        ]
        self.integrations = [
            "Salesforce CRM",
            "Demo platform tools",
            "Zoom",
            "Slack"
        ]

    def execute(self, task=None):
        """
        Execute presales engineering tasks
        """
        if task:
            return f"Presales Engineer executing: {task}"
        return "Presales Engineer standing by for technical sales support directives"

    def conduct_product_demo(self):
        """
        Conduct product demonstrations for prospects
        """
        return "Conducting technical product demonstrations"

    def design_proof_of_concept(self):
        """
        Design and execute proof of concept projects
        """
        return "Designing and executing proof of concept initiatives"

    def provide_technical_support(self):
        """
        Provide technical support to sales team
        """
        return "Providing technical expertise and sales support"
