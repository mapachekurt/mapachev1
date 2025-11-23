"use client";

import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';

interface CodeDisplayProps {
  code: string;
  language: string;
}

export function CodeDisplay({ code, language }: CodeDisplayProps) {
  return (
    <SyntaxHighlighter
      style={oneDark}
      language={language}
      PreTag="div"
    >
      {code}
    </SyntaxHighlighter>
  );
}
