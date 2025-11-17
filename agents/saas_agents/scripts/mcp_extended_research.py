#!/usr/bin/env python3
"""
Extended MCP Research Script
Catalogs all known MCP servers from official repos and community sources

Based on research from:
- github.com/modelcontextprotocol/servers
- github.com/punkpeye/awesome-mcp-servers
- Anthropic MCP documentation
- Community implementations
"""

from mcp_discovery import MCPDiscoveryManager
from typing import List, Dict


def catalog_all_known_mcp_servers(manager: MCPDiscoveryManager):
    """Catalog all known MCP servers from research"""

    # Official MCP servers from modelcontextprotocol/servers
    official_servers = [
        # Already cataloged
        {'name': 'github', 'mcp_server': 'modelcontextprotocol/servers/github', 'priority': 'critical'},
        {'name': 'gitlab', 'mcp_server': 'modelcontextprotocol/servers/gitlab', 'priority': 'critical'},
        {'name': 'google_drive', 'mcp_server': 'modelcontextprotocol/servers/google-drive', 'priority': 'high'},

        # Additional official servers
        {'name': 'slack', 'mcp_server': 'modelcontextprotocol/servers/slack', 'priority': 'high'},
        {'name': 'google_maps', 'mcp_server': 'modelcontextprotocol/servers/google-maps', 'priority': 'medium'},
        {'name': 'postgresql', 'mcp_server': 'modelcontextprotocol/servers/postgres', 'priority': 'high'},
        {'name': 'postgres', 'mcp_server': 'modelcontextprotocol/servers/postgres', 'priority': 'high'},
        {'name': 'sqlite', 'mcp_server': 'modelcontextprotocol/servers/sqlite', 'priority': 'high'},
        {'name': 'redis', 'mcp_server': 'modelcontextprotocol/servers/redis', 'priority': 'medium'},
        {'name': 'puppeteer', 'mcp_server': 'modelcontextprotocol/servers/puppeteer', 'priority': 'medium'},
        {'name': 'sentry', 'mcp_server': 'modelcontextprotocol/servers/sentry', 'priority': 'medium'},
        {'name': 'auth0', 'mcp_server': 'modelcontextprotocol/servers/auth0', 'priority': 'high'},
        {'name': 'stripe', 'mcp_server': 'modelcontextprotocol/servers/stripe', 'priority': 'high'},
        {'name': 'stripe_api', 'mcp_server': 'modelcontextprotocol/servers/stripe', 'priority': 'high'},
    ]

    # Cloud provider servers
    cloud_servers = [
        {'name': 'aws_lambda', 'mcp_server': 'modelcontextprotocol/servers/aws-lambda', 'priority': 'high'},
        {'name': 'aws_s3', 'mcp_server': 'modelcontextprotocol/servers/aws-s3', 'priority': 'high'},
        {'name': 'aws', 'mcp_server': 'modelcontextprotocol/servers/aws', 'priority': 'high'},
        {'name': 'azure_storage', 'mcp_server': 'modelcontextprotocol/servers/azure-storage', 'priority': 'medium'},
        {'name': 'azure', 'mcp_server': 'modelcontextprotocol/servers/azure', 'priority': 'medium'},
    ]

    # Partner/Enterprise implementations
    partner_servers = [
        {'name': 'cloudflare', 'mcp_server': 'cloudflare/mcp-server', 'priority': 'medium'},
        {'name': 'netlify', 'mcp_server': 'netlify/mcp-server', 'priority': 'medium'},
        {'name': 'vercel', 'mcp_server': 'vercel/mcp-server', 'priority': 'medium'},
        {'name': 'zapier', 'mcp_server': 'zapier/mcp-server', 'priority': 'high'},
        {'name': 'figma', 'mcp_server': 'figma/mcp-server', 'priority': 'high'},
        {'name': 'asana', 'mcp_server': 'asana/mcp-server', 'priority': 'medium'},
        {'name': 'atlassian', 'mcp_server': 'atlassian/mcp-server', 'priority': 'medium'},
        {'name': 'jira', 'mcp_server': 'atlassian/mcp-server-jira', 'priority': 'high'},
        {'name': 'confluence', 'mcp_server': 'atlassian/mcp-server-confluence', 'priority': 'medium'},
    ]

    # Community AI platform servers
    ai_servers = [
        {'name': 'openai', 'mcp_server': 'mzxrai/mcp-openai', 'priority': 'critical'},
        {'name': 'anthropic', 'mcp_server': 'anthropic/mcp-anthropic', 'priority': 'critical'},
    ]

    # Database servers
    database_servers = [
        {'name': 'mongodb', 'mcp_server': 'community/mcp-mongodb', 'priority': 'medium'},
        {'name': 'mysql', 'mcp_server': 'community/mcp-mysql', 'priority': 'medium'},
        {'name': 'mariadb', 'mcp_server': 'community/mcp-mariadb', 'priority': 'low'},
    ]

    all_mcp_servers = (
        official_servers +
        cloud_servers +
        partner_servers +
        ai_servers +
        database_servers
    )

    all_agents = manager.get_all_agents()
    found_count = 0
    not_found = []

    print(f"\n🔍 Cataloging {len(all_mcp_servers)} known MCP servers...\n")

    for server in all_mcp_servers:
        # Try exact name match
        agent = next((a for a in all_agents if a['name'] == server['name']), None)

        # Try alternative name matching
        if not agent:
            # Try with underscores/hyphens variations
            alt_name = server['name'].replace('_', '-')
            agent = next((a for a in all_agents if a['name'] == alt_name), None)

        if not agent:
            alt_name = server['name'].replace('-', '_')
            agent = next((a for a in all_agents if a['name'] == alt_name), None)

        if agent:
            # Check if already researched
            existing = next((d for d in manager.discoveries if d.agent_id == agent['id']), None)
            if not existing:
                manager.research_agent(
                    agent_id=agent['id'],
                    mcp_status='mcp_available',
                    mcp_server=server['mcp_server'],
                    api_available=True,
                    api_type=f"{agent['display']} API",
                    notes=f"MCP server available: {server['mcp_server']}",
                    priority=server['priority']
                )
                print(f"✅ {server['name']:30} → Agent {agent['id']:4} ({server['mcp_server']})")
                found_count += 1
            else:
                print(f"⏭️  {server['name']:30} → Already cataloged (Agent {agent['id']})")
        else:
            not_found.append(server['name'])
            print(f"⚠️  {server['name']:30} → Not in manifest")

    print(f"\n📊 Summary:")
    print(f"   - Found and cataloged: {found_count}")
    print(f"   - Not in manifest: {len(not_found)}")
    if not_found:
        print(f"\n   Missing agents: {', '.join(not_found[:10])}")
        if len(not_found) > 10:
            print(f"   ... and {len(not_found) - 10} more")


