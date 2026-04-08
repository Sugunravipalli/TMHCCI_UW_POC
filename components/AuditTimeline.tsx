"use client";

import { CheckCircle2, Clock, AlertCircle, Zap } from "lucide-react";

interface AuditStep {
  step: number;
  name: string;
  function: string;
  result: string;
  executionMs: number;
  missingDocs?: string;
  followUpText?: string;
}

interface AuditTimelineProps {
  steps: AuditStep[];
  totalProcessingSeconds: string;
  manualEquivalentMinutes: number;
}

export function AuditTimeline({
  steps,
  totalProcessingSeconds,
  manualEquivalentMinutes,
}: AuditTimelineProps) {
  const icons = [CheckCircle2, Zap, Zap, AlertCircle, Clock];

  return (
    <div className="space-y-6">
      {/* Speed comparison banner */}
      <div className="rounded-lg border border-primary/30 bg-primary/5 p-4 text-center">
        <div className="flex items-center justify-center gap-3">
          <div>
            <p className="text-2xl font-bold text-primary">
              {totalProcessingSeconds}s
            </p>
            <p className="text-xs text-muted-foreground">Automated</p>
          </div>
          <span className="text-muted-foreground">vs</span>
          <div>
            <p className="text-2xl font-bold text-muted-foreground">
              {manualEquivalentMinutes} min
            </p>
            <p className="text-xs text-muted-foreground">Manual</p>
          </div>
        </div>
        <p className="text-xs text-muted-foreground mt-2">
          {Math.round((manualEquivalentMinutes * 60) / parseFloat(totalProcessingSeconds))}x
          faster than manual processing
        </p>
      </div>

      {/* Timeline */}
      <div className="relative">
        {steps.map((step, idx) => {
          const Icon = icons[idx] || CheckCircle2;
          return (
            <div key={step.step} className="relative flex gap-4 pb-6">
              {/* Vertical line */}
              {idx < steps.length - 1 && (
                <div className="absolute left-[15px] top-[30px] w-px h-[calc(100%-20px)] bg-border/50" />
              )}
              {/* Icon */}
              <div className="flex-shrink-0 rounded-full bg-primary/10 p-1.5 z-10">
                <Icon className="h-4 w-4 text-primary" />
              </div>
              {/* Content */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-medium text-foreground">
                    {step.name}
                  </span>
                  <span className="text-xs font-mono text-muted-foreground bg-muted/50 px-1.5 py-0.5 rounded">
                    {step.executionMs}ms
                  </span>
                </div>
                <p className="text-xs text-muted-foreground font-mono mt-0.5">
                  {step.function}
                </p>
                <p className="text-sm text-foreground/80 mt-1">{step.result}</p>
                {step.missingDocs && (
                  <p className="text-xs text-amber-600 mt-1">
                    Missing: {step.missingDocs}
                  </p>
                )}
                {step.followUpText && (
                    <div className="mt-2 rounded border border-border bg-card p-2">
                    <p className="text-xs text-muted-foreground whitespace-pre-wrap">
                      {step.followUpText.slice(0, 300)}
                      {step.followUpText.length > 300 ? "..." : ""}
                    </p>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
