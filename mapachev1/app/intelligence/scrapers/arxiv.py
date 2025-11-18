"""ArXiv scraper for AI/ML research papers."""

import logging
from datetime import datetime, timedelta
from typing import Any

import feedparser

from ..utils.models import ContentType, RawContent, SourceType
from .base import BaseScraper

logger = logging.getLogger(__name__)


class ArXivScraper(BaseScraper):
    """Scraper for ArXiv AI/ML papers."""

    BASE_URL = "http://export.arxiv.org/api/query"

    CATEGORIES = [
        "cs.AI",  # Artificial Intelligence
        "cs.CL",  # Computation and Language
        "cs.LG",  # Machine Learning
        "cs.NE",  # Neural and Evolutionary Computing
        "stat.ML",  # Machine Learning (Statistics)
    ]

    def __init__(self) -> None:
        """Initialize the ArXiv scraper."""
        super().__init__("arxiv")

    def search_category(
        self, category: str, max_results: int = 20
    ) -> list[dict[str, Any]]:
        """Search ArXiv for papers in a category.

        Args:
            category: ArXiv category
            max_results: Maximum number of results

        Returns:
            List of paper entries
        """
        try:
            # Search for recent papers (last 7 days)
            query = f"cat:{category}"
            params = {
                "search_query": query,
                "sortBy": "submittedDate",
                "sortOrder": "descending",
                "max_results": max_results,
            }

            # Build URL
            param_str = "&".join(f"{k}={v}" for k, v in params.items())
            url = f"{self.BASE_URL}?{param_str}"

            # Fetch and parse feed
            feed = feedparser.parse(url)

            entries = []
            for entry in feed.entries:
                # Check if paper is recent (last 7 days)
                published_parsed = entry.get("published_parsed")
                if published_parsed:
                    published_date = datetime(*published_parsed[:6])
                    if datetime.utcnow() - published_date > timedelta(days=7):
                        continue

                entries.append({
                    "title": entry.get("title", "").replace("\n", " "),
                    "link": entry.get("link", ""),
                    "summary": entry.get("summary", "").replace("\n", " "),
                    "published": entry.get("published", ""),
                    "authors": [
                        author.get("name", "") for author in entry.get("authors", [])
                    ],
                    "categories": [
                        tag.get("term", "") for tag in entry.get("tags", [])
                    ],
                    "pdf_link": entry.get("link", "").replace("/abs/", "/pdf/"),
                })

            return entries
        except Exception as e:
            logger.error(f"Error searching ArXiv category {category}: {e}")
            return []

    def scrape(self) -> list[RawContent]:
        """Scrape ArXiv AI/ML papers.

        Returns:
            List of raw content items
        """
        logger.info(f"Scraping ArXiv for {len(self.CATEGORIES)} categories...")

        raw_contents: list[RawContent] = []

        for category in self.CATEGORIES:
            entries = self.search_category(category)

            for entry in entries:
                # Create raw content
                raw_content = RawContent(
                    source=SourceType.ARXIV,
                    content_type=ContentType.RESEARCH_PAPER,
                    title=entry["title"],
                    url=entry["link"],
                    content=entry["summary"],
                    metadata={
                        "authors": entry["authors"],
                        "categories": entry["categories"],
                        "published": entry["published"],
                        "pdf_link": entry["pdf_link"],
                    },
                    scraped_at=datetime.utcnow(),
                )

                raw_contents.append(raw_content)

        logger.info(f"Scraped {len(raw_contents)} papers from ArXiv")
        return raw_contents


def main() -> None:
    """Main entry point for Cloud Run Job."""
    logging.basicConfig(level=logging.INFO)

    scraper = ArXivScraper()
    result = scraper.run()

    logger.info(f"Scraper result: {result}")


if __name__ == "__main__":
    main()
