import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Bot, Search, Zap } from 'lucide-react';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-white">
      <div className="container mx-auto px-4 py-16">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <div className="flex items-center justify-center mb-6">
            <div className="w-20 h-20 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center">
              <Bot className="w-12 h-12 text-white" />
            </div>
          </div>

          <h1 className="text-6xl font-bold mb-4 bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
            Mapache
          </h1>

          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Your gateway to 511 specialized AI agents. From financial analysis to project management,
            discover the perfect agent for any task.
          </p>

          <div className="flex gap-4 justify-center">
            <Link href="/marketplace">
              <Button size="lg" className="gap-2">
                <Search className="w-5 h-5" />
                Explore Agents
              </Button>
            </Link>

            <Link href="/marketplace">
              <Button size="lg" variant="outline" className="gap-2">
                <Zap className="w-5 h-5" />
                Quick Start
              </Button>
            </Link>
          </div>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <div className="bg-white p-6 rounded-lg shadow-sm">
            <div className="w-12 h-12 rounded-full bg-purple-100 flex items-center justify-center mb-4">
              <Bot className="w-6 h-6 text-purple-600" />
            </div>
            <h3 className="font-semibold mb-2">511 Specialized Agents</h3>
            <p className="text-sm text-gray-600">
              Access a vast library of AI agents, each specialized in different domains and tasks.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm">
            <div className="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center mb-4">
              <Zap className="w-6 h-6 text-blue-600" />
            </div>
            <h3 className="font-semibold mb-2">Real-time Streaming</h3>
            <p className="text-sm text-gray-600">
              Experience smooth, real-time conversations with streaming responses and tool execution visibility.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm">
            <div className="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center mb-4">
              <Search className="w-6 h-6 text-green-600" />
            </div>
            <h3 className="font-semibold mb-2">Smart Discovery</h3>
            <p className="text-sm text-gray-600">
              Find the perfect agent with advanced search and filtering by category, capability, and performance.
            </p>
          </div>
        </div>

        {/* Stats */}
        <div className="mt-16 grid grid-cols-4 gap-8 max-w-3xl mx-auto text-center">
          <div>
            <div className="text-4xl font-bold text-purple-600">511</div>
            <div className="text-sm text-gray-600">AI Agents</div>
          </div>
          <div>
            <div className="text-4xl font-bold text-blue-600">611</div>
            <div className="text-sm text-gray-600">MCP Servers</div>
          </div>
          <div>
            <div className="text-4xl font-bold text-green-600">99.8%</div>
            <div className="text-sm text-gray-600">Uptime</div>
          </div>
          <div>
            <div className="text-4xl font-bold text-orange-600">24/7</div>
            <div className="text-sm text-gray-600">Available</div>
          </div>
        </div>
      </div>
    </div>
  );
}
