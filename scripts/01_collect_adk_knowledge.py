#!/usr/bin/env python3
"""
Phase 1: ADK Knowledge Collection Script

Collects comprehensive Google ADK knowledge from multiple sources:
- Official ADK documentation
- ADK starter kit repository
- ADK sample agents repository
- Compiled best practices and patterns

Outputs:
- knowledge_corpus/ directory with all collected resources
- knowledge_manifest.json with inventory and metadata
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import urllib.request
import urllib.error


class ADKKnowledgeCollector:
    """Collects and organizes ADK knowledge resources."""

    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.corpus_dir = self.base_dir / "knowledge_corpus"
        self.docs_dir = self.corpus_dir / "docs"
        self.starter_kit_dir = self.corpus_dir / "starter_kit"
        self.sample_agents_dir = self.corpus_dir / "sample_agents"
        self.best_practices_dir = self.corpus_dir / "best_practices"

        self.manifest = {
            "collection_date": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "sources": [],
            "files_collected": [],
            "statistics": {}
        }

    def setup_directories(self):
        """Create necessary directory structure."""
        print("📁 Setting up directory structure...")
        for directory in [self.docs_dir, self.starter_kit_dir,
                         self.sample_agents_dir, self.best_practices_dir]:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"   ✓ Created: {directory}")

    def clone_repository(self, url: str, target_dir: Path, name: str) -> bool:
        """Clone a Git repository."""
        print(f"\n📦 Cloning {name}...")
        print(f"   URL: {url}")
        print(f"   Target: {target_dir}")

        try:
            # Remove existing directory if present
            if target_dir.exists():
                import shutil
                shutil.rmtree(target_dir)

            # Clone repository
            result = subprocess.run(
                ["git", "clone", "--depth", "1", url, str(target_dir)],
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                print(f"   ✓ Successfully cloned {name}")
                self.manifest["sources"].append({
                    "name": name,
                    "type": "git_repository",
                    "url": url,
                    "status": "success",
                    "location": str(target_dir.relative_to(self.base_dir))
                })
                return True
            else:
                print(f"   ✗ Failed to clone {name}")
                print(f"   Error: {result.stderr}")
                self.manifest["sources"].append({
                    "name": name,
                    "type": "git_repository",
                    "url": url,
                    "status": "failed",
                    "error": result.stderr
                })
                return False
        except subprocess.TimeoutExpired:
            print(f"   ✗ Timeout cloning {name}")
            return False
        except Exception as e:
            print(f"   ✗ Exception cloning {name}: {e}")
            return False

    def fetch_adk_documentation(self):
        """Fetch ADK documentation pages."""
        print("\n📚 Fetching ADK Documentation...")

        # Key documentation pages to fetch
        doc_pages = [
            ("overview", "https://google.github.io/adk-docs/"),
            ("quickstart", "https://google.github.io/adk-docs/docs/quickstart"),
            ("concepts", "https://google.github.io/adk-docs/docs/concepts"),
            ("agents", "https://google.github.io/adk-docs/docs/agents"),
            ("tools", "https://google.github.io/adk-docs/docs/tools"),
            ("deployment", "https://google.github.io/adk-docs/docs/deployment"),
            ("api-reference", "https://google.github.io/adk-docs/docs/api-reference"),
        ]

        docs_fetched = 0
        for name, url in doc_pages:
            try:
                print(f"   Fetching: {name}...")
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=30) as response:
                    content = response.read().decode('utf-8')

                    # Save as HTML
                    output_file = self.docs_dir / f"{name}.html"
                    output_file.write_text(content)

                    self.manifest["files_collected"].append({
                        "name": name,
                        "type": "documentation",
                        "source_url": url,
                        "file_path": str(output_file.relative_to(self.base_dir)),
                        "size_bytes": len(content)
                    })

                    docs_fetched += 1
                    print(f"   ✓ Saved: {output_file.name}")
            except urllib.error.URLError as e:
                print(f"   ⚠ Could not fetch {name}: {e}")
            except Exception as e:
                print(f"   ⚠ Error fetching {name}: {e}")

        print(f"   📄 Documentation pages fetched: {docs_fetched}/{len(doc_pages)}")
        return docs_fetched > 0

    def create_adk_best_practices(self):
        """Create comprehensive ADK best practices JSON."""
        print("\n📝 Creating ADK Best Practices...")

        best_practices = {
            "version": "1.0.0",
            "last_updated": datetime.utcnow().isoformat(),
            "categories": {
                "agent_architecture": {
                    "description": "Agent architecture patterns and design principles",
                    "practices": [
                        {
                            "title": "Sequential Agent Pattern",
                            "description": "Use SequentialAgent for linear workflows where tasks must be completed in order",
                            "use_cases": ["Data processing pipelines", "Multi-step analysis", "Ordered task execution"],
                            "example": "SequentialAgent with sub-agents for: requirements -> design -> implementation -> testing",
                            "benefits": ["Clear execution flow", "Easy debugging", "Predictable behavior"]
                        },
                        {
                            "title": "Parallel Agent Pattern",
                            "description": "Use ParallelAgent for independent tasks that can run simultaneously",
                            "use_cases": ["Multi-source data gathering", "Concurrent analysis", "Independent validations"],
                            "example": "ParallelAgent dispatching to: data_fetcher, validator, analyzer concurrently",
                            "benefits": ["Faster execution", "Resource efficiency", "Scalability"]
                        },
                        {
                            "title": "Loop Agent Pattern",
                            "description": "Use LoopAgent for iterative refinement and repeated tasks",
                            "use_cases": ["Code refinement", "Iterative optimization", "Quality improvement loops"],
                            "example": "LoopAgent for: generate -> review -> refine until quality threshold met",
                            "benefits": ["Self-improvement", "Quality assurance", "Adaptive behavior"]
                        },
                        {
                            "title": "Hierarchical Agent Architecture",
                            "description": "Design agents in hierarchies with root coordinators and specialized sub-agents",
                            "use_cases": ["Complex multi-domain systems", "Enterprise workflows", "Large-scale automation"],
                            "example": "CEO root agent coordinating CTO, CFO, CMO sub-agents, each with their own teams",
                            "benefits": ["Separation of concerns", "Modularity", "Maintainability", "Scalability"]
                        }
                    ]
                },
                "tool_integration": {
                    "description": "Best practices for integrating tools with agents",
                    "practices": [
                        {
                            "title": "MCP Tool Integration",
                            "description": "Use Model Context Protocol (MCP) for standardized tool integration",
                            "use_cases": ["External API integration", "System tool access", "Cross-platform tools"],
                            "implementation": "Define tools in config.yaml with MCP server specifications",
                            "benefits": ["Standardization", "Reusability", "Ecosystem compatibility"]
                        },
                        {
                            "title": "Python Function Tools",
                            "description": "Define Python functions as tools for custom logic and integrations",
                            "use_cases": ["Business logic", "Data transformations", "Custom integrations"],
                            "implementation": "Decorate functions with @tool or define in tools/ directory",
                            "benefits": ["Flexibility", "Custom logic", "Easy testing"]
                        },
                        {
                            "title": "Tool Error Handling",
                            "description": "Implement robust error handling and retry logic for tool calls",
                            "practices": ["Validate inputs", "Handle timeouts", "Implement retries", "Log failures"],
                            "benefits": ["Reliability", "User experience", "Debugging capability"]
                        },
                        {
                            "title": "Tool Documentation",
                            "description": "Provide clear descriptions and parameter specifications for all tools",
                            "importance": "Critical for model understanding and proper tool usage",
                            "benefits": ["Model comprehension", "Correct usage", "Self-documenting code"]
                        }
                    ]
                },
                "deployment_strategies": {
                    "description": "Strategies for deploying ADK agents to production",
                    "practices": [
                        {
                            "title": "Vertex AI Agent Engine Deployment",
                            "description": "Deploy agents to Google Cloud Vertex AI Agent Engine for scalable, managed hosting",
                            "use_cases": ["Production deployments", "Enterprise applications", "Scalable services"],
                            "steps": ["Package agent", "Create AdkApp", "Deploy to Vertex AI", "Configure endpoints"],
                            "benefits": ["Managed infrastructure", "Auto-scaling", "Integration with GCP services"]
                        },
                        {
                            "title": "Cloud Run Deployment",
                            "description": "Deploy agents as containerized services on Cloud Run",
                            "use_cases": ["Custom hosting", "Multi-cloud", "Flexible infrastructure"],
                            "steps": ["Containerize agent", "Build Docker image", "Deploy to Cloud Run", "Configure routing"],
                            "benefits": ["Flexibility", "Multi-cloud support", "Cost optimization"]
                        },
                        {
                            "title": "Local Development and Testing",
                            "description": "Use local execution for development and testing before deployment",
                            "practices": ["Use AdkApp.serve() for local testing", "Test with sample inputs", "Validate behavior"],
                            "benefits": ["Fast iteration", "Easy debugging", "Cost-free testing"]
                        },
                        {
                            "title": "Environment Configuration",
                            "description": "Use environment variables and config files for different deployment environments",
                            "practices": ["Separate dev/staging/prod configs", "Use secrets management", "Version control configs"],
                            "benefits": ["Security", "Flexibility", "Consistency"]
                        }
                    ]
                },
                "error_handling": {
                    "description": "Error handling and resilience patterns",
                    "practices": [
                        {
                            "title": "Graceful Degradation",
                            "description": "Design agents to handle failures gracefully and provide partial results",
                            "implementation": "Try-except blocks, fallback logic, default responses",
                            "benefits": ["Better UX", "Resilience", "Reliability"]
                        },
                        {
                            "title": "Retry Logic with Exponential Backoff",
                            "description": "Implement retry logic for transient failures",
                            "implementation": "Use tenacity library or custom retry decorators",
                            "benefits": ["Handle transient failures", "Rate limit protection", "Improved success rates"]
                        },
                        {
                            "title": "Comprehensive Logging",
                            "description": "Log all significant events, errors, and decisions",
                            "implementation": "Use Python logging module with appropriate levels",
                            "benefits": ["Debugging", "Monitoring", "Audit trails"]
                        },
                        {
                            "title": "Input Validation",
                            "description": "Validate all inputs before processing",
                            "implementation": "Use Pydantic models for type validation and data validation",
                            "benefits": ["Security", "Data quality", "Early error detection"]
                        }
                    ]
                },
                "model_selection": {
                    "description": "Guidelines for selecting appropriate models",
                    "practices": [
                        {
                            "title": "Gemini Flash for Speed",
                            "description": "Use Gemini Flash (1.5 or 2.0) for fast, cost-effective operations",
                            "use_cases": ["Simple tasks", "High-volume operations", "Quick responses", "Sub-agents"],
                            "characteristics": ["Low latency", "Cost-effective", "Good for straightforward tasks"],
                            "benefits": ["Fast execution", "Lower costs", "Scalability"]
                        },
                        {
                            "title": "Gemini Pro for Complex Reasoning",
                            "description": "Use Gemini Pro for complex reasoning and analysis tasks",
                            "use_cases": ["Complex analysis", "Strategic planning", "Creative tasks", "Root agents"],
                            "characteristics": ["Advanced reasoning", "Better context understanding", "Higher accuracy"],
                            "benefits": ["Quality", "Complex problem solving", "Better results"]
                        },
                        {
                            "title": "Model Selection Strategy",
                            "description": "Choose models based on task complexity and requirements",
                            "strategy": "Use Pro for root/complex agents, Flash for sub-agents and simple tasks",
                            "considerations": ["Task complexity", "Latency requirements", "Cost constraints", "Quality needs"],
                            "benefits": ["Cost optimization", "Performance balance", "Quality assurance"]
                        }
                    ]
                },
                "rag_integration": {
                    "description": "Retrieval-Augmented Generation (RAG) integration patterns",
                    "practices": [
                        {
                            "title": "Gemini File Search Integration",
                            "description": "Use Gemini File Search for RAG capabilities with document corpora",
                            "use_cases": ["Knowledge-base agents", "Documentation assistants", "Domain experts"],
                            "implementation": "Configure tool_config with Gemini File Search corpus",
                            "benefits": ["Accurate retrieval", "Managed infrastructure", "Easy integration"]
                        },
                        {
                            "title": "Knowledge Base Organization",
                            "description": "Organize knowledge bases with clear structure and metadata",
                            "practices": ["Group related documents", "Add metadata", "Version control", "Regular updates"],
                            "benefits": ["Better retrieval", "Maintainability", "Quality control"]
                        },
                        {
                            "title": "Source Citation",
                            "description": "Ensure agents cite sources when using RAG",
                            "implementation": "Configure agents to include source references in responses",
                            "benefits": ["Transparency", "Verification", "Trust", "Accuracy"]
                        }
                    ]
                },
                "performance_optimization": {
                    "description": "Performance optimization techniques",
                    "practices": [
                        {
                            "title": "Caching Strategies",
                            "description": "Implement caching for frequently accessed data and responses",
                            "implementation": "Use in-memory caching or external caching services",
                            "benefits": ["Reduced latency", "Cost savings", "Better UX"]
                        },
                        {
                            "title": "Parallel Execution",
                            "description": "Use ParallelAgent for independent operations",
                            "implementation": "Identify independent tasks and run them concurrently",
                            "benefits": ["Faster execution", "Better resource utilization", "Scalability"]
                        },
                        {
                            "title": "Prompt Optimization",
                            "description": "Optimize prompts for clarity and conciseness",
                            "practices": ["Clear instructions", "Minimal examples", "Structured output", "Avoid redundancy"],
                            "benefits": ["Better results", "Lower costs", "Faster responses"]
                        }
                    ]
                },
                "security": {
                    "description": "Security best practices for ADK agents",
                    "practices": [
                        {
                            "title": "Secret Management",
                            "description": "Use Google Secret Manager or environment variables for secrets",
                            "implementation": "Never hardcode secrets, use Secret Manager API",
                            "benefits": ["Security", "Compliance", "Auditability"]
                        },
                        {
                            "title": "Input Sanitization",
                            "description": "Sanitize and validate all user inputs",
                            "implementation": "Use Pydantic validation, escape special characters",
                            "benefits": ["Prevent injection attacks", "Data quality", "Security"]
                        },
                        {
                            "title": "Access Control",
                            "description": "Implement proper IAM and access controls",
                            "implementation": "Use GCP IAM, service accounts with minimal permissions",
                            "benefits": ["Security", "Compliance", "Least privilege"]
                        }
                    ]
                }
            },
            "common_patterns": {
                "agent_creation": {
                    "description": "Common patterns for creating agents",
                    "code_example": """
