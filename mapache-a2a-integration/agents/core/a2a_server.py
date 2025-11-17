"""
A2A Server - Exposes agents via A2A Protocol

This module wraps ADK agents with FastAPI to expose them as A2A-compatible services.
"""

import logging
import os
from typing import Optional

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

try:
    from google.adk.agents import LlmAgent
    from google.adk import to_a2a
except ImportError:
    # Mock for development
    LlmAgent = None
    def to_a2a(agent):
        return FastAPI()

from .base_agent import BaseA2AAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()


class A2AServer:
    """
    A2A Server wrapper that exposes agents via the A2A protocol.

    This class:
    - Uses ADK's to_a2a() function to expose agents
    - Adds authentication middleware
    - Provides health check endpoints
    - Configures CORS
    - Manages the FastAPI server lifecycle
    """

    def __init__(
        self,
        agent: BaseA2AAgent,
        port: int = 8000,
        host: str = "0.0.0.0",
        bearer_token: Optional[str] = None,
    ):
        """
        Initialize the A2A server.

        Args:
            agent: The BaseA2AAgent to expose
            port: Port to run the server on
            host: Host to bind to
            bearer_token: Optional bearer token for authentication
        """
        self.agent = agent
        self.port = port
        self.host = host
        self.bearer_token = bearer_token or os.getenv("BEARER_TOKEN", "dev-token")

        # Create FastAPI app
        self.app = FastAPI(
            title=f"{agent.config.name} A2A Service",
            description=agent.config.description,
            version=agent.config.version,
        )

        # Configure CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Configure appropriately for production
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Add routes
        self._add_routes()

        # Wrap agent with A2A protocol
        self._wrap_agent_with_a2a()

    def verify_token(
        self, credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
        """Verify bearer token authentication"""
        if credentials.credentials != self.bearer_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return credentials.credentials

    def _add_routes(self):
        """Add custom routes to the FastAPI app"""

        @self.app.get("/")
        async def root():
            """Service information endpoint"""
            return {
                "service": self.agent.config.name,
                "version": self.agent.config.version,
                "description": self.agent.config.description,
                "department": self.agent.config.department,
                "role": self.agent.config.role,
                "status": "operational",
            }

        @self.app.get("/health")
        async def health():
            """Health check endpoint"""
            return {
                "status": "healthy",
                "agent": self.agent.config.name,
                "version": self.agent.config.version,
            }

        @self.app.get("/.well-known/agent.json")
        async def agent_card():
            """Serve the agent card"""
            return self.agent.get_agent_card()

        @self.app.get("/metrics")
        async def metrics(token: str = Depends(self.verify_token)):
            """Metrics endpoint (protected)"""
            return {
                "agent": self.agent.config.name,
                "status": "operational",
                # Add more metrics as needed
            }

    def _wrap_agent_with_a2a(self):
        """Wrap the agent with A2A protocol using ADK's to_a2a()"""
        try:
            adk_agent = self.agent.get_adk_agent()

            # Use ADK's to_a2a() to add A2A routes to our FastAPI app
            # Note: This integrates the A2A protocol endpoints into our existing app
            a2a_app = to_a2a(adk_agent)

            # Mount the A2A routes into our app
            # The to_a2a function returns a FastAPI app with A2A endpoints
            # We'll merge them into our app
            for route in a2a_app.routes:
                self.app.routes.append(route)

            logger.info(f"Successfully wrapped {self.agent.config.name} with A2A protocol")

        except Exception as e:
            logger.error(f"Error wrapping agent with A2A: {e}")
            # For development, we'll continue even if A2A wrapping fails
            logger.warning("Continuing without full A2A integration")

    def run(self, reload: bool = False):
        """
        Run the A2A server.

        Args:
            reload: Enable auto-reload for development
        """
        logger.info(f"Starting A2A server for {self.agent.config.name}")
        logger.info(f"Server running on http://{self.host}:{self.port}")
        logger.info(f"Agent card available at http://{self.host}:{self.port}/.well-known/agent.json")

        uvicorn.run(
            self.app,
            host=self.host,
            port=self.port,
            reload=reload,
            log_level="info",
        )

    def get_app(self) -> FastAPI:
        """Get the FastAPI app instance"""
        return self.app
