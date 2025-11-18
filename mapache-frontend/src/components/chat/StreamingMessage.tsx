"use client";

import ReactMarkdown from 'react-markdown';
import { Card } from '@/components/ui/card';
import { Bot } from 'lucide-react';
import { Agent } from '@/lib/types';

interface StreamingMessageProps {
  content: string;
  agent: Agent;
}

export function StreamingMessage({
  content,
  agent
}: StreamingMessageProps) {
  return (
    <div className="flex gap-3">
      {/* Avatar */}
      <div className="w-8 h-8 rounded-full bg-purple-500 flex items-center justify-center flex-shrink-0">
        <Bot className="w-5 h-5 text-white" />
      </div>

      {/* Streaming Content */}
      <div className="flex-1 max-w-3xl">
        <Card className="p-4 bg-white">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium">{agent.name}</span>
            <div className="flex items-center gap-2 text-xs text-gray-500">
              <div className="flex gap-1">
                <span className="w-2 h-2 bg-purple-500 rounded-full animate-bounce"
                      style={{ animationDelay: '0ms' }} />
                <span className="w-2 h-2 bg-purple-500 rounded-full animate-bounce"
                      style={{ animationDelay: '150ms' }} />
                <span className="w-2 h-2 bg-purple-500 rounded-full animate-bounce"
                      style={{ animationDelay: '300ms' }} />
              </div>
              Thinking...
            </div>
          </div>

          <div className="prose prose-sm max-w-none">
            <ReactMarkdown>{content}</ReactMarkdown>
            <span className="inline-block w-2 h-4 bg-purple-500 animate-pulse ml-1">▊</span>
          </div>
        </Card>
      </div>
    </div>
  );
}
