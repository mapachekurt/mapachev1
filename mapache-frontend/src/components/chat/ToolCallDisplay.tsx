"use client";

import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import {
  Wrench,
  CheckCircle,
  XCircle,
  Loader2
} from 'lucide-react';
import { ToolCall } from '@/lib/types';
import { TableDisplay } from '../tools/TableDisplay';
import { CodeDisplay } from '../tools/CodeDisplay';
import { JsonViewer } from '../tools/JsonViewer';

interface ToolCallDisplayProps {
  toolCall: ToolCall;
}

export function ToolCallDisplay({ toolCall }: ToolCallDisplayProps) {
  const { tool, parameters, result, status } = toolCall;

  return (
    <Card className="p-3 bg-gray-50 border-gray-200">
      {/* Tool Header */}
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <Wrench className="w-4 h-4 text-gray-600" />
          <span className="text-sm font-medium">{tool}</span>
        </div>

        <Badge variant={
          status === 'success' ? 'success' :
          status === 'error' ? 'destructive' :
          'secondary'
        }>
          {status === 'pending' && <Loader2 className="w-3 h-3 mr-1 animate-spin" />}
          {status === 'success' && <CheckCircle className="w-3 h-3 mr-1" />}
          {status === 'error' && <XCircle className="w-3 h-3 mr-1" />}
          {status}
        </Badge>
      </div>

      {/* Parameters (collapsed by default) */}
      {parameters && Object.keys(parameters).length > 0 && (
        <details className="mb-2">
          <summary className="text-xs text-gray-600 cursor-pointer">
            Parameters
          </summary>
          <JsonViewer data={parameters} />
        </details>
      )}

      {/* Tool Result */}
      {result && (
        <div className="mt-2">
          {renderToolResult(result)}
        </div>
      )}

      {/* Error Message */}
      {status === 'error' && toolCall.error && (
        <div className="mt-2 text-sm text-red-600 bg-red-50 p-2 rounded">
          {toolCall.error}
        </div>
      )}
    </Card>
  );
}

function renderToolResult(result: any) {
  switch (result.type) {
    case 'table':
      return <TableDisplay data={result.data} />;

    case 'code':
      return <CodeDisplay
        code={result.data}
        language={result.language || 'text'}
      />;

    case 'json':
      return <JsonViewer data={result.data} />;

    case 'text':
    default:
      return (
        <div className="text-sm whitespace-pre-wrap">
          {result.data}
        </div>
      );
  }
}
