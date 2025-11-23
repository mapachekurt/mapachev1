"""Base scraper class."""

import hashlib
import logging
from abc import ABC, abstractmethod
from typing import Any

from ..utils.config import config
from ..utils.gcs_client import gcs_client
from ..utils.models import RawContent
from ..utils.pubsub_client import publisher

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Base class for all scrapers."""

    def __init__(self, source_name: str) -> None:
        """Initialize the scraper.

        Args:
            source_name: Name of the source (e.g., 'hackernews')
        """
        self.source_name = source_name
        self.config = config.scraper

    @abstractmethod
    def scrape(self) -> list[RawContent]:
        """Scrape content from the source.

        Returns:
            List of raw content items
        """
        pass

    def generate_content_id(self, url: str, title: str) -> str:
        """Generate a unique content ID.

        Args:
            url: Content URL
            title: Content title

        Returns:
            Unique content ID (hash)
        """
        content_string = f"{url}_{title}"
        return hashlib.sha256(content_string.encode()).hexdigest()[:16]

    def process_and_publish(self, raw_content: RawContent) -> None:
        """Process and publish raw content.

        Args:
            raw_content: Raw content item
        """
        try:
            # Generate content ID
            content_id = self.generate_content_id(
                raw_content.url, raw_content.title
            )

            # Convert to dict
            content_dict = raw_content.to_dict()
            content_dict["content_id"] = content_id

            # Store in GCS
            gcs_path = gcs_client.store_raw_content(
                content_dict, self.source_name, content_id
            )
            content_dict["gcs_path"] = gcs_path

            # Publish to Pub/Sub
            publisher.publish_raw_content(content_dict)

            logger.info(
                f"Processed and published content: {raw_content.title[:50]}..."
            )
        except Exception as e:
            logger.error(f"Error processing content: {e}", exc_info=True)

    def run(self) -> dict[str, Any]:
        """Run the scraper.

        Returns:
            Summary statistics
        """
        logger.info(f"Starting {self.source_name} scraper...")

        try:
            # Scrape content
            raw_contents = self.scrape()

            # Process and publish each item
            for content in raw_contents:
                self.process_and_publish(content)

            logger.info(
                f"Completed {self.source_name} scraper. Processed {len(raw_contents)} items."
            )

            return {
                "source": self.source_name,
                "items_scraped": len(raw_contents),
                "status": "success",
            }
        except Exception as e:
            logger.error(f"Error running {self.source_name} scraper: {e}", exc_info=True)
            return {
                "source": self.source_name,
                "items_scraped": 0,
                "status": "error",
                "error": str(e),
            }
