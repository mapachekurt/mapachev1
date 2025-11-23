"""Competitive intelligence gathering and analysis."""
import os
import json
from typing import List, Dict
from google import genai
from google.genai import types


class CompetitorIntel:
    """Analyze competitive landscape and identify positioning opportunities."""

    def __init__(self):
        """Initialize Gemini client."""
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    def analyze_competitors(
        self,
        competitors: List[str],
        market_segment: str
    ) -> Dict:
        """
        Analyze competitive landscape.

        Args:
            competitors: List of competitor names
            market_segment: Market they operate in

        Returns:
            {
                "competitors": List[Dict],
                "market_positioning": Dict,
                "gaps": List[str],
                "differentiation_opportunities": List[str]
            }
        """
        if not competitors:
            return {
                "competitors": [],
                "market_positioning": {},
                "gaps": [],
                "differentiation_opportunities": []
            }

        prompt = f"""Analyze these competitors in {market_segment}:
{', '.join(competitors)}

For each competitor, provide:
1. Company overview
2. Key features
3. Pricing model
4. Target customer segment
5. Strengths
6. Weaknesses
7. Estimated market share

Then identify:
- Market positioning map (price vs features)
- Gaps in the market
- Top 5 differentiation opportunities for a new entrant

Output as JSON:
{{
  "competitors": [
    {{
      "name": "...",
      "overview": "...",
      "key_features": ["f1", "f2"],
      "pricing_model": "...",
      "target_segment": "...",
      "strengths": ["s1", "s2"],
      "weaknesses": ["w1", "w2"],
      "estimated_market_share": "X%"
    }}
  ],
  "market_positioning": {{
    "price_leaders": ["comp1"],
    "feature_leaders": ["comp2"],
    "niche_players": ["comp3"]
  }},
  "gaps": ["gap1", "gap2"],
  "differentiation_opportunities": ["opp1", "opp2", "opp3", "opp4", "opp5"]
}}"""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=8192,
                    tools=[types.Tool(google_search=types.GoogleSearch())]
                )
            )

            data = self._parse_json(response.text)

            # Calculate average rating
            ratings = []
            for comp in data.get("competitors", []):
                if "rating" in comp:
                    ratings.append(float(comp["rating"]))

            data["average_rating"] = sum(ratings) / len(ratings) if ratings else 0

            return data

        except Exception as e:
            print(f"Error analyzing competitors: {e}")
            return {
                "competitors": [],
                "market_positioning": {},
                "gaps": [],
                "differentiation_opportunities": [],
                "error": str(e)
            }

    def find_market_gaps(
        self,
        market_segment: str,
        existing_solutions: List[str]
    ) -> List[Dict]:
        """
        Identify underserved market segments.

        Args:
            market_segment: Overall market
            existing_solutions: List of existing products

        Returns:
            List of market gaps with opportunity scores
        """
        prompt = f"""In {market_segment}, given existing solutions like {', '.join(existing_solutions)}:

Identify the top 5 underserved market segments or use cases.

For each gap:
1. Description
2. Why it's underserved
3. Estimated size (small/medium/large)
4. Difficulty to serve (low/medium/high)
5. Opportunity score (0-100)

Output as JSON array."""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    tools=[types.Tool(google_search=types.GoogleSearch())]
                )
            )

            return self._parse_json(response.text)

        except Exception as e:
            print(f"Error finding market gaps: {e}")
            return []

    def analyze_pricing_strategies(
        self,
        competitors: List[str]
    ) -> Dict:
        """
        Analyze competitor pricing and recommend strategy.

        Args:
            competitors: List of competitors to analyze

        Returns:
            Pricing analysis and recommendations
        """
        prompt = f"""Analyze the pricing strategies of: {', '.join(competitors)}

Provide:
1. Pricing range (low to high)
2. Common pricing models (per-user, tiered, usage-based, etc.)
3. Typical features at each price point
4. Recommended pricing strategy for new entrant
5. Price anchoring opportunities

Output as JSON."""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    tools=[types.Tool(google_search=types.GoogleSearch())]
                )
            )

            return self._parse_json(response.text)

        except Exception as e:
            return {"error": str(e)}

    def _parse_json(self, response_text: str):
        """Parse JSON from response."""
        try:
            text = response_text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

            return json.loads(text)
        except Exception as e:
            print(f"JSON parse error: {e}")
            return {}
