"""
Custom MCP Server Template

Use this template to build custom MCP servers for SaaS tools that have APIs
but no existing MCP server.

Example use cases:
- Gmail (Google Gmail API)
- Linear (GraphQL API)
- Microsoft Teams (Graph API)
- Notion (Notion API)
"""

from typing import Any, Callable, Dict, List, Optional
import asyncio
import httpx
from mcp.server import Server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    Resource,
    Prompt,
    PromptMessage,
    GetPromptResult,
    CallToolResult,
)
from mcp.server.stdio import stdio_server


class CustomMCPServer:
    """
    Template for building a custom MCP server.

    This template demonstrates:
    1. Defining MCP tools (functions the AI can call)
    2. Defining MCP resources (data the AI can read)
    3. Defining MCP prompts (conversation templates)
    4. Implementing API calls to the SaaS platform
    5. Handling authentication
    6. Error handling
    """

    def __init__(
        self,
        name: str,
        version: str,
        api_base_url: str,
        api_key: Optional[str] = None,
        oauth_token: Optional[str] = None
    ):
        """
        Initialize custom MCP server.

        Args:
            name: Server name (e.g., "gmail-server")
            version: Server version (e.g., "1.0.0")
            api_base_url: Base URL for API calls
            api_key: API key for authentication (if applicable)
            oauth_token: OAuth token for authentication (if applicable)
        """
        self.server = Server(name)
        self.version = version
        self.api_base_url = api_base_url
        self.api_key = api_key
        self.oauth_token = oauth_token

        # HTTP client for API calls
        self.http_client = httpx.AsyncClient(
            base_url=api_base_url,
            headers=self._get_auth_headers(),
            timeout=30.0
        )

        # Register handlers
        self._register_tools()
        self._register_resources()
        self._register_prompts()

    def _get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers for API requests."""
        headers = {}

        if self.oauth_token:
            headers["Authorization"] = f"Bearer {self.oauth_token}"
        elif self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        return headers

    def _register_tools(self):
        """Register MCP tools (functions the AI can call)."""

        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """Return list of available tools."""
            return [
                Tool(
                    name="example_read",
                    description="Read data from the API",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "resource_id": {
                                "type": "string",
                                "description": "ID of the resource to read"
                            }
                        },
                        "required": ["resource_id"]
                    }
                ),
                Tool(
                    name="example_create",
                    description="Create a new resource",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Name of the resource"
                            },
                            "data": {
                                "type": "object",
                                "description": "Resource data"
                            }
                        },
                        "required": ["name", "data"]
                    }
                ),
                Tool(
                    name="example_update",
                    description="Update an existing resource",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "resource_id": {
                                "type": "string",
                                "description": "ID of the resource to update"
                            },
                            "data": {
                                "type": "object",
                                "description": "Updated resource data"
                            }
                        },
                        "required": ["resource_id", "data"]
                    }
                ),
                Tool(
                    name="example_delete",
                    description="Delete a resource",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "resource_id": {
                                "type": "string",
                                "description": "ID of the resource to delete"
                            }
                        },
                        "required": ["resource_id"]
                    }
                ),
                Tool(
                    name="example_list",
                    description="List all resources",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "number",
                                "description": "Maximum number of results",
                                "default": 10
                            },
                            "offset": {
                                "type": "number",
                                "description": "Offset for pagination",
                                "default": 0
                            }
                        }
                    }
                ),
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            """Execute a tool call."""
            try:
                if name == "example_read":
                    result = await self._api_read(arguments["resource_id"])
                elif name == "example_create":
                    result = await self._api_create(arguments["name"], arguments["data"])
                elif name == "example_update":
                    result = await self._api_update(arguments["resource_id"], arguments["data"])
                elif name == "example_delete":
                    result = await self._api_delete(arguments["resource_id"])
                elif name == "example_list":
                    result = await self._api_list(
                        arguments.get("limit", 10),
                        arguments.get("offset", 0)
                    )
                else:
                    raise ValueError(f"Unknown tool: {name}")

                return CallToolResult(
                    content=[TextContent(type="text", text=str(result))]
                )

            except Exception as e:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error: {str(e)}")]
                )

    def _register_resources(self):
        """Register MCP resources (data the AI can read)."""

        @self.server.list_resources()
        async def list_resources() -> List[Resource]:
            """Return list of available resources."""
            return [
                Resource(
                    uri="resource://config",
                    name="Server Configuration",
                    description="Current server configuration and status",
                    mimeType="application/json"
                ),
                Resource(
                    uri="resource://stats",
                    name="API Statistics",
                    description="Current API usage statistics",
                    mimeType="application/json"
                ),
            ]

        @self.server.read_resource()
        async def read_resource(uri: str) -> str:
            """Read a resource."""
            if uri == "resource://config":
                return {
                    "name": self.server.name,
                    "version": self.version,
                    "api_base_url": self.api_base_url,
                    "authenticated": bool(self.oauth_token or self.api_key)
                }
            elif uri == "resource://stats":
                # In production, fetch real stats from API
                return {
                    "requests_today": 0,
                    "rate_limit_remaining": 1000,
                    "rate_limit_reset": "2025-11-18T00:00:00Z"
                }
            else:
                raise ValueError(f"Unknown resource: {uri}")

    def _register_prompts(self):
        """Register MCP prompts (conversation templates)."""

        @self.server.list_prompts()
        async def list_prompts() -> List[Prompt]:
            """Return list of available prompts."""
            return [
                Prompt(
                    name="analyze_data",
                    description="Analyze data from the API",
                    arguments=[
                        {
                            "name": "resource_id",
                            "description": "ID of resource to analyze",
                            "required": True
                        }
                    ]
                ),
            ]

        @self.server.get_prompt()
        async def get_prompt(name: str, arguments: Dict[str, str]) -> GetPromptResult:
            """Get a prompt template."""
            if name == "analyze_data":
                resource_id = arguments.get("resource_id", "")
                return GetPromptResult(
                    description=f"Analyzing resource {resource_id}",
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(
                                type="text",
                                text=f"Please analyze the data from resource {resource_id} and provide insights."
                            )
                        )
                    ]
                )
            else:
                raise ValueError(f"Unknown prompt: {name}")

    # API Implementation Methods
    # These methods make actual API calls to the SaaS platform

    async def _api_read(self, resource_id: str) -> Dict[str, Any]:
        """Read a resource from the API."""
        response = await self.http_client.get(f"/resources/{resource_id}")
        response.raise_for_status()
        return response.json()

    async def _api_create(self, name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a resource via the API."""
        response = await self.http_client.post(
            "/resources",
            json={"name": name, **data}
        )
        response.raise_for_status()
        return response.json()

    async def _api_update(self, resource_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a resource via the API."""
        response = await self.http_client.patch(
            f"/resources/{resource_id}",
            json=data
        )
        response.raise_for_status()
        return response.json()

    async def _api_delete(self, resource_id: str) -> Dict[str, Any]:
        """Delete a resource via the API."""
        response = await self.http_client.delete(f"/resources/{resource_id}")
        response.raise_for_status()
        return {"status": "deleted", "resource_id": resource_id}

    async def _api_list(self, limit: int = 10, offset: int = 0) -> Dict[str, Any]:
        """List resources from the API."""
        response = await self.http_client.get(
            "/resources",
            params={"limit": limit, "offset": offset}
        )
        response.raise_for_status()
        return response.json()

    async def run(self):
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


# Example: Gmail MCP Server
class GmailMCPServer(CustomMCPServer):
    """
    Example custom MCP server for Gmail API.
    """

    def __init__(self, oauth_token: str):
        super().__init__(
            name="gmail-server",
            version="1.0.0",
            api_base_url="https://gmail.googleapis.com/gmail/v1",
            oauth_token=oauth_token
        )

    def _register_tools(self):
        """Register Gmail-specific tools."""

        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            return [
                Tool(
                    name="list_messages",
                    description="List Gmail messages",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query (Gmail search syntax)"
                            },
                            "max_results": {
                                "type": "number",
                                "description": "Maximum number of results",
                                "default": 10
                            }
                        }
                    }
                ),
                Tool(
                    name="send_message",
                    description="Send an email",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "to": {"type": "string", "description": "Recipient email"},
                            "subject": {"type": "string", "description": "Email subject"},
                            "body": {"type": "string", "description": "Email body"}
                        },
                        "required": ["to", "subject", "body"]
                    }
                ),
                Tool(
                    name="read_message",
                    description="Read a specific message",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "message_id": {
                                "type": "string",
                                "description": "Message ID to read"
                            }
                        },
                        "required": ["message_id"]
                    }
                ),
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            # Implementation would call actual Gmail API endpoints
            pass


# Example: Linear MCP Server
class LinearMCPServer(CustomMCPServer):
    """
    Example custom MCP server for Linear (GraphQL API).
    """

    def __init__(self, api_key: str):
        super().__init__(
            name="linear-server",
            version="1.0.0",
            api_base_url="https://api.linear.app/graphql",
            api_key=api_key
        )

    def _register_tools(self):
        """Register Linear-specific tools."""

        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            return [
                Tool(
                    name="create_issue",
                    description="Create a Linear issue",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "description": {"type": "string"},
                            "team_id": {"type": "string"}
                        },
                        "required": ["title", "team_id"]
                    }
                ),
                Tool(
                    name="list_issues",
                    description="List Linear issues",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "team_id": {"type": "string"},
                            "limit": {"type": "number", "default": 10}
                        }
                    }
                ),
            ]


if __name__ == "__main__":
    # Example usage
    print("=" * 80)
    print("Custom MCP Server Template")
    print("=" * 80)
    print("\nThis template provides a foundation for building custom MCP servers.")
    print("\nTo use:")
    print("  1. Extend CustomMCPServer class")
    print("  2. Override _register_tools() to define API operations")
    print("  3. Implement API call methods")
    print("  4. Run with: asyncio.run(server.run())")
    print()