# Sequential Agent with Sub-agents
from google.adk import Agent, SequentialAgent

# Define sub-agents
requirements_agent = Agent(
    name="requirements_gatherer",
    instruction="Gather and analyze requirements...",
    model="gemini-2.0-flash-001"
)

design_agent = Agent(
    name="architecture_designer",
    instruction="Design system architecture...",
    model="gemini-2.0-flash-001"
)

# Create root sequential agent
root_agent = SequentialAgent(
    name="agent_builder_pro",
    instruction="Build complete agent systems...",
    model="gemini-1.5-pro",
    sub_agents=[requirements_agent, design_agent]
)
"""
                },
                "tool_definition": {
                    "description": "Common patterns for defining tools",
                    "code_example": """
# Python Function Tool
from google.adk import tool

@tool
def search_documentation(query: str) -> str:
    '''Search ADK documentation for relevant information.

    Args:
        query: Search query string

    Returns:
        Relevant documentation excerpts
    '''
    # Implementation
    return results

# MCP Tool Configuration (config.yaml)
tools:
  - type: mcp
    server: filesystem
    config:
      allowed_paths: ["/workspace"]
"""
                },
                "rag_configuration": {
                    "description": "Pattern for configuring RAG with Gemini File Search",
                    "code_example": """
# Configure RAG with File Search
from google.adk import Agent
from google.genai import FileSearchTool

