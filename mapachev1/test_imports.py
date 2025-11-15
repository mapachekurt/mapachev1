#!/usr/bin/env python3
"""
Test script to verify agent imports work correctly
"""

import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

def test_root_orchestrator():
    """Test importing root orchestrator"""
    try:
        from app.agent import agent, root_orchestrator
        print("✓ Root orchestrator imported successfully")
        print(f"  - Agent name: {root_orchestrator.name}")
        print(f"  - Model: {root_orchestrator.model}")
        print(f"  - Sub-agents: {len(root_orchestrator.sub_agents)}")
        return True
    except Exception as e:
        print(f"✗ Failed to import root orchestrator: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_division_coordinators():
    """Test importing division coordinators"""
    divisions = [
        "executivestrategydivision",
        "securitylegaldivision",
        "technologyinfrastructuredivision",
        "financeaccountingdivision",
        "peopleculturedivision",
        "revenueoperationsdivision",
        "engineeringproductdivision",
        "customersuccessdivision",
        "operationssupplychaindivision",
        "dataanalyticsdivision",
        "integrationinnovationdivision"
    ]

    success_count = 0
    for division in divisions:
        try:
            module = __import__(f"app.agents.coordinators.{division}", fromlist=[division])
            agent = getattr(module, division)
            print(f"✓ {division}")
            success_count += 1
        except Exception as e:
            print(f"✗ {division}: {e}")

    print(f"\nDivision Coordinators: {success_count}/{len(divisions)} imported successfully")
    return success_count == len(divisions)


def test_sample_teams():
    """Test importing sample team agents"""
    teams = [
        "executiveleadershipteam",
        "legalteam",
        "cloudinfrastructureteam",
        "financialplanningteam",
        "talentacquisitionteam",
        "enterprisesalesteam",
        "productmanagementteam",
        "customersuccessteam",
        "supplychainteam",
        "dataarchitectureteam"
    ]

    success_count = 0
    for team in teams:
        try:
            module = __import__(f"app.agents.teams.{team}", fromlist=[team])
            agent = getattr(module, team)
            print(f"✓ {team}")
            success_count += 1
        except Exception as e:
            print(f"✗ {team}: {e}")

    print(f"\nTeam Agents: {success_count}/{len(teams)} imported successfully")
    return success_count == len(teams)


def test_sample_specialists():
    """Test importing sample specialist agents"""
    specialists = [
        ("executivestrategydivision", "agent_001"),
        ("securitylegaldivision", "agent_013"),
        ("technologyinfrastructuredivision", "agent_020"),
        ("financeaccountingdivision", "agent_021"),
        ("peopleculturedivision", "agent_041"),
        ("revenueoperationsdivision", "agent_061"),
        ("engineeringproductdivision", "agent_097"),
        ("customersuccessdivision", "agent_100"),
        ("operationssupplychaindivision", "agent_101"),
        ("dataanalyticsdivision", "agent_153")
    ]

    success_count = 0
    for division, specialist in specialists:
        try:
            module = __import__(f"app.agents.specialists.{division}.{specialist}", fromlist=[specialist])
            agent = getattr(module, specialist)
            print(f"✓ {division}/{specialist}")
            success_count += 1
        except Exception as e:
            print(f"✗ {division}/{specialist}: {e}")

    print(f"\nSpecialist Agents: {success_count}/{len(specialists)} imported successfully")
    return success_count == len(specialists)


def main():
    """Run all tests"""
    print("=== Testing Agent Imports ===\n")

    results = []

    print("--- Testing Root Orchestrator ---")
    results.append(("Root Orchestrator", test_root_orchestrator()))

    print("\n--- Testing Division Coordinators ---")
    results.append(("Division Coordinators", test_division_coordinators()))

    print("\n--- Testing Sample Team Agents ---")
    results.append(("Team Agents", test_sample_teams()))

    print("\n--- Testing Sample Specialist Agents ---")
    results.append(("Specialist Agents", test_sample_specialists()))

    print("\n=== Test Summary ===")
    for name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {name}")

    all_passed = all(success for _, success in results)
    if all_passed:
        print("\n✓ All imports working correctly!")
        return 0
    else:
        print("\n✗ Some imports failed. Check errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
