"""Validation Agent entry point."""
import os
import json
from typing import List, Dict
from tools.reddit_scraper import RedditScraper
from tools.twitter_api import TwitterAPI
from tools.hackernews_api import HackerNewsAPI
from tools.g2_reviews import G2Reviews
from tools.sentiment_analyzer import SentimentAnalyzer


class ValidationAgent:
    """Main validation agent for pain point validation and evidence collection."""

    def __init__(self):
        """Initialize all tools."""
        self.reddit = RedditScraper()
        self.twitter = TwitterAPI()
        self.hackernews = HackerNewsAPI()
        self.g2 = G2Reviews()
        self.sentiment = SentimentAnalyzer()

    def validate_opportunity(
        self,
        problem_hypothesis: str,
        target_subreddits: List[str],
        competitors: List[str] = None,
        timeframe: str = "week"
    ) -> Dict:
        """
        Validate if people are suffering from this problem.

        Args:
            problem_hypothesis: The problem statement to validate
            target_subreddits: List of subreddits to search
            competitors: Optional list of competitors to analyze
            timeframe: Time window for search (week, month, year)

        Returns:
            Validation report with evidence score 0-100
        """
        print(f"🔍 Validating opportunity: {problem_hypothesis}")
        print(f"📊 Searching {len(target_subreddits)} subreddits over the past {timeframe}")

        # 1. Collect mentions from Reddit
        print("\n1️⃣ Collecting Reddit mentions...")
        reddit_data = self.reddit.search_pain_points(
            query=problem_hypothesis,
            subreddits=target_subreddits,
            timeframe=timeframe
        )
        print(f"   ✓ Found {reddit_data['mentions']} Reddit mentions")

        # 2. Search Twitter (optional, if API key available)
        twitter_data = {"mention_count": 0, "tweets": []}
        if os.getenv("TWITTER_BEARER_TOKEN"):
            print("\n2️⃣ Searching Twitter...")
            try:
                twitter_data = self.twitter.search_mentions(
                    query=problem_hypothesis,
                    days_back=7 if timeframe == "week" else 30
                )
                print(f"   ✓ Found {twitter_data['mention_count']} Twitter mentions")
            except Exception as e:
                print(f"   ⚠ Twitter search skipped: {e}")

        # 3. Search HackerNews
        print("\n3️⃣ Searching HackerNews...")
        hn_data = self.hackernews.search_discussions(
            query=problem_hypothesis,
            days_back=7 if timeframe == "week" else 30
        )
        print(f"   ✓ Found {hn_data['story_count']} stories, {hn_data['comment_count']} comments")

        # Combine all mentions
        all_mentions = reddit_data["posts"] + twitter_data.get("tweets", []) + hn_data.get("top_comments", [])

        # 4. Analyze sentiment
        print("\n4️⃣ Analyzing sentiment and frustration levels...")
        sentiment_data = self.sentiment.analyze_frustration(all_mentions)
        print(f"   ✓ Frustration score: {sentiment_data['frustration_score']}/100")
        print(f"   ✓ Urgency score: {sentiment_data['urgency_score']}/100")

        # 5. Check competitor weaknesses
        competitor_data = {}
        if competitors:
            print(f"\n5️⃣ Analyzing {len(competitors)} competitors...")
            competitor_data = self.sentiment.detect_competitor_weaknesses(
                all_mentions,
                competitors
            )
            for comp, data in competitor_data.items():
                print(f"   ✓ {comp}: {data['mention_count']} mentions")

        # 6. Calculate validation score
        print("\n6️⃣ Calculating validation score...")
        score = self._calculate_validation_score(
            reddit_data,
            twitter_data,
            hn_data,
            sentiment_data,
            competitor_data
        )
        print(f"   ✓ Final validation score: {score}/100")

        result = {
            "problem_hypothesis": problem_hypothesis,
            "validation_score": score,
            "evidence": {
                "mention_count": len(all_mentions),
                "reddit_mentions": reddit_data["mentions"],
                "twitter_mentions": twitter_data.get("mention_count", 0),
                "hackernews_mentions": hn_data["story_count"] + hn_data["comment_count"],
                "frustration_score": sentiment_data["frustration_score"],
                "urgency_score": sentiment_data["urgency_score"],
                "top_quotes": sentiment_data.get("top_quotes", [])[:5],
                "sentiment_breakdown": sentiment_data.get("sentiment_breakdown", {}),
                "competitor_weaknesses": competitor_data
            },
            "recommendation": self._generate_recommendation(score),
            "data_sources": {
                "reddit": reddit_data,
                "twitter": twitter_data,
                "hackernews": hn_data
            }
        }

        print(f"\n✅ {result['recommendation']}")
        return result

    def _calculate_validation_score(
        self,
        reddit: Dict,
        twitter: Dict,
        hackernews: Dict,
        sentiment: Dict,
        competitors: Dict
    ) -> int:
        """Calculate 0-100 validation score."""
        score = 0

        # Total mentions across all platforms
        total_mentions = (
            reddit["mentions"] +
            twitter.get("mention_count", 0) +
            hackernews.get("story_count", 0) +
            hackernews.get("comment_count", 0)
        )

        # Mention frequency (0-30 points)
        if total_mentions >= 100:
            score += 30
        elif total_mentions >= 50:
            score += 25
        elif total_mentions >= 20:
            score += 20
        elif total_mentions >= 10:
            score += 15
        elif total_mentions >= 5:
            score += 10

        # Frustration level (0-40 points)
        frustration = sentiment.get("frustration_score", 0)
        score += min(40, int(frustration * 0.4))

        # Urgency level (0-20 points)
        urgency = sentiment.get("urgency_score", 0)
        score += min(20, int(urgency * 0.2))

        # Competitor weakness evidence (0-10 points)
        if competitors:
            competitor_mention_total = sum(
                c.get("mention_count", 0) for c in competitors.values()
            )
            if competitor_mention_total >= 20:
                score += 10
            elif competitor_mention_total >= 10:
                score += 7
            elif competitor_mention_total >= 5:
                score += 5
            elif competitor_mention_total >= 1:
                score += 3

        return min(100, int(score))

    def _generate_recommendation(self, score: int) -> str:
        """Generate action recommendation based on score."""
        if score >= 75:
            return "🟢 STRONG VALIDATION: High demand with clear pain points. Build immediately."
        elif score >= 50:
            return "🟡 MODERATE VALIDATION: Demand exists but verify with deeper research."
        elif score >= 25:
            return "🟠 WEAK VALIDATION: Low signal. Consider alternative angles."
        else:
            return "🔴 NO VALIDATION: Insufficient evidence of demand. Abandon or pivot."


# A2A Protocol Handler
def handle_a2a_request(request: Dict) -> Dict:
    """
    Handle incoming A2A protocol requests.

    Args:
        request: A2A request payload

    Returns:
        Validation result
    """
    agent = ValidationAgent()

    return agent.validate_opportunity(
        problem_hypothesis=request.get("problem", ""),
        target_subreddits=request.get("subreddits", []),
        competitors=request.get("competitors", []),
        timeframe=request.get("timeframe", "week")
    )


def main():
    """CLI entry point for testing."""
    import sys

    # Example usage
    if len(sys.argv) < 2:
        print("Usage: python main.py '<problem hypothesis>'")
        print("\nExample:")
        print("  python main.py 'construction equipment tracking'")
        sys.exit(1)

    problem = sys.argv[1]

    agent = ValidationAgent()
    result = agent.validate_opportunity(
        problem_hypothesis=problem,
        target_subreddits=["construction", "contractors", "BuildingTech"],
        competitors=["ToolTracker", "EquipmentManager"],
        timeframe="month"
    )

    print("\n" + "="*80)
    print("VALIDATION REPORT")
    print("="*80)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
