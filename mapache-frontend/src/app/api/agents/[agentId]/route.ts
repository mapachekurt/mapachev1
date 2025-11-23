import { NextRequest, NextResponse } from 'next/server';

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ agentId: string }> }
) {
  const { agentId } = await params;

  // TODO: Fetch from actual agent registry
  // For now, fetch from the list endpoint and find the agent
  const baseUrl = request.nextUrl.origin;
  const response = await fetch(`${baseUrl}/api/agents/list`);
  const data = await response.json();

  const agent = data.agents.find((a: any) => a.id === agentId);

  if (!agent) {
    return NextResponse.json(
      { error: 'Agent not found' },
      { status: 404 }
    );
  }

  return NextResponse.json(agent);
}
