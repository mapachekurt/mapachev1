"""Orchestrator Agent entry point."""
import os
import json
import asyncio
from typing import List, Dict
from tools.agent_router import AgentRouter
from tools.result_synthesizer import ResultSynthesizer
from tools.linear_creator import LinearCreator


class OrchestratorAgent:
    """Main orchestrator agent for coordinating opportunity discovery workflow."""

    def __init__(self):
        """Initialize all tools."""
        self.router = AgentRouter()
        self.synthesizer = ResultSynthesizer()
        self.linear = LinearCreator()

    async def discover_opportunities(
        self,
        opportunity_hypotheses: List[Dict]
    ) -> Dict:
        """
        Complete opportunity discovery workflow.

        Args:
            opportunity_hypotheses: List of opportunities to validate/analyze
                [{
                    "problem": str,
                    "market": str,
                    "functionality": str,
                    "subreddits": List[str],
                    "competitors": List[str],
                    "timeframe": str (optional),
                    "language": str (optional)
                }]

        Returns:
            {
                "ranked_opportunities": List[Dict],
                "synthesis": str,
                "linear_project": Dict (for #1 opportunity if score >= 50),
                "recommendation": str
            }
        """
        print("="*80)
        print("🎯 OPPORTUNITY DISCOVERY ORCHESTRATOR")
        print("="*80)
        print(f"\n📊 Analyzing {len(opportunity_hypotheses)} opportunity hypotheses\n")

        # 1. Call validation + opportunity agents in parallel
        print("🔄 Step 1: Parallel agent analysis...")
        combined_results = await self.router.parallel_analysis(opportunity_hypotheses)

        # 2. Synthesize and rank results
        print("\n📈 Step 2: Synthesizing and ranking results...")
        synthesis = self.synthesizer.synthesize_and_rank(combined_results)

        # 3. Create Linear project for #1 opportunity (if score >= 50)
        top_opportunity = synthesis["top_recommendation"]
        linear_project = None

        if top_opportunity and top_opportunity["combined_score"] >= 50:
            print(f"\n📋 Step 3: Creating Linear project for top opportunity...")
            linear_project = self.linear.create_project(top_opportunity)
        else:
            print(f"\n⚠️  Step 3: Skipping Linear project creation (score too low)")

        # 4. Generate final recommendation
        recommendation = self._generate_final_recommendation(
            synthesis,
            linear_project
        )

        result = {
            "ranked_opportunities": synthesis["ranked_opportunities"],
            "synthesis": synthesis["synthesis_summary"],
            "linear_project": linear_project,
            "recommendation": recommendation,
            "total_analyzed": len(opportunity_hypotheses),
            "timestamp": asyncio.get_event_loop().time()
        }

        print("\n" + "="*80)
        print("✅ ORCHESTRATION COMPLETE")
        print("="*80)
        print(f"\n{recommendation}\n")

        return result

    def _generate_final_recommendation(
        self,
        synthesis: Dict,
        linear_project: Dict
    ) -> str:
        """Generate final action recommendation."""
        top = synthesis["top_recommendation"]

        if not top:
            return """🔴 NO VIABLE OPPORTUNITIES FOUND

No opportunities met the minimum threshold for validation and market size.

Recommended Actions:
1. Explore different market segments
2. Refine problem hypotheses based on user research
3. Consider adjacent markets or different customer segments
"""

        score = top["combined_score"]
        problem = top["input"]["problem"]

        if score >= 75:
            project_info = ""
            if linear_project and linear_project.get("project_url"):
                project_info = f"\n🔗 Linear Project: {linear_project['project_url']}\n"

            return f"""🟢 STRONG RECOMMENDATION: BUILD IMMEDIATELY

**Top Opportunity:** {problem}
**Combined Score:** {score}/100
**Validation Score:** {top['validation'].get('validation_score', 0)}/100
**Opportunity Score:** {top['opportunity'].get('opportunity_score', 0)}/100
{project_info}
**Next Steps:**
1. Review Linear project issues and timeline
2. Assemble development team
3. Start with research & requirements issue
4. Target beta launch in 6-8 weeks
5. Plan public launch for week 12

**Why This is Strong:**
- High validation score indicates clear demand
- Large market with growth potential
- Clear differentiation opportunities
- Feasible build strategy identified
"""

        elif score >= 50:
            project_info = ""
            if linear_project and linear_project.get("project_url"):
                project_info = f"\n🔗 Linear Project: {linear_project['project_url']}\n"

            return f"""🟡 MODERATE RECOMMENDATION: VALIDATE FURTHER

**Top Opportunity:** {problem}
**Combined Score:** {score}/100
{project_info}
**Next Steps:**
1. Interview 5-10 target users to validate demand
2. Build landing page to gauge interest (target: 50+ signups)
3. Create technical prototype to test feasibility
4. If validation improves, proceed with Linear project plan

**Caution Areas:**
- Validation or market size below ideal threshold
- Need stronger evidence before full commitment
- Consider starting with smaller MVP
"""

        else:
            return f"""🟠 WEAK RECOMMENDATION: HIGH RISK

**Top Opportunity:** {problem}
**Combined Score:** {score}/100

This opportunity shows insufficient validation or market size.

**Recommended Actions:**
1. Pivot to different angle or customer segment
2. Explore adjacent markets with stronger signals
3. Conduct deeper user research before building
4. Consider if you have unfair advantages that could overcome weak scores

**Alternative Approaches:**
- Start with manual/concierge MVP to test demand
- Target niche segment first to prove model
- Partner with established player rather than building
"""

    async def analyze_single_opportunity(
        self,
        problem: str,
        market: str,
        functionality: str,
        **kwargs
    ) -> Dict:
        """
        Convenience method to analyze a single opportunity.

        Args:
            problem: Problem statement
            market: Market segment
            functionality: What to build
            **kwargs: Additional parameters (subreddits, competitors, etc.)

        Returns:
            Analysis result for single opportunity
        """
        opportunity = {
            "problem": problem,
            "market": market,
            "functionality": functionality,
            **kwargs
        }

        result = await self.discover_opportunities([opportunity])

        return {
            "analysis": result["ranked_opportunities"][0] if result["ranked_opportunities"] else None,
            "synthesis": result["synthesis"],
            "linear_project": result["linear_project"],
            "recommendation": result["recommendation"]
        }


