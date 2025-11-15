#!/usr/bin/env python3
"""
Script to generate the complete multi-agent hierarchy based on agent_hierarchy.json
"""

import json
import os
from pathlib import Path
import csv
import shutil


# Paths
BASE_DIR = Path("/home/user/mapachev1/mapachev1")
HIERARCHY_JSON = BASE_DIR / "docs/architecture/agent_hierarchy.json"
AGENT_INVENTORY_CSV = BASE_DIR / "docs/analysis/agent_inventory.csv"
ORIGINAL_AGENTS_DIR = Path("/home/user/mapachev1/python/agents")
APP_DIR = BASE_DIR / "app"
AGENTS_DIR = APP_DIR / "agents"
COORDINATORS_DIR = AGENTS_DIR / "coordinators"
TEAMS_DIR = AGENTS_DIR / "teams"
SPECIALISTS_DIR = AGENTS_DIR / "specialists"


def to_snake_case(text):
    """Convert text to snake_case"""
    # Replace spaces and special characters with underscores
    text = text.replace(", ", "_")  # Handle commas first
    text = text.replace(",", "_")   # Handle remaining commas
    text = text.replace(" & ", "_")
    text = text.replace("&", "_")
    text = text.replace(" ", "_")
    text = text.replace("-", "_")
    text = text.replace("/", "_")
    # Remove any double underscores
    while "__" in text:
        text = text.replace("__", "_")
    text = text.lower()
    # Ensure the name starts with a letter or underscore (Python identifier requirement)
    if text and text[0].isdigit():
        text = "n_" + text  # Prepend 'n_' for names starting with numbers
    return text


def to_python_class_name(text):
    """Convert text to PythonClassName"""
    # Remove special characters and convert to title case
    text = text.replace(" & ", " ")
    text = text.replace("-", " ")
    text = text.replace("/", " ")
    words = text.split()
    return "".join(word.capitalize() for word in words)


