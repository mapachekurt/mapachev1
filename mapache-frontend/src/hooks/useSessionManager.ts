"use client";

import { useState, useCallback } from 'react';
import { Session } from '@/lib/types';

export function useSessionManager() {
  const [session, setSession] = useState<Session | null>(null);

  const startSession = useCallback(async (
    agentId: string,
    taskType: string
  ) => {
    try {
      const response = await fetch('/api/sessions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          agentId,
          taskType
        })
      });

      if (!response.ok) {
        throw new Error('Failed to start session');
      }

      const newSession = await response.json();
      setSession(newSession);
      return newSession;
    } catch (error) {
      console.error('Failed to start session:', error);
      throw error;
    }
  }, []);

  const endSession = useCallback(async () => {
    if (!session) return;

    try {
      const response = await fetch(`/api/sessions/${session.id}`, {
        method: 'DELETE'
      });

      if (!response.ok) {
        throw new Error('Failed to end session');
      }

      const summary = await response.json();
      setSession(null);
      return summary;
    } catch (error) {
      console.error('Failed to end session:', error);
      throw error;
    }
  }, [session]);

  return {
    session,
    startSession,
    endSession
  };
}
