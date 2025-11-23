"""Data models for the intelligence system."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class SourceType(str, Enum):
    """Content source types."""

    HACKERNEWS = "hackernews"
    REDDIT = "reddit"
    PRODUCTHUNT = "producthunt"
    BLOG = "blog"
    ARXIV = "arxiv"
    GITHUB = "github"
    CHANGELOG = "changelog"


class ContentType(str, Enum):
    """Content types."""

    ARTICLE = "article"
    DISCUSSION = "discussion"
    RESEARCH_PAPER = "research_paper"
    PRODUCT_LAUNCH = "product_launch"
    RELEASE = "release"
    CHANGELOG_ENTRY = "changelog"


@dataclass
class RawContent:
    """Raw scraped content before analysis."""

    source: SourceType
    content_type: ContentType
    title: str
    url: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    scraped_at: datetime = field(default_factory=datetime.utcnow)
    scraper_version: str = "1.0.0"

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "source": self.source.value,
            "content_type": self.content_type.value,
            "title": self.title,
            "url": self.url,
            "content": self.content,
            "metadata": self.metadata,
            "scraped_at": self.scraped_at.isoformat(),
            "scraper_version": self.scraper_version,
        }


@dataclass
class AnalyzedContent:
    """Content after AI analysis."""

    raw_content: RawContent
    relevance_score: int  # 0-100
    strategic_value: str
    key_insights: list[str]
    action_items: list[str]
    tags: list[str]
    embedding: Optional[list[float]] = None
    analyzed_at: datetime = field(default_factory=datetime.utcnow)
    analyzer_model: str = "gemini-2.0-flash-exp"

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for Firestore."""
        return {
            "source": self.raw_content.source.value,
            "content_type": self.raw_content.content_type.value,
            "title": self.raw_content.title,
            "url": self.raw_content.url,
            "content": self.raw_content.content,
            "metadata": self.raw_content.metadata,
            "scraped_at": self.raw_content.scraped_at.isoformat(),
            "relevance_score": self.relevance_score,
            "strategic_value": self.strategic_value,
            "key_insights": self.key_insights,
            "action_items": self.action_items,
            "tags": self.tags,
            "analyzed_at": self.analyzed_at.isoformat(),
            "analyzer_model": self.analyzer_model,
        }


@dataclass
class LinearProject:
    """Linear project specification."""

    title: str
    description: str
    technical_requirements: list[str]
    acceptance_criteria: list[str]
    rollback_plan: str
    assignee: Optional[str] = None  # "Claude Code" or "Google Jules"
    priority: str = "medium"  # low, medium, high, urgent
    source_discovery_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for Linear API."""
        return {
            "title": self.title,
            "description": self.description,
            "technical_requirements": self.technical_requirements,
            "acceptance_criteria": self.acceptance_criteria,
            "rollback_plan": self.rollback_plan,
            "assignee": self.assignee,
            "priority": self.priority,
            "source_discovery_id": self.source_discovery_id,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class DailyBriefing:
    """Daily intelligence briefing."""

    date: datetime
    top_opportunities: list[dict[str, Any]]
    projects_created: list[str]  # Linear project IDs
    summary: str
    total_discoveries: int
    relevant_discoveries: int

    def to_slack_message(self) -> dict[str, Any]:
        """Convert to Slack message format."""
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"🧠 Daily Intelligence Briefing - {self.date.strftime('%Y-%m-%d')}",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Summary:* {self.summary}",
                },
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Total Discoveries:*\n{self.total_discoveries}",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Relevant Discoveries:*\n{self.relevant_discoveries}",
                    },
                ],
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Projects Created:* {len(self.projects_created)}",
                },
            },
        ]

        # Add top opportunities
        if self.top_opportunities:
            blocks.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*🎯 Top Opportunities:*",
                    },
                }
            )
            for i, opp in enumerate(self.top_opportunities[:5], 1):
                blocks.append(
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*{i}. {opp.get('title', 'Untitled')}*\n{opp.get('description', '')}",
                        },
                    }
                )

        return {"blocks": blocks}
