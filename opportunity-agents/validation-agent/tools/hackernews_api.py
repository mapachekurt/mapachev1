"""HackerNews API integration."""
import requests
from typing import List, Dict
from datetime import datetime, timedelta


class HackerNewsAPI:
    """Analyze HackerNews discussions for pain points."""

    def __init__(self):
        """Initialize HackerNews API client."""
        self.base_url = "https://hn.algolia.com/api/v1"

    def search_discussions(
        self,
        query: str,
        days_back: int = 7,
        max_results: int = 100
    ) -> Dict:
        """
        Search HackerNews for discussions.

        Args:
            query: Search term
            days_back: Number of days to search back
            max_results: Maximum results

        Returns:
            {
                "story_count": int,
                "comment_count": int,
                "stories": List[Dict],
                "top_comments": List[Dict]
            }
        """
        # Calculate timestamp
        timestamp = int((datetime.now() - timedelta(days=days_back)).timestamp())

        params = {
            "query": query,
            "tags": "story",
            "numericFilters": f"created_at_i>{timestamp}",
            "hitsPerPage": max_results
        }

        try:
            response = requests.get(f"{self.base_url}/search", params=params)
            response.raise_for_status()
            data = response.json()

            stories = []
            for hit in data.get("hits", []):
                stories.append({
                    "title": hit.get("title", ""),
                    "url": hit.get("url", ""),
                    "hn_url": f"https://news.ycombinator.com/item?id={hit['objectID']}",
                    "points": hit.get("points", 0),
                    "num_comments": hit.get("num_comments", 0),
                    "created_at": datetime.fromtimestamp(hit["created_at_i"]).isoformat(),
                    "author": hit.get("author", "")
                })

            # Search for comments
            comment_params = {
                "query": query,
                "tags": "comment",
                "numericFilters": f"created_at_i>{timestamp}",
                "hitsPerPage": 50
            }

            comment_response = requests.get(f"{self.base_url}/search", params=comment_params)
            comment_data = comment_response.json()

            comments = []
            for hit in comment_data.get("hits", []):
                if hit.get("comment_text"):
                    comments.append({
                        "text": hit["comment_text"],
                        "author": hit.get("author", ""),
                        "points": hit.get("points", 0),
                        "created_at": datetime.fromtimestamp(hit["created_at_i"]).isoformat(),
                        "url": f"https://news.ycombinator.com/item?id={hit['objectID']}"
                    })

            return {
                "story_count": len(stories),
                "comment_count": len(comments),
                "stories": stories,
                "top_comments": sorted(comments, key=lambda x: x["points"], reverse=True)[:20]
            }

        except Exception as e:
            print(f"Error searching HackerNews: {e}")
            return {
                "story_count": 0,
                "comment_count": 0,
                "stories": [],
                "top_comments": [],
                "error": str(e)
            }

    def get_trending_tech_topics(self, limit: int = 20) -> List[Dict]:
        """Get current trending topics on HackerNews."""
        try:
            response = requests.get(f"{self.base_url}/search?tags=front_page&hitsPerPage={limit}")
            response.raise_for_status()
            data = response.json()

            trending = []
            for hit in data.get("hits", []):
                trending.append({
                    "title": hit.get("title", ""),
                    "url": f"https://news.ycombinator.com/item?id={hit['objectID']}",
                    "points": hit.get("points", 0),
                    "num_comments": hit.get("num_comments", 0)
                })

            return trending

        except Exception as e:
            print(f"Error getting trending topics: {e}")
            return []
