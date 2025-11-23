"use client";

interface JsonViewerProps {
  data: any;
}

export function JsonViewer({ data }: JsonViewerProps) {
  return (
    <pre className="bg-gray-900 text-gray-100 p-3 rounded text-xs overflow-x-auto">
      {JSON.stringify(data, null, 2)}
    </pre>
  );
}
