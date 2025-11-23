"""Sentiment analysis using Gemini."""
import os
import json
from typing import List, Dict
from google import genai
from google.genai import types


class SentimentAnalyzer:
    """Analyze sentiment and extract insights using Gemini."""

    def __init__(self):
        """Initialize Gemini client."""
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    def analyze_frustration(self, mentions: List[Dict]) -> Dict:
        """
        Analyze frustration level and extract top quotes.

        Args:
            mentions: List of posts/comments to analyze

        Returns:
            {
                "frustration_score": 0-100,
                "urgency_score": 0-100,
                "top_quotes": List[str],
                "sentiment_breakdown": Dict
            }
        """
        if not mentions:
            return {
                "frustration_score": 0,
                "urgency_score": 0,
                "top_quotes": [],
                "sentiment_breakdown": {
                    "very_frustrated": 0,
                    "frustrated": 0,
                    "mild": 0,
                    "neutral": 0
                }
            }

        # Batch mentions for analysis (limit to first 50 to avoid token limits)
        text_batch = "\n\n---\n\n".join([
            m.get("text", "")[:500] for m in mentions[:50]
        ])

        prompt = f"""Analyze these social media posts for pain point severity.

Posts:
{text_batch}

Provide:
1. Frustration score (0-100): How frustrated are users?
2. Urgency score (0-100): How urgently do they need a solution?
3. Top 5 quotes that best capture the pain (include the actual quote text)
4. Sentiment breakdown with counts:
   - very_frustrated: Count of very frustrated users
   - frustrated: Count of frustrated users
   - mild: Count with mild frustration
   - neutral: Count with neutral sentiment

Output ONLY valid JSON in this exact format:
{{
  "frustration_score": <number 0-100>,
  "urgency_score": <number 0-100>,
  "top_quotes": ["quote1", "quote2", "quote3", "quote4", "quote5"],
  "sentiment_breakdown": {{
    "very_frustrated": <count>,
    "frustrated": <count>,
    "mild": <count>,
    "neutral": <count>
  }}
}}"""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    max_output_tokens=2048
                )
            )

            return self._parse_response(response.text)

        except Exception as e:
            print(f"Error analyzing frustration: {e}")
            return {
                "frustration_score": 0,
                "urgency_score": 0,
                "top_quotes": [],
                "sentiment_breakdown": {
                    "very_frustrated": 0,
                    "frustrated": 0,
                    "mild": 0,
                    "neutral": 0
                },
                "error": str(e)
            }

    def detect_competitor_weaknesses(
        self,
        mentions: List[Dict],
        competitors: List[str]
    ) -> Dict:
        """Extract specific complaints about competitors."""
        complaints_by_competitor = {}

        for competitor in competitors:
            # Filter mentions that mention this competitor
            competitor_mentions = [
                m for m in mentions
                if competitor.lower() in m.get("text", "").lower()
            ]

            if not competitor_mentions:
                complaints_by_competitor[competitor] = {
                    "mention_count": 0,
                    "complaints": []
                }
                continue

            # Analyze complaints
            mention_texts = "\n\n".join([
                m.get("text", "")[:300] for m in competitor_mentions[:20]
            ])

            prompt = f"""Extract specific complaints about {competitor} from these posts:

{mention_texts}

List the top 5 specific feature complaints or issues.
Focus on actionable weaknesses that a new product could address.

Output as JSON array of strings:
["complaint 1", "complaint 2", ...]"""

            try:
                response = self.client.models.generate_content(
                    model="gemini-2.0-flash-exp",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.1,
                        max_output_tokens=1024
                    )
                )

                complaints = self._parse_complaints(response.text)

                complaints_by_competitor[competitor] = {
                    "mention_count": len(competitor_mentions),
                    "complaints": complaints
                }

            except Exception as e:
                print(f"Error analyzing {competitor}: {e}")
                complaints_by_competitor[competitor] = {
                    "mention_count": len(competitor_mentions),
                    "complaints": [],
                    "error": str(e)
                }

        return complaints_by_competitor

    def _parse_response(self, response_text: str) -> Dict:
        """Parse JSON response from Gemini."""
        try:
            # Try to extract JSON from response
            # Remove markdown code blocks if present
            text = response_text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

            return json.loads(text)
        except json.JSONDecodeError:
            # If JSON parsing fails, return default structure
            return {
                "frustration_score": 50,
                "urgency_score": 50,
                "top_quotes": [],
                "sentiment_breakdown": {
                    "very_frustrated": 0,
                    "frustrated": 0,
                    "mild": 0,
                    "neutral": 0
                }
            }

    def _parse_complaints(self, response_text: str) -> List[str]:
        """Parse complaints list from response."""
        try:
            text = response_text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

            complaints = json.loads(text)
            if isinstance(complaints, list):
                return complaints
            return []
        except:
            return []
