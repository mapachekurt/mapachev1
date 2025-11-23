"""
BaseA2AAgent - Foundation class for all A2A-compatible agents

This class provides the core functionality for creating agents that can communicate
using Google's Agent-to-Agent (A2A) protocol.
"""

import json
import os
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
from pathlib import Path

try:
    from google.adk.agents import LlmAgent
except ImportError:
    # Mock LlmAgent for development without ADK installed
    class LlmAgent:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
            self.sub_agents = kwargs.get('sub_agents', [])


@dataclass
class AgentConfig:
    """Configuration for an A2A Agent"""

    name: str
    description: str
    role: str
    department: str
    skills: List[str]
    tools: List[str] = field(default_factory=list)
    reports_to: Optional[str] = None
    manages: List[str] = field(default_factory=list)
    model: str = "gemini-2.0-flash-exp"
    contact_email: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    version: str = "1.0.0"

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return asdict(self)


class BaseA2AAgent:
    """
    Base class for all A2A-compatible agents.

    This class handles:
    - ADK Agent initialization
    - Agent Card generation
    - Tool registration
    - A2A protocol compatibility
    """

    def __init__(self, config: AgentConfig):
        """
        Initialize the A2A agent.

        Args:
            config: Agent configuration
        """
        self.config = config
        self._adk_agent = None
        self._agent_card = None
        self._initialize_agent()
        self._generate_agent_card()

    def _initialize_agent(self):
        """Initialize the underlying ADK agent"""
        instruction = self._build_instruction()

        # Create the ADK agent
        self._adk_agent = LlmAgent(
            name=self.config.name,
            model=self.config.model,
            description=self.config.description,
            instruction=instruction,
        )

    def _build_instruction(self) -> str:
        """Build the agent's instruction prompt"""
        instruction = f"""You are {self.config.name}, a {self.config.role} in the {self.config.department} department.

ROLE AND RESPONSIBILITIES:
{self.config.description}

SKILLS AND CAPABILITIES:
You have expertise in the following areas:
{chr(10).join(f'- {skill}' for skill in self.config.skills)}

ORGANIZATIONAL CONTEXT:
- Department: {self.config.department}
- Reports to: {self.config.reports_to or 'N/A'}
- Manages: {', '.join(self.config.manages) if self.config.manages else 'N/A'}

COMMUNICATION GUIDELINES:
- You communicate with other agents using the A2A protocol
- Be professional, concise, and action-oriented
- When delegating tasks, provide clear context and expectations
- Always acknowledge requests and provide status updates
- Escalate issues to your manager when needed

COLLABORATION:
- Work effectively with agents across departments
- Share relevant information to enable better decisions
- Respect organizational hierarchy and reporting relationships
- Be proactive in identifying blockers and dependencies
"""
        return instruction

    def _generate_agent_card(self):
        """Generate the A2A Agent Card"""
        self._agent_card = {
            "name": self.config.name,
            "description": self.config.description,
            "version": self.config.version,
            "capabilities": {
                "skills": self.config.skills,
                "tools": self.config.tools,
                "model": self.config.model,
            },
            "metadata": {
                "role": self.config.role,
                "department": self.config.department,
                "reports_to": self.config.reports_to,
                "manages": self.config.manages,
                "tags": self.config.tags + [self.config.department],
            },
            "authentication": {
                "type": "bearer",
                "required": True,
            },
            "contact": {
                "email": self.config.contact_email or f"{self.config.name}@mapache.ai",
            },
        }

    def get_adk_agent(self) -> LlmAgent:
        """Get the underlying ADK agent"""
        return self._adk_agent

    def get_agent_card(self) -> Dict[str, Any]:
        """Get the agent card"""
        return self._agent_card

    def save_agent_card(self, output_dir: str = "agent_cards") -> str:
        """
        Save the agent card to a JSON file.

        Args:
            output_dir: Directory to save the agent card

        Returns:
            Path to the saved agent card
        """
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Generate filename
        filename = f"{self.config.name}.json"
        filepath = os.path.join(output_dir, filename)

        # Save agent card
        with open(filepath, 'w') as f:
            json.dump(self._agent_card, f, indent=2)

        return filepath

    def add_sub_agent(self, sub_agent: 'BaseA2AAgent'):
        """
        Add a sub-agent (managed agent) to this agent.

        Args:
            sub_agent: Another BaseA2AAgent instance
        """
        if hasattr(self._adk_agent, 'sub_agents'):
            if self._adk_agent.sub_agents is None:
                self._adk_agent.sub_agents = []
            self._adk_agent.sub_agents.append(sub_agent.get_adk_agent())
        else:
            # Initialize sub_agents if not exists
            self._adk_agent.sub_agents = [sub_agent.get_adk_agent()]

    def __repr__(self) -> str:
        return f"BaseA2AAgent(name='{self.config.name}', role='{self.config.role}', department='{self.config.department}')"
