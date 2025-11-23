"""Pub/Sub client utilities."""

import json
import logging
from typing import Any

from google.cloud import pubsub_v1

from .config import config

logger = logging.getLogger(__name__)


class PubSubPublisher:
    """Publisher for Pub/Sub messages."""

    def __init__(self) -> None:
        """Initialize the publisher."""
        self.client = pubsub_v1.PublisherClient()
        self.project_id = config.gcp.project_id

    def publish_raw_content(self, content: dict[str, Any]) -> str:
        """Publish raw content to Pub/Sub.

        Args:
            content: Raw content dictionary

        Returns:
            Message ID
        """
        topic_path = self.client.topic_path(
            self.project_id, config.pubsub.raw_content_topic
        )
        message_data = json.dumps(content).encode("utf-8")

        future = self.client.publish(topic_path, message_data)
        message_id = future.result()

        logger.info(
            f"Published raw content to {config.pubsub.raw_content_topic}: {message_id}"
        )
        return message_id

    def publish_analyzed_content(self, content: dict[str, Any]) -> str:
        """Publish analyzed content to Pub/Sub.

        Args:
            content: Analyzed content dictionary

        Returns:
            Message ID
        """
        topic_path = self.client.topic_path(
            self.project_id, config.pubsub.analyzed_content_topic
        )
        message_data = json.dumps(content).encode("utf-8")

        future = self.client.publish(topic_path, message_data)
        message_id = future.result()

        logger.info(
            f"Published analyzed content to {config.pubsub.analyzed_content_topic}: {message_id}"
        )
        return message_id


# Singleton instance
publisher = PubSubPublisher()
