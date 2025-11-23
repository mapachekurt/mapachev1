"""Create Linear project for validated opportunity."""
import os
import requests
from typing import Dict, List
from datetime import datetime, timedelta


class LinearCreator:
    """Create Linear projects with issues based on opportunity analysis."""

    def __init__(self):
        """Initialize Linear API client."""
        self.linear_api_key = os.getenv("LINEAR_API_KEY")
        self.linear_endpoint = "https://api.linear.app/graphql"
        self.team_id = os.getenv("LINEAR_TEAM_ID")

    def create_project(self, opportunity: Dict) -> Dict:
        """
        Create Linear project with issues based on opportunity analysis.

        Args:
            opportunity: Combined validation + opportunity analysis result

        Returns:
            {
                "project_id": str,
                "project_url": str,
                "issues": List[Dict]
            }
        """
        if not self.linear_api_key:
            print("⚠️  LINEAR_API_KEY not set, skipping project creation")
            return {
                "project_id": None,
                "project_url": None,
                "issues": [],
                "error": "Linear API key not configured"
            }

        print(f"📋 Creating Linear project for: {opportunity['input']['problem'][:50]}...")

        # Extract data
        problem = opportunity["input"]["problem"]
        validation = opportunity["validation"]
        opp_analysis = opportunity["opportunity"]

        try:
            # Create project
            project = self._create_linear_project(problem, opportunity)

            if not project:
                return {
                    "project_id": None,
                    "project_url": None,
                    "issues": [],
                    "error": "Failed to create project"
                }

            print(f"✓ Project created: {project['url']}")

            # Create issues
            print("📝 Creating project issues...")
            issues = self._create_project_issues(project["id"], opportunity)

            print(f"✓ Created {len(issues)} issues")

            return {
                "project_id": project["id"],
                "project_url": project["url"],
                "project_name": project["name"],
                "issues": issues
            }

        except Exception as e:
            print(f"Error creating Linear project: {e}")
            return {
                "project_id": None,
                "project_url": None,
                "issues": [],
                "error": str(e)
            }

    def _create_linear_project(self, problem: str, opportunity: Dict) -> Dict:
        """Create the Linear project."""
        project_mutation = """
        mutation CreateProject($input: ProjectCreateInput!) {
          projectCreate(input: $input) {
            project {
              id
              url
              name
            }
          }
        }
        """

        project_data = {
            "name": f"Build: {problem[:60]}",
            "description": self._generate_project_description(opportunity),
            "teamIds": [self.team_id] if self.team_id else [],
            "startDate": datetime.now().isoformat(),
            "targetDate": (datetime.now() + timedelta(days=90)).isoformat()
        }

        try:
            response = requests.post(
                self.linear_endpoint,
                json={
                    "query": project_mutation,
                    "variables": {"input": project_data}
                },
                headers={
                    "Authorization": self.linear_api_key,
                    "Content-Type": "application/json"
                }
            )

            response.raise_for_status()
            data = response.json()

            if "errors" in data:
                print(f"Linear API errors: {data['errors']}")
                return None

            return data["data"]["projectCreate"]["project"]

        except Exception as e:
            print(f"Error creating project: {e}")
            return None

    def _generate_project_description(self, opportunity: Dict) -> str:
        """Generate comprehensive project description."""
        val = opportunity["validation"]
        opp = opportunity["opportunity"]

        description = f"""## Problem
{opportunity['input']['problem']}

## Validation Evidence (Score: {val.get('validation_score', 0)}/100)
- Total Mentions: {val.get('evidence', {}).get('mention_count', 0)}
- Frustration Score: {val.get('evidence', {}).get('frustration_score', 0)}/100
- Urgency Score: {val.get('evidence', {}).get('urgency_score', 0)}/100

### Top User Quotes
"""

        # Add top quotes
        for i, quote in enumerate(val.get('evidence', {}).get('top_quotes', [])[:3], 1):
            description += f'{i}. "{quote}"\n'

        description += f"""
## Market Opportunity (Score: {opp.get('opportunity_score', 0)}/100)
- TAM: ${opp.get('market_size', {}).get('TAM_dollars', 0):,}
- SAM: ${opp.get('market_size', {}).get('SAM_dollars', 0):,}
- SOM (3-year target): ${opp.get('market_size', {}).get('SOM_dollars', 0):,}
- Growth Rate: {opp.get('market_size', {}).get('growth_rate_cagr', 0)*100:.1f}% CAGR

## Build Strategy
**Recommendation:** {opp.get('build_strategy', {}).get('recommendation', 'TBD').upper()}

**Rationale:** {opp.get('build_strategy', {}).get('rationale', 'See analysis')}

**Time Savings:** {opp.get('build_strategy', {}).get('estimated_time_savings', 'N/A')}
**Cost Savings:** {opp.get('build_strategy', {}).get('estimated_cost_savings', 'N/A')}

## Competitor Weaknesses
"""

        # Add competitor weaknesses
        comp_weaknesses = val.get('evidence', {}).get('competitor_weaknesses', {})
        for comp, data in list(comp_weaknesses.items())[:3]:
            description += f"\n### {comp}\n"
            for complaint in data.get('complaints', [])[:3]:
                description += f"- {complaint}\n"

        description += f"""
## Strategic Recommendation
{opp.get('strategic_recommendation', 'See full analysis')}

## Validation Recommendation
{val.get('recommendation', 'See full analysis')}
"""

        return description

    def _create_project_issues(self, project_id: str, opportunity: Dict) -> List[Dict]:
        """Create issues based on build strategy."""
        strategy = opportunity["opportunity"].get("build_strategy", {})
        issues = []

        # Issue 1: Research & Planning
        issues.append(self._create_issue(
            project_id,
            "📋 Research & Requirements Definition",
            f"""Define technical requirements based on validation evidence.

**Deliverables:**
- Technical specification document
- Architecture diagram
- Technology stack decision
- Database schema design

**Key Requirements from Validation:**
{self._format_requirements(opportunity)}

**Acceptance Criteria:**
- [ ] Technical spec reviewed and approved
- [ ] Architecture diagram created
- [ ] Tech stack selected and documented
- [ ] Database schema designed
""",
            priority=1
        ))

        # Issue 2: OSS Fork/Setup (if applicable)
        if strategy.get("recommendation") in ["fork", "hybrid"]:
            selected_project = strategy.get("selected_project", {})
            issues.append(self._create_issue(
                project_id,
                f"🔧 Fork & Setup: {selected_project.get('name', 'OSS Project')}",
                f"""Fork the selected open source project and set up development environment.

**OSS Project:** {selected_project.get('url', 'TBD')}
**License:** {selected_project.get('license', 'Unknown')}
**Stars:** {selected_project.get('stars', 0)}

**Steps:**
1. Fork repository to our organization
2. Set up CI/CD pipeline
3. Configure development environment
4. Remove unnecessary features
5. Add custom branding
6. Update documentation

**Acceptance Criteria:**
- [ ] Repository forked and configured
- [ ] CI/CD pipeline working
- [ ] Dev environment documented
- [ ] Unnecessary features removed
- [ ] Custom branding applied
""",
                priority=1
            ))

        # Issue 3: MVP Development
        issues.append(self._create_issue(
            project_id,
            "🚀 Build MVP - Core Features",
            f"""Implement minimum viable product with core features based on validation evidence.

**Must-Have Features:**
{self._format_core_features(opportunity)}

**Build Strategy:** {strategy.get('recommendation', 'TBD').upper()}

**Acceptance Criteria:**
- [ ] All core features implemented
- [ ] Unit tests written (>80% coverage)
- [ ] Integration tests passing
- [ ] Performance benchmarks met
- [ ] Security audit completed
""",
            priority=2
        ))

        # Issue 4: Beta Testing
        issues.append(self._create_issue(
            project_id,
            "🧪 Beta Testing with Target Users",
            """Recruit and run beta testing program with target users.

**Goals:**
- Validate product-market fit
- Identify usability issues
- Gather feature feedback
- Test at scale

**Channels for Recruitment:**
- Reddit communities from validation
- Direct outreach to users who complained about competitors
- ProductHunt beta list
- LinkedIn outreach

**Success Criteria:**
- [ ] 10-20 beta users recruited
- [ ] 80%+ retention after 2 weeks
- [ ] Average rating 4+/5
- [ ] All P0 bugs fixed
- [ ] Feature feedback documented
""",
            priority=3
        ))

        # Issue 5: Launch Preparation
        issues.append(self._create_issue(
            project_id,
            "🎯 Launch Preparation & Go-to-Market",
            """Prepare for public launch across multiple channels.

**Launch Channels:**
- ProductHunt
- HackerNews
- Reddit (target communities from validation)
- LinkedIn
- Industry publications

**Deliverables:**
- [ ] Landing page with social proof
- [ ] Demo video (2-3 min)
- [ ] Launch post template
- [ ] Email drip campaign
- [ ] Analytics & tracking setup
- [ ] Customer support system

**Launch Success Metrics:**
- 100+ signups in week 1
- 20+ paying customers in month 1
- 4+ star average rating
""",
            priority=4
        ))

        return [issue for issue in issues if issue is not None]

    def _create_issue(
        self,
        project_id: str,
        title: str,
        description: str,
        priority: int
    ) -> Dict:
        """Create a single Linear issue."""
        issue_mutation = """
        mutation CreateIssue($input: IssueCreateInput!) {
          issueCreate(input: $input) {
            issue {
              id
              url
              identifier
              title
            }
          }
        }
        """

        try:
            response = requests.post(
                self.linear_endpoint,
                json={
                    "query": issue_mutation,
                    "variables": {
                        "input": {
                            "projectId": project_id,
                            "title": title,
                            "description": description,
                            "priority": priority,
                            "teamId": self.team_id
                        }
                    }
                },
                headers={
                    "Authorization": self.linear_api_key,
                    "Content-Type": "application/json"
                }
            )

            response.raise_for_status()
            data = response.json()

            if "errors" in data:
                print(f"Error creating issue '{title}': {data['errors']}")
                return None

            return data["data"]["issueCreate"]["issue"]

        except Exception as e:
            print(f"Error creating issue '{title}': {e}")
            return None

    def _format_requirements(self, opportunity: Dict) -> str:
        """Format key requirements from validation evidence."""
        quotes = opportunity["validation"].get("evidence", {}).get("top_quotes", [])
        if not quotes:
            return "- See validation evidence"

        reqs = []
        for quote in quotes[:5]:
            reqs.append(f"- {quote[:100]}...")

        return "\n".join(reqs)

    def _format_core_features(self, opportunity: Dict) -> str:
        """Extract core features from analysis."""
        # This would ideally extract features from the validation evidence
        # For now, return a placeholder
        return """- Feature 1: [Extract from validation evidence]
- Feature 2: [Extract from competitor gaps]
- Feature 3: [Extract from user quotes]
- Feature 4: [Based on market trends]
- Feature 5: [Differentiation opportunity]

**Note:** Review validation evidence and competitive analysis to define specific features.
"""
