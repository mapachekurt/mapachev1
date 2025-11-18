import { NextRequest } from 'next/server';

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ agentId: string }> }
) {
  const { agentId } = await params;
  const { message, files } = await request.json();

  // Create streaming response
  const encoder = new TextEncoder();
  const stream = new ReadableStream({
    async start(controller) {
      try {
        // TODO: Connect to actual agent backend
        // For now, mock streaming response

        // Send initial content
        const words = `Hello! I'm agent ${agentId}. I received your message: "${message}". This is a mock response that demonstrates streaming.`.split(' ');

        for (const word of words) {
          const data = {
            type: 'content',
            content: word + ' '
          };

          controller.enqueue(
            encoder.encode(`data: ${JSON.stringify(data)}\n\n`)
          );

          // Simulate streaming delay
          await new Promise(resolve => setTimeout(resolve, 50));
        }

        // Mock tool call
        if (message.toLowerCase().includes('tool') || message.toLowerCase().includes('execute')) {
          const toolCall = {
            type: 'tool_call',
            toolCall: {
              tool: 'example_tool',
              parameters: { query: message },
              result: {
                type: 'text',
                data: 'Tool executed successfully!'
              },
              status: 'success'
            }
          };

          controller.enqueue(
            encoder.encode(`data: ${JSON.stringify(toolCall)}\n\n`)
          );
        }

        controller.close();
      } catch (error) {
        controller.error(error);
      }
    }
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  });
}
