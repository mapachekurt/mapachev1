"""Gemini-powered content analyzer."""

import json
import logging
from datetime import datetime
from typing import Any

import vertexai
from google.cloud import firestore
from vertexai.generative_models import GenerativeModel, GenerationConfig

from ..utils.config import config
from ..utils.models import AnalyzedContent, RawContent, SourceType

logger = logging.getLogger(__name__)


class GeminiAnalyzer:
    """Analyzer using Gemini 2.0 Flash for content analysis."""

    ANALYSIS_PROMPT = """You are an AI strategic analyst for Mapache, a company building AI agents and automation solutions.

Analyze the following content and provide:
1. Relevance Score (0-100): How relevant is this to Mapache's business?
   - 0-30: Not relevant
   - 31-60: Somewhat relevant
   - 61-80: Highly relevant
   - 81-100: Critical/game-changing

2. Strategic Value: What strategic value does this offer? (1-2 sentences)

3. Key Insights: 2-4 bullet points of key insights

4. Action Items: 2-3 concrete action items Mapache should consider

5. Tags: 3-5 relevant tags for categorization

Content to analyze:
Title: {title}
Source: {source}
Content: {content}

Respond in JSON format:
{{
  "relevance_score": <number>,
  "strategic_value": "<string>",
  "key_insights": ["<string>", ...],
  "action_items": ["<string>", ...],
  "tags": ["<string>", ...]
}}
"""

    def __init__(self) -> None:
        """Initialize the Gemini analyzer."""
        # Initialize Vertex AI
        vertexai.init(
            project=config.gcp.project_id,
            location=config.gcp.location,
        )

        # Initialize Gemini model
        self.model = GenerativeModel(config.gemini.model)

        # Initialize Firestore
        self.db = firestore.Client(project=config.gcp.project_id)

    def analyze_content(self, raw_content: dict[str, Any]) -> AnalyzedContent | None:
        """Analyze raw content with Gemini.

        Args:
            raw_content: Raw content dictionary

        Returns:
            AnalyzedContent or None if analysis fails
        """
        try:
            # Format prompt
            prompt = self.ANALYSIS_PROMPT.format(
                title=raw_content.get("title", ""),
                source=raw_content.get("source", ""),
                content=raw_content.get("content", "")[:2000],  # Truncate long content
            )

            # Generate analysis
            generation_config = GenerationConfig(
                temperature=config.gemini.temperature,
                max_output_tokens=config.gemini.max_tokens,
            )

            response = self.model.generate_content(
                prompt,
                generation_config=generation_config,
            )

            # Parse JSON response
            response_text = response.text.strip()
            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            analysis = json.loads(response_text.strip())

            # Reconstruct RawContent
            raw_obj = RawContent(
                source=SourceType(raw_content["source"]),
                content_type=raw_content["content_type"],
                title=raw_content["title"],
                url=raw_content["url"],
                content=raw_content["content"],
                metadata=raw_content.get("metadata", {}),
                scraped_at=datetime.fromisoformat(raw_content["scraped_at"]),
                scraper_version=raw_content.get("scraper_version", "1.0.0"),
            )

            # Create AnalyzedContent
            analyzed = AnalyzedContent(
                raw_content=raw_obj,
                relevance_score=analysis["relevance_score"],
                strategic_value=analysis["strategic_value"],
                key_insights=analysis["key_insights"],
                action_items=analysis["action_items"],
                tags=analysis["tags"],
                analyzed_at=datetime.utcnow(),
                analyzer_model=config.gemini.model,
            )

            logger.info(
                f"Analyzed content: {raw_content['title'][:50]}... "
                f"(relevance: {analysis['relevance_score']})"
            )

            return analyzed

        except Exception as e:
            logger.error(f"Error analyzing content: {e}", exc_info=True)
            return None

    def store_in_firestore(self, analyzed: AnalyzedContent) -> str:
        """Store analyzed content in Firestore.

        Args:
            analyzed: Analyzed content

        Returns:
            Document ID
        """
        try:
            # Only store if above relevance threshold
            if analyzed.relevance_score < config.gemini.relevance_threshold:
                logger.info(
                    f"Skipping storage: relevance {analyzed.relevance_score} "
                    f"below threshold {config.gemini.relevance_threshold}"
                )
                return ""

            # Add to Firestore
            doc_ref = self.db.collection(config.firestore.discoveries_collection).add(
                analyzed.to_dict()
            )

            doc_id = doc_ref[1].id
            logger.info(f"Stored analyzed content in Firestore: {doc_id}")

            return doc_id

        except Exception as e:
            logger.error(f"Error storing in Firestore: {e}", exc_info=True)
            return ""

    def process_message(self, message_data: dict[str, Any]) -> dict[str, Any]:
        """Process a Pub/Sub message.

        Args:
            message_data: Message data from Pub/Sub

        Returns:
            Processing result
        """
        try:
            # Analyze content
            analyzed = self.analyze_content(message_data)
            if not analyzed:
                return {"status": "error", "message": "Analysis failed"}

            # Store in Firestore
            doc_id = self.store_in_firestore(analyzed)

            return {
                "status": "success",
                "relevance_score": analyzed.relevance_score,
                "firestore_doc_id": doc_id,
            }

        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}


# Singleton instance
analyzer = GeminiAnalyzer()
