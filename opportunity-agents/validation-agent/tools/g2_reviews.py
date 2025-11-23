"""G2 review scraping for competitor analysis."""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time


class G2Reviews:
    """Scrape competitor reviews from G2."""

    def __init__(self):
        """Initialize G2 scraper."""
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def scrape_product_reviews(
        self,
        product_slug: str,
        max_reviews: int = 50
    ) -> Dict:
        """
        Scrape reviews for a product on G2.

        Args:
            product_slug: G2 product slug (e.g., "tooltracker")
            max_reviews: Maximum number of reviews to scrape

        Returns:
            {
                "product": str,
                "average_rating": float,
                "total_reviews": int,
                "reviews": List[Dict],
                "common_complaints": List[str]
            }
        """
        # Note: This is a simplified implementation
        # In production, you'd need to handle pagination, rate limiting, etc.
        # Consider using G2's official API if available

        url = f"https://www.g2.com/products/{product_slug}/reviews"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            reviews = []
            review_elements = soup.find_all('div', class_='paper paper--white paper--box', limit=max_reviews)

            for review_elem in review_elements:
                # Extract review data (structure may vary)
                try:
                    rating_elem = review_elem.find('div', class_='stars')
                    rating = len(rating_elem.find_all('div', class_='star')) if rating_elem else 0

                    title_elem = review_elem.find('h3')
                    title = title_elem.text.strip() if title_elem else ""

                    text_elem = review_elem.find('div', class_='review-text')
                    text = text_elem.text.strip() if text_elem else ""

                    # Extract pros/cons
                    pros_elem = review_elem.find('div', {'data-test-id': 'pros'})
                    cons_elem = review_elem.find('div', {'data-test-id': 'cons'})

                    pros = pros_elem.text.strip() if pros_elem else ""
                    cons = cons_elem.text.strip() if cons_elem else ""

                    reviews.append({
                        "rating": rating,
                        "title": title,
                        "text": text,
                        "pros": pros,
                        "cons": cons
                    })
                except Exception as e:
                    print(f"Error parsing review: {e}")
                    continue

                time.sleep(0.5)  # Rate limiting

            # Calculate average rating
            avg_rating = sum(r["rating"] for r in reviews) / len(reviews) if reviews else 0

            # Extract common complaints from cons
            all_cons = " ".join([r["cons"] for r in reviews if r["cons"]])

            return {
                "product": product_slug,
                "average_rating": round(avg_rating, 2),
                "total_reviews": len(reviews),
                "reviews": reviews,
                "all_complaints": all_cons
            }

        except Exception as e:
            print(f"Error scraping G2 reviews: {e}")
            return {
                "product": product_slug,
                "average_rating": 0,
                "total_reviews": 0,
                "reviews": [],
                "all_complaints": "",
                "error": str(e)
            }

    def analyze_competitor_weaknesses(self, reviews_data: Dict) -> List[str]:
        """Extract top competitor weaknesses from reviews."""
        if not reviews_data.get("reviews"):
            return []

        # Count mentions of common complaint themes
        complaint_keywords = {
            "pricing": ["expensive", "cost", "price", "pricing"],
            "usability": ["difficult", "confusing", "complex", "hard to use"],
            "support": ["support", "customer service", "response time"],
            "features": ["missing", "lack", "doesn't have", "need"],
            "bugs": ["bug", "crash", "error", "broken"],
            "performance": ["slow", "lag", "performance", "speed"]
        }

        complaint_counts = {category: 0 for category in complaint_keywords}

        for review in reviews_data["reviews"]:
            cons_text = review.get("cons", "").lower()
            for category, keywords in complaint_keywords.items():
                if any(kw in cons_text for kw in keywords):
                    complaint_counts[category] += 1

        # Return top complaints
        sorted_complaints = sorted(
            complaint_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            f"{category}: {count} mentions"
            for category, count in sorted_complaints[:5]
            if count > 0
        ]
