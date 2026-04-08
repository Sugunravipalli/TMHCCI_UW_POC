"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Inbox,
  Users,
  ShieldCheck,
  ClipboardList,
} from "lucide-react";

const navItems = [
  { href: "/", label: "Command Center", icon: LayoutDashboard },
  { href: "/inbox", label: "Inbox Triage", icon: Inbox },
  { href: "/brokers", label: "Broker Intelligence", icon: Users },
  { href: "/quality", label: "Data Quality", icon: ShieldCheck },
  { href: "/audit", label: "Audit Trail", icon: ClipboardList },
];

export function NavSidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed left-0 top-0 h-full w-56 border-r border-sidebar-border bg-sidebar flex flex-col z-50">
      {/* Logo area */}
      <div className="p-4 border-b border-sidebar-border">
        <div className="flex items-center gap-2">
          <div className="h-8 w-8 rounded-lg bg-white/20 flex items-center justify-center">
            <span className="text-white text-xs font-bold">TM</span>
          </div>
          <div>
            <p className="text-sm font-bold text-white">TMHCCI</p>
            <p className="text-[10px] text-white/60 leading-tight">
              Underwriting Intelligence
            </p>
          </div>
        </div>
      </div>

      {/* Nav links */}
      <nav className="flex-1 p-3 space-y-1">
        {navItems.map(({ href, label, icon: Icon }) => {
          const isActive =
            href === "/" ? pathname === "/" : pathname.startsWith(href);
          return (
            <Link
              key={href}
              href={href}
              className={`flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm transition-colors ${
                isActive
                  ? "bg-sidebar-primary text-white font-medium"
                  : "text-white/70 hover:bg-sidebar-accent hover:text-white"
              }`}
            >
              <Icon className="h-4 w-4" />
              {label}
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-sidebar-border">
        <p className="text-[10px] text-white/40 text-center">
          POC v1.0 — Snowflake Native
        </p>
      </div>
    </aside>
  );
}
