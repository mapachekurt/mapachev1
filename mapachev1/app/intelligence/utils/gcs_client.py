"""Google Cloud Storage client utilities."""

import json
import logging
from datetime import datetime
from typing import Any

from google.cloud import storage

from .config import config

logger = logging.getLogger(__name__)


class GCSClient:
    """Client for Google Cloud Storage operations."""

    def __init__(self, bucket_name: str = "mapache-intelligence-raw-content") -> None:
        """Initialize the GCS client.

        Args:
            bucket_name: Name of the GCS bucket
        """
        self.client = storage.Client(project=config.gcp.project_id)
        self.bucket_name = bucket_name
        self.bucket = self.client.bucket(bucket_name)

    def store_raw_content(
        self, content: dict[str, Any], source: str, content_id: str
    ) -> str:
        """Store raw content in GCS.

        Args:
            content: Content dictionary
            source: Source type (e.g., 'hackernews', 'reddit')
            content_id: Unique content identifier

        Returns:
            GCS object path
        """
        # Create path: source/YYYY/MM/DD/content_id.json
        now = datetime.utcnow()
        blob_path = (
            f"{source}/{now.year}/{now.month:02d}/{now.day:02d}/{content_id}.json"
        )

        blob = self.bucket.blob(blob_path)
        blob.upload_from_string(
            json.dumps(content, indent=2), content_type="application/json"
        )

        logger.info(f"Stored raw content in GCS: gs://{self.bucket_name}/{blob_path}")
        return f"gs://{self.bucket_name}/{blob_path}"

    def retrieve_raw_content(self, blob_path: str) -> dict[str, Any]:
        """Retrieve raw content from GCS.

        Args:
            blob_path: GCS blob path (without gs://bucket/ prefix)

        Returns:
            Content dictionary
        """
        blob = self.bucket.blob(blob_path)
        content = blob.download_as_text()
        return json.loads(content)


# Singleton instance
gcs_client = GCSClient()