# A2A Protocol Handler
async def handle_a2a_request(request: Dict) -> Dict:
    """
    Handle incoming A2A protocol requests.

    Args:
        request: A2A request payload
            {
                "opportunities": List[Dict]
            }

    Returns:
        Orchestration result
    """
    agent = OrchestratorAgent()

    return await agent.discover_opportunities(
        request.get("opportunities", [])
    )


async def main():
    """CLI entry point for testing."""
    import sys

    # Example opportunities
    example_opportunities = [
        {
            "problem": "construction equipment tracking",
            "market": "construction management software",
            "functionality": "equipment tracking with offline mobile support",
            "subreddits": ["construction", "contractors", "BuildingTech"],
            "competitors": ["ToolTracker", "EquipmentManager"],
            "timeframe": "month",
            "language": "Python"
        },
        {
            "problem": "restaurant inventory waste reduction",
            "market": "restaurant management software",
            "functionality": "automated inventory tracking with predictive ordering",
            "subreddits": ["restaurateur", "KitchenConfidential", "restaurantowners"],
            "competitors": ["MarketMan", "BlueCart"],
            "timeframe": "month",
            "language": "TypeScript"
        }
    ]

    # Allow custom opportunities from command line
    if len(sys.argv) > 1:
        # Parse custom opportunity from args
        # Format: python main.py "problem" "market" "functionality"
        if len(sys.argv) >= 4:
            example_opportunities = [{
                "problem": sys.argv[1],
                "market": sys.argv[2],
                "functionality": sys.argv[3],
                "subreddits": sys.argv[4].split(",") if len(sys.argv) > 4 else [],
                "competitors": sys.argv[5].split(",") if len(sys.argv) > 5 else []
            }]

    agent = OrchestratorAgent()
    result = await agent.discover_opportunities(example_opportunities)

    # Save results to file
    output_file = "opportunity_analysis_results.json"
    with open(output_file, "w") as f:
        json.dumps(result, indent=2, default=str)
        f.write(json.dumps(result, indent=2, default=str))

    print(f"\n💾 Full results saved to: {output_file}")

    # Print synthesis
    print("\n" + "="*80)
    print("EXECUTIVE SYNTHESIS")
    print("="*80)
    print(result["synthesis"])

    # Print top opportunities
    print("\n" + "="*80)
    print("TOP OPPORTUNITIES")
    print("="*80)

    for opp in result["ranked_opportunities"][:3]:
        print(f"\n#{opp['rank']}: {opp['input']['problem']}")
        print(f"   Combined Score: {opp['combined_score']}/100")
        print(f"   Validation: {opp['validation'].get('validation_score', 0)}/100")
        print(f"   Opportunity: {opp['opportunity'].get('opportunity_score', 0)}/100")


if __name__ == "__main__":
    asyncio.run(main())
