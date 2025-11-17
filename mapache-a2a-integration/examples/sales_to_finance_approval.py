"""
Sales to Finance Approval Workflow

This example demonstrates a workflow where:
1. Sales agent identifies a large deal requiring approval
2. Sales agent sends request to Finance agent via A2A
3. Finance agent checks budget using MCP tool
4. Finance agent approves/denies and responds via A2A
5. Sales agent proceeds based on response
"""

import sys
from pathlib import Path
import asyncio

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.core import RemoteAgent


async def sales_to_finance_approval_workflow():
    """Execute the sales to finance approval workflow"""

    print("="*60)
    print("Sales to Finance Approval Workflow")
    print("="*60)
    print()

    # Step 1: Sales agent identifies large deal
    print("Step 1: Sales agent identifies large deal requiring approval")
    deal = {
        "deal_id": "DEAL-12345",
        "customer": "Acme Corporation",
        "amount": 150000,
        "term": "12 months",
        "discount": 15,
        "account_executive": "account_executive_1_1_1"
    }
    print(f"  Deal: {deal['deal_id']}")
    print(f"  Customer: {deal['customer']}")
    print(f"  Amount: ${deal['amount']:,}")
    print(f"  Discount: {deal['discount']}%")
    print()

    # Step 2: Connect to finance agent
    print("Step 2: Connecting to Finance agent...")
    try:
        finance_agent = RemoteAgent("cfo")
        print(f"  ✓ Connected to Finance agent")
    except Exception as e:
        print(f"  ✗ Could not connect to Finance agent: {e}")
        print("  Note: Ensure registry is running and agents are registered")
        return
    print()

    # Step 3: Submit approval request
    print("Step 3: Submitting approval request to Finance...")
    approval_request = {
        "type": "deal_approval",
        "deal": deal,
        "reason": "Deal exceeds $100k threshold",
        "requested_by": deal["account_executive"],
        "urgency": "high"
    }

    try:
        response = finance_agent.send_message(
            f"Requesting approval for {deal['customer']} deal: ${deal['amount']:,}",
            context=approval_request
        )
        print(f"  ✓ Request sent")
        print(f"  Response: {response}")
    except Exception as e:
        print(f"  ✗ Error sending request: {e}")
        response = {"error": str(e)}
    print()

    # Step 4: Finance checks budget (simulated)
    print("Step 4: Finance agent reviews request...")
    print("  - Checking budget availability")
    print("  - Reviewing discount policy")
    print("  - Assessing deal terms")
    print()

    # Step 5: Process response
    print("Step 5: Processing finance response...")
    if "error" in response:
        print(f"  ✗ Error: {response['error']}")
    elif response.get("status") == "approved":
        print(f"  ✓ Deal APPROVED")
        print(f"  Comments: {response.get('comments', 'N/A')}")
        print()
        print("Step 6: Sales agent proceeds with deal")
        print("  - Sending contract to customer")
        print("  - Updating CRM")
        print("  - Notifying sales team")
    else:
        print(f"  ✗ Deal DENIED")
        print(f"  Reason: {response.get('reason', 'N/A')}")
        print()
        print("Step 6: Sales agent takes corrective action")
        print("  - Revising deal terms")
        print("  - Escalating to VP Sales")

    print()
    print("="*60)
    print("Workflow Complete")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(sales_to_finance_approval_workflow())
