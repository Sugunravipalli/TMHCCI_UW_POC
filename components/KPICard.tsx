"use client";

import { Card, CardContent } from "@/components/ui/card";
import { type LucideIcon } from "lucide-react";

interface KPICardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  trend?: "up" | "down" | "neutral";
  accentColor?: string;
}

export function KPICard({
  title,
  value,
  subtitle,
  icon: Icon,
  accentColor = "text-primary",
}: KPICardProps) {
  return (
    <Card className="border-border/50 hover:border-primary/30 transition-colors">
      <CardContent className="p-5">
        <div className="flex items-start justify-between">
          <div className="space-y-1">
            <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
              {title}
            </p>
            <p className={`text-2xl font-bold ${accentColor}`}>{value}</p>
            {subtitle && (
              <p className="text-xs text-muted-foreground">{subtitle}</p>
            )}
          </div>
          <div className="rounded-lg bg-primary/10 p-2.5">
            <Icon className="h-5 w-5 text-primary" />
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
