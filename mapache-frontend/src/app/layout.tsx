import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Mapache - AI Agent Marketplace",
  description: "Interact with 511 AI agents and discover their capabilities",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="font-sans antialiased">{children}</body>
    </html>
  );
}
