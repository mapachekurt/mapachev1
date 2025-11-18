"use client";

import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ToolCallDisplay } from './ToolCallDisplay';
import {
  ThumbsUp,
  ThumbsDown,
  Copy,
  RefreshCw,
  User,
  Bot
} from 'lucide-react';
import { Message as MessageType, Agent } from '@/lib/types';
import { cn } from '@/lib/utils';

interface MessageProps {
  message: MessageType;
  agent: Agent;
  onRetry?: (messageId: string) => void;
  onFeedback?: (messageId: string, rating: number) => void;
}

export function Message({
  message,
  agent,
  onRetry,
  onFeedback
}: MessageProps) {
  const [copied, setCopied] = useState(false);
  const isUser = message.role === 'user';

  const handleCopy = async () => {
    await navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className={cn(
      "flex gap-3",
      isUser && "flex-row-reverse"
    )}>
      {/* Avatar */}
      <div className={cn(
        "w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0",
        isUser ? "bg-blue-500" : "bg-purple-500"
      )}>
        {isUser ? (
          <User className="w-5 h-5 text-white" />
        ) : (
          <Bot className="w-5 h-5 text-white" />
        )}
      </div>

      {/* Message Content */}
      <div className={cn(
        "flex-1 max-w-3xl",
        isUser && "flex justify-end"
      )}>
        <Card className={cn(
          "p-4",
          isUser
            ? "bg-blue-50 border-blue-200"
            : "bg-white"
        )}>
          {/* Message Header */}
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium">
              {isUser ? "You" : agent.name}
            </span>
            <span className="text-xs text-gray-500">
              {new Date(message.timestamp).toLocaleTimeString()}
            </span>
          </div>

          {/* Files (if any) */}
          {message.files && message.files.length > 0 && (
            <div className="mb-3 space-y-1">
              {message.files.map((file, idx) => (
                <Badge key={idx} variant="secondary" className="mr-2">
                  📎 {file.name}
                </Badge>
              ))}
            </div>
          )}

          {/* Message Content */}
          <div className="prose prose-sm max-w-none">
            <ReactMarkdown
              components={{
                code({ inline, className, children, ...props }: any) {
                  const match = /language-(\w+)/.exec(className || '');
                  return !inline && match ? (
                    <SyntaxHighlighter
                      style={oneDark}
                      language={match[1]}
                      PreTag="div"
                      {...props}
                    >
                      {String(children).replace(/\n$/, '')}
                    </SyntaxHighlighter>
                  ) : (
                    <code className={className} {...props}>
                      {children}
                    </code>
                  );
                }
              }}
            >
              {message.content}
            </ReactMarkdown>
          </div>

          {/* Tool Calls */}
          {message.toolCalls && message.toolCalls.length > 0 && (
            <div className="mt-4 space-y-2">
              {message.toolCalls.map((toolCall, idx) => (
                <ToolCallDisplay
                  key={idx}
                  toolCall={toolCall}
                />
              ))}
            </div>
          )}

          {/* Message Actions */}
          {!isUser && (
            <div className="flex items-center gap-2 mt-3 pt-3 border-t">
              <Button
                size="sm"
                variant="ghost"
                onClick={handleCopy}
              >
                {copied ? (
                  <>✓ Copied</>
                ) : (
                  <><Copy className="w-4 h-4 mr-1" /> Copy</>
                )}
              </Button>

              {onRetry && (
                <Button
                  size="sm"
                  variant="ghost"
                  onClick={() => onRetry(message.id)}
                >
                  <RefreshCw className="w-4 h-4 mr-1" />
                  Retry
                </Button>
              )}

              {onFeedback && (
                <div className="flex gap-1 ml-auto">
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => onFeedback(message.id, 1)}
                  >
                    <ThumbsUp className="w-4 h-4" />
                  </Button>
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => onFeedback(message.id, -1)}
                  >
                    <ThumbsDown className="w-4 h-4" />
                  </Button>
                </div>
              )}
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
