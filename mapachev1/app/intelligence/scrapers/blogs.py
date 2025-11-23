"""Blog scraper for AI/ML company blogs."""

import logging
from datetime import datetime
from typing import Any

import feedparser
import requests

from ..utils.models import ContentType, RawContent, SourceType
from .base import BaseScraper

logger = logging.getLogger(__name__)


class BlogScraper(BaseScraper):
    """Scraper for AI/ML company blogs."""

    BLOG_FEEDS = {
        "google_cloud": "https://cloud.google.com/blog/products/ai-machine-learning/rss",
        "anthropic": "https://www.anthropic.com/news/rss.xml",
        "openai": "https://openai.com/blog/rss.xml",
        "langchain": "https://blog.langchain.dev/rss/",
        "huggingface": "https://huggingface.co/blog/feed.xml",
        "deepmind": "https://www.deepmind.com/blog/rss.xml",
    }

    def __init__(self) -> None:
        """Initialize the Blog scraper."""
        super().__init__("blog")

    def fetch_feed(self, feed_url: str, blog_name: str) -> list[dict[str, Any]]:
        """Fetch and parse RSS feed.

        Args:
            feed_url: RSS feed URL
            blog_name: Blog name

        Returns:
            List of entries
        """
        try:
            feed = feedparser.parse(feed_url)
            entries = []

            for entry in feed.entries[:10]:  # Last 10 entries
                entries.append({
                    "blog_name": blog_name,
                    "title": entry.get("title", "Untitled"),
                    "link": entry.get("link", ""),
                    "summary": entry.get("summary", ""),
                    "published": entry.get("published", ""),
                    "published_parsed": entry.get("published_parsed", None),
                })

            return entries
        except Exception as e:
            logger.error(f"Error fetching {blog_name} feed: {e}")
            return []

    def scrape(self) -> list[RawContent]:
        """Scrape AI/ML blog posts.

        Returns:
            List of raw content items
        """
        logger.info(f"Scraping {len(self.BLOG_FEEDS)} AI/ML blogs...")

        raw_contents: list[RawContent] = []

        for blog_name, feed_url in self.BLOG_FEEDS.items():
            entries = self.fetch_feed(feed_url, blog_name)

            for entry in entries:
                # Create raw content
                raw_content = RawContent(
                    source=SourceType.BLOG,
                    content_type=ContentType.ARTICLE,
                    title=entry["title"],
                    url=entry["link"],
                    content=entry["summary"],
                    metadata={
                        "blog_name": blog_name,
                        "published": entry.get("published", ""),
                        "published_parsed": str(entry.get("published_parsed", "")),
                    },
                    scraped_at=datetime.utcnow(),
                )

                raw_contents.append(raw_content)

        logger.info(f"Scraped {len(raw_contents)} blog posts")
        return raw_contents


def main() -> None:
    """Main entry point for Cloud Run Job."""
    logging.basicConfig(level=logging.INFO)

    scraper = BlogScraper()
    result = scraper.run()

    logger.info(f"Scraper result: {result}")


if __name__ == "__main__":
    main()
