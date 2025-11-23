"use client";

import { useEffect, useRef } from 'react';
import { Message } from './Message';
import { StreamingMessage } from './StreamingMessage';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Message as MessageType, Agent } from '@/lib/types';

interface MessageListProps {
  messages: MessageType[];
  isStreaming: boolean;
  streamingContent: string;
  agent: Agent;
  onRetry?: (messageId: string) => void;
  onFeedback?: (messageId: string, rating: number) => void;
}

export function MessageList({
  messages,
  isStreaming,
  streamingContent,
  agent,
  onRetry,
  onFeedback
}: MessageListProps) {
  const scrollAreaRef = useRef<HTMLDivElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: 'smooth',
      block: 'end'
    });
  }, [messages, streamingContent]);

  return (
    <ScrollArea
      ref={scrollAreaRef}
      className="flex-1 p-4"
    >
      <div className="max-w-4xl mx-auto space-y-4">
        {messages.map((message) => (
          <Message
            key={message.id}
            message={message}
            agent={agent}
            onRetry={onRetry}
            onFeedback={onFeedback}
          />
        ))}

        {isStreaming && streamingContent && (
          <StreamingMessage
            content={streamingContent}
            agent={agent}
          />
        )}

        <div ref={messagesEndRef} />
      </div>
    </ScrollArea>
  );
}
