"""
Agent 303: Technical Product Manager
Role: Technical Product Manager - Technical Product Strategy
Tier: Product Leadership
"""


class TechnicalProductManagerAgent:
    """
    Technical Product Manager Agent - Technical product leadership
    Manages technical products, APIs, and platform capabilities
    """

    def __init__(self):
        self.agent_id = "agent_303"
        self.role = "Technical Product Manager"
        self.tier = "Product Leadership"
        self.department = "Product & Engineering"
        self.responsibilities = [
            "Technical product roadmap development",
            "API and platform product management",
            "Technical requirements and specifications",
            "Architecture and design collaboration",
            "Developer experience optimization",
            "Technical debt prioritization",
            "Integration and compatibility planning",
            "Technical documentation strategy"
        ]
        self.integrations = [
            "Jira",
            "Confluence",
            "GitHub",
            "Postman"
        ]

    def execute(self, task=None):
        """
        Execute technical product management tasks
        """
        if task:
            return f"Technical Product Manager executing: {task}"
        return "Technical Product Manager standing by for technical product directives"

    def manage_technical_roadmap(self):
        """
        Manage technical product roadmap and priorities
        """
        return "Managing technical product roadmap and platform strategy"

    def define_technical_specs(self):
        """
        Define technical specifications and requirements
        """
        return "Defining technical specifications and API contracts"

    def optimize_developer_experience(self):
        """
        Optimize developer experience and tooling
        """
        return "Optimizing developer experience and platform usability"
