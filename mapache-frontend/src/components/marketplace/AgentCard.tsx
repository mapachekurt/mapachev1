"use client";

import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import {
  Bot,
  Activity,
  TrendingUp,
  MessageSquare
} from 'lucide-react';
import { Agent } from '@/lib/types';
import Link from 'next/link';

interface AgentCardProps {
  agent: Agent;
}

export function AgentCard({ agent }: AgentCardProps) {
  return (
    <Card className="p-4 hover:shadow-lg transition-shadow">
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center">
            <Bot className="w-6 h-6 text-white" />
          </div>
          <div>
            <h3 className="font-semibold">{agent.name}</h3>
            <Badge variant="secondary" className="mt-1">
              {agent.category}
            </Badge>
          </div>
        </div>

        {/* Health Status */}
        <div className={`w-3 h-3 rounded-full ${
          agent.health === 'healthy' ? 'bg-green-500' :
          agent.health === 'degraded' ? 'bg-yellow-500' :
          'bg-red-500'
        }`} />
      </div>

      {/* Description */}
      <p className="text-sm text-gray-600 mb-4 line-clamp-2">
        {agent.description}
      </p>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4 mb-4">
        <div className="text-center">
          <div className="flex items-center justify-center gap-1 text-xs text-gray-500">
            <Activity className="w-3 h-3" />
            Uptime
          </div>
          <div className="text-sm font-medium">{agent.uptime}%</div>
        </div>

        <div className="text-center">
          <div className="flex items-center justify-center gap-1 text-xs text-gray-500">
            <TrendingUp className="w-3 h-3" />
            Success
          </div>
          <div className="text-sm font-medium">{agent.successRate}%</div>
        </div>

        <div className="text-center">
          <div className="flex items-center justify-center gap-1 text-xs text-gray-500">
            <MessageSquare className="w-3 h-3" />
            Requests
          </div>
          <div className="text-sm font-medium">{agent.requestCount}</div>
        </div>
      </div>

      {/* Capabilities */}
      <div className="flex flex-wrap gap-1 mb-4">
        {agent.capabilities?.slice(0, 3).map((cap, idx) => (
          <Badge key={idx} variant="outline" className="text-xs">
            {cap}
          </Badge>
        ))}
        {agent.capabilities && agent.capabilities.length > 3 && (
          <Badge variant="outline" className="text-xs">
            +{agent.capabilities.length - 3} more
          </Badge>
        )}
      </div>

      {/* Action */}
      <Link href={`/chat/${agent.id}`}>
        <Button className="w-full">
          <MessageSquare className="w-4 h-4 mr-2" />
          Start Chat
        </Button>
      </Link>
    </Card>
  );
}
