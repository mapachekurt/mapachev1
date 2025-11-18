import { Agent } from '@/lib/types';

export const mockAgents: Agent[] = [
  {
    id: 'test-agent-1',
    name: 'Test Agent 1',
    description: 'A test agent for unit testing',
    category: 'fte_roles',
    health: 'healthy',
    uptime: 99.9,
    successRate: 98.5,
    requestCount: 100,
    capabilities: ['testing', 'mocking'],
    mcpServers: ['test-mcp']
  },
  {
    id: 'test-agent-2',
    name: 'Test Agent 2',
    description: 'Another test agent',
    category: 'saas_tools',
    health: 'healthy',
    uptime: 99.5,
    successRate: 97.2,
    requestCount: 50,
    capabilities: ['integration-testing'],
    mcpServers: ['test-mcp-2']
  },
];
