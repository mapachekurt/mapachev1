#!/usr/bin/env python3
"""
Test Agent Builder Pro with RAG Capabilities

Comprehensive testing script for Agent Builder Pro including:
- Knowledge retrieval tests
- End-to-end agent building tests
- RAG source citation validation
- Production deployment verification

Usage:
    python test_rag_agent.py [--mode MODE]

Modes:
    - knowledge: Test RAG knowledge retrieval
    - agent: Test end-to-end agent building
    - production: Test production deployment
    - all: Run all tests (default)

Environment Variables:
    GOOGLE_CLOUD_PROJECT - GCP project ID (required)
    ADK_CORPUS_RESOURCE_NAME - RAG corpus resource name (required for RAG tests)

Example:
    export GOOGLE_CLOUD_PROJECT="my-project"
    export ADK_CORPUS_RESOURCE_NAME="projects/.../corpora/adk-knowledge-base"
    python test_rag_agent.py --mode all
"""

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    from vertexai.agent_engines import AdkApp
except ImportError as e:
    print(f"ERROR: Missing required dependencies: {e}")
    print("\nInstall with:")
    print("  pip install google-cloud-aiplatform[agent_engines,adk]")
    sys.exit(1)

try:
    from agent import agent_builder_pro_root, create_agent_builder_pro
except ImportError as e:
    print(f"ERROR: Cannot import agent: {e}")
    print("\nMake sure you're running from the agent-builder-pro directory")
    sys.exit(1)


