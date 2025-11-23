"""ProductHunt scraper for AI products."""

import logging
import os
from datetime import datetime
from typing import Any

import requests

from ..utils.models import ContentType, RawContent, SourceType
from .base import BaseScraper

logger = logging.getLogger(__name__)


class ProductHuntScraper(BaseScraper):
    """Scraper for ProductHunt AI products."""

    GRAPHQL_ENDPOINT = "https://api.producthunt.com/v2/api/graphql"

    def __init__(self) -> None:
        """Initialize the ProductHunt scraper."""
        super().__init__("producthunt")
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": self.config.user_agent,
            "Accept": "application/json",
        })
        self._authenticate()

    def _authenticate(self) -> None:
        """Set up ProductHunt API authentication."""
        # Get API token from environment (Secret Manager in production)
        api_token = os.environ.get("PRODUCTHUNT_API_TOKEN", "")

        if api_token:
            self.session.headers.update({"Authorization": f"Bearer {api_token}"})
            logger.info("Authenticated with ProductHunt")
        else:
            logger.warning("ProductHunt API token not found")

    def get_today_posts(self) -> list[dict[str, Any]]:
        """Get today's posts from ProductHunt.

        Returns:
            List of post data
        """
        # GraphQL query for today's posts
        query = """
        query {
          posts {
            edges {
              node {
                id
                name
                tagline
                description
                url
                votesCount
                commentsCount
                topics {
                  edges {
                    node {
                      name
                    }
                  }
                }
              }
            }
          }
        }
        """

        try:
            response = self.session.post(
                self.GRAPHQL_ENDPOINT,
                json={"query": query},
                timeout=self.config.timeout,
            )
            response.raise_for_status()
            data = response.json()
            return [edge["node"] for edge in data["data"]["posts"]["edges"]]
        except Exception as e:
            logger.error(f"Error fetching ProductHunt posts: {e}")
            return []

    def is_ai_product(self, post: dict[str, Any]) -> bool:
        """Check if product is AI-related.

        Args:
            post: Post data

        Returns:
            True if AI-related
        """
        # Extract topics
        topics = [
            edge["node"]["name"].lower()
            for edge in post.get("topics", {}).get("edges", [])
        ]

        # Check for AI-related topics
        ai_topics = ["ai", "artificial-intelligence", "machine-learning", "chatgpt", "llm"]
        if any(topic in topics for topic in ai_topics):
            return True

        # Check text content
        text = f"{post.get('name', '')} {post.get('tagline', '')} {post.get('description', '')}".lower()
        ai_keywords = ["ai", "artificial intelligence", "machine learning", "llm", "gpt", "claude", "agent"]
        return any(keyword in text for keyword in ai_keywords)

    def scrape(self) -> list[RawContent]:
        """Scrape ProductHunt AI products.

        Returns:
            List of raw content items
        """
        logger.info("Scraping ProductHunt for AI products...")

        raw_contents: list[RawContent] = []

        try:
            posts = self.get_today_posts()

            for post in posts:
                # Filter AI products
                if not self.is_ai_product(post):
                    continue

                # Extract post details
                title = post.get("name", "Untitled")
                url = post.get("url", "")
                tagline = post.get("tagline", "")
                description = post.get("description", "")
                votes_count = post.get("votesCount", 0)
                comments_count = post.get("commentsCount", 0)

                # Combine tagline and description
                content = f"{tagline}\n\n{description}" if description else tagline

                # Create raw content
                raw_content = RawContent(
                    source=SourceType.PRODUCTHUNT,
                    content_type=ContentType.PRODUCT_LAUNCH,
                    title=title,
                    url=url,
                    content=content,
                    metadata={
                        "product_id": post.get("id", ""),
                        "votes_count": votes_count,
                        "comments_count": comments_count,
                        "topics": [
                            edge["node"]["name"]
                            for edge in post.get("topics", {}).get("edges", [])
                        ],
                    },
                    scraped_at=datetime.utcnow(),
                )

                raw_contents.append(raw_content)

            logger.info(f"Scraped {len(raw_contents)} AI products from ProductHunt")
        except Exception as e:
            logger.error(f"Error scraping ProductHunt: {e}", exc_info=True)

        return raw_contents


def main() -> None:
    """Main entry point for Cloud Run Job."""
    logging.basicConfig(level=logging.INFO)

    scraper = ProductHuntScraper()
    result = scraper.run()

    logger.info(f"Scraper result: {result}")


if __name__ == "__main__":
    main()
