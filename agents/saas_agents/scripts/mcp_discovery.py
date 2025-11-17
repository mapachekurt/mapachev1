#!/usr/bin/env python3
"""
MCP Server Discovery and Cataloging Script
Phase 2: MCP Integration for SaaS Agent Army

This script helps discover and catalog MCP server availability for all 1000 SaaS agents.
"""

import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class MCPDiscovery:
    """Data class for MCP discovery results"""
    agent_id: int
    name: str
    display_name: str
    category: str
    tier: str
    mcp_status: str  # mcp_available, api_available, api_documented, no_public_api, research_pending
    mcp_server: Optional[str] = None
    api_available: bool = False
    api_type: Optional[str] = None
    api_docs_url: Optional[str] = None
    notes: str = ""
    priority: str = "medium"  # critical, high, medium, low
    researched_date: Optional[str] = None


class MCPDiscoveryManager:
    """Manage MCP discovery process for SaaS agents"""

    def __init__(self, base_path: str = "agents/saas_agents"):
        self.base_path = Path(base_path)
        self.tracker_path = self.base_path / "mcp_discovery" / "mcp_availability_tracker.yaml"
        self.manifest_path = self.base_path / "saas_tools_manifest.yaml"
        self.discoveries: List[MCPDiscovery] = []

    def load_manifest(self) -> Dict:
        """Load the SaaS tools manifest"""
        with open(self.manifest_path, 'r') as f:
            return yaml.safe_load(f)

    def load_tracker(self) -> Dict:
        """Load the MCP availability tracker"""
        with open(self.tracker_path, 'r') as f:
            return yaml.safe_load(f)

    def save_tracker(self, data: Dict):
        """Save updated tracker data"""
        with open(self.tracker_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, indent=2)

    def get_all_agents(self) -> List[Dict]:
        """Extract all agents from manifest"""
        manifest = self.load_manifest()
        all_agents = []

        tiers = manifest.get('tiers', {})

        for tier_key, tier_data in tiers.items():
            if tier_key.startswith('tier_'):
                tier_name = tier_key

                # Handle direct agents list (Tier 1)
                if 'agents' in tier_data:
                    for agent in tier_data['agents']:
                        agent['tier'] = tier_name
                        if 'category' not in agent:
                            agent['category'] = 'general'
                        all_agents.append(agent)

                # Handle categorized agents (Tier 2-5)
                if 'categories' in tier_data:
                    for category_key, category_data in tier_data['categories'].items():
                        for agent in category_data.get('agents', []):
                            agent['tier'] = tier_name
                            if 'category' not in agent:
                                agent['category'] = category_key
                            all_agents.append(agent)

        return all_agents

    def research_agent(self, agent_id: int, **updates) -> MCPDiscovery:
        """
        Record research findings for an agent

        Usage:
            manager.research_agent(
                agent_id=512,
                mcp_status="mcp_available",
                mcp_server="modelcontextprotocol/servers/teams",
                api_available=True,
                api_type="Microsoft Graph API",
                api_docs_url="https://docs.microsoft.com/graph",
                notes="Official MCP server available",
                priority="high"
            )
        """
        all_agents = self.get_all_agents()
        agent = next((a for a in all_agents if a['id'] == agent_id), None)

        if not agent:
            raise ValueError(f"Agent {agent_id} not found in manifest")

        discovery = MCPDiscovery(
            agent_id=agent['id'],
            name=agent['name'],
            display_name=agent['display'],
            category=agent.get('category', 'unknown'),
            tier=agent.get('tier', 'unknown'),
            mcp_status=updates.get('mcp_status', 'research_pending'),
            mcp_server=updates.get('mcp_server'),
            api_available=updates.get('api_available', False),
            api_type=updates.get('api_type'),
            api_docs_url=updates.get('api_docs_url'),
            notes=updates.get('notes', ''),
            priority=updates.get('priority', 'medium'),
            researched_date=datetime.now().strftime('%Y-%m-%d')
        )

        self.discoveries.append(discovery)
        return discovery

    def batch_research_known_mcp_servers(self):
        """Research and catalog known MCP servers from official repos"""

        # Known MCP servers from modelcontextprotocol/servers
        known_servers = [
            {
                'name': 'github',
                'mcp_server': 'modelcontextprotocol/servers/github',
                'api_type': 'GitHub REST API',
                'api_docs_url': 'https://docs.github.com/rest',
                'priority': 'critical',
                'notes': 'Official MCP server available'
            },
            {
                'name': 'gitlab',
                'mcp_server': 'modelcontextprotocol/servers/gitlab',
                'api_type': 'GitLab REST API',
                'api_docs_url': 'https://docs.gitlab.com/ee/api/',
                'priority': 'critical',
                'notes': 'Official MCP server available'
            },
            {
                'name': 'google_drive',
                'mcp_server': 'modelcontextprotocol/servers/google-drive',
                'api_type': 'Google Drive API',
                'api_docs_url': 'https://developers.google.com/drive',
                'priority': 'high',
                'notes': 'Official MCP server available, OAuth required'
            },
            {
                'name': 'slack',
                'mcp_server': 'modelcontextprotocol/servers/slack',
                'api_type': 'Slack API',
                'api_docs_url': 'https://api.slack.com/',
                'priority': 'high',
                'notes': 'Official MCP server available'
            }
        ]

        all_agents = self.get_all_agents()

        for server in known_servers:
            # Find matching agent by name
            agent = next((a for a in all_agents if a['name'] == server['name']), None)
            if agent:
                self.research_agent(
                    agent_id=agent['id'],
                    mcp_status='mcp_available',
                    mcp_server=server['mcp_server'],
                    api_available=True,
                    api_type=server['api_type'],
                    api_docs_url=server['api_docs_url'],
                    notes=server['notes'],
                    priority=server['priority']
                )
                print(f"✅ Cataloged MCP server for {server['name']} (Agent {agent['id']})")
            else:
                print(f"⚠️  Agent not found for {server['name']} - may not be in our manifest")

    def generate_discovery_report(self) -> str:
        """Generate a markdown report of discovery findings"""

        tracker = self.load_tracker()
        all_agents = self.get_all_agents()

        # Count statistics
        total_agents = len(all_agents)
        mcp_available = len([d for d in self.discoveries if d.mcp_status == 'mcp_available'])
        api_available = len([d for d in self.discoveries if d.api_available])
        researched = len(self.discoveries)

        report = f"""# MCP Discovery Report
## Phase 2: MCP Server Integration

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total Agents**: {total_agents}
**Agents Researched**: {researched} ({researched/total_agents*100:.1f}%)
**MCP Servers Found**: {mcp_available}
**Public APIs Available**: {api_available}

---

## Summary Statistics

| Category | Count | Percentage |
|----------|-------|------------|
| Total Agents | {total_agents} | 100% |
| Researched | {researched} | {researched/total_agents*100:.1f}% |
| MCP Available | {mcp_available} | {mcp_available/total_agents*100:.1f}% |
| API Available | {api_available} | {api_available/total_agents*100:.1f}% |
| Pending Research | {total_agents - researched} | {(total_agents - researched)/total_agents*100:.1f}% |

---

## MCP Servers Found

"""

        mcp_discoveries = [d for d in self.discoveries if d.mcp_status == 'mcp_available']

        if mcp_discoveries:
            report += "| Agent ID | Name | Display Name | MCP Server | Priority |\n"
            report += "|----------|------|--------------|------------|----------|\n"
            for d in sorted(mcp_discoveries, key=lambda x: x.agent_id):
                report += f"| {d.agent_id} | {d.name} | {d.display_name} | {d.mcp_server} | {d.priority} |\n"
        else:
            report += "*No MCP servers cataloged yet.*\n"

        report += "\n---\n\n## Agents with Public APIs (Custom MCP Needed)\n\n"

        api_discoveries = [d for d in self.discoveries if d.api_available and d.mcp_status != 'mcp_available']

        if api_discoveries:
            report += "| Agent ID | Name | Display Name | API Type | Docs URL | Priority |\n"
            report += "|----------|------|--------------|----------|----------|----------|\n"
            for d in sorted(api_discoveries, key=lambda x: x.agent_id):
                docs_link = f"[Docs]({d.api_docs_url})" if d.api_docs_url else "N/A"
                report += f"| {d.agent_id} | {d.name} | {d.display_name} | {d.api_type or 'N/A'} | {docs_link} | {d.priority} |\n"
        else:
            report += "*No API-only agents cataloged yet.*\n"

        report += "\n---\n\n## Research Progress by Tier\n\n"

        # Calculate tier progress
        for tier in ['tier_1', 'tier_2', 'tier_3', 'tier_4', 'tier_5']:
            tier_agents = [a for a in all_agents if a.get('tier') == tier]
            tier_researched = [d for d in self.discoveries if d.tier == tier]
            total = len(tier_agents)
            researched_count = len(tier_researched)
            percentage = researched_count / total * 100 if total > 0 else 0

            report += f"**{tier.replace('_', ' ').title()}**: {researched_count}/{total} ({percentage:.1f}%)\n\n"

        report += "\n---\n\n## Next Steps\n\n"
        report += "1. Complete MCP discovery for all Tier 1 agents (20 agents)\n"
        report += "2. Research emerging tech platforms (AI tools - high priority)\n"
        report += "3. Build custom MCP servers for high-priority APIs without existing MCP\n"
        report += "4. Implement OAuth authentication for top 50 agents\n"
        report += "5. Create MCP integration templates and patterns\n"

        report += f"\n---\n\n*Report generated by MCP Discovery Manager*\n"

        return report

    def export_discoveries_json(self, output_path: Optional[Path] = None):
        """Export discoveries to JSON format"""
        if output_path is None:
            output_path = self.base_path / "mcp_discovery" / "discoveries.json"

        data = {
            'metadata': {
                'generated': datetime.now().isoformat(),
                'total_discoveries': len(self.discoveries)
            },
            'discoveries': [asdict(d) for d in self.discoveries]
        }

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"✅ Exported discoveries to {output_path}")

    def update_tracker_statistics(self):
        """Update the tracker YAML with latest statistics"""
        tracker = self.load_tracker()

        # Update statistics
        tracker['metadata']['last_updated'] = datetime.now().strftime('%Y-%m-%d')
        tracker['metadata']['agents_researched'] = len(self.discoveries)
        tracker['metadata']['mcp_servers_found'] = len([d for d in self.discoveries if d.mcp_status == 'mcp_available'])

        # Update status counts
        tracker['discovery_status']['mcp_available'] = len([d for d in self.discoveries if d.mcp_status == 'mcp_available'])
        tracker['discovery_status']['api_available'] = len([d for d in self.discoveries if d.api_available and d.mcp_status != 'mcp_available'])
        tracker['discovery_status']['research_pending'] = 1000 - len(self.discoveries)

        self.save_tracker(tracker)
        print("✅ Updated tracker statistics")


