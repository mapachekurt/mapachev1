"""
Product Launch Workflow

Demonstrates complex multi-team coordination:
1. Product Director agent initiates launch
2. Coordinates with Engineering, Marketing, Sales via A2A
3. Each department provides updates asynchronously
4. Product Director aggregates status
5. CEO agent receives summary report
"""

import sys
from pathlib import Path
import asyncio
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.core import RemoteAgent, discover_agents_by_department


async def product_launch_workflow():
    """Execute the product launch workflow"""

    print("="*60)
    print("Product Launch Workflow - AI Analytics Feature")
    print("="*60)
    print()

    # Define the product launch
    launch = {
        "feature": "AI Analytics Dashboard",
        "launch_date": "2024-03-01",
        "product_director": "director_product_1",
        "teams_involved": ["engineering", "marketing", "sales", "customer_success"],
        "status": "planning"
    }

    print(f"Feature: {launch['feature']}")
    print(f"Launch Date: {launch['launch_date']}")
    print(f"Teams Involved: {', '.join(launch['teams_involved'])}")
    print()

    # Step 1: Product Director initiates launch
    print("Step 1: Product Director initiates launch planning")
    print("  - Creating launch plan")
    print("  - Identifying stakeholders")
    print("  - Setting milestones")
    print()

    # Step 2: Connect to key stakeholders
    print("Step 2: Connecting to team leads...")
    team_agents = {}
    for team in ["vp_engineering", "vp_marketing", "vp_sales", "vp_customer_success"]:
        try:
            agent = RemoteAgent(team)
            team_agents[team] = agent
            print(f"  ✓ Connected to {team}")
        except Exception as e:
            print(f"  ✗ Could not connect to {team}: {e}")
    print()

    # Step 3: Engineering updates
    print("Step 3: Engineering provides development status...")
    print("  Engineering VP:")
    print("    - Feature development: 75% complete")
    print("    - QA testing: 50% complete")
    print("    - Performance testing: Pending")
    print("    - Estimated completion: 2024-02-20")
    print("    - Blockers: None")
    print()

    # Step 4: Marketing updates
    print("Step 4: Marketing provides campaign status...")
    print("  Marketing VP:")
    print("    - Landing page: Ready")
    print("    - Blog posts: 3/5 complete")
    print("    - Social media plan: Ready")
    print("    - Email campaign: Draft ready")
    print("    - Demo video: In production")
    print()

    # Step 5: Sales updates
    print("Step 5: Sales provides enablement status...")
    print("  Sales VP:")
    print("    - Sales training: Scheduled for 2024-02-25")
    print("    - Demo environment: Ready")
    print("    - Sales collateral: 80% complete")
    print("    - Customer prospects: 15 identified")
    print()

    # Step 6: Customer Success updates
    print("Step 6: Customer Success provides readiness status...")
    print("  Customer Success VP:")
    print("    - Support documentation: In progress")
    print("    - Training materials: Ready")
    print("    - Customer communications: Draft ready")
    print("    - Success team training: Scheduled")
    print()

    # Step 7: Product Director aggregates status
    print("Step 7: Product Director aggregates launch readiness...")
    print()
    print("  Launch Readiness Dashboard:")
    print("  ┌─────────────────────┬──────────┬──────────┐")
    print("  │ Team                │ Status   │ Progress │")
    print("  ├─────────────────────┼──────────┼──────────┤")
    print("  │ Engineering         │ On Track │   75%    │")
    print("  │ Marketing           │ On Track │   85%    │")
    print("  │ Sales               │ On Track │   80%    │")
    print("  │ Customer Success    │ On Track │   70%    │")
    print("  └─────────────────────┴──────────┴──────────┘")
    print()
    print("  Overall Status: GREEN - On track for 2024-03-01 launch")
    print()

    # Step 8: Report to CEO
    print("Step 8: Sending executive summary to CEO...")
    try:
        ceo = RemoteAgent("ceo")
        summary = {
            "feature": launch['feature'],
            "launch_date": launch['launch_date'],
            "status": "GREEN",
            "overall_progress": "78%",
            "risks": "None identified",
            "next_steps": [
                "Complete engineering development by 2024-02-20",
                "Finalize marketing content by 2024-02-25",
                "Conduct sales training on 2024-02-25",
                "Go-live on 2024-03-01"
            ]
        }
        response = ceo.send_message(
            f"Product Launch Update: {launch['feature']}",
            context=summary
        )
        print(f"  ✓ Executive summary sent to CEO")
    except Exception as e:
        print(f"  (Simulated) Executive summary sent to CEO")
    print()

    # Step 9: Launch day coordination
    print("Step 9: Launch day coordination (2024-03-01)...")
    print("  06:00 - Engineering deploys feature to production")
    print("  08:00 - Customer Success activates for early access customers")
    print("  09:00 - Marketing launches campaign")
    print("  10:00 - Sales enabled to pitch feature")
    print("  12:00 - PR announcement goes live")
    print("  14:00 - Monitor metrics and customer feedback")
    print()

    # Step 10: Post-launch metrics
    print("Step 10: Post-launch metrics (Day 1)...")
    print("  Launch Metrics:")
    print("    - Website visitors: 5,200")
    print("    - Demo requests: 45")
    print("    - Early adopters: 12")
    print("    - Support tickets: 3 (all resolved)")
    print("    - Social media reach: 50,000")
    print()

    print("="*60)
    print("Product Launch Workflow Complete")
    print(f"Feature '{launch['feature']}' successfully launched!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(product_launch_workflow())
