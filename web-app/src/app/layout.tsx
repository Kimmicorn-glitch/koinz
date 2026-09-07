import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Local Hands 2.0",
  description: "AI-Powered Township Employment Intelligence Platform",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
