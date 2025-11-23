"""Recommend build from scratch vs fork OSS."""
import os
import json
from typing import List, Dict
from google import genai
from google.genai import types


class BuildForkAdvisor:
    """Recommend whether to build from scratch or fork open source."""

    def __init__(self):
        """Initialize Gemini client."""
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    def recommend(
        self,
        requirements: str,
        oss_options: List[Dict],
        time_to_market_importance: int = 5
    ) -> Dict:
        """
        Recommend whether to build from scratch or fork OSS.

        Args:
            requirements: Product requirements description
            oss_options: List of OSS projects found
            time_to_market_importance: 1-10 scale

        Returns:
            {
                "recommendation": "build" | "fork" | "hybrid",
                "rationale": str,
                "selected_project": Dict if fork,
                "estimated_time_savings": str,
                "estimated_cost_savings": str,
                "risks": List[str],
                "implementation_strategy": str
            }
        """
        if not oss_options:
            return {
                "recommendation": "build",
                "rationale": "No suitable OSS projects found. Building from scratch is the only option.",
                "selected_project": None,
                "estimated_time_savings": "N/A",
                "estimated_cost_savings": "N/A",
                "risks": [
                    "Full development cost",
                    "Longer time to market",
                    "Need to build everything from scratch"
                ],
                "implementation_strategy": "Build MVP with core features, iterate based on user feedback"
            }

        # Format OSS options for prompt
        oss_summary = []
        for i, proj in enumerate(oss_options[:5], 1):
            oss_summary.append(
                f"{i}. {proj['name']} ({proj['stars']} stars)\n"
                f"   - License: {proj['license']}\n"
                f"   - Fork Score: {proj.get('fork_score', 0)}/100\n"
                f"   - Active: {proj['days_since_push']} days since last push\n"
                f"   - Recommendation: {proj.get('fork_recommendation', 'Unknown')}"
            )

        oss_text = "\n\n".join(oss_summary)

        prompt = f"""Given these requirements:
{requirements}

And these OSS options:
{oss_text}

Time-to-market importance: {time_to_market_importance}/10

Should we:
1. Build from scratch
2. Fork one of these OSS projects
3. Use hybrid approach (fork + custom modules)

Provide:
- Recommendation (build/fork/hybrid)
- Which project to fork (if applicable) - use the number
- Estimated time savings compared to building from scratch
- Estimated development cost savings
- Key risks for the recommended approach
- Detailed implementation strategy

Output as JSON:
{{
  "recommendation": "build|fork|hybrid",
  "selected_project_number": <1-5 or null>,
  "rationale": "Detailed explanation...",
  "estimated_time_savings": "X months" or "N/A",
  "estimated_cost_savings": "$X" or "N/A",
  "risks": ["risk1", "risk2", "risk3"],
  "implementation_strategy": "Step by step strategy...",
  "customization_effort": "low|medium|high",
  "maintenance_complexity": "low|medium|high"
}}"""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=4096
                )
            )

            result = self._parse_recommendation(response.text)

            # Add selected project details
            if result.get("selected_project_number"):
                idx = result["selected_project_number"] - 1
                if 0 <= idx < len(oss_options):
                    result["selected_project"] = oss_options[idx]

            return result

        except Exception as e:
            print(f"Error generating recommendation: {e}")
            return {
                "recommendation": "build",
                "rationale": f"Error analyzing options: {e}",
                "selected_project": None,
                "estimated_time_savings": "Unknown",
                "estimated_cost_savings": "Unknown",
                "risks": ["Analysis failed"],
                "error": str(e)
            }

    def compare_options(
        self,
        build_from_scratch: Dict,
        fork_oss: Dict
    ) -> Dict:
        """
        Compare build vs fork options side-by-side.

        Args:
            build_from_scratch: Build option details
            fork_oss: Fork option details

        Returns:
            Comparison matrix
        """
        comparison = {
            "criteria": [
                "Time to Market",
                "Development Cost",
                "Maintenance Burden",
                "Customization Flexibility",
                "Technical Debt Risk",
                "Community Support"
            ],
            "build_scores": {},
            "fork_scores": {},
            "winner": None
        }

        # Score each criterion (simplified - in production use more sophisticated analysis)
        comparison["build_scores"] = {
            "Time to Market": 3,
            "Development Cost": 3,
            "Maintenance Burden": 5,
            "Customization Flexibility": 10,
            "Technical Debt Risk": 7,
            "Community Support": 2
        }

        comparison["fork_scores"] = {
            "Time to Market": 9,
            "Development Cost": 8,
            "Maintenance Burden": 6,
            "Customization Flexibility": 6,
            "Technical Debt Risk": 5,
            "Community Support": 8
        }

        # Calculate totals
        build_total = sum(comparison["build_scores"].values())
        fork_total = sum(comparison["fork_scores"].values())

        comparison["build_total"] = build_total
        comparison["fork_total"] = fork_total
        comparison["winner"] = "fork" if fork_total > build_total else "build"

        return comparison

    def _parse_recommendation(self, response_text: str) -> Dict:
        """Parse recommendation from Gemini response."""
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
            print(f"Parse error: {e}")
            return {
                "recommendation": "build",
                "rationale": "Failed to parse recommendation",
                "selected_project": None,
                "estimated_time_savings": "Unknown",
                "estimated_cost_savings": "Unknown",
                "risks": ["Analysis parsing failed"],
                "parse_error": str(e)
            }
