"""A2A agent routing and coordination."""
import os
import requests
import asyncio
import aiohttp
from typing import Dict, List


class AgentRouter:
    """Route requests to validation and opportunity agents via A2A protocol."""

    def __init__(self):
        """Initialize agent endpoints."""
        self.validation_agent_url = os.getenv("VALIDATION_AGENT_ENDPOINT")
        self.opportunity_agent_url = os.getenv("OPPORTUNITY_AGENT_ENDPOINT")
        self.timeout = 60

    async def call_validation_agent(self, request: Dict) -> Dict:
        """
        Call validation agent via A2A protocol.

        Args:
            request: Validation request
                {
                    "problem": str,
                    "subreddits": List[str],
                    "competitors": List[str],
                    "timeframe": str
                }

        Returns:
            Validation result
        """
        if not self.validation_agent_url:
            # Fallback to local agent if endpoint not configured
            print("⚠️  VALIDATION_AGENT_ENDPOINT not set, using local fallback")
            return await self._call_local_validation_agent(request)

        headers = {
            "Content-Type": "application/json",
            "A2A-Protocol-Version": "1.0"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.validation_agent_url}/a2a/validate",
                    json=request,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    response.raise_for_status()
                    return await response.json()

        except Exception as e:
            print(f"Error calling validation agent: {e}")
            return await self._call_local_validation_agent(request)

    async def call_opportunity_agent(self, request: Dict) -> Dict:
        """
        Call opportunity agent via A2A protocol.

        Args:
            request: Opportunity analysis request
                {
                    "market": str,
                    "functionality": str,
                    "competitors": List[str]
                }

        Returns:
            Opportunity analysis result
        """
        if not self.opportunity_agent_url:
            # Fallback to local agent if endpoint not configured
            print("⚠️  OPPORTUNITY_AGENT_ENDPOINT not set, using local fallback")
            return await self._call_local_opportunity_agent(request)

        headers = {
            "Content-Type": "application/json",
            "A2A-Protocol-Version": "1.0"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.opportunity_agent_url}/a2a/analyze",
                    json=request,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    response.raise_for_status()
                    return await response.json()

        except Exception as e:
            print(f"Error calling opportunity agent: {e}")
            return await self._call_local_opportunity_agent(request)

    async def parallel_analysis(self, opportunity_list: List[Dict]) -> List[Dict]:
        """
        Analyze multiple opportunities in parallel.

        Args:
            opportunity_list: List of opportunities to analyze
                [{
                    "problem": str,
                    "market": str,
                    "functionality": str,
                    "subreddits": List[str],
                    "competitors": List[str]
                }]

        Returns:
            Combined results from both agents for each opportunity
        """
        print(f"🚀 Analyzing {len(opportunity_list)} opportunities in parallel...")

        tasks = []
        for opp in opportunity_list:
            # Create tasks for validation + opportunity analysis
            validation_task = self.call_validation_agent({
                "problem": opp["problem"],
                "subreddits": opp.get("subreddits", []),
                "competitors": opp.get("competitors", []),
                "timeframe": opp.get("timeframe", "week")
            })

            opportunity_task = self.call_opportunity_agent({
                "market": opp["market"],
                "functionality": opp["functionality"],
                "competitors": opp.get("competitors", []),
                "language": opp.get("language")
            })

            tasks.append((validation_task, opportunity_task, opp))

        # Execute all in parallel
        results = []
        for validation_task, opportunity_task, opp in tasks:
            try:
                val_result, opp_result = await asyncio.gather(
                    validation_task,
                    opportunity_task
                )

                results.append({
                    "input": opp,
                    "validation": val_result,
                    "opportunity": opp_result
                })

                print(f"✓ Analyzed: {opp['problem'][:50]}...")
            except Exception as e:
                print(f"✗ Failed to analyze {opp['problem'][:50]}: {e}")
                results.append({
                    "input": opp,
                    "validation": {"validation_score": 0, "error": str(e)},
                    "opportunity": {"opportunity_score": 0, "error": str(e)}
                })

        return results

    async def _call_local_validation_agent(self, request: Dict) -> Dict:
        """Fallback to local validation agent."""
        try:
            # Import locally to avoid circular dependencies
            import sys
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../validation-agent'))
            from main import ValidationAgent

            agent = ValidationAgent()
            return agent.validate_opportunity(
                problem_hypothesis=request.get("problem", ""),
                target_subreddits=request.get("subreddits", []),
                competitors=request.get("competitors", []),
                timeframe=request.get("timeframe", "week")
            )
        except Exception as e:
            print(f"Local validation agent error: {e}")
            return {
                "validation_score": 0,
                "evidence": {},
                "recommendation": "Error: Could not run validation",
                "error": str(e)
            }

    async def _call_local_opportunity_agent(self, request: Dict) -> Dict:
        """Fallback to local opportunity agent."""
        try:
            # Import locally to avoid circular dependencies
            import sys
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../opportunity-agent'))
            from main import OpportunityAgent

            agent = OpportunityAgent()
            return agent.analyze_opportunity(
                market_segment=request.get("market", ""),
                functionality=request.get("functionality", ""),
                competitors=request.get("competitors", []),
                preferred_language=request.get("language")
            )
        except Exception as e:
            print(f"Local opportunity agent error: {e}")
            return {
                "opportunity_score": 0,
                "market_size": {},
                "build_strategy": {},
                "strategic_recommendation": "Error: Could not run opportunity analysis",
                "error": str(e)
            }
