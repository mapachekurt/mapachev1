"""Configuration management for the intelligence system."""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class GCPConfig:
    """Google Cloud Platform configuration."""

    project_id: str
    region: str = "europe-west1"
    location: str = "europe-west1"

    @classmethod
    def from_env(cls) -> "GCPConfig":
        """Load configuration from environment variables."""
        project_id = os.environ.get("GCP_PROJECT_ID", "mapache-intelligence-prod")
        region = os.environ.get("GCP_REGION", "europe-west1")
        return cls(project_id=project_id, region=region, location=region)


@dataclass
class PubSubConfig:
    """Pub/Sub topic configuration."""

    raw_content_topic: str = "intelligence-raw-content"
    analyzed_content_topic: str = "intelligence-analyzed-content"
    dead_letter_topic: str = "intelligence-dead-letter"


@dataclass
class FirestoreConfig:
    """Firestore collection configuration."""

    discoveries_collection: str = "discoveries"
    projects_collection: str = "linear_projects"
    metadata_collection: str = "scraper_metadata"


@dataclass
class VectorSearchConfig:
    """Vector Search configuration."""

    index_endpoint: str = "intelligence-vector-index"
    embedding_model: str = "text-embedding-004"
    dimensions: int = 768
    distance_measure: str = "DOT_PRODUCT_DISTANCE"


@dataclass
class GeminiConfig:
    """Gemini AI configuration."""

    model: str = "gemini-2.0-flash-exp"
    temperature: float = 0.7
    max_tokens: int = 2048
    relevance_threshold: int = 60  # Minimum relevance score for storage
    project_threshold: int = 70  # Minimum relevance score for project creation


@dataclass
class ScraperConfig:
    """Scraper configuration."""

    timeout: int = 30
    retry_attempts: int = 3
    user_agent: str = "MapacheIntelligenceBot/1.0"


@dataclass
class IntelligenceConfig:
    """Main configuration for the intelligence system."""

    gcp: GCPConfig
    pubsub: PubSubConfig
    firestore: FirestoreConfig
    vector_search: VectorSearchConfig
    gemini: GeminiConfig
    scraper: ScraperConfig

    @classmethod
    def load(cls) -> "IntelligenceConfig":
        """Load complete configuration."""
        return cls(
            gcp=GCPConfig.from_env(),
            pubsub=PubSubConfig(),
            firestore=FirestoreConfig(),
            vector_search=VectorSearchConfig(),
            gemini=GeminiConfig(),
            scraper=ScraperConfig(),
        )


# Global config instance
config = IntelligenceConfig.load()
