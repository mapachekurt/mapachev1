"use client";

import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  Clock,
  StopCircle,
  Bot
} from 'lucide-react';
import { Session, Agent } from '@/lib/types';
import { formatDistanceToNow } from 'date-fns';

interface SessionHeaderProps {
  session: Session | null;
  agent: Agent;
  onEndSession: () => void;
}

export function SessionHeader({
  session,
  agent,
  onEndSession
}: SessionHeaderProps) {
  if (!session) {
    return null;
  }

  const duration = formatDistanceToNow(
    new Date(session.startedAt),
    { addSuffix: false }
  );

  return (
    <div className="border-b bg-white px-4 py-3">
      <div className="max-w-4xl mx-auto flex items-center justify-between">
        {/* Agent Info */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-purple-500 flex items-center justify-center">
            <Bot className="w-6 h-6 text-white" />
          </div>
          <div>
            <h2 className="font-semibold">{agent.name}</h2>
            <p className="text-sm text-gray-600">{agent.description}</p>
          </div>
        </div>

        {/* Session Info */}
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <Clock className="w-4 h-4" />
            <span>{duration}</span>
          </div>

          <Badge variant="secondary">
            {session.taskType}
          </Badge>

          <Button
            size="sm"
            variant="outline"
            onClick={onEndSession}
          >
            <StopCircle className="w-4 h-4 mr-2" />
            End Session
          </Button>
        </div>
      </div>
    </div>
  );
}
