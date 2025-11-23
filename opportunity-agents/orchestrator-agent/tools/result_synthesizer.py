"""Synthesize and rank results from multiple agents."""
import os
import json
from typing import List, Dict
from google import genai
from google.genai import types


class ResultSynthesizer:
    """Combine validation + opportunity analysis and rank opportunities."""

    def __init__(self):
        """Initialize Gemini client."""
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.validation_weight = 0.6
        self.opportunity_weight = 0.4

    def synthesize_and_rank(self, combined_results: List[Dict]) -> Dict:
        """
        Combine validation + opportunity analysis and rank opportunities.

        Args:
            combined_results: Results from parallel agent calls
                [{
                    "input": {...},
                    "validation": {...},
                    "opportunity": {...}
                }]

        Returns:
            {
                "ranked_opportunities": List[Dict],
                "synthesis_summary": str,
                "top_recommendation": Dict
            }
        """
        print("📊 Synthesizing and ranking opportunities...")

        # Calculate combined score for each opportunity
        ranked = []

        for result in combined_results:
            validation_score = result["validation"].get("validation_score", 0)
            opportunity_score = result["opportunity"].get("opportunity_score", 0)

            # Weighted combination: 60% validation, 40% opportunity
            combined_score = (
                validation_score * self.validation_weight +
                opportunity_score * self.opportunity_weight
            )

            ranked.append({
                **result,
                "combined_score": round(combined_score, 1),
                "rank": 0  # Will be set after sorting
            })

        # Sort by combined score
        ranked.sort(key=lambda x: x["combined_score"], reverse=True)

        # Assign ranks
        for i, opp in enumerate(ranked):
            opp["rank"] = i + 1

        print(f"✓ Ranked {len(ranked)} opportunities")

        # Generate synthesis using Gemini
        print("📝 Generating executive summary...")
        synthesis = self._generate_synthesis(ranked)

        return {
            "ranked_opportunities": ranked,
            "synthesis_summary": synthesis,
            "top_recommendation": ranked[0] if ranked else None
        }

    def _generate_synthesis(self, ranked: List[Dict]) -> str:
        """Generate executive summary using Gemini."""
        # Create a concise summary of each opportunity for the prompt
        opp_summaries = []
        for i, opp in enumerate(ranked[:5], 1):  # Top 5 only
            summary = f"""
#{i}: {opp['input']['problem']}
- Combined Score: {opp['combined_score']}/100
- Validation: {opp['validation'].get('validation_score', 0)}/100
  - Mentions: {opp['validation'].get('evidence', {}).get('mention_count', 0)}
  - Frustration: {opp['validation'].get('evidence', {}).get('frustration_score', 0)}/100
- Opportunity: {opp['opportunity'].get('opportunity_score', 0)}/100
  - TAM: ${opp['opportunity'].get('market_size', {}).get('TAM_dollars', 0):,}
  - Strategy: {opp['opportunity'].get('build_strategy', {}).get('recommendation', 'unknown')}
"""
            opp_summaries.append(summary)

        opportunities_text = "\n".join(opp_summaries)

        prompt = f"""Synthesize these opportunity analyses into an executive summary:

{opportunities_text}

Provide:
1. Key findings across all opportunities (2-3 sentences)
2. Why the #1 ranked opportunity is best (2-3 sentences)
3. Top 3 risks and mitigations for #1 opportunity
4. Recommended next steps (3-5 action items)

Keep it concise (300 words max). Be direct and actionable."""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    max_output_tokens=2048
                )
            )

            return response.text

        except Exception as e:
            print(f"Error generating synthesis: {e}")
            return self._generate_fallback_synthesis(ranked)

    def _generate_fallback_synthesis(self, ranked: List[Dict]) -> str:
        """Generate basic synthesis if Gemini fails."""
        if not ranked:
            return "No opportunities analyzed."

        top = ranked[0]

        return f"""## Executive Summary

Top Opportunity: {top['input']['problem']}
Combined Score: {top['combined_score']}/100

This opportunity shows strong validation with {top['validation'].get('evidence', {}).get('mention_count', 0)} mentions and {top['validation'].get('evidence', {}).get('frustration_score', 0)}/100 frustration score.

Market size: ${top['opportunity'].get('market_size', {}).get('TAM_dollars', 0):,} TAM

Recommended strategy: {top['opportunity'].get('build_strategy', {}).get('recommendation', 'unknown').upper()}

Next steps:
1. Review detailed validation evidence
2. Interview target users
3. Build MVP based on recommended strategy
"""

    def compare_opportunities(
        self,
        opportunity_a: Dict,
        opportunity_b: Dict
    ) -> Dict:
        """
        Head-to-head comparison of two opportunities.

        Args:
            opportunity_a: First opportunity
            opportunity_b: Second opportunity

        Returns:
            Comparison analysis
        """
        comparison = {
            "opportunity_a": opportunity_a['input']['problem'],
            "opportunity_b": opportunity_b['input']['problem'],
            "winner": None,
            "comparison": {}
        }

        # Compare key metrics
        comparison["comparison"] = {
            "validation_score": {
                "a": opportunity_a['validation'].get('validation_score', 0),
                "b": opportunity_b['validation'].get('validation_score', 0),
                "winner": "a" if opportunity_a['validation'].get('validation_score', 0) > opportunity_b['validation'].get('validation_score', 0) else "b"
            },
            "opportunity_score": {
                "a": opportunity_a['opportunity'].get('opportunity_score', 0),
                "b": opportunity_b['opportunity'].get('opportunity_score', 0),
                "winner": "a" if opportunity_a['opportunity'].get('opportunity_score', 0) > opportunity_b['opportunity'].get('opportunity_score', 0) else "b"
            },
            "combined_score": {
                "a": opportunity_a.get('combined_score', 0),
                "b": opportunity_b.get('combined_score', 0),
                "winner": "a" if opportunity_a.get('combined_score', 0) > opportunity_b.get('combined_score', 0) else "b"
            }
        }

        comparison["winner"] = "a" if opportunity_a.get('combined_score', 0) > opportunity_b.get('combined_score', 0) else "b"

        return comparison
