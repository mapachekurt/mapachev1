"""Cloud Function entry point for content analysis."""

import base64
import json
import logging
from typing import Any

import functions_framework
from cloudevents.http import CloudEvent

from .gemini_analyzer import analyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@functions_framework.cloud_event
def analyze_content(cloud_event: CloudEvent) -> None:
    """Cloud Function triggered by Pub/Sub to analyze content.

    Args:
        cloud_event: CloudEvent containing Pub/Sub message
    """
    try:
        # Decode Pub/Sub message
        message_data = base64.b64decode(cloud_event.data["message"]["data"]).decode()
        content = json.loads(message_data)

        logger.info(f"Processing content: {content.get('title', 'Untitled')[:50]}...")

        # Process with Gemini analyzer
        result = analyzer.process_message(content)

        logger.info(f"Processing result: {result}")

    except Exception as e:
        logger.error(f"Error in Cloud Function: {e}", exc_info=True)
        raise
