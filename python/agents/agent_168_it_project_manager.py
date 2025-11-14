"""
Agent 168: IT Project Manager
Role: IT Project Manager - Technology Project Leadership
Tier: IT Management
"""


class ITProjectManagerAgent:
    """
    IT Project Manager Agent - Manages IT projects from initiation to delivery
    Coordinates resources, timelines, and stakeholders for successful project execution
    """

    def __init__(self):
        self.agent_id = "agent_168"
        self.role = "IT Project Manager"
        self.tier = "IT Management"
        self.department = "IT Operations"
        self.responsibilities = [
            "IT project planning and execution",
            "Resource allocation and management",
            "Timeline and milestone tracking",
            "Risk identification and mitigation",
            "Stakeholder communication and reporting",
            "Budget management and forecasting",
            "Change management coordination",
            "Project documentation and governance"
        ]
        self.integrations = [
            "Microsoft Project",
            "JIRA",
            "Asana",
            "Monday.com",
            "Smartsheet",
            "Confluence",
            "MS Teams",
            "Slack",
            "Project portfolio management tools"
        ]

    def execute(self, task=None):
        """
        Execute IT project management tasks
        """
        if task:
            return f"IT Project Manager executing: {task}"
        return "IT Project Manager standing by for project coordination"

    def plan_project_execution(self):
        """
        Develop comprehensive project plans and schedules
        """
        return "Creating detailed project plans with timelines, resources, and deliverables"

    def manage_project_risks(self):
        """
        Identify and mitigate project risks
        """
        return "Identifying potential risks and developing mitigation strategies"

    def coordinate_stakeholders(self):
        """
        Manage stakeholder communication and expectations
        """
        return "Coordinating stakeholder communications and managing expectations"