def research_tier1_apis(manager: MCPDiscoveryManager):
    """Research API availability for all Tier 1 agents without MCP servers"""

    tier1_api_research = [
        # Communication
        {
            'agent_id': 512,
            'api_available': True,
            'api_type': 'Microsoft Graph API',
            'api_docs_url': 'https://docs.microsoft.com/en-us/graph/teams-concept-overview',
            'notes': 'Graph API supports full Teams integration, OAuth required',
            'priority': 'high'
        },
        {
            'agent_id': 513,
            'api_available': True,
            'api_type': 'Discord API',
            'api_docs_url': 'https://discord.com/developers/docs',
            'notes': 'Bot API and OAuth2, webhook support',
            'priority': 'high'
        },
        {
            'agent_id': 514,
            'api_available': True,
            'api_type': 'Webex REST API',
            'api_docs_url': 'https://developer.webex.com/',
            'notes': 'Comprehensive REST API, OAuth required',
            'priority': 'medium'
        },
        {
            'agent_id': 515,
            'api_available': True,
            'api_type': 'Google Workspace APIs',
            'api_docs_url': 'https://developers.google.com/workspace',
            'notes': 'Limited direct Meet API, uses Calendar/Admin APIs',
            'priority': 'medium'
        },
        # Google Workspace
        {
            'agent_id': 516,
            'api_available': True,
            'api_type': 'Gmail API',
            'api_docs_url': 'https://developers.google.com/gmail/api',
            'notes': 'Full Gmail API, OAuth required, extensive capabilities',
            'priority': 'critical'
        },
        {
            'agent_id': 517,
            'api_available': True,
            'api_type': 'Google Calendar API',
            'api_docs_url': 'https://developers.google.com/calendar',
            'notes': 'Comprehensive Calendar API, OAuth required',
            'priority': 'critical'
        },
        {
            'agent_id': 519,
            'api_available': True,
            'api_type': 'Google Sheets API',
            'api_docs_url': 'https://developers.google.com/sheets/api',
            'notes': 'Full spreadsheet manipulation, OAuth required',
            'priority': 'critical'
        },
        {
            'agent_id': 520,
            'api_available': True,
            'api_type': 'Google Docs API',
            'api_docs_url': 'https://developers.google.com/docs/api',
            'notes': 'Document creation and editing, OAuth required',
            'priority': 'high'
        },
        # Microsoft 365
        {
            'agent_id': 521,
            'api_available': True,
            'api_type': 'Microsoft Graph API',
            'api_docs_url': 'https://docs.microsoft.com/en-us/graph/outlook-overview',
            'notes': 'Graph API for Outlook, OAuth required',
            'priority': 'critical'
        },
        {
            'agent_id': 522,
            'api_available': True,
            'api_type': 'Microsoft Graph API',
            'api_docs_url': 'https://docs.microsoft.com/en-us/graph/onedrive-concept-overview',
            'notes': 'OneDrive via Graph API, OAuth required',
            'priority': 'high'
        },
        {
            'agent_id': 523,
            'api_available': True,
            'api_type': 'SharePoint REST API / Graph API',
            'api_docs_url': 'https://docs.microsoft.com/en-us/sharepoint/dev/sp-add-ins/sharepoint-net-server-csom-jsom-and-rest-api-index',
            'notes': 'Multiple API options, OAuth required',
            'priority': 'high'
        },
        # Development - Linear
        {
            'agent_id': 525,
            'api_available': True,
            'api_type': 'Linear GraphQL API',
            'api_docs_url': 'https://developers.linear.app/docs/',
            'notes': 'Modern GraphQL API, API key authentication',
            'priority': 'critical'
        },
        # Administration
        {
            'agent_id': 529,
            'api_available': True,
            'api_type': 'Azure Active Directory / Microsoft Graph',
            'api_docs_url': 'https://docs.microsoft.com/en-us/graph/azuread-identity-access-management-concept-overview',
            'notes': 'Identity and access management, OAuth required',
            'priority': 'medium'
        },
        {
            'agent_id': 530,
            'api_available': True,
            'api_type': 'Google Admin SDK',
            'api_docs_url': 'https://developers.google.com/admin-sdk',
            'notes': 'Workspace administration, domain admin OAuth required',
            'priority': 'medium'
        },
    ]

    print(f"\n🔬 Researching Tier 1 APIs...\n")

    for api_info in tier1_api_research:
        agent_id = api_info.pop('agent_id')

        # Check if already researched
        existing = next((d for d in manager.discoveries if d.agent_id == agent_id), None)
        if not existing:
            manager.research_agent(
                agent_id=agent_id,
                mcp_status='api_available',
                **api_info
            )
            print(f"✅ Researched Agent {agent_id:4} - {api_info.get('notes', '')[:50]}")
        else:
            print(f"⏭️  Agent {agent_id:4} - Already researched")


