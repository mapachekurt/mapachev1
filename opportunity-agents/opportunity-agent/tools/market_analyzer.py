"""Market size calculation using Gemini + web search."""
import os
import json
from typing import Dict
from google import genai
from google.genai import types


class MarketAnalyzer:
    """Calculate market size and analyze trends using Gemini with Google Search."""

    def __init__(self):
        """Initialize Gemini client."""
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    def calculate_tam_sam_som(
        self,
        market_segment: str,
        geography: str = "United States"
    ) -> Dict:
        """
        Calculate Total Addressable Market, Serviceable Available Market,
        and Serviceable Obtainable Market.

        Uses Gemini with Google Search grounding for current data.

        Args:
            market_segment: Market description (e.g., "construction management software")
            geography: Geographic scope

        Returns:
            {
                "TAM_dollars": int,
                "SAM_dollars": int,
                "SOM_dollars": int,
                "growth_rate_cagr": float,
                "market_drivers": List[str],
                "sources": List[str]
            }
        """
        prompt = f"""Calculate the market size for: {market_segment} in {geography}

Provide:
1. TAM (Total Addressable Market) - Total market demand in USD
2. SAM (Serviceable Available Market) - Portion addressable with typical SaaS product
3. SOM (Serviceable Obtainable Market) - Realistic capture in 3 years for new entrant
4. Market growth rate (CAGR %)
5. Top 5 key market drivers
6. Sources for all numbers

Use current 2025 data. Search for recent market research reports.

Output ONLY valid JSON in this exact format:
{{
  "TAM_dollars": <number>,
  "SAM_dollars": <number>,
  "SOM_dollars": <number>,
  "growth_rate_cagr": <percentage as decimal, e.g. 0.15 for 15%>,
  "market_drivers": ["driver1", "driver2", "driver3", "driver4", "driver5"],
  "sources": ["source1", "source2", "source3"],
  "analysis_notes": "Brief explanation of calculations"
}}"""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    max_output_tokens=4096,
                    tools=[types.Tool(google_search=types.GoogleSearch())]
                )
            )

            return self._parse_market_data(response.text)

        except Exception as e:
            print(f"Error calculating market size: {e}")
            return {
                "TAM_dollars": 0,
                "SAM_dollars": 0,
                "SOM_dollars": 0,
                "growth_rate_cagr": 0.0,
                "market_drivers": [],
                "sources": [],
                "error": str(e)
            }

    def analyze_market_trends(self, market_segment: str) -> Dict:
        """
        Identify key trends shaping the market.

        Args:
            market_segment: Market to analyze

        Returns:
            {
                "trends": List[Dict],
                "opportunities": List[str],
                "threats": List[str]
            }
        """
        prompt = f"""What are the top 5 trends in {market_segment} for 2025-2026?

For each trend:
1. Name and description
2. Impact on new entrants (positive/negative/neutral)
3. Adoption timeline (early/growing/mature)
4. Key players driving the trend

Also identify:
- Top 3 opportunities these trends create
- Top 3 threats for new entrants

Use recent sources. Output as JSON:
{{
  "trends": [
    {{
      "name": "Trend name",
      "description": "...",
      "impact_on_new_entrants": "positive/negative/neutral",
      "adoption_timeline": "early/growing/mature",
      "key_players": ["player1", "player2"]
    }}
  ],
  "opportunities": ["opp1", "opp2", "opp3"],
  "threats": ["threat1", "threat2", "threat3"]
}}"""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    max_output_tokens=4096,
                    tools=[types.Tool(google_search=types.GoogleSearch())]
                )
            )

            return self._parse_json_response(response.text)

        except Exception as e:
            print(f"Error analyzing trends: {e}")
            return {
                "trends": [],
                "opportunities": [],
                "threats": [],
                "error": str(e)
            }

    def estimate_customer_acquisition_cost(
        self,
        market_segment: str,
        avg_deal_size: int
    ) -> Dict:
        """
        Estimate CAC (Customer Acquisition Cost) for the market.

        Args:
            market_segment: Market segment
            avg_deal_size: Average deal size in dollars

        Returns:
            CAC estimate and benchmarks
        """
        prompt = f"""For {market_segment} with average deal size ${avg_deal_size}:

Estimate:
1. Typical CAC (Customer Acquisition Cost)
2. CAC payback period (months)
3. LTV:CAC ratio benchmark
4. Primary acquisition channels
5. Estimated conversion rates

Output as JSON."""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    tools=[types.Tool(google_search=types.GoogleSearch())]
                )
            )

            return self._parse_json_response(response.text)

        except Exception as e:
            return {"error": str(e)}

    def _parse_market_data(self, response_text: str) -> Dict:
        """Parse market data from Gemini response."""
        try:
            text = self._clean_json_response(response_text)
            data = json.loads(text)

            # Ensure required fields exist
            return {
                "TAM_dollars": int(data.get("TAM_dollars", 0)),
                "SAM_dollars": int(data.get("SAM_dollars", 0)),
                "SOM_dollars": int(data.get("SOM_dollars", 0)),
                "growth_rate_cagr": float(data.get("growth_rate_cagr", 0.0)),
                "market_drivers": data.get("market_drivers", []),
                "sources": data.get("sources", []),
                "analysis_notes": data.get("analysis_notes", "")
            }
        except Exception as e:
            print(f"Error parsing market data: {e}")
            return {
                "TAM_dollars": 0,
                "SAM_dollars": 0,
                "SOM_dollars": 0,
                "growth_rate_cagr": 0.0,
                "market_drivers": [],
                "sources": [],
                "parse_error": str(e)
            }

    def _parse_json_response(self, response_text: str) -> Dict:
        """Parse generic JSON response."""
        try:
            text = self._clean_json_response(response_text)
            return json.loads(text)
        except Exception as e:
            return {"parse_error": str(e), "raw_response": response_text[:500]}

    def _clean_json_response(self, text: str) -> str:
        """Clean JSON from markdown code blocks."""
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()
