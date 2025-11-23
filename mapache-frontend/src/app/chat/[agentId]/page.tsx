"use client";

import { use, useEffect, useState } from 'react';
import { ChatContainer } from '@/components/chat/ChatContainer';
import { Agent } from '@/lib/types';

interface ChatPageProps {
  params: Promise<{ agentId: string }>;
}

export default function ChatPage({ params }: ChatPageProps) {
  const { agentId } = use(params);
  const [agent, setAgent] = useState<Agent | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchAgent = async () => {
      try {
        const response = await fetch(`/api/agents/${agentId}`);
        if (response.ok) {
          const data = await response.json();
          setAgent(data);
        }
      } catch (error) {
        console.error('Failed to fetch agent:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchAgent();
  }, [agentId]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500 mx-auto mb-4" />
          <p className="text-gray-600">Loading agent...</p>
        </div>
      </div>
    );
  }

  if (!agent) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <p className="text-xl text-gray-600">Agent not found</p>
        </div>
      </div>
    );
  }

  return <ChatContainer agent={agent} />;
}
