export interface Message {
  id: string;
  role: 'user' | 'agent';
  content: string;
  timestamp: string;
  files?: FileAttachment[];
  toolCalls?: ToolCall[];
  error?: string;
}

export interface FileAttachment {
  name: string;
  size: number;
  type: string;
  url?: string;
}

export interface ToolCall {
  tool: string;
  parameters: Record<string, any>;
  result?: ToolResult;
  status: 'pending' | 'success' | 'error';
  error?: string;
}

export interface ToolResult {
  type: 'text' | 'json' | 'table' | 'code' | 'file';
  data: any;
  language?: string; // For code type
}
