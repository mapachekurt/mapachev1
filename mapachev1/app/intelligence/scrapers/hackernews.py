"""HackerNews scraper."""

import logging
from datetime import datetime
from typing import Any

import requests

from ..utils.models import ContentType, RawContent, SourceType
from .base import BaseScraper

logger = logging.getLogger(__name__)


class HackerNewsScraper(BaseScraper):
    """Scraper for HackerNews top stories."""

    BASE_URL = "https://hacker-news.firebaseio.com/v0"

    def __init__(self) -> None:
        """Initialize the HackerNews scraper."""
        super().__init__("hackernews")
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.config.user_agent})

    def get_top_stories(self, limit: int = 30) -> list[int]:
        """Get top story IDs.

        Args:
            limit: Maximum number of stories to fetch

        Returns:
            List of story IDs
        """
        url = f"{self.BASE_URL}/topstories.json"
        response = self.session.get(url, timeout=self.config.timeout)
        response.raise_for_status()
        return response.json()[:limit]

    def get_story(self, story_id: int) -> dict[str, Any] | None:
        """Get story details.

        Args:
            story_id: Story ID

        Returns:
            Story data or None if error
        """
        try:
            url = f"{self.BASE_URL}/item/{story_id}.json"
            response = self.session.get(url, timeout=self.config.timeout)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching story {story_id}: {e}")
            return None

    def is_ai_related(self, story: dict[str, Any]) -> bool:
        """Check if story is AI/ML related (simple keyword filtering).

        Args:
            story: Story data

        Returns:
            True if AI-related
        """
        ai_keywords = [
            "ai",
            "artificial intelligence",
            "machine learning",
            "ml",
            "llm",
            "gpt",
            "claude",
            "gemini",
            "neural",
            "deep learning",
            "transformer",
            "openai",
            "anthropic",
            "agent",
            "rag",
            "embedding",
            "vector",
            "langchain",
            "llamaindex",
        ]

        title = story.get("title", "").lower()
        text = story.get("text", "").lower()

        combined_text = f"{title} {text}"
        return any(keyword in combined_text for keyword in ai_keywords)

    def scrape(self) -> list[RawContent]:
        """Scrape HackerNews top stories.

        Returns:
            List of raw content items
        """
        logger.info("Scraping HackerNews top stories...")

        raw_contents: list[RawContent] = []

        try:
            # Get top stories
            story_ids = self.get_top_stories(limit=50)  # Fetch more, filter later

            for story_id in story_ids:
                story = self.get_story(story_id)
                if not story:
                    continue

                # Filter AI-related stories
                if not self.is_ai_related(story):
                    continue

                # Extract story details
                title = story.get("title", "Untitled")
                url = story.get("url") or f"https://news.ycombinator.com/item?id={story_id}"
                text = story.get("text", "")
                score = story.get("score", 0)
                num_comments = story.get("descendants", 0)

                # Create raw content
                raw_content = RawContent(
                    source=SourceType.HACKERNEWS,
                    content_type=ContentType.DISCUSSION,
                    title=title,
                    url=url,
                    content=text or f"HackerNews discussion: {title}",
                    metadata={
                        "story_id": story_id,
                        "score": score,
                        "num_comments": num_comments,
                        "by": story.get("by", "unknown"),
                        "time": story.get("time", 0),
                    },
                    scraped_at=datetime.utcnow(),
                )

                raw_contents.append(raw_content)

            logger.info(f"Scraped {len(raw_contents)} AI-related stories from HackerNews")
        except Exception as e:
            logger.error(f"Error scraping HackerNews: {e}", exc_info=True)

        return raw_contents


def main() -> None:
    """Main entry point for Cloud Run Job."""
    logging.basicConfig(level=logging.INFO)

    scraper = HackerNewsScraper()
    result = scraper.run()

    logger.info(f"Scraper result: {result}")


if __name__ == "__main__":
    main()
