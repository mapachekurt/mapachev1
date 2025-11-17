"""
Hiring Workflow

Demonstrates cross-functional collaboration:
1. Hiring Manager agent posts job requisition
2. Recruiter agent sources candidates
3. Recruiter coordinates with Hiring Manager via A2A
4. Schedule interviews through Calendar agent
5. HR Ops agent handles offer via A2A coordination
"""

import sys
from pathlib import Path
import asyncio

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.core import RemoteAgent


async def hiring_workflow():
    """Execute the hiring workflow"""

    print("="*60)
    print("Hiring Workflow - Senior Software Engineer")
    print("="*60)
    print()

    # Step 1: Hiring Manager posts job requisition
    print("Step 1: Hiring Manager posts job requisition")
    job_req = {
        "req_id": "REQ-2024-123",
        "title": "Senior Software Engineer",
        "department": "engineering",
        "hiring_manager": "engineering_manager_1_1",
        "level": "L5",
        "headcount": 1,
        "location": "Remote",
        "skills_required": [
            "python",
            "distributed_systems",
            "cloud_architecture"
        ]
    }
    print(f"  Position: {job_req['title']}")
    print(f"  Department: {job_req['department']}")
    print(f"  Hiring Manager: {job_req['hiring_manager']}")
    print(f"  Skills: {', '.join(job_req['skills_required'])}")
    print()

    # Step 2: Connect to recruiter
    print("Step 2: Connecting to Recruiter agent...")
    try:
        recruiter = RemoteAgent("recruiter_1_1")
        print("  ✓ Connected to Recruiter")
    except Exception as e:
        print(f"  ✗ Could not connect: {e}")
        print("  Note: This is a demo - agents need to be deployed")
        recruiter = None
    print()

    # Step 3: Recruiter sources candidates
    print("Step 3: Recruiter sources candidates...")
    print("  - Searching internal database")
    print("  - Posting to job boards")
    print("  - Reaching out to passive candidates")
    print()
    print("  Found 5 qualified candidates:")
    candidates = [
        {"name": "Alice Johnson", "match_score": 95},
        {"name": "Bob Smith", "match_score": 88},
        {"name": "Carol White", "match_score": 85},
        {"name": "David Lee", "match_score": 82},
        {"name": "Eva Martinez", "match_score": 79},
    ]
    for candidate in candidates:
        print(f"    - {candidate['name']} (match: {candidate['match_score']}%)")
    print()

    # Step 4: Coordinate with Hiring Manager
    print("Step 4: Recruiter coordinates with Hiring Manager...")
    if recruiter:
        try:
            hiring_manager = RemoteAgent(job_req['hiring_manager'])
            response = hiring_manager.send_message(
                f"Found {len(candidates)} candidates for {job_req['title']}",
                context={"candidates": candidates, "req_id": job_req['req_id']}
            )
            print(f"  ✓ Hiring Manager response: {response}")
        except Exception as e:
            print(f"  ✗ Error: {e}")
    else:
        print("  (Simulated) Hiring Manager approves top 3 candidates for interviews")
    print()

    # Step 5: Schedule interviews
    print("Step 5: Scheduling interviews...")
    print("  - Coordinating calendars")
    print("  - Sending interview invites")
    print("  - Preparing interview questions")
    print()
    print("  Interviews scheduled:")
    print("    - Alice Johnson: Monday 2pm")
    print("    - Bob Smith: Tuesday 10am")
    print("    - Carol White: Wednesday 3pm")
    print()

    # Step 6: Conduct interviews and make decision
    print("Step 6: Conducting interviews...")
    print("  - Technical interviews completed")
    print("  - Team fit interviews completed")
    print("  - Hiring Manager decision: Offer to Alice Johnson")
    print()

    # Step 7: HR Ops handles offer
    print("Step 7: HR Ops agent prepares offer...")
    try:
        hr_ops = RemoteAgent("hr_ops_manager_1")
        offer = {
            "candidate": "Alice Johnson",
            "position": job_req['title'],
            "level": job_req['level'],
            "salary": 150000,
            "equity": 0.05,
            "start_date": "2024-02-01"
        }
        response = hr_ops.send_message(
            f"Prepare offer for {offer['candidate']}",
            context={"offer": offer, "req_id": job_req['req_id']}
        )
        print(f"  ✓ Offer prepared")
    except Exception as e:
        print(f"  (Simulated) Offer prepared and sent")
    print()

    print("Step 8: Candidate accepts offer")
    print("  - Offer letter sent")
    print("  - Candidate accepted")
    print("  - Onboarding scheduled")
    print()

    print("="*60)
    print("Hiring Workflow Complete")
    print("Requisition closed: REQ-2024-123")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(hiring_workflow())