def load_agent_inventory():
    """Load agent inventory CSV"""
    agents = {}
    with open(AGENT_INVENTORY_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            agent_num = row['agent_number']
            agents[f"agent_{agent_num}"] = {
                'name': row['agent_name'],
                'description': row['description'],
                'file': row['agent_file']
            }
    return agents


def generate_division_coordinator(division_data, teams_modules):
    """Generate a division coordinator Python file"""
    division_id = division_data['id']
    division_name = division_data['name']
    description = division_data['description']
    model = division_data['model']

    # Generate filename
    filename = f"{to_snake_case(division_id)}.py"

    # Convert division name to valid identifier
    division_name_identifier = to_snake_case(division_name)

    # Generate imports
    imports = []
    sub_agent_names = []
    for team in division_data['sub_agents']:
        team_id = team['id']
        team_module = to_snake_case(team_id)
        team_var = to_snake_case(team['name']).replace('_team', '').replace('_', '_')
        imports.append(f"from app.agents.teams.{team_module} import {team_module}")
        sub_agent_names.append(team_module)

    imports_str = "\n".join(imports)
    sub_agents_str = ", ".join(sub_agent_names)

    # Generate routing instructions
    team_descriptions = []
    for team in division_data['sub_agents']:
        team_name = team['name']
        team_descriptions.append(f"  - {team_name}: {team['description']}")

    teams_list = "\n".join(team_descriptions)

    instruction = f'''You are the {division_name} coordinator.

Your role is to route requests to the appropriate team based on the nature of the request.

Available teams:
{teams_list}

Routing Guidelines:
- Analyze the incoming request carefully
- Determine which team is best suited to handle it
- Route to the most specialized team when possible
- Escalate complex cross-team issues as needed
- Ensure high quality and timely responses

Always route to sub-agents. Do not attempt to answer requests directly.'''

    # Generate file content
    content = f'''"""
{division_name} Coordinator

This coordinator manages {division_name.lower()} functions.
"""

from google.adk.agents import LlmAgent
{imports_str}


{to_snake_case(division_id)} = LlmAgent(
    name="{division_name_identifier}",
    model="{model}",
    description="{description}",
    sub_agents=[{sub_agents_str}],
    instruction="""{instruction}"""
)
'''

    return filename, content


def generate_team_agent(team_data, specialists_modules, division_name):
    """Generate a team agent Python file"""
    team_id = team_data['id']
    team_name = team_data['name']
    description = team_data['description']
    model = team_data['model']
    specialists = team_data.get('specialists', [])

    # Generate filename
    filename = f"{to_snake_case(team_id)}.py"

    # Convert team name to valid identifier
    team_name_identifier = to_snake_case(team_name)

    # Generate imports
    imports = []
    sub_agent_names = []

    # Group specialists by domain for organization
    division_module = to_snake_case(division_name).replace('_division', '')

    for agent_id in specialists:
        agent_module = agent_id  # e.g., "agent_001"
        imports.append(f"from app.agents.specialists.{division_module}.{agent_module} import {agent_module}")
        sub_agent_names.append(agent_module)

    imports_str = "\n".join(imports) if imports else "# No specialist imports yet"
    sub_agents_str = ", ".join(sub_agent_names) if sub_agent_names else ""

    # Generate routing instructions
    instruction = f'''You are the {team_name} coordinator.

Your role is to route requests to the appropriate specialist agent based on their expertise.

Available specialists: {len(specialists)} specialized agents

Routing Guidelines:
- Analyze the incoming request to understand the specific expertise needed
- Route to the specialist best suited for the task
- Consider specialist availability and workload
- Ensure requests are handled by the most qualified agent
- Coordinate multi-specialist tasks when needed

Always route to sub-agents when available. Provide direct assistance only when no specialist is available.'''

    # Generate file content
    content = f'''"""
{team_name}

This team handles {description.lower()}.
"""

from google.adk.agents import LlmAgent
{imports_str}


{to_snake_case(team_id)} = LlmAgent(
    name="{team_name_identifier}",
    model="{model}",
    description="{description}",
    sub_agents=[{sub_agents_str}],
    instruction="""{instruction}"""
)
'''

    return filename, content


def generate_specialist_agent(agent_id, agent_info, division_module):
    """Generate a specialist agent Python file"""
    filename = f"{agent_id}.py"

    name = agent_info['name']
    description = agent_info['description']

    # Convert name to valid identifier (snake_case)
    agent_name_identifier = to_snake_case(name)

    # Generate file content (simple stub for now)
    content = f'''"""
{description}
"""

from google.adk.agents import LlmAgent


{agent_id} = LlmAgent(
    name="{agent_name_identifier}",
    model="gemini-flash",
    description="{description}",
    instruction="""You are a {name.lower()} specialist.

Handle requests related to {name.lower()} with expertise and precision.
Provide detailed, accurate, and helpful responses based on your specialized knowledge.
"""
)
'''

    return filename, content


def generate_root_orchestrator(hierarchy_data, divisions_modules):
    """Generate the root orchestrator"""
    root_data = hierarchy_data['root']

    # Convert root name to valid identifier
    root_name_identifier = to_snake_case(root_data['name'])

    # Generate imports
    imports = []
    sub_agent_names = []
    for division in root_data['sub_agents']:
        division_id = division['id']
        division_module = to_snake_case(division_id)
        imports.append(f"from app.agents.coordinators.{division_module} import {division_module}")
        sub_agent_names.append(division_module)

    imports_str = "\n".join(imports)
    sub_agents_str = ", ".join(sub_agent_names)

    # Generate routing instructions
    division_descriptions = []
    for division in root_data['sub_agents']:
        division_name = division['name']
        division_descriptions.append(f"  - {division_name}: {division['description']}")

    divisions_list = "\n".join(division_descriptions)

    instruction = f'''You are the Root Orchestrator, the master coordinator of the entire organization.

Your role is to analyze incoming requests and route them to the appropriate division coordinator.

Available divisions:
{divisions_list}

Routing Guidelines:
- Carefully analyze each request to understand its functional area
- Route to the most appropriate division based on the request type
- Consider cross-functional requests and route to the primary responsible division
- Balance load across divisions when multiple could handle a request
- Ensure all requests receive expert attention from the right division
- Track routing patterns to optimize future decisions

Always route to division coordinators. Do not attempt to answer requests directly.
You are a router and coordinator, not an executor.'''

    content = f'''"""
Root Orchestrator - Master Coordinator

This is the root orchestrator that routes requests to appropriate divisions.
"""

from google.adk.agents import LlmAgent
{imports_str}


root_orchestrator = LlmAgent(
    name="{root_name_identifier}",
    model="{root_data['model']}",
    description="{root_data['description']}",
    sub_agents=[{sub_agents_str}],
    instruction="""{instruction}"""
)

# Export for ADK
agent = root_orchestrator
app = root_orchestrator  # Alias for compatibility
'''

    return content


def create_init_files():
    """Create __init__.py files for all directories"""
    init_files = []

    # Main agents __init__.py
    agents_init = AGENTS_DIR / "__init__.py"
    init_files.append((agents_init, '"""Agent modules"""'))

    # Coordinators __init__.py
    coordinators_init = COORDINATORS_DIR / "__init__.py"
    init_files.append((coordinators_init, '"""Division coordinator agents"""'))

    # Teams __init__.py
    teams_init = TEAMS_DIR / "__init__.py"
    init_files.append((teams_init, '"""Team agents"""'))

    # Specialists __init__.py
    specialists_init = SPECIALISTS_DIR / "__init__.py"
    init_files.append((specialists_init, '"""Specialist agents"""'))

    # Specialist subdirectories __init__.py
    for subdir in SPECIALISTS_DIR.iterdir():
        if subdir.is_dir():
            init_file = subdir / "__init__.py"
            init_files.append((init_file, f'"""Specialist agents for {subdir.name}"""'))

    return init_files


def main():
    """Main generation function"""
    print("=== Starting Agent Generation ===\n")

    # Load hierarchy
    print("Loading hierarchy JSON...")
    with open(HIERARCHY_JSON, 'r') as f:
        hierarchy = json.load(f)

    # Load agent inventory
    print("Loading agent inventory...")
    agents_inventory = load_agent_inventory()

    root_data = hierarchy['root']
    divisions = root_data['sub_agents']

    # Statistics
    stats = {
        'divisions': 0,
        'teams': 0,
        'specialists': 0,
        'files_created': 0
    }

    # Generate division coordinators
    print("\n--- Generating Division Coordinators ---")
    for division in divisions:
        division_id = division['id']
        division_name = division['name']

        filename, content = generate_division_coordinator(division, division['sub_agents'])
        filepath = COORDINATORS_DIR / filename

        with open(filepath, 'w') as f:
            f.write(content)

        print(f"Created: {filepath.name}")
        stats['divisions'] += 1
        stats['files_created'] += 1

    # Generate team agents
    print("\n--- Generating Team Agents ---")
    for division in divisions:
        division_id = division['id']
        division_name = division_id

        for team in division['sub_agents']:
            filename, content = generate_team_agent(team, team.get('specialists', []), division_name)
            filepath = TEAMS_DIR / filename

            with open(filepath, 'w') as f:
                f.write(content)

            print(f"Created: {filepath.name}")
            stats['teams'] += 1
            stats['files_created'] += 1

    # Generate specialist agents
    print("\n--- Generating Specialist Agents ---")
    for division in divisions:
        division_id = division['id']
        division_module = to_snake_case(division_id).replace('_division', '')
        division_specialists_dir = SPECIALISTS_DIR / division_module

        # Ensure directory exists
        division_specialists_dir.mkdir(parents=True, exist_ok=True)

        # Collect all specialists for this division
        all_specialists = []
        for team in division['sub_agents']:
            all_specialists.extend(team.get('specialists', []))

        # Generate specialist files
        for agent_id in all_specialists:
            if agent_id in agents_inventory:
                agent_info = agents_inventory[agent_id]
                filename, content = generate_specialist_agent(agent_id, agent_info, division_module)
                filepath = division_specialists_dir / filename

                with open(filepath, 'w') as f:
                    f.write(content)

                stats['specialists'] += 1
                stats['files_created'] += 1

        print(f"Created {len(all_specialists)} specialists in {division_module}/")

    # Generate root orchestrator
    print("\n--- Generating Root Orchestrator ---")
    root_content = generate_root_orchestrator(hierarchy, divisions)
    root_filepath = APP_DIR / "agent.py"

    with open(root_filepath, 'w') as f:
        f.write(root_content)

    print(f"Created: {root_filepath.name}")
    stats['files_created'] += 1

    # Create __init__.py files
    print("\n--- Creating __init__.py Files ---")
    init_files = create_init_files()

    for filepath, content in init_files:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Created: {filepath}")
        stats['files_created'] += 1

    # Print statistics
    print("\n=== Generation Complete ===")
    print(f"\nStatistics:")
    print(f"  - Divisions Created: {stats['divisions']}")
    print(f"  - Teams Created: {stats['teams']}")
    print(f"  - Specialists Created: {stats['specialists']}")
    print(f"  - Total Files Created: {stats['files_created']}")
    print(f"  - __init__.py Files: {len(init_files)}")

    print("\nDirectory Structure:")
    print(f"  - Coordinators: {COORDINATORS_DIR}")
    print(f"  - Teams: {TEAMS_DIR}")
    print(f"  - Specialists: {SPECIALISTS_DIR}")
    print(f"  - Root Orchestrator: {root_filepath}")


if __name__ == "__main__":
    main()
