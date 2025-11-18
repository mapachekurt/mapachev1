"""Tools for the Chief Agent."""

import json
import logging
import os
from datetime import datetime
from typing import Any

import requests
from google.cloud import firestore

from ..utils.config import config
from ..utils.models import LinearProject

logger = logging.getLogger(__name__)


class LinearTool:
    """Tool for creating Linear projects."""

    def __init__(self) -> None:
        """Initialize the Linear tool."""
        self.api_key = os.environ.get("LINEAR_API_KEY", "")
        self.api_url = "https://api.linear.app/graphql"
        self.team_id = os.environ.get("LINEAR_TEAM_ID", "")

    def create_project(
        self,
        title: str,
        description: str,
        technical_requirements: list[str],
        acceptance_criteria: list[str],
        rollback_plan: str,
        priority: str = "medium",
    ) -> dict[str, Any]:
        """Create a Linear project.

        Args:
            title: Project title
            description: Project description
            technical_requirements: List of technical requirements
            acceptance_criteria: List of acceptance criteria
            rollback_plan: Rollback plan
            priority: Priority (low, medium, high, urgent)

        Returns:
            Created project data
        """
        try:
            # Format full description with all sections
            full_description = f"""# {title}

{description}

## Technical Requirements
{chr(10).join(f'- {req}' for req in technical_requirements)}

## Acceptance Criteria
{chr(10).join(f'- {crit}' for crit in acceptance_criteria)}

## Rollback Plan
{rollback_plan}

## Priority
{priority.upper()}

---
*Created by Mapache Intelligence System*
"""

            # Create Linear issue via GraphQL
            mutation = """
            mutation CreateIssue($title: String!, $description: String!, $teamId: String!, $priority: Int!) {
              issueCreate(input: {
                title: $title
                description: $description
                teamId: $teamId
                priority: $priority
              }) {
                success
                issue {
                  id
                  identifier
                  url
                }
              }
            }
            """

            # Map priority to Linear priority (1-4)
            priority_map = {"low": 4, "medium": 3, "high": 2, "urgent": 1}
            linear_priority = priority_map.get(priority.lower(), 3)

            variables = {
                "title": title,
                "description": full_description,
                "teamId": self.team_id,
                "priority": linear_priority,
            }

            headers = {
                "Authorization": self.api_key,
                "Content-Type": "application/json",
            }

            response = requests.post(
                self.api_url,
                json={"query": mutation, "variables": variables},
                headers=headers,
                timeout=30,
            )

            response.raise_for_status()
            data = response.json()

            if data.get("data", {}).get("issueCreate", {}).get("success"):
                issue = data["data"]["issueCreate"]["issue"]
                logger.info(f"Created Linear project: {issue['identifier']} - {title}")
                return {
                    "success": True,
                    "project_id": issue["id"],
                    "project_identifier": issue["identifier"],
                    "project_url": issue["url"],
                }
            else:
                logger.error(f"Failed to create Linear project: {data}")
                return {"success": False, "error": "Linear API returned failure"}

        except Exception as e:
            logger.error(f"Error creating Linear project: {e}", exc_info=True)
            return {"success": False, "error": str(e)}


class SlackTool:
    """Tool for sending Slack notifications."""

    def __init__(self) -> None:
        """Initialize the Slack tool."""
        self.webhook_url = os.environ.get("SLACK_WEBHOOK_URL", "")

    def send_briefing(
        self,
        date: datetime,
        summary: str,
        top_opportunities: list[dict[str, Any]],
        projects_created: list[dict[str, Any]],
        total_discoveries: int,
        relevant_discoveries: int,
    ) -> dict[str, Any]:
        """Send daily briefing to Slack.

        Args:
            date: Briefing date
            summary: Summary text
            top_opportunities: List of top opportunities
            projects_created: List of created projects
            total_discoveries: Total discoveries count
            relevant_discoveries: Relevant discoveries count

        Returns:
            Result dictionary
        """
        try:
            # Build Slack message
            blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"🧠 Daily Intelligence Briefing - {date.strftime('%Y-%m-%d')}",
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Summary:* {summary}",
                    },
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Total Discoveries:*\n{total_discoveries}",
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Relevant Discoveries:*\n{relevant_discoveries}",
                        },
                    ],
                },
                {"type": "divider"},
            ]

            # Add projects created
            if projects_created:
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*📋 Projects Created:* {len(projects_created)}",
                    },
                })

                for project in projects_created[:5]:
                    blocks.append({
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"• <{project['url']}|{project['identifier']}>: {project['title']}",
                        },
                    })

            # Add top opportunities
            if top_opportunities:
                blocks.append({"type": "divider"})
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*🎯 Top Opportunities:*",
                    },
                })

                for i, opp in enumerate(top_opportunities[:5], 1):
                    blocks.append({
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*{i}. {opp['title']}*\n{opp['description']}\nRelevance: {opp['relevance_score']}/100",
                        },
                    })

            # Send to Slack
            response = requests.post(
                self.webhook_url,
                json={"blocks": blocks},
                timeout=30,
            )

            response.raise_for_status()

            logger.info("Sent daily briefing to Slack")
            return {"success": True}

        except Exception as e:
            logger.error(f"Error sending Slack notification: {e}", exc_info=True)
            return {"success": False, "error": str(e)}


# Singleton instances
linear_tool = LinearTool()
slack_tool = SlackTool()
