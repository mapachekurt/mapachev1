import { NextResponse } from 'next/server';
import { Agent } from '@/lib/types';

// Mock agent data (will be replaced with real data from backend)
const mockAgents: Agent[] = [
  {
    id: 'financial-analyst',
    name: 'Financial Analyst Agent',
    description: 'Analyzes financial data, generates reports, and provides insights',
    category: 'fte_roles',
    health: 'healthy',
    uptime: 99.8,
    successRate: 95.3,
    requestCount: 1247,
    capabilities: ['financial-analysis', 'report-generation', 'data-visualization'],
    mcpServers: ['excel-mcp', 'finance-api-mcp']
  },
  {
    id: 'pm-agent',
    name: 'Project Manager Agent',
    description: 'Manages projects, coordinates teams, tracks progress',
    category: 'fte_roles',
    health: 'healthy',
    uptime: 99.5,
    successRate: 97.1,
    requestCount: 892,
    capabilities: ['project-planning', 'team-coordination', 'status-tracking'],
    mcpServers: ['linear-mcp', 'github-mcp', 'slack-mcp']
  },
  {
    id: 'data-scientist',
    name: 'Data Scientist Agent',
    description: 'Performs statistical analysis, builds ML models, and visualizes data',
    category: 'fte_roles',
    health: 'healthy',
    uptime: 99.2,
    successRate: 94.8,
    requestCount: 1534,
    capabilities: ['statistical-analysis', 'machine-learning', 'data-visualization'],
    mcpServers: ['jupyter-mcp', 'pandas-mcp', 'sklearn-mcp']
  },
  {
    id: 'salesforce-agent',
    name: 'Salesforce Integration Agent',
    description: 'Manages Salesforce CRM operations, data sync, and reporting',
    category: 'saas_tools',
    health: 'healthy',
    uptime: 99.9,
    successRate: 98.2,
    requestCount: 2145,
    capabilities: ['crm-management', 'data-sync', 'salesforce-api'],
    mcpServers: ['salesforce-mcp']
  },
  {
    id: 'slack-agent',
    name: 'Slack Communication Agent',
    description: 'Automates Slack workflows, manages channels, and sends notifications',
    category: 'saas_tools',
    health: 'healthy',
    uptime: 99.7,
    successRate: 96.5,
    requestCount: 3421,
    capabilities: ['messaging', 'workflow-automation', 'notifications'],
    mcpServers: ['slack-mcp']
  },
  {
    id: 'healthcare-agent',
    name: 'Healthcare Analytics Agent',
    description: 'Analyzes patient data, generates health insights, ensures HIPAA compliance',
    category: 'industry',
    health: 'healthy',
    uptime: 99.9,
    successRate: 99.1,
    requestCount: 567,
    capabilities: ['patient-analytics', 'compliance', 'health-insights'],
    mcpServers: ['healthcare-db-mcp', 'hipaa-mcp']
  },
  // Add more mock agents to demonstrate the marketplace
  {
    id: 'legal-research-agent',
    name: 'Legal Research Agent',
    description: 'Conducts legal research, summarizes case law, and drafts legal documents',
    category: 'industry',
    health: 'healthy',
    uptime: 98.5,
    successRate: 93.2,
    requestCount: 324,
    capabilities: ['legal-research', 'document-drafting', 'case-analysis'],
    mcpServers: ['legal-db-mcp', 'westlaw-mcp']
  },
  {
    id: 'marketing-agent',
    name: 'Marketing Campaign Agent',
    description: 'Plans marketing campaigns, analyzes metrics, and optimizes ad spend',
    category: 'fte_roles',
    health: 'healthy',
    uptime: 99.3,
    successRate: 95.7,
    requestCount: 1876,
    capabilities: ['campaign-planning', 'analytics', 'ad-optimization'],
    mcpServers: ['google-ads-mcp', 'facebook-ads-mcp', 'analytics-mcp']
  },
];

export async function GET() {
  // TODO: Fetch from actual agent registry
  return NextResponse.json({
    agents: mockAgents,
    total: mockAgents.length
  });
}
