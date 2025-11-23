"""Find relevant OSS projects using GitHub API."""
import os
import requests
from typing import List, Dict
from datetime import datetime, timedelta


class OSSFinder:
    """Find and evaluate open source projects for forking opportunities."""

    def __init__(self):
        """Initialize GitHub API client."""
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.headers = {
            "Authorization": f"token {self.github_token}" if self.github_token else "",
            "Accept": "application/vnd.github.v3+json"
        }

    def find_relevant_projects(
        self,
        functionality: str,
        language: str = None,
        min_stars: int = 100
    ) -> List[Dict]:
        """
        Find open source projects matching desired functionality.

        Args:
            functionality: What you want to build (e.g., "equipment tracking system")
            language: Preferred language (e.g., "Python", "TypeScript")
            min_stars: Minimum GitHub stars

        Returns:
            List of relevant OSS projects with fork analysis
        """
        # Build search query
        query_parts = [functionality]
        if language:
            query_parts.append(f"language:{language}")
        query_parts.append(f"stars:>={min_stars}")

        query = " ".join(query_parts)

        try:
            # Search GitHub
            response = requests.get(
                "https://api.github.com/search/repositories",
                headers=self.headers,
                params={
                    "q": query,
                    "sort": "stars",
                    "order": "desc",
                    "per_page": 20
                }
            )
            response.raise_for_status()
            data = response.json()

            projects = []
            for repo in data.get("items", []):
                # Get additional details
                project_data = self._enrich_project_data(repo)
                # Analyze fork potential
                project_data = self._analyze_fork_potential(project_data)
                projects.append(project_data)

            # Sort by fork score
            projects.sort(key=lambda x: x.get("fork_score", 0), reverse=True)

            return projects[:10]  # Return top 10

        except Exception as e:
            print(f"Error searching GitHub: {e}")
            return []

    def _enrich_project_data(self, repo: Dict) -> Dict:
        """Enrich project data with additional metrics."""
        # Calculate activity score
        last_push = datetime.fromisoformat(repo["pushed_at"].replace("Z", "+00:00"))
        days_since_push = (datetime.now(last_push.tzinfo) - last_push).days

        # Get languages
        languages = []
        if repo.get("language"):
            languages.append(repo["language"])

        try:
            lang_response = requests.get(repo["languages_url"], headers=self.headers)
            if lang_response.ok:
                lang_data = lang_response.json()
                languages = list(lang_data.keys())
        except:
            pass

        # Get contributors count
        contributors_count = 0
        try:
            contrib_response = requests.get(
                repo["contributors_url"],
                headers=self.headers,
                params={"per_page": 1}
            )
            if contrib_response.ok and "Link" in contrib_response.headers:
                # Parse link header for total count
                link_header = contrib_response.headers["Link"]
                if "last" in link_header:
                    contributors_count = int(link_header.split("page=")[-1].split(">")[0])
                else:
                    contributors_count = len(contrib_response.json())
        except:
            pass

        return {
            "name": repo["name"],
            "full_name": repo["full_name"],
            "url": repo["html_url"],
            "description": repo.get("description", ""),
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "open_issues": repo["open_issues_count"],
            "language": repo.get("language", ""),
            "languages": languages,
            "license": repo.get("license", {}).get("spdx_id", "Unknown") if repo.get("license") else "Unknown",
            "created_at": repo["created_at"],
            "updated_at": repo["updated_at"],
            "pushed_at": repo["pushed_at"],
            "days_since_push": days_since_push,
            "contributors": contributors_count,
            "has_wiki": repo.get("has_wiki", False),
            "has_pages": repo.get("has_pages", False),
            "size_kb": repo.get("size", 0)
        }

    def _analyze_fork_potential(self, project: Dict) -> Dict:
        """Assess if project is good fork candidate."""
        fork_score = 0
        reasons = []

        # Active maintenance (+30 points)
        if project["days_since_push"] < 90:
            fork_score += 30
            reasons.append("Recently active (pushed within 90 days)")
        elif project["days_since_push"] < 180:
            fork_score += 20
            reasons.append("Moderately active")
        elif project["days_since_push"] < 365:
            fork_score += 10
        else:
            reasons.append("⚠️ Not recently updated")

        # Good documentation (+20 points)
        if project["has_wiki"] or project["has_pages"]:
            fork_score += 15
            reasons.append("Has documentation")
        if len(project.get("description", "")) > 50:
            fork_score += 5

        # Permissive license (+25 points)
        permissive_licenses = ["MIT", "Apache-2.0", "BSD-3-Clause", "BSD-2-Clause"]
        if project["license"] in permissive_licenses:
            fork_score += 25
            reasons.append(f"Permissive license ({project['license']})")
        elif project["license"] != "Unknown":
            fork_score += 10
        else:
            reasons.append("⚠️ License unclear")

        # Active community (+15 points)
        if project["contributors"] > 20:
            fork_score += 15
            reasons.append(f"Active community ({project['contributors']} contributors)")
        elif project["contributors"] > 10:
            fork_score += 10
        elif project["contributors"] > 5:
            fork_score += 5

        # Popularity (+10 points)
        if project["stars"] > 1000:
            fork_score += 10
            reasons.append(f"Popular ({project['stars']} stars)")
        elif project["stars"] > 500:
            fork_score += 7
        elif project["stars"] > 100:
            fork_score += 5

        project["fork_score"] = fork_score
        project["fork_reasons"] = reasons
        project["fork_recommendation"] = self._get_fork_recommendation(fork_score)

        return project

    def _get_fork_recommendation(self, score: int) -> str:
        """Get fork recommendation based on score."""
        if score >= 75:
            return "🟢 Excellent fork candidate"
        elif score >= 60:
            return "🟡 Good fork candidate with minor concerns"
        elif score >= 40:
            return "🟠 Risky fork - evaluate carefully"
        else:
            return "🔴 Not recommended for forking"

    def analyze_codebase_quality(self, repo_url: str) -> Dict:
        """
        Analyze code quality metrics.

        Args:
            repo_url: GitHub repository URL

        Returns:
            Code quality metrics
        """
        # Extract owner/repo from URL
        parts = repo_url.rstrip("/").split("/")
        if len(parts) < 2:
            return {"error": "Invalid repository URL"}

        owner, repo = parts[-2], parts[-1]

        try:
            # Get repository details
            response = requests.get(
                f"https://api.github.com/repos/{owner}/{repo}",
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()

            # Calculate quality score
            quality_score = 0

            # Has CI/CD
            # (Check for common CI files would require additional API calls)

            # Has tests
            # (Would need to check for test directories)

            # Code of conduct
            if data.get("has_code_of_conduct"):
                quality_score += 10

            # Contributing guidelines
            # (Would need additional check)

            # Issue templates
            if data.get("has_issues"):
                quality_score += 10

            return {
                "quality_score": quality_score,
                "has_issues": data.get("has_issues", False),
                "has_projects": data.get("has_projects", False),
                "has_wiki": data.get("has_wiki", False)
            }

        except Exception as e:
            return {"error": str(e)}
