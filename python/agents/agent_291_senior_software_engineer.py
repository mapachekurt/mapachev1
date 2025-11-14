"""
Agent 291: Senior Software Engineer
Role: Senior Software Engineer
Tier: Individual Contributor
"""


class SeniorSoftwareEngineerAgent:
    """
    Senior Software Engineer Agent - Advanced software development
    Performs complex software development and technical leadership
    """

    def __init__(self):
        self.agent_id = "agent_291"
        self.role = "Senior Software Engineer"
        self.tier = "Individual Contributor"
        self.department = "Product & Engineering"
        self.responsibilities = [
            "Complex feature development",
            "Technical design and architecture",
            "Code review and mentorship",
            "Performance optimization",
            "Technical debt reduction",
            "Cross-team collaboration",
            "Best practices advocacy",
            "System troubleshooting"
        ]
        self.integrations = [
            "GitHub",
            "GitLab",
            "JIRA",
            "VS Code",
            "IntelliJ",
            "Docker",
            "Jenkins",
            "SonarQube"
        ]

    def execute(self, task=None):
        """
        Execute senior software engineer tasks
        """
        if task:
            return f"Senior Software Engineer executing: {task}"
        return "Senior Software Engineer developing and mentoring"

    def develop_complex_features(self):
        """
        Develop complex features and systems
        """
        return "Developing complex features and technical solutions"

    def conduct_code_reviews(self):
        """
        Conduct code reviews and mentor engineers
        """
        return "Conducting code reviews and mentoring team members"

    def design_technical_solutions(self):
        """
        Design technical solutions and architecture
        """
        return "Designing technical solutions and system architecture"