def main():
    """Main discovery workflow"""
    print("=" * 60)
    print("MCP Discovery Manager - Phase 2")
    print("=" * 60)
    print()

    manager = MCPDiscoveryManager()

    # Step 1: Catalog known MCP servers
    print("📋 Step 1: Cataloging known MCP servers...")
    manager.batch_research_known_mcp_servers()
    print()

    # Step 2: Generate discovery report
    print("📊 Step 2: Generating discovery report...")
    report = manager.generate_discovery_report()
    report_path = manager.base_path / "mcp_discovery" / "discovery_report.md"
    with open(report_path, 'w') as f:
        f.write(report)
    print(f"✅ Discovery report saved to {report_path}")
    print()

    # Step 3: Export discoveries to JSON
    print("💾 Step 3: Exporting discoveries to JSON...")
    manager.export_discoveries_json()
    print()

    # Step 4: Update tracker statistics
    print("📈 Step 4: Updating tracker statistics...")
    manager.update_tracker_statistics()
    print()

    print("=" * 60)
    print("✅ MCP Discovery Complete!")
    print("=" * 60)
    print()
    print(f"📝 View report: {report_path}")
    print(f"📋 View tracker: {manager.tracker_path}")
    print()
    print("Next steps:")
    print("  1. Review discovery_report.md for MCP server availability")
    print("  2. Research Tier 1 agents manually and update discoveries")
    print("  3. Build custom MCP servers for high-priority APIs")
    print()


if __name__ == "__main__":
    main()
