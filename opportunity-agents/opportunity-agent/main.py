"""Opportunity Agent entry point."""
import os
import json
from typing import List, Dict
from tools.market_analyzer import MarketAnalyzer
from tools.competitor_intel import CompetitorIntel
from tools.oss_finder import OSSFinder
from tools.build_fork_advisor import BuildForkAdvisor


class OpportunityAgent:
    """Main opportunity agent for market analysis and strategic recommendations."""

    def __init__(self):
        """Initialize all tools."""
        self.market = MarketAnalyzer()
        self.competitor = CompetitorIntel()
        self.oss = OSSFinder()
        self.advisor = BuildForkAdvisor()

    def analyze_opportunity(
        self,
        market_segment: str,
        functionality: str,
        competitors: List[str] = None,
        preferred_language: str = None
    ) -> Dict:
        """
        Complete strategic analysis of an opportunity.

        Args:
            market_segment: Market description (e.g., "construction management software")
            functionality: What to build (e.g., "equipment tracking with offline mobile")
            competitors: List of competitor names
            preferred_language: Preferred programming language

        Returns:
            {
                "market_size": Dict,
                "competitive_landscape": Dict,
                "oss_recommendations": List[Dict],
                "build_strategy": Dict,
                "opportunity_score": 0-100,
                "strategic_recommendation": str
            }
        """
        print(f"🔍 Analyzing opportunity: {market_segment}")
        print(f"💡 Functionality: {functionality}")

        # 1. Market sizing
        print("\n1️⃣ Calculating market size (TAM/SAM/SOM)...")
        market_data = self.market.calculate_tam_sam_som(market_segment)
        if market_data.get("TAM_dollars"):
            print(f"   ✓ TAM: ${market_data['TAM_dollars']:,}")
            print(f"   ✓ SAM: ${market_data['SAM_dollars']:,}")
            print(f"   ✓ SOM: ${market_data['SOM_dollars']:,}")
            print(f"   ✓ Growth: {market_data['growth_rate_cagr']*100:.1f}% CAGR")

        print("\n2️⃣ Analyzing market trends...")
        trends = self.market.analyze_market_trends(market_segment)
        if trends.get("trends"):
            print(f"   ✓ Identified {len(trends['trends'])} key trends")

        # 3. Competitive analysis
        competitive_landscape = {}
        if competitors:
            print(f"\n3️⃣ Analyzing {len(competitors)} competitors...")
            competitive_landscape = self.competitor.analyze_competitors(
                competitors,
                market_segment
            )
            if competitive_landscape.get("competitors"):
                print(f"   ✓ Analyzed {len(competitive_landscape['competitors'])} competitors")
                if competitive_landscape.get("differentiation_opportunities"):
                    print(f"   ✓ Found {len(competitive_landscape['differentiation_opportunities'])} differentiation opportunities")

        # 4. OSS options
        print(f"\n4️⃣ Searching for relevant open source projects...")
        oss_options = self.oss.find_relevant_projects(
            functionality,
            language=preferred_language
        )
        if oss_options:
            print(f"   ✓ Found {len(oss_options)} relevant OSS projects")
            print(f"   ✓ Top project: {oss_options[0]['name']} ({oss_options[0]['fork_score']}/100 fork score)")

        # 5. Build/fork recommendation
        print(f"\n5️⃣ Generating build vs fork recommendation...")
        build_strategy = self.advisor.recommend(
            requirements=functionality,
            oss_options=oss_options,
            time_to_market_importance=7
        )
        print(f"   ✓ Recommendation: {build_strategy['recommendation'].upper()}")
        if build_strategy.get("estimated_time_savings") != "N/A":
            print(f"   ✓ Time savings: {build_strategy['estimated_time_savings']}")

        # 6. Calculate opportunity score
        print(f"\n6️⃣ Calculating opportunity score...")
        score = self._calculate_opportunity_score(
            market_data,
            competitive_landscape,
            oss_options
        )
        print(f"   ✓ Opportunity score: {score}/100")

        result = {
            "market_segment": market_segment,
            "functionality": functionality,
            "market_size": market_data,
            "trends": trends,
            "competitive_landscape": competitive_landscape,
            "oss_recommendations": oss_options[:5] if oss_options else [],
            "build_strategy": build_strategy,
            "opportunity_score": score,
            "strategic_recommendation": self._generate_strategy(score, build_strategy)
        }

        print(f"\n✅ {result['strategic_recommendation']}")
        return result

    def _calculate_opportunity_score(
        self,
        market: Dict,
        competitors: Dict,
        oss: List[Dict]
    ) -> int:
        """Calculate 0-100 opportunity score."""
        score = 0

        # Large market (0-30 points)
        tam = market.get("TAM_dollars", 0)
        if tam >= 1_000_000_000:  # $1B+
            score += 30
        elif tam >= 100_000_000:  # $100M+
            score += 25
        elif tam >= 10_000_000:  # $10M+
            score += 20
        elif tam >= 1_000_000:  # $1M+
            score += 10

        # High growth rate (0-10 points)
        growth = market.get("growth_rate_cagr", 0)
        if growth >= 0.20:  # 20%+
            score += 10
        elif growth >= 0.10:  # 10%+
            score += 7
        elif growth >= 0.05:  # 5%+
            score += 4

        # Weak/fragmented competition (0-35 points)
        if competitors:
            avg_rating = competitors.get("average_rating", 5.0)
            num_competitors = len(competitors.get("competitors", []))

            if avg_rating < 3.5:
                score += 25  # Weak competitors
            elif avg_rating < 4.0:
                score += 15
            elif avg_rating < 4.5:
                score += 10

            # Fragmented market is good
            if num_competitors > 10:
                score += 10  # Fragmented = opportunity
            elif num_competitors < 3:
                score += 5  # Blue ocean but risky
        else:
            score += 20  # No known competitors

        # Good OSS leverage (0-25 points)
        if oss:
            best_fork_score = max(p.get("fork_score", 0) for p in oss)
            if best_fork_score >= 75:
                score += 25
            elif best_fork_score >= 60:
                score += 20
            elif best_fork_score >= 40:
                score += 15
            elif best_fork_score >= 20:
                score += 10

        return min(100, int(score))

    def _generate_strategy(self, score: int, build_strategy: Dict) -> str:
        """Generate strategic recommendation."""
        strategy = build_strategy.get("recommendation", "build").upper()

        if score >= 75:
            return f"🟢 STRONG OPPORTUNITY: {strategy} strategy recommended. Large market with exploitable gaps."
        elif score >= 50:
            return f"🟡 VIABLE OPPORTUNITY: {strategy} approach. Validate with pilot customers first."
        elif score >= 25:
            return f"🟠 RISKY OPPORTUNITY: Consider if you have unique advantages. {strategy} to minimize investment."
        else:
            return f"🔴 WEAK OPPORTUNITY: Market too small or too competitive. Explore alternative segments."


# A2A Protocol Handler
def handle_a2a_request(request: Dict) -> Dict:
    """
    Handle incoming A2A protocol requests.

    Args:
        request: A2A request payload

    Returns:
        Opportunity analysis result
    """
    agent = OpportunityAgent()

    return agent.analyze_opportunity(
        market_segment=request.get("market", ""),
        functionality=request.get("functionality", ""),
        competitors=request.get("competitors", []),
        preferred_language=request.get("language")
    )


def main():
    """CLI entry point for testing."""
    import sys

    if len(sys.argv) < 3:
        print("Usage: python main.py '<market segment>' '<functionality>'")
        print("\nExample:")
        print("  python main.py 'construction management software' 'equipment tracking with offline mobile'")
        sys.exit(1)

    market = sys.argv[1]
    functionality = sys.argv[2]

    agent = OpportunityAgent()
    result = agent.analyze_opportunity(
        market_segment=market,
        functionality=functionality,
        competitors=["ToolTracker", "EquipmentManager"] if len(sys.argv) < 4 else sys.argv[3].split(","),
        preferred_language="Python"
    )

    print("\n" + "="*80)
    print("OPPORTUNITY ANALYSIS REPORT")
    print("="*80)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
