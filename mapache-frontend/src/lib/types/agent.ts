export interface Agent {
  id: string;
  name: string;
  description: string;
  category: 'saas_tools' | 'fte_roles' | 'industry';
  health: 'healthy' | 'degraded' | 'unhealthy';
  uptime: number; // percentage
  successRate: number; // percentage
  requestCount: number;
  capabilities: string[];
  mcpServers: string[];
  version?: string;
  lastUpdated?: string;
}

export interface AgentStats {
  avgResponseTime: number; // ms
  errorRate: number; // percentage
  costPerRequest: number; // USD
  totalCost: number; // USD
  popularity: number; // usage rank
}
