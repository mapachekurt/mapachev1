"""A2A Protocol Implementation (Linux Foundation Standard)."""
import requests
import uuid
from typing import Dict, Any, List


class A2AClient:
    """
    Agent-to-Agent communication client following Linux Foundation A2A spec.

    Specification: https://a2aprotocol.org/spec
    """

    PROTOCOL_VERSION = "1.0"

    def __init__(self, agent_id: str, agent_endpoint: str):
        """
        Initialize A2A client.

        Args:
            agent_id: Unique identifier for this agent
            agent_endpoint: URL endpoint where this agent can be reached
        """
        self.agent_id = agent_id
        self.endpoint = agent_endpoint

    def send_request(
        self,
        target_agent_url: str,
        capability: str,
        payload: Dict[str, Any],
        timeout: int = 30
    ) -> Dict:
        """
        Send A2A request to another agent.

        Args:
            target_agent_url: URL of target agent's A2A endpoint
            capability: Capability being requested (e.g., "pain_point_validation")
            payload: Request payload
            timeout: Request timeout in seconds

        Returns:
            Response payload from target agent

        Raises:
            A2AError: If request fails or times out
        """
        request_body = {
            "protocol_version": self.PROTOCOL_VERSION,
            "source_agent": {
                "id": self.agent_id,
                "endpoint": self.endpoint
            },
            "capability": capability,
            "payload": payload,
            "request_id": self._generate_request_id()
        }

        headers = {
            "Content-Type": "application/json",
            "A2A-Protocol-Version": self.PROTOCOL_VERSION,
            "A2A-Source-Agent": self.agent_id
        }

        try:
            response = requests.post(
                f"{target_agent_url}/a2a",
                json=request_body,
                headers=headers,
                timeout=timeout
            )

            response.raise_for_status()

            return response.json()

        except requests.exceptions.Timeout:
            raise A2AError(f"Request to {target_agent_url} timed out after {timeout}s")
        except requests.exceptions.HTTPError as e:
            raise A2AError(f"HTTP error from {target_agent_url}: {e}")
        except Exception as e:
            raise A2AError(f"Failed to communicate with {target_agent_url}: {e}")

    def register_capability(
        self,
        capability_registry_url: str,
        capabilities: List[str],
        metadata: Dict = None
    ) -> Dict:
        """
        Register agent capabilities with A2A registry.

        Args:
            capability_registry_url: URL of capability registry
            capabilities: List of capabilities this agent provides
            metadata: Optional metadata about agent

        Returns:
            Registration confirmation
        """
        registration = {
            "agent_id": self.agent_id,
            "endpoint": self.endpoint,
            "capabilities": capabilities,
            "protocol_version": self.PROTOCOL_VERSION,
            "metadata": metadata or {}
        }

        try:
            response = requests.post(
                f"{capability_registry_url}/register",
                json=registration,
                headers={"Content-Type": "application/json"}
            )

            response.raise_for_status()
            return response.json()

        except Exception as e:
            raise A2AError(f"Failed to register capabilities: {e}")

    def discover_agents(
        self,
        capability_registry_url: str,
        capability: str
    ) -> List[Dict]:
        """
        Discover agents that provide a specific capability.

        Args:
            capability_registry_url: URL of capability registry
            capability: Capability to search for

        Returns:
            List of agents that provide the capability
        """
        try:
            response = requests.get(
                f"{capability_registry_url}/discover",
                params={"capability": capability},
                headers={"Content-Type": "application/json"}
            )

            response.raise_for_status()
            return response.json().get("agents", [])

        except Exception as e:
            raise A2AError(f"Failed to discover agents: {e}")

    def _generate_request_id(self) -> str:
        """Generate unique request ID."""
        return str(uuid.uuid4())


class A2AError(Exception):
    """Exception raised for A2A protocol errors."""
    pass


class A2AServer:
    """
    A2A Protocol server handler for receiving requests.

    Use this to handle incoming A2A requests in your agent.
    """

    def __init__(self, agent_id: str, capabilities: List[str]):
        """
        Initialize A2A server.

        Args:
            agent_id: Unique identifier for this agent
            capabilities: List of capabilities this agent provides
        """
        self.agent_id = agent_id
        self.capabilities = capabilities
        self.handlers = {}

    def register_handler(self, capability: str, handler_func):
        """
        Register a handler function for a capability.

        Args:
            capability: Capability name
            handler_func: Function to handle requests for this capability
                          Should accept (payload: Dict) and return Dict
        """
        if capability not in self.capabilities:
            raise ValueError(f"Capability {capability} not declared for this agent")

        self.handlers[capability] = handler_func

    def handle_request(self, request: Dict) -> Dict:
        """
        Handle incoming A2A request.

        Args:
            request: A2A request payload

        Returns:
            Response payload

        Raises:
            A2AError: If request is invalid or capability not supported
        """
        # Validate protocol version
        if request.get("protocol_version") != A2AClient.PROTOCOL_VERSION:
            raise A2AError(
                f"Unsupported protocol version: {request.get('protocol_version')}"
            )

        # Get capability
        capability = request.get("capability")
        if not capability:
            raise A2AError("No capability specified in request")

        # Check if we support this capability
        if capability not in self.capabilities:
            raise A2AError(
                f"Capability {capability} not supported. "
                f"Supported: {', '.join(self.capabilities)}"
            )

        # Get handler
        handler = self.handlers.get(capability)
        if not handler:
            raise A2AError(f"No handler registered for capability {capability}")

        # Execute handler
        try:
            result = handler(request.get("payload", {}))

            return {
                "protocol_version": A2AClient.PROTOCOL_VERSION,
                "request_id": request.get("request_id"),
                "agent_id": self.agent_id,
                "capability": capability,
                "status": "success",
                "result": result
            }

        except Exception as e:
            return {
                "protocol_version": A2AClient.PROTOCOL_VERSION,
                "request_id": request.get("request_id"),
                "agent_id": self.agent_id,
                "capability": capability,
                "status": "error",
                "error": str(e)
            }
