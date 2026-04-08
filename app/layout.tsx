import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import { cn } from "@/lib/utils";
import { TooltipProvider } from "@/components/ui/tooltip";
import { NavSidebar } from "@/components/NavSidebar";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-sans",
  weight: "100 900",
});

const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-mono",
  weight: "100 900",
});

export const metadata: Metadata = {
  title: "TMHCCI Underwriting Intelligence",
  description:
    "Tokio Marine HCC — Underwriting Acceleration POC powered by Snowflake",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={cn("font-sans", geistSans.variable, geistMono.variable)}
    >
      <body className="antialiased">
        <TooltipProvider>
          <NavSidebar />
          <main className="ml-56 min-h-screen p-6">{children}</main>
        </TooltipProvider>
      </body>
    </html>
  );
}
