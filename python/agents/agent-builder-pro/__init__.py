"""
Agent Builder Pro - RAG-Enhanced Agent Development System

A sophisticated multi-agent system that leverages comprehensive ADK knowledge
through Gemini File Search RAG to build production-ready agent systems.

Features:
- RAG-enhanced knowledge base with ADK best practices
- Multi-stage sequential pipeline for agent development
- Tool integration and validation
- Automated testing and deployment support
- Production-ready code generation

Sub-Agents:
1. Requirements Gatherer - Analyzes and structures requirements
2. Architecture Designer - Designs optimal agent architecture
3. Tool Specification - Defines and validates tool integrations
4. Code Generator - Generates production-ready implementation
5. Validation & Deployment - Validates and prepares for deployment
"""

__version__ = "1.0.0"
__author__ = "Agent Builder Pro Team"

from .agent import create_agent_builder_pro, agent_builder_pro_root

__all__ = ["create_agent_builder_pro", "agent_builder_pro_root"]