file_search_tool = FileSearchTool(
    corpus_name="projects/{project}/locations/{location}/corpora/{corpus_id}"
)

agent = Agent(
    name="knowledge_agent",
    instruction="Answer questions using knowledge base...",
    model="gemini-1.5-pro",
    tool_config={
        "file_search": {
            "corpus_resource_name": corpus_name
        }
    }
)
"""
                }
            }
        }

        output_file = self.best_practices_dir / "adk_best_practices.json"
        output_file.write_text(json.dumps(best_practices, indent=2))
        print(f"   ✓ Created: {output_file.name}")

        self.manifest["files_collected"].append({
            "name": "adk_best_practices",
            "type": "best_practices",
            "file_path": str(output_file.relative_to(self.base_dir)),
            "size_bytes": output_file.stat().st_size
        })

        return True

    def create_agent_patterns_reference(self):
        """Create agent patterns reference guide."""
        print("\n🏗️  Creating Agent Patterns Reference...")

        patterns = {
            "version": "1.0.0",
            "last_updated": datetime.utcnow().isoformat(),
            "patterns": [
                {
                    "name": "Single Agent Pattern",
                    "description": "A standalone agent handling a specific task",
                    "complexity": "Simple",
                    "use_when": "Task is straightforward and doesn't require decomposition",
                    "structure": {
                        "agent_type": "Agent",
                        "sub_agents": 0,
                        "tools": "0-5"
                    },
                    "example_use_cases": [
                        "Document summarization",
                        "Data extraction",
                        "Simple Q&A",
                        "Text classification"
                    ],
                    "code_template": "agent = Agent(name='task_agent', instruction='...', model='gemini-2.0-flash-001')"
                },
                {
                    "name": "Sequential Multi-Agent Pattern",
                    "description": "Multiple agents executing in sequence, each building on previous results",
                    "complexity": "Moderate",
                    "use_when": "Tasks have dependencies and must be executed in order",
                    "structure": {
                        "agent_type": "SequentialAgent",
                        "sub_agents": "2-10",
                        "tools": "Variable per agent"
                    },
                    "example_use_cases": [
                        "Software development pipeline (requirements -> design -> code -> test)",
                        "Content creation workflow (research -> outline -> draft -> edit)",
                        "Data analysis pipeline (collect -> clean -> analyze -> visualize)",
                        "Agent building workflow"
                    ],
                    "code_template": "root = SequentialAgent(name='pipeline', sub_agents=[agent1, agent2, agent3], ...)"
                },
                {
                    "name": "Parallel Multi-Agent Pattern",
                    "description": "Multiple agents executing concurrently on independent tasks",
                    "complexity": "Moderate",
                    "use_when": "Tasks are independent and can run simultaneously",
                    "structure": {
                        "agent_type": "ParallelAgent",
                        "sub_agents": "2-10",
                        "tools": "Variable per agent"
                    },
                    "example_use_cases": [
                        "Multi-source data gathering",
                        "Concurrent analysis from different perspectives",
                        "Parallel validation checks",
                        "Multi-channel communication"
                    ],
                    "code_template": "root = ParallelAgent(name='parallel', sub_agents=[agent1, agent2, agent3], ...)"
                },
                {
                    "name": "Loop Agent Pattern",
                    "description": "Agent that iteratively refines output until criteria are met",
                    "complexity": "Moderate-Advanced",
                    "use_when": "Task requires iterative improvement or refinement",
                    "structure": {
                        "agent_type": "LoopAgent",
                        "sub_agents": "1-3",
                        "tools": "Variable"
                    },
                    "example_use_cases": [
                        "Code refinement loops",
                        "Quality improvement iterations",
                        "Test-driven development cycles",
                        "Creative refinement"
                    ],
                    "code_template": "root = LoopAgent(name='refiner', sub_agents=[generator, reviewer], max_iterations=5, ...)"
                },
                {
                    "name": "Hierarchical Agent Pattern",
                    "description": "Multi-level agent hierarchy with coordinator and specialized teams",
                    "complexity": "Advanced",
                    "use_when": "Complex systems requiring multiple specializations",
                    "structure": {
                        "agent_type": "Mixed (Sequential/Parallel root with nested structures)",
                        "sub_agents": "5+",
                        "levels": "2-3"
                    },
                    "example_use_cases": [
                        "Enterprise automation (CEO -> dept heads -> teams)",
                        "Complex project management",
                        "Large-scale system design",
                        "Multi-domain expert systems"
                    ],
                    "code_template": "ceo = SequentialAgent(name='ceo', sub_agents=[cto_team, cfo_team, cmo_team], ...)"
                },
                {
                    "name": "RAG-Enhanced Agent Pattern",
                    "description": "Agent with retrieval-augmented generation using knowledge bases",
                    "complexity": "Moderate-Advanced",
                    "use_when": "Agent needs access to large knowledge bases or documentation",
                    "structure": {
                        "agent_type": "Agent with RAG tool_config",
                        "knowledge_base": "Gemini File Search corpus",
                        "tools": "File search + custom tools"
                    },
                    "example_use_cases": [
                        "Documentation assistants",
                        "Domain expert agents",
                        "Technical support agents",
                        "Research assistants"
                    ],
                    "code_template": "agent = Agent(name='expert', tool_config={'file_search': {'corpus_resource_name': corpus}}, ...)"
                },
                {
                    "name": "Tool-Augmented Agent Pattern",
                    "description": "Agent with extensive tool integration for actions and data access",
                    "complexity": "Moderate",
                    "use_when": "Agent needs to interact with external systems and APIs",
                    "structure": {
                        "agent_type": "Agent",
                        "tools": "5+ tools (MCP servers + Python functions)",
                        "integrations": "Multiple external systems"
                    },
                    "example_use_cases": [
                        "SaaS integration agents",
                        "System automation agents",
                        "API orchestration",
                        "DevOps automation"
                    ],
                    "code_template": "agent = Agent(name='integrator', tools=[tool1, tool2, tool3], ...)"
                }
            ],
            "selection_guide": {
                "decision_tree": [
                    {
                        "question": "Does the task require multiple steps?",
                        "if_no": "Use Single Agent Pattern",
                        "if_yes": "Continue to next question"
                    },
                    {
                        "question": "Do steps have dependencies (must run in order)?",
                        "if_yes": "Use Sequential Multi-Agent Pattern",
                        "if_no": "Continue to next question"
                    },
                    {
                        "question": "Can steps run independently and concurrently?",
                        "if_yes": "Use Parallel Multi-Agent Pattern",
                        "if_no": "Continue to next question"
                    },
                    {
                        "question": "Does output need iterative refinement?",
                        "if_yes": "Use Loop Agent Pattern",
                        "if_no": "Continue to next question"
                    },
                    {
                        "question": "Is there a multi-level organizational structure?",
                        "if_yes": "Use Hierarchical Agent Pattern",
                        "if_no": "Use Sequential Multi-Agent Pattern as default"
                    }
                ],
                "additional_considerations": [
                    {
                        "consideration": "Need access to knowledge base?",
                        "add": "RAG-Enhanced Agent Pattern features"
                    },
                    {
                        "consideration": "Need external system integration?",
                        "add": "Tool-Augmented Agent Pattern features"
                    }
                ]
            }
        }

        output_file = self.best_practices_dir / "adk_agent_patterns.json"
        output_file.write_text(json.dumps(patterns, indent=2))
        print(f"   ✓ Created: {output_file.name}")

        self.manifest["files_collected"].append({
            "name": "adk_agent_patterns",
            "type": "patterns_reference",
            "file_path": str(output_file.relative_to(self.base_dir)),
            "size_bytes": output_file.stat().st_size
        })

        return True

    def generate_manifest(self):
        """Generate final knowledge manifest."""
        print("\n📋 Generating knowledge manifest...")

        # Calculate statistics
        total_files = len(self.manifest["files_collected"])
        total_size = sum(f.get("size_bytes", 0) for f in self.manifest["files_collected"])

        self.manifest["statistics"] = {
            "total_files": total_files,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "sources_count": len(self.manifest["sources"]),
            "documentation_pages": len([f for f in self.manifest["files_collected"] if f["type"] == "documentation"]),
            "repositories_cloned": len([s for s in self.manifest["sources"] if s["type"] == "git_repository" and s["status"] == "success"]),
            "best_practices_files": len([f for f in self.manifest["files_collected"] if f["type"] in ["best_practices", "patterns_reference"]])
        }

        # Save manifest
        manifest_file = self.corpus_dir / "knowledge_manifest.json"
        manifest_file.write_text(json.dumps(self.manifest, indent=2))
        print(f"   ✓ Saved: {manifest_file}")

        # Also save to outputs
        output_manifest = Path("/mnt/user-data/outputs/02_knowledge_manifest.json")
        output_manifest.parent.mkdir(parents=True, exist_ok=True)
        output_manifest.write_text(json.dumps(self.manifest, indent=2))
        print(f"   ✓ Saved copy to: {output_manifest}")

    def run(self):
        """Execute the complete knowledge collection process."""
        print("=" * 70)
        print("ADK KNOWLEDGE COLLECTION - PHASE 1")
        print("=" * 70)

        try:
            # Step 1: Setup
            self.setup_directories()

            # Step 2: Clone repositories
            self.clone_repository(
                "https://github.com/google/adk-starter-kit",
                self.starter_kit_dir / "adk-starter-kit",
                "ADK Starter Kit"
            )

            self.clone_repository(
                "https://github.com/google/adk-sample-agents",
                self.sample_agents_dir / "adk-sample-agents",
                "ADK Sample Agents"
            )

            # Step 3: Fetch documentation
            self.fetch_adk_documentation()

            # Step 4: Create best practices
            self.create_adk_best_practices()

            # Step 5: Create patterns reference
            self.create_agent_patterns_reference()

            # Step 6: Generate manifest
            self.generate_manifest()

            # Final summary
            print("\n" + "=" * 70)
            print("✅ KNOWLEDGE COLLECTION COMPLETE")
            print("=" * 70)
            print(f"Total files collected: {self.manifest['statistics']['total_files']}")
            print(f"Total size: {self.manifest['statistics']['total_size_mb']} MB")
            print(f"Documentation pages: {self.manifest['statistics']['documentation_pages']}")
            print(f"Repositories cloned: {self.manifest['statistics']['repositories_cloned']}")
            print(f"Best practices files: {self.manifest['statistics']['best_practices_files']}")
            print("\nKnowledge corpus ready at: knowledge_corpus/")
            print("Manifest saved to: knowledge_corpus/knowledge_manifest.json")
            print("=" * 70)

            return True

        except Exception as e:
            print(f"\n❌ ERROR: Knowledge collection failed: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Main entry point."""
    collector = ADKKnowledgeCollector()
    success = collector.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
