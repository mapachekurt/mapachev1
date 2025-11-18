import { NextRequest, NextResponse } from 'next/server';
import { Session } from '@/lib/types';

export async function POST(request: NextRequest) {
  const { agentId, taskType } = await request.json();

  // TODO: Create session in backend
  const session: Session = {
    id: crypto.randomUUID(),
    agentId,
    userId: 'current-user', // TODO: Get from auth
    taskType,
    startedAt: new Date().toISOString(),
    status: 'active',
    messageCount: 0,
    cost: 0
  };

  return NextResponse.json(session);
}
