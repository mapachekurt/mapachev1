"""
Remote Agent - Client for connecting to remote A2A agents

This module provides utilities for discovering and communicating with remote agents.
"""

import logging
import os
from typing import List, Dict, Any, Optional

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


class RemoteAgent:
    """
    Client for interacting with remote A2A agents.

    This class:
    - Discovers agent URLs from the registry
    - Establishes connections to remote agents
    - Provides methods for sending messages
    - Handles authentication
    """

    def __init__(
        self,
        agent_name: str,
        registry_url: Optional[str] = None,
        bearer_token: Optional[str] = None,
    ):
        """
        Initialize a connection to a remote agent.

        Args:
            agent_name: Name of the agent to connect to
            registry_url: URL of the agent registry
            bearer_token: Bearer token for authentication
        """
        self.agent_name = agent_name
        self.registry_url = registry_url or os.getenv(
            "A2A_REGISTRY_URL", "http://localhost:8080"
        )
        self.bearer_token = bearer_token or os.getenv("BEARER_TOKEN", "dev-token")

        self.agent_url = None
        self.agent_card = None

        # Discover the agent
        self._discover_agent()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    def _discover_agent(self):
        """Discover the agent's URL from the registry"""
        try:
            headers = {"Authorization": f"Bearer {self.bearer_token}"}
            response = httpx.get(
                f"{self.registry_url}/agents/{self.agent_name}",
                headers=headers,
                timeout=10.0,
            )
            response.raise_for_status()

            agent_info = response.json()
            self.agent_card = agent_info

            # Get agent URL from registry response
            # For local development, construct URL from agent name
            # In production, this would come from the registry
            self.agent_url = agent_info.get(
                "url", f"http://localhost:800{hash(self.agent_name) % 90 + 1}"
            )

            logger.info(f"Discovered agent {self.agent_name} at {self.agent_url}")

        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to discover agent {self.agent_name}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error discovering agent: {e}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    def send_message(
        self, message: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send a message to the remote agent.

        Args:
            message: The message to send
            context: Optional context information

        Returns:
            Response from the agent
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.bearer_token}",
                "Content-Type": "application/json",
            }

            payload = {
                "message": message,
                "context": context or {},
            }

            # Send message to agent
            # Note: The actual A2A protocol endpoint would be used here
            # For now, we'll use a generic /message endpoint
            response = httpx.post(
                f"{self.agent_url}/message",
                headers=headers,
                json=payload,
                timeout=30.0,
            )
            response.raise_for_status()

            return response.json()

        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to send message to {self.agent_name}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            raise

    def get_agent_card(self) -> Dict[str, Any]:
        """Get the agent's card"""
        if not self.agent_card:
            self._discover_agent()
        return self.agent_card

    def __repr__(self) -> str:
        return f"RemoteAgent(name='{self.agent_name}', url='{self.agent_url}')"


def discover_agents_by_skill(
    skill: str,
    registry_url: Optional[str] = None,
    bearer_token: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Discover agents by skill from the registry.

    Args:
        skill: Skill to search for
        registry_url: URL of the agent registry
        bearer_token: Bearer token for authentication

    Returns:
        List of agent cards matching the skill
    """
    registry_url = registry_url or os.getenv("A2A_REGISTRY_URL", "http://localhost:8080")
    bearer_token = bearer_token or os.getenv("BEARER_TOKEN", "dev-token")

    try:
        headers = {"Authorization": f"Bearer {bearer_token}"}
        response = httpx.post(
            f"{registry_url}/agents/search",
            headers=headers,
            json={"skill": skill},
            timeout=10.0,
        )
        response.raise_for_status()

        return response.json().get("agents", [])

    except Exception as e:
        logger.error(f"Error discovering agents by skill: {e}")
        return []


def discover_agents_by_department(
    department: str,
    registry_url: Optional[str] = None,
    bearer_token: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Discover agents by department from the registry.

    Args:
        department: Department to search for
        registry_url: URL of the agent registry
        bearer_token: Bearer token for authentication

    Returns:
        List of agent cards in the department
    """
    registry_url = registry_url or os.getenv("A2A_REGISTRY_URL", "http://localhost:8080")
    bearer_token = bearer_token or os.getenv("BEARER_TOKEN", "dev-token")

    try:
        headers = {"Authorization": f"Bearer {bearer_token}"}
        response = httpx.post(
            f"{registry_url}/agents/search",
            headers=headers,
            json={"department": department},
            timeout=10.0,
        )
        response.raise_for_status()

        return response.json().get("agents", [])

    except Exception as e:
        logger.error(f"Error discovering agents by department: {e}")
        return []
