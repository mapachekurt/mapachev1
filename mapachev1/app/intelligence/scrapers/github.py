"""GitHub scraper for releases and repository activity."""

import logging
import os
from datetime import datetime
from typing import Any

import requests

from ..utils.models import ContentType, RawContent, SourceType
from .base import BaseScraper

logger = logging.getLogger(__name__)


class GitHubScraper(BaseScraper):
    """Scraper for GitHub releases and activity."""

    # Key repositories to monitor
    REPOSITORIES = [
        "google/generative-ai-python",
        "anthropics/anthropic-sdk-python",
        "openai/openai-python",
        "langchain-ai/langchain",
        "run-llama/llama_index",
        "microsoft/autogen",
        "stanfordnlp/dspy",
        "crewAIInc/crewAI",
    ]

    def __init__(self) -> None:
        """Initialize the GitHub scraper."""
        super().__init__("github")
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": self.config.user_agent,
            "Accept": "application/vnd.github+json",
        })
        self._authenticate()

    def _authenticate(self) -> None:
        """Set up GitHub API authentication."""
        # Get GitHub token from environment (Secret Manager in production)
        github_token = os.environ.get("GITHUB_TOKEN", "")

        if github_token:
            self.session.headers.update({"Authorization": f"Bearer {github_token}"})
            logger.info("Authenticated with GitHub")
        else:
            logger.warning("GitHub token not found. Rate limits will apply.")

    def get_latest_releases(self, repo: str, limit: int = 5) -> list[dict[str, Any]]:
        """Get latest releases for a repository.

        Args:
            repo: Repository in format owner/repo
            limit: Maximum number of releases

        Returns:
            List of release data
        """
        try:
            url = f"https://api.github.com/repos/{repo}/releases"
            params = {"per_page": limit}

            response = self.session.get(
                url, params=params, timeout=self.config.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching releases for {repo}: {e}")
            return []

    def scrape(self) -> list[RawContent]:
        """Scrape GitHub releases.

        Returns:
            List of raw content items
        """
        logger.info(f"Scraping {len(self.REPOSITORIES)} GitHub repositories...")

        raw_contents: list[RawContent] = []

        for repo in self.REPOSITORIES:
            releases = self.get_latest_releases(repo)

            for release in releases:
                # Extract release details
                title = f"{repo}: {release.get('name', release.get('tag_name', 'Unnamed Release'))}"
                url = release.get("html_url", "")
                body = release.get("body", "")
                tag_name = release.get("tag_name", "")
                published_at = release.get("published_at", "")

                # Create raw content
                raw_content = RawContent(
                    source=SourceType.GITHUB,
                    content_type=ContentType.RELEASE,
                    title=title,
                    url=url,
                    content=body or f"Release {tag_name} for {repo}",
                    metadata={
                        "repository": repo,
                        "tag_name": tag_name,
                        "published_at": published_at,
                        "author": release.get("author", {}).get("login", "unknown"),
                        "prerelease": release.get("prerelease", False),
                        "draft": release.get("draft", False),
                    },
                    scraped_at=datetime.utcnow(),
                )

                raw_contents.append(raw_content)

        logger.info(f"Scraped {len(raw_contents)} releases from GitHub")
        return raw_contents


def main() -> None:
    """Main entry point for Cloud Run Job."""
    logging.basicConfig(level=logging.INFO)

    scraper = GitHubScraper()
    result = scraper.run()

    logger.info(f"Scraper result: {result}")


if __name__ == "__main__":
    main()
