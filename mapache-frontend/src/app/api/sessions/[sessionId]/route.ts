import { NextRequest, NextResponse } from 'next/server';

export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ sessionId: string }> }
) {
  const { sessionId } = await params;

  // TODO: End session in backend and get summary

  const summary = {
    sessionId,
    endedAt: new Date().toISOString(),
    messageCount: 10,
    cost: 0.05,
    memories: []
  };

  return NextResponse.json(summary);
}
