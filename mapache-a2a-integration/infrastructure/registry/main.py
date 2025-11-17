"""
Agent Registry Service

Centralized service for agent discovery and registration.
Provides endpoints for:
- Listing all agents
- Getting specific agent details
- Searching agents by skill/department/tags
- Registering new agents
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Any, Optional

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()

# Initialize FastAPI app
app = FastAPI(
    title="A2A Agent Registry",
    description="Centralized registry for agent discovery and management",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
AGENTS_DB: Dict[str, Dict[str, Any]] = {}

# Configuration
BEARER_TOKEN = os.getenv("BEARER_TOKEN", "dev-token")
AGENT_CARDS_DIR = os.getenv("AGENT_CARDS_DIR", "agent_cards")


# Pydantic models
class SearchRequest(BaseModel):
    """Search request model"""

    skill: Optional[str] = None
    department: Optional[str] = None
    tag: Optional[str] = None
    role: Optional[str] = None


class AgentRegistration(BaseModel):
    """Agent registration request model"""

    name: str = Field(..., description="Unique agent name")
    description: str = Field(..., description="Agent description")
    version: str = Field(default="1.0.0", description="Agent version")
    capabilities: Dict[str, Any] = Field(..., description="Agent capabilities")
    metadata: Dict[str, Any] = Field(..., description="Agent metadata")
    authentication: Dict[str, str] = Field(..., description="Authentication requirements")
    contact: Dict[str, str] = Field(..., description="Contact information")
    url: Optional[str] = Field(None, description="Agent URL")


# Authentication dependency
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify bearer token authentication"""
    if credentials.credentials != BEARER_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials


# Startup event
@app.on_event("startup")
async def startup_event():
    """Load agent cards from disk on startup"""
    logger.info("Starting Agent Registry Service...")
    load_agent_cards()
    logger.info(f"Loaded {len(AGENTS_DB)} agents from disk")


def load_agent_cards():
    """Load all agent cards from the agent_cards directory"""
    cards_dir = Path(AGENT_CARDS_DIR)

    if not cards_dir.exists():
        logger.warning(f"Agent cards directory {cards_dir} does not exist")
        cards_dir.mkdir(parents=True, exist_ok=True)
        return

    # Load all JSON files from the directory
    for card_file in cards_dir.glob("*.json"):
        try:
            with open(card_file, 'r') as f:
                agent_card = json.load(f)
                agent_name = agent_card.get("name")

                if agent_name:
                    AGENTS_DB[agent_name] = agent_card
                    logger.debug(f"Loaded agent card: {agent_name}")
                else:
                    logger.warning(f"Agent card {card_file} missing 'name' field")

        except Exception as e:
            logger.error(f"Error loading agent card {card_file}: {e}")


def save_agent_card(agent_name: str, agent_card: Dict[str, Any]):
    """Save an agent card to disk"""
    cards_dir = Path(AGENT_CARDS_DIR)
    cards_dir.mkdir(parents=True, exist_ok=True)

    card_file = cards_dir / f"{agent_name}.json"

    try:
        with open(card_file, 'w') as f:
            json.dump(agent_card, f, indent=2)
        logger.info(f"Saved agent card: {agent_name}")
    except Exception as e:
        logger.error(f"Error saving agent card {agent_name}: {e}")
        raise


# Routes
@app.get("/")
async def root():
    """Service information endpoint"""
    return {
        "service": "A2A Agent Registry",
        "version": "1.0.0",
        "description": "Centralized registry for agent discovery and management",
        "total_agents": len(AGENTS_DB),
        "endpoints": {
            "list_agents": "GET /agents",
            "get_agent": "GET /agents/{name}",
            "search_agents": "POST /agents/search",
            "register_agent": "POST /agents/register",
            "health": "GET /health",
        },
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agents_count": len(AGENTS_DB),
    }


@app.get("/agents")
async def list_agents(
    token: str = Depends(verify_token),
    department: Optional[str] = Query(None, description="Filter by department"),
    skip: int = Query(0, ge=0, description="Number of agents to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of agents to return"),
):
    """
    List all registered agents.

    Returns a list of all agent cards in the registry.
    """
    agents = list(AGENTS_DB.values())

    # Filter by department if specified
    if department:
        agents = [
            agent for agent in agents
            if agent.get("metadata", {}).get("department") == department
        ]

    # Apply pagination
    total = len(agents)
    agents = agents[skip : skip + limit]

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "agents": agents,
    }


@app.get("/agents/{name}")
async def get_agent(name: str, token: str = Depends(verify_token)):
    """
    Get a specific agent by name.

    Returns the complete agent card for the specified agent.
    """
    if name not in AGENTS_DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent '{name}' not found",
        )

    return AGENTS_DB[name]


@app.post("/agents/search")
async def search_agents(
    search: SearchRequest,
    token: str = Depends(verify_token),
):
    """
    Search for agents by skill, department, tag, or role.

    Returns a list of agent cards matching the search criteria.
    """
    results = []

    for agent_card in AGENTS_DB.values():
        match = True

        # Check skill
        if search.skill:
            skills = agent_card.get("capabilities", {}).get("skills", [])
            if search.skill.lower() not in [s.lower() for s in skills]:
                match = False

        # Check department
        if search.department:
            dept = agent_card.get("metadata", {}).get("department", "")
            if search.department.lower() != dept.lower():
                match = False

        # Check tag
        if search.tag:
            tags = agent_card.get("metadata", {}).get("tags", [])
            if search.tag.lower() not in [t.lower() for t in tags]:
                match = False

        # Check role
        if search.role:
            role = agent_card.get("metadata", {}).get("role", "")
            if search.role.lower() not in role.lower():
                match = False

        if match:
            results.append(agent_card)

    return {
        "total": len(results),
        "agents": results,
    }


@app.post("/agents/register")
async def register_agent(
    registration: AgentRegistration,
    token: str = Depends(verify_token),
):
    """
    Register a new agent.

    Validates and stores the agent card in the registry.
    """
    agent_name = registration.name

    # Check if agent already exists
    if agent_name in AGENTS_DB:
        logger.warning(f"Agent {agent_name} already exists, updating...")

    # Create agent card
    agent_card = {
        "name": registration.name,
        "description": registration.description,
        "version": registration.version,
        "capabilities": registration.capabilities,
        "metadata": registration.metadata,
        "authentication": registration.authentication,
        "contact": registration.contact,
    }

    if registration.url:
        agent_card["url"] = registration.url

    # Store in database
    AGENTS_DB[agent_name] = agent_card

    # Persist to disk
    try:
        save_agent_card(agent_name, agent_card)
    except Exception as e:
        logger.error(f"Failed to save agent card to disk: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to persist agent card",
        )

    logger.info(f"Registered agent: {agent_name}")

    return {
        "status": "success",
        "message": f"Agent '{agent_name}' registered successfully",
        "agent": agent_card,
    }


def main():
    """Run the registry service"""
    port = int(os.getenv("REGISTRY_PORT", "8080"))
    host = os.getenv("REGISTRY_HOST", "0.0.0.0")

    logger.info(f"Starting Agent Registry on {host}:{port}")

    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
    )


if __name__ == "__main__":
    main()
