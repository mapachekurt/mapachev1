"use client";

import { useState, useCallback } from 'react';
import { Message, ToolCall } from '@/lib/types';

export function useAgentChat(agentId: string) {
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamingContent, setStreamingContent] = useState('');

  const sendMessage = useCallback(async (
    content: string,
    files?: File[]
  ): Promise<Message> => {
    setIsStreaming(true);
    setStreamingContent('');

    try {
      // Send message to agent
      const response = await fetch(`/api/agents/${agentId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: content,
          files: files?.map(f => f.name) // In real impl, upload files first
        })
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      // Handle streaming response
      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let fullContent = '';
      let toolCalls: ToolCall[] = [];

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value);
          const lines = chunk.split('\n');

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              try {
                const data = JSON.parse(line.slice(6));

                if (data.type === 'content') {
                  fullContent += data.content;
                  setStreamingContent(fullContent);
                } else if (data.type === 'tool_call') {
                  toolCalls.push(data.toolCall);
                }
              } catch (e) {
                // Ignore JSON parse errors
              }
            }
          }
        }
      }

      setIsStreaming(false);
      setStreamingContent('');

      // Return complete message
      return {
        id: crypto.randomUUID(),
        role: 'agent',
        content: fullContent,
        timestamp: new Date().toISOString(),
        toolCalls: toolCalls.length > 0 ? toolCalls : undefined
      };
    } catch (error) {
      setIsStreaming(false);
      setStreamingContent('');

      // Return error message
      return {
        id: crypto.randomUUID(),
        role: 'agent',
        content: 'Sorry, I encountered an error processing your message.',
        timestamp: new Date().toISOString(),
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }, [agentId]);

  return {
    sendMessage,
    isStreaming,
    streamingContent
  };
}
