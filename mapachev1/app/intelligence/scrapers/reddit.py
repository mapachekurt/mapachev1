"""Reddit scraper for AI/ML subreddits."""

import logging
import os
from datetime import datetime
from typing import Any

import requests

from ..utils.models import ContentType, RawContent, SourceType
from .base import BaseScraper

logger = logging.getLogger(__name__)


class RedditScraper(BaseScraper):
    """Scraper for Reddit AI/ML subreddits."""

    SUBREDDITS = [
        "MachineLearning",
        "artificial",
        "learnmachinelearning",
        "LanguageTechnology",
        "LocalLLaMA",
        "OpenAI",
        "ClaudeAI",
    ]

    def __init__(self) -> None:
        """Initialize the Reddit scraper."""
        super().__init__("reddit")
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.config.user_agent})
        self._authenticate()

    def _authenticate(self) -> None:
        """Authenticate with Reddit OAuth."""
        # Get credentials from environment (Secret Manager in production)
        client_id = os.environ.get("REDDIT_CLIENT_ID", "")
        client_secret = os.environ.get("REDDIT_CLIENT_SECRET", "")

        if not client_id or not client_secret:
            logger.warning("Reddit credentials not found. Using public API.")
            return

        # OAuth authentication
        auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
        data = {
            "grant_type": "client_credentials",
        }

        response = requests.post(
            "https://www.reddit.com/api/v1/access_token",
            auth=auth,
            data=data,
            headers={"User-Agent": self.config.user_agent},
        )

        if response.status_code == 200:
            token = response.json()["access_token"]
            self.session.headers.update({"Authorization": f"Bearer {token}"})
            logger.info("Authenticated with Reddit")
        else:
            logger.warning("Reddit authentication failed. Using public API.")

    def get_subreddit_posts(
        self, subreddit: str, limit: int = 25
    ) -> list[dict[str, Any]]:
        """Get recent posts from a subreddit.

        Args:
            subreddit: Subreddit name
            limit: Maximum number of posts

        Returns:
            List of post data
        """
        url = f"https://oauth.reddit.com/r/{subreddit}/hot.json"
        params = {"limit": limit}

        try:
            response = self.session.get(
                url, params=params, timeout=self.config.timeout
            )
            response.raise_for_status()
            data = response.json()
            return [child["data"] for child in data["data"]["children"]]
        except Exception as e:
            logger.error(f"Error fetching r/{subreddit}: {e}")
            return []

    def scrape(self) -> list[RawContent]:
        """Scrape Reddit AI/ML subreddits.

        Returns:
            List of raw content items
        """
        logger.info(f"Scraping {len(self.SUBREDDITS)} Reddit subreddits...")

        raw_contents: list[RawContent] = []

        for subreddit in self.SUBREDDITS:
            posts = self.get_subreddit_posts(subreddit)

            for post in posts:
                # Extract post details
                title = post.get("title", "Untitled")
                url = post.get("url", "")
                selftext = post.get("selftext", "")
                score = post.get("score", 0)
                num_comments = post.get("num_comments", 0)

                # Combine title and selftext for content
                content = f"{title}\n\n{selftext}" if selftext else title

                # Create raw content
                raw_content = RawContent(
                    source=SourceType.REDDIT,
                    content_type=ContentType.DISCUSSION,
                    title=title,
                    url=url,
                    content=content,
                    metadata={
                        "subreddit": subreddit,
                        "score": score,
                        "num_comments": num_comments,
                        "author": post.get("author", "unknown"),
                        "created_utc": post.get("created_utc", 0),
                        "permalink": f"https://reddit.com{post.get('permalink', '')}",
                    },
                    scraped_at=datetime.utcnow(),
                )

                raw_contents.append(raw_content)

        logger.info(f"Scraped {len(raw_contents)} posts from Reddit")
        return raw_contents


def main() -> None:
    """Main entry point for Cloud Run Job."""
    logging.basicConfig(level=logging.INFO)

    scraper = RedditScraper()
    result = scraper.run()

    logger.info(f"Scraper result: {result}")


if __name__ == "__main__":
    main()
