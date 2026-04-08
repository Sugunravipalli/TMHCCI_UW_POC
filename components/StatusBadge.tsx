"use client";

import { Badge } from "@/components/ui/badge";

interface StatusBadgeProps {
  status: string;
  className?: string;
}

export function StatusBadge({ status, className = "" }: StatusBadgeProps) {
  const s = status.toUpperCase();

  let colors = "bg-gray-100 text-gray-600 border-gray-200";
  if (s === "PASS" || s === "COMPLETE" || s === "SUCCESS" || s === "BOUND")
    colors = "bg-emerald-50 text-emerald-700 border-emerald-200";
  else if (s === "FAIL" || s === "INCOMPLETE" || s === "DECLINED")
    colors = "bg-red-50 text-red-700 border-red-200";
  else if (s === "WARNING" || s === "NTU" || s === "QUOTED")
    colors = "bg-amber-50 text-amber-700 border-amber-200";

  return (
    <Badge variant="outline" className={`${colors} font-mono text-xs ${className}`}>
      {status}
    </Badge>
  );
}