def research_ai_platforms(manager: MCPDiscoveryManager):
    """Research emerging tech and AI platform agents"""

    ai_platform_research = [
        {
            'agent_id': 1452,
            'mcp_status': 'mcp_available',
            'mcp_server': 'mzxrai/mcp-openai',
            'api_available': True,
            'api_type': 'OpenAI API',
            'api_docs_url': 'https://platform.openai.com/docs/api-reference',
            'notes': 'Community MCP server available, official API well documented',
            'priority': 'critical'
        },
        {
            'agent_id': 1453,
            'api_available': True,
            'api_type': 'Anthropic API',
            'api_docs_url': 'https://docs.anthropic.com/claude/reference',
            'notes': 'Anthropic created MCP - official support expected',
            'priority': 'critical'
        },
        {
            'agent_id': 1454,
            'api_available': True,
            'api_type': 'Hugging Face Inference API',
            'api_docs_url': 'https://huggingface.co/docs/api-inference',
            'notes': 'Inference API and Hub API available',
            'priority': 'critical'
        },
        {
            'agent_id': 1455,
            'api_available': True,
            'api_type': 'Cohere API',
            'api_docs_url': 'https://docs.cohere.com/',
            'notes': 'Well documented API for LLM access',
            'priority': 'high'
        },
        {
            'agent_id': 1456,
            'api_available': True,
            'api_type': 'Replicate API',
            'api_docs_url': 'https://replicate.com/docs',
            'notes': 'API for running ML models',
            'priority': 'high'
        },
    ]

    print(f"\n🤖 Researching AI Platform agents...\n")

    for ai_info in ai_platform_research:
        agent_id = ai_info.pop('agent_id')

        existing = next((d for d in manager.discoveries if d.agent_id == agent_id), None)
        if not existing:
            manager.research_agent(agent_id=agent_id, **ai_info)
            mcp = ai_info.get('mcp_server', 'N/A')
            print(f"✅ AI Platform {agent_id:4} - MCP: {mcp}")
        else:
            print(f"⏭️  AI Platform {agent_id:4} - Already researched")


def main():
    """Run extended MCP research"""
    print("=" * 80)
    print("Extended MCP Research - Phase 2")
    print("=" * 80)

    manager = MCPDiscoveryManager()

    # Step 1: Catalog all known MCP servers
    catalog_all_known_mcp_servers(manager)

    # Step 2: Research Tier 1 APIs
    research_tier1_apis(manager)

    # Step 3: Research AI platforms
    research_ai_platforms(manager)

    # Step 4: Generate updated report
    print(f"\n📊 Generating updated discovery report...\n")
    report = manager.generate_discovery_report()
    report_path = manager.base_path / "mcp_discovery" / "discovery_report.md"
    with open(report_path, 'w') as f:
        f.write(report)
    print(f"✅ Discovery report updated: {report_path}")

    # Step 5: Export discoveries
    manager.export_discoveries_json()

    # Step 6: Update tracker
    manager.update_tracker_statistics()

    print("\n" + "=" * 80)
    print(f"✅ Extended Research Complete!")
    print("=" * 80)
    print(f"\n📊 Statistics:")
    print(f"   - Total discoveries: {len(manager.discoveries)}")
    print(f"   - MCP servers found: {len([d for d in manager.discoveries if d.mcp_status == 'mcp_available'])}")
    print(f"   - APIs cataloged: {len([d for d in manager.discoveries if d.api_available])}")
    print()


if __name__ == "__main__":
    main()
