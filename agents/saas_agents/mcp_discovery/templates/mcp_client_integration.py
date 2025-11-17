"""
MCP Client Integration Template

This template shows how to integrate an existing MCP server with a SaaS agent.
Use this when an MCP server already exists for the SaaS tool.

Example: GitHub, GitLab, Google Drive, Slack, etc.
"""

from typing import Any, Dict, List, Optional
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPIntegratedAgent:
    """
    Template for integrating a SaaS agent with an existing MCP server.

    This template demonstrates:
    1. Connecting to an MCP server
    2. Discovering available tools/resources
    3. Invoking MCP tools
    4. Handling responses
    5. Error handling
    """

    def __init__(
        self,
        agent_id: str,
        agent_name: str,
        mcp_server_command: str,
        mcp_server_args: Optional[List[str]] = None
    ):
        """
        Initialize MCP-integrated agent.

        Args:
            agent_id: Unique agent identifier (e.g., "agent_526")
            agent_name: Agent name (e.g., "github")
            mcp_server_command: Command to start MCP server (e.g., "npx")
            mcp_server_args: Arguments for MCP server (e.g., ["-y", "@modelcontextprotocol/server-github"])
        """
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.mcp_server_command = mcp_server_command
        self.mcp_server_args = mcp_server_args or []

        self.session: Optional[ClientSession] = None
        self.available_tools: List[Dict[str, Any]] = []
        self.available_resources: List[Dict[str, Any]] = []

    async def __aenter__(self):
        """Async context manager entry - connect to MCP server."""
        server_params = StdioServerParameters(
            command=self.mcp_server_command,
            args=self.mcp_server_args,
            env=None  # Can add environment variables here
        )

        # Connect to MCP server
        self.stdio, self.write = await stdio_client(server_params)
        self.session = ClientSession(self.stdio, self.write)

        await self.session.__aenter__()

        # Initialize and discover capabilities
        await self.session.initialize()

        # Discover tools
        tools_result = await self.session.list_tools()
        self.available_tools = tools_result.tools

        # Discover resources
        resources_result = await self.session.list_resources()
        self.available_resources = resources_result.resources

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit - disconnect from MCP server."""
        if self.session:
            await self.session.__aexit__(exc_type, exc_val, exc_tb)

    async def call_tool(
        self,
        tool_name: str,
        arguments: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Call an MCP tool.

        Args:
            tool_name: Name of the tool to call
            arguments: Tool arguments

        Returns:
            Tool execution result

        Raises:
            ValueError: If tool not found
            Exception: If tool execution fails
        """
        if not self.session:
            raise RuntimeError("MCP session not initialized. Use async with context manager.")

        # Verify tool exists
        tool = next((t for t in self.available_tools if t.name == tool_name), None)
        if not tool:
            available = [t.name for t in self.available_tools]
            raise ValueError(
                f"Tool '{tool_name}' not found. Available tools: {', '.join(available)}"
            )

        # Call tool
        result = await self.session.call_tool(tool_name, arguments or {})

        return result

    async def read_resource(self, resource_uri: str) -> Any:
        """
        Read an MCP resource.

        Args:
            resource_uri: URI of the resource to read

        Returns:
            Resource content
        """
        if not self.session:
            raise RuntimeError("MCP session not initialized")

        result = await self.session.read_resource(resource_uri)
        return result

    def get_available_tools(self) -> List[str]:
        """Get list of available tool names."""
        return [tool.name for tool in self.available_tools]

    def get_available_resources(self) -> List[str]:
        """Get list of available resource URIs."""
        return [resource.uri for resource in self.available_resources]


# Example usage for GitHub agent
async def github_agent_example():
    """
    Example: GitHub agent using official MCP server
    """
    agent = MCPIntegratedAgent(
        agent_id="agent_526",
        agent_name="github",
        mcp_server_command="npx",
        mcp_server_args=[
            "-y",
            "@modelcontextprotocol/server-github",
        ]
    )

    async with agent:
        # Discover available tools
        print(f"Available tools: {agent.get_available_tools()}")

        # Example: List repositories
        result = await agent.call_tool(
            "list_repositories",
            arguments={"username": "modelcontextprotocol"}
        )
        print(f"Repositories: {result}")

        # Example: Create issue
        result = await agent.call_tool(
            "create_issue",
            arguments={
                "owner": "modelcontextprotocol",
                "repo": "servers",
                "title": "Example issue",
                "body": "This is an example issue created via MCP"
            }
        )
        print(f"Created issue: {result}")


# Example usage for Google Drive agent
async def google_drive_agent_example():
    """
    Example: Google Drive agent using official MCP server
    """
    agent = MCPIntegratedAgent(
        agent_id="agent_518",
        agent_name="google_drive",
        mcp_server_command="npx",
        mcp_server_args=[
            "-y",
            "@modelcontextprotocol/server-google-drive",
        ]
    )

    async with agent:
        # List available tools
        print(f"Available tools: {agent.get_available_tools()}")

        # Example: List files
        result = await agent.call_tool("list_files", arguments={})
        print(f"Files: {result}")

        # Example: Search files
        result = await agent.call_tool(
            "search_files",
            arguments={"query": "*.pdf"}
        )
        print(f"PDF files: {result}")


# Example usage for GitLab agent
async def gitlab_agent_example():
    """
    Example: GitLab agent using official MCP server
    """
    agent = MCPIntegratedAgent(
        agent_id="agent_527",
        agent_name="gitlab",
        mcp_server_command="npx",
        mcp_server_args=[
            "-y",
            "@modelcontextprotocol/server-gitlab",
        ]
    )

    async with agent:
        # Discover capabilities
        print(f"Tools: {agent.get_available_tools()}")

        # Example: List projects
        result = await agent.call_tool("list_projects", arguments={})
        print(f"Projects: {result}")


if __name__ == "__main__":
    import asyncio

    # Run examples
    print("=" * 80)
    print("MCP Client Integration Examples")
    print("=" * 80)
    print("\nNote: These examples require:")
    print("  1. Node.js and npx installed")
    print("  2. Appropriate authentication tokens set in environment")
    print("  3. MCP servers to be installed")
    print()

    # Uncomment to run examples:
    # asyncio.run(github_agent_example())
    # asyncio.run(google_drive_agent_example())
    # asyncio.run(gitlab_agent_example())