class AgentBuilderProTester:
    """Comprehensive tester for Agent Builder Pro."""

    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        self.corpus_resource_name = os.getenv("ADK_CORPUS_RESOURCE_NAME")

        self.test_results = {
            "test_date": datetime.utcnow().isoformat(),
            "project_id": self.project_id,
            "tests": []
        }

    def _record_test(self, test_name: str, passed: bool, details: Dict[str, Any]):
        """Record test result."""
        self.test_results["tests"].append({
            "test_name": test_name,
            "passed": passed,
            "timestamp": datetime.utcnow().isoformat(),
            "details": details
        })

    async def test_knowledge_retrieval(self) -> bool:
        """Test RAG knowledge retrieval with ADK questions."""
        print("\n" + "=" * 70)
        print("TEST 1: Knowledge Retrieval (RAG)")
        print("=" * 70)

        if not self.corpus_resource_name:
            print("⚠ Skipping: ADK_CORPUS_RESOURCE_NAME not set")
            self._record_test("knowledge_retrieval", False, {
                "reason": "corpus_not_configured"
            })
            return False

        test_queries = [
            "What are the different types of agents in ADK?",
            "How do I create a SequentialAgent?",
            "What are best practices for tool integration?",
            "How do I deploy an ADK agent to Vertex AI?",
        ]

        print(f"\nTesting {len(test_queries)} knowledge queries...")

        try:
            # Create agent with RAG
            agent = create_agent_builder_pro(
                corpus_resource_name=self.corpus_resource_name
            )
            app = AdkApp(agent=agent)

            query_results = []

            for i, query in enumerate(test_queries, 1):
                print(f"\n[{i}/{len(test_queries)}] Query: {query}")

                response_text = []
                has_citations = False

                try:
                    async for event in app.async_stream_query(
                        user_id="test-user",
                        message=query
                    ):
                        if hasattr(event, "text"):
                            response_text.append(event.text)

                        # Check for citations (implementation may vary)
                        if hasattr(event, "citations") or "source" in str(event).lower():
                            has_citations = True

                    full_response = "".join(response_text)
                    print(f"Response length: {len(full_response)} characters")
                    print(f"Has citations: {has_citations}")

                    query_results.append({
                        "query": query,
                        "success": len(full_response) > 0,
                        "response_length": len(full_response),
                        "has_citations": has_citations
                    })

                except Exception as e:
                    print(f"✗ Query failed: {e}")
                    query_results.append({
                        "query": query,
                        "success": False,
                        "error": str(e)
                    })

            # Evaluate results
            successful_queries = sum(1 for r in query_results if r.get("success"))
            queries_with_citations = sum(1 for r in query_results if r.get("has_citations"))

            print(f"\n{'='*70}")
            print(f"Knowledge Retrieval Results:")
            print(f"  Successful queries: {successful_queries}/{len(test_queries)}")
            print(f"  Queries with citations: {queries_with_citations}/{len(test_queries)}")

            passed = successful_queries >= len(test_queries) * 0.75  # 75% success rate

            if passed:
                print(f"  ✓ PASSED")
            else:
                print(f"  ✗ FAILED")

            self._record_test("knowledge_retrieval", passed, {
                "total_queries": len(test_queries),
                "successful": successful_queries,
                "with_citations": queries_with_citations,
                "query_results": query_results
            })

            return passed

        except Exception as e:
            print(f"\n✗ Knowledge retrieval test failed: {e}")
            import traceback
            traceback.print_exc()

            self._record_test("knowledge_retrieval", False, {
                "error": str(e)
            })
            return False

    async def test_agent_building_end_to_end(self) -> bool:
        """Test end-to-end agent creation."""
        print("\n" + "=" * 70)
        print("TEST 2: End-to-End Agent Building")
        print("=" * 70)

        test_cases = [
            {
                "name": "Simple Customer Service Agent",
                "prompt": "Build a simple customer service agent that handles product inquiries",
                "expected_elements": ["requirements", "architecture", "tool", "code", "deployment"]
            },
            {
                "name": "Data Analysis Agent",
                "prompt": "Create a data analysis agent with visualization capabilities",
                "expected_elements": ["requirements", "architecture", "tool", "code", "deployment"]
            }
        ]

        print(f"\nTesting {len(test_cases)} agent building scenarios...")

        try:
            agent = agent_builder_pro_root
            app = AdkApp(agent=agent)

            case_results = []

            for i, test_case in enumerate(test_cases, 1):
                print(f"\n[{i}/{len(test_cases)}] {test_case['name']}")
                print(f"Prompt: {test_case['prompt']}")

                response_text = []

                try:
                    print("Executing agent pipeline...")
                    async for event in app.async_stream_query(
                        user_id="test-user",
                        message=test_case['prompt']
                    ):
                        if hasattr(event, "text"):
                            response_text.append(event.text)
                            # Show progress
                            if "Gatherer" in event.text or "Designer" in event.text or "Generator" in event.text:
                                print(".", end="", flush=True)

                    print()  # New line after progress dots

                    full_response = "".join(response_text)
                    response_lower = full_response.lower()

                    # Check for expected elements
                    elements_found = []
                    for element in test_case['expected_elements']:
                        if element in response_lower:
                            elements_found.append(element)

                    print(f"Response length: {len(full_response)} characters")
                    print(f"Elements found: {len(elements_found)}/{len(test_case['expected_elements'])}")
                    print(f"  Found: {', '.join(elements_found)}")

                    passed = len(elements_found) >= len(test_case['expected_elements']) * 0.6  # 60% of elements

                    case_results.append({
                        "name": test_case['name'],
                        "success": passed,
                        "response_length": len(full_response),
                        "elements_found": elements_found,
                        "elements_expected": test_case['expected_elements']
                    })

                    if passed:
                        print(f"✓ Test case passed")
                    else:
                        print(f"✗ Test case failed")

                except Exception as e:
                    print(f"✗ Test case failed: {e}")
                    case_results.append({
                        "name": test_case['name'],
                        "success": False,
                        "error": str(e)
                    })

            # Evaluate results
            successful_cases = sum(1 for r in case_results if r.get("success"))

            print(f"\n{'='*70}")
            print(f"End-to-End Building Results:")
            print(f"  Successful cases: {successful_cases}/{len(test_cases)}")

            passed = successful_cases >= len(test_cases) * 0.5  # 50% success rate

            if passed:
                print(f"  ✓ PASSED")
            else:
                print(f"  ✗ FAILED")

            self._record_test("end_to_end_building", passed, {
                "total_cases": len(test_cases),
                "successful": successful_cases,
                "case_results": case_results
            })

            return passed

        except Exception as e:
            print(f"\n✗ End-to-end test failed: {e}")
            import traceback
            traceback.print_exc()

            self._record_test("end_to_end_building", False, {
                "error": str(e)
            })
            return False

    def test_production_deployment(self) -> bool:
        """Test production deployment configuration."""
        print("\n" + "=" * 70)
        print("TEST 3: Production Deployment Verification")
        print("=" * 70)

        try:
            # Check if deployment info exists
            deployment_info_file = Path("deployment_info.json")

            if not deployment_info_file.exists():
                print("⚠ No deployment info found - agent not yet deployed")
                print("Run: python deploy_to_vertex.py")

                self._record_test("production_deployment", False, {
                    "reason": "not_deployed"
                })
                return False

            # Load deployment info
            deployment_info = json.loads(deployment_info_file.read_text())

            print(f"\nDeployment Information:")
            print(f"  Status: {deployment_info.get('status', 'unknown')}")
            print(f"  Resource: {deployment_info.get('resource_name', 'N/A')}")
            print(f"  Endpoint: {deployment_info.get('endpoint', 'N/A')}")
            print(f"  Project: {deployment_info.get('project_id', 'N/A')}")
            print(f"  Location: {deployment_info.get('location', 'N/A')}")

            # Verify status
            status = deployment_info.get('status')
            if status == 'deployed':
                print(f"\n✓ Agent successfully deployed to production")
                passed = True
            else:
                print(f"\n✗ Agent deployment status: {status}")
                passed = False

            self._record_test("production_deployment", passed, deployment_info)

            return passed

        except Exception as e:
            print(f"\n✗ Production deployment test failed: {e}")

            self._record_test("production_deployment", False, {
                "error": str(e)
            })
            return False

    def save_test_results(self):
        """Save test results to file."""
        print(f"\n💾 Saving test results...")

        try:
            # Calculate summary
            total_tests = len(self.test_results["tests"])
            passed_tests = sum(1 for t in self.test_results["tests"] if t["passed"])

            self.test_results["summary"] = {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": total_tests - passed_tests,
                "success_rate": round(passed_tests / total_tests * 100, 1) if total_tests > 0 else 0
            }

            # Save locally
            output_file = Path("test_results.txt")
            output_file.write_text(json.dumps(self.test_results, indent=2))
            print(f"   ✓ Saved: {output_file}")

            # Save to outputs
            output_manifest = Path("/mnt/user-data/outputs/06_test_results.txt")
            output_manifest.parent.mkdir(parents=True, exist_ok=True)
            output_manifest.write_text(json.dumps(self.test_results, indent=2))
            print(f"   ✓ Saved to outputs: {output_manifest}")

        except Exception as e:
            print(f"   ⚠ Could not save test results: {e}")

    async def run(self, mode: str = "all") -> bool:
        """Execute test suite."""
        print("=" * 70)
        print("AGENT BUILDER PRO - COMPREHENSIVE TESTING")
        print("=" * 70)
        print(f"Mode: {mode}")
        print(f"Project: {self.project_id or 'Not configured'}")
        print(f"RAG Corpus: {'Configured' if self.corpus_resource_name else 'Not configured'}")

        results = []

        try:
            if mode in ["knowledge", "all"]:
                result = await self.test_knowledge_retrieval()
                results.append(("Knowledge Retrieval", result))

            if mode in ["agent", "all"]:
                result = await self.test_agent_building_end_to_end()
                results.append(("Agent Building", result))

            if mode in ["production", "all"]:
                result = self.test_production_deployment()
                results.append(("Production Deployment", result))

            # Save results
            self.save_test_results()

            # Final summary
            print("\n" + "=" * 70)
            print("TEST SUMMARY")
            print("=" * 70)

            for test_name, passed in results:
                status = "✓ PASSED" if passed else "✗ FAILED"
                print(f"{test_name:.<50} {status}")

            passed_count = sum(1 for _, p in results if p)
            total_count = len(results)

            print(f"\nOverall: {passed_count}/{total_count} tests passed")

            if passed_count == total_count:
                print("\n🎉 All tests passed!")
                return True
            elif passed_count > 0:
                print(f"\n⚠ Some tests failed")
                return False
            else:
                print(f"\n❌ All tests failed")
                return False

        except KeyboardInterrupt:
            print("\n\n⚠ Testing cancelled by user")
            return False
        except Exception as e:
            print(f"\n❌ ERROR: Testing failed: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Test Agent Builder Pro with RAG capabilities"
    )
    parser.add_argument(
        "--mode",
        choices=["knowledge", "agent", "production", "all"],
        default="all",
        help="Test mode to run"
    )

    args = parser.parse_args()

    # Check project ID
    if not os.getenv("GOOGLE_CLOUD_PROJECT"):
        print("WARNING: GOOGLE_CLOUD_PROJECT not set")
        print("Some tests may be skipped")

    # Create tester and run
    tester = AgentBuilderProTester()

    try:
        success = asyncio.run(tester.run(mode=args.mode))
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTesting interrupted")
        sys.exit(1)


if __name__ == "__main__":
    main()
