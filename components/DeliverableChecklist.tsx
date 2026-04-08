"use client";

import { CheckCircle2 } from "lucide-react";

interface Deliverable {
  id: string;
  name: string;
  description: string;
  status: string;
  detail: string;
}

interface DeliverableChecklistProps {
  deliverables: Deliverable[];
}

export function DeliverableChecklist({
  deliverables,
}: DeliverableChecklistProps) {
  return (
    <div className="space-y-2">
      {deliverables.map((d) => (
        <div
          key={d.id}
          className="flex items-start gap-3 rounded-lg border border-border bg-card p-3"
        >
          <CheckCircle2
            className={`h-5 w-5 mt-0.5 flex-shrink-0 ${
              d.status === "COMPLETE" ? "text-emerald-600" : "text-red-600"
            }`}
          />
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2">
              <span className="text-xs font-mono font-bold text-primary">
                {d.id}
              </span>
              <span className="text-sm font-medium text-foreground">
                {d.name}
              </span>
            </div>
            <p className="text-xs text-muted-foreground mt-0.5">
              {d.description}
            </p>
            <p className="text-xs text-muted-foreground/70 font-mono mt-0.5">
              {d.detail}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
}
