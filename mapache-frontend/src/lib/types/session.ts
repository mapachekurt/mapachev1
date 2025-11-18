export interface Session {
  id: string;
  agentId: string;
  userId: string;
  taskType: string;
  startedAt: string;
  endedAt?: string;
  status: 'active' | 'completed' | 'failed';
  messageCount: number;
  cost: number;
  memories?: Memory[];
}

export interface Memory {
  type: 'declarative' | 'procedural';
  content: string;
  confidence: number;
  createdAt: string;
}
