"use client";

import { useState, useEffect } from 'react';
import { AgentCard } from '@/components/marketplace/AgentCard';
import { Agent } from '@/lib/types';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

export default function MarketplacePage() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [filteredAgents, setFilteredAgents] = useState<Agent[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchAgents();
  }, []);

  useEffect(() => {
    filterAgents();
  }, [searchQuery, selectedCategory, agents]);

  const fetchAgents = async () => {
    try {
      const response = await fetch('/api/agents/list');
      const data = await response.json();
      setAgents(data.agents);
      setFilteredAgents(data.agents);
    } catch (error) {
      console.error('Failed to fetch agents:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const filterAgents = () => {
    let filtered = agents;

    // Filter by search query
    if (searchQuery) {
      filtered = filtered.filter(agent =>
        agent.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        agent.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        agent.capabilities.some(cap =>
          cap.toLowerCase().includes(searchQuery.toLowerCase())
        )
      );
    }

    // Filter by category
    if (selectedCategory) {
      filtered = filtered.filter(agent => agent.category === selectedCategory);
    }

    setFilteredAgents(filtered);
  };

  const categories = [
    { value: null, label: 'All Agents', count: agents.length },
    {
      value: 'saas_tools',
      label: 'SaaS Tools',
      count: agents.filter(a => a.category === 'saas_tools').length
    },
    {
      value: 'fte_roles',
      label: 'FTE Roles',
      count: agents.filter(a => a.category === 'fte_roles').length
    },
    {
      value: 'industry',
      label: 'Industry',
      count: agents.filter(a => a.category === 'industry').length
    },
  ];

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500 mx-auto mb-4" />
          <p className="text-gray-600">Loading agents...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">Agent Marketplace</h1>
        <p className="text-gray-600">
          Discover and interact with {agents.length} AI agents
        </p>
      </div>

      {/* Search */}
      <div className="mb-6">
        <Input
          type="search"
          placeholder="Search agents by name, description, or capability..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="max-w-xl"
        />
      </div>

      {/* Category Tabs */}
      <Tabs defaultValue="all" className="mb-6">
        <TabsList>
          {categories.map((category) => (
            <TabsTrigger
              key={category.value || 'all'}
              value={category.value || 'all'}
              onClick={() => setSelectedCategory(category.value)}
            >
              {category.label} ({category.count})
            </TabsTrigger>
          ))}
        </TabsList>
      </Tabs>

      {/* Results */}
      <div className="mb-4 text-sm text-gray-600">
        Showing {filteredAgents.length} of {agents.length} agents
      </div>

      {/* Agent Grid */}
      {filteredAgents.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-600">No agents found matching your criteria</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredAgents.map((agent) => (
            <AgentCard key={agent.id} agent={agent} />
          ))}
        </div>
      )}
    </div>
  );
}
