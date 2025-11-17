"""
Populate Registry

This script reads all agent cards from the agent_cards directory
and registers them with the central registry.
"""

import json
import os
from pathlib import Path
import httpx


def populate_registry(
    agent_cards_dir: str = "agent_cards",
    registry_url: str = None,
    bearer_token: str = None,
):
    """
    Populate the registry with all agent cards.

    Args:
        agent_cards_dir: Directory containing agent card JSON files
        registry_url: URL of the registry service
        bearer_token: Bearer token for authentication
    """
    registry_url = registry_url or os.getenv("A2A_REGISTRY_URL", "http://localhost:8080")
    bearer_token = bearer_token or os.getenv("BEARER_TOKEN", "dev-bearer-token-change-in-production")

    print(f"Populating registry at {registry_url}")
    print(f"Reading agent cards from {agent_cards_dir}")

    cards_dir = Path(agent_cards_dir)

    if not cards_dir.exists():
        print(f"Error: Agent cards directory {cards_dir} does not exist")
        return

    # Get all JSON files
    card_files = list(cards_dir.glob("*.json"))
    print(f"Found {len(card_files)} agent cards")

    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json",
    }

    success_count = 0
    error_count = 0

    for card_file in card_files:
        try:
            with open(card_file, 'r') as f:
                agent_card = json.load(f)

            agent_name = agent_card.get("name")

            # Prepare registration payload
            registration_payload = {
                "name": agent_card["name"],
                "description": agent_card["description"],
                "version": agent_card.get("version", "1.0.0"),
                "capabilities": agent_card["capabilities"],
                "metadata": agent_card["metadata"],
                "authentication": agent_card["authentication"],
                "contact": agent_card["contact"],
            }

            # Register with registry
            response = httpx.post(
                f"{registry_url}/agents/register",
                headers=headers,
                json=registration_payload,
                timeout=10.0,
            )
            response.raise_for_status()

            success_count += 1
            print(f"  ✓ Registered {agent_name}")

        except Exception as e:
            error_count += 1
            print(f"  ✗ Error registering {card_file.name}: {e}")

    print("")
    print("="*60)
    print(f"Successfully registered {success_count} agents")
    if error_count > 0:
        print(f"Failed to register {error_count} agents")
    print("="*60)


if __name__ == "__main__":
    populate_registry()
