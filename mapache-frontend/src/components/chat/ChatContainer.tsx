"use client";

import { useState, useEffect } from 'react';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { SessionHeader } from '../session/SessionHeader';
import { useAgentChat } from '@/hooks/useAgentChat';
import { useSessionManager } from '@/hooks/useSessionManager';
import { Agent, Message } from '@/lib/types';

interface ChatContainerProps {
  agent: Agent;
}

export function ChatContainer({ agent }: ChatContainerProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const { session, startSession, endSession } = useSessionManager();
  const { sendMessage, isStreaming, streamingContent } = useAgentChat(agent.id);

  // Start session on mount
  useEffect(() => {
    if (!session) {
      startSession(agent.id, 'general');
    }
  }, [agent.id, session, startSession]);

  const handleSendMessage = async (content: string, files?: File[]) => {
    // Add user message immediately
    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content,
      timestamp: new Date().toISOString(),
      files: files?.map(f => ({
        name: f.name,
        size: f.size,
        type: f.type
      }))
    };

    setMessages(prev => [...prev, userMessage]);

    // Send to agent and get response
    const response = await sendMessage(content, files);

    // Add agent response
    setMessages(prev => [...prev, response]);
  };

  const handleEndSession = async () => {
    await endSession();
    // Could navigate away or reset state
  };

  return (
    <div className="flex flex-col h-screen">
      <SessionHeader
        session={session}
        agent={agent}
        onEndSession={handleEndSession}
      />

      <MessageList
        messages={messages}
        isStreaming={isStreaming}
        streamingContent={streamingContent}
        agent={agent}
      />

      <MessageInput
        onSend={handleSendMessage}
        disabled={isStreaming}
        placeholder={`Message ${agent.name}...`}
      />
    </div>
  );
}
