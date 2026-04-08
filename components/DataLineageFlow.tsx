"use client";

import { ArrowRight, Database, CheckCircle2 } from "lucide-react";

interface LineageStep {
  STEP_ORDER: number;
  STEP_NAME: string;
  SOURCE_SCHEMA: string;
  SOURCE_TABLES: string;
  TARGET_TABLE: string;
  DESCRIPTION: string;
  ROWS_AFFECTED: number;
  EXECUTION_SECONDS: number;
  STATUS: string;
}

interface DataLineageFlowProps {
  steps: LineageStep[];
}

export function DataLineageFlow({ steps }: DataLineageFlowProps) {
  return (
    <div className="space-y-3">
      {steps.map((step, idx) => (
        <div key={step.STEP_ORDER} className="flex items-stretch gap-2">
          {/* Step node */}
          <div className="flex-1 rounded-lg border border-border bg-card p-3 hover:border-primary/30 transition-colors">
            <div className="flex items-center gap-2 mb-1">
              <div className="rounded bg-primary/10 p-1">
                <Database className="h-3.5 w-3.5 text-primary" />
              </div>
              <span className="text-xs font-mono font-bold text-primary">
                Step {step.STEP_ORDER}
              </span>
              <span className="text-sm font-medium text-foreground">
                {step.STEP_NAME}
              </span>
              <div className="flex-1" />
              <CheckCircle2
                className={`h-4 w-4 ${
                  step.STATUS === "SUCCESS"
                    ? "text-emerald-600"
                    : "text-red-600"
                }`}
              />
            </div>
            <p className="text-xs text-muted-foreground">{step.DESCRIPTION}</p>
            <div className="flex items-center gap-4 mt-2 text-xs text-muted-foreground/70 font-mono">
              <span>
                {step.SOURCE_SCHEMA ? `${step.SOURCE_SCHEMA}.` : ""}
                {step.SOURCE_TABLES}
              </span>
              <ArrowRight className="h-3 w-3" />
              <span className="text-foreground/70">{step.TARGET_TABLE}</span>
              <span className="ml-auto">{step.ROWS_AFFECTED} rows</span>
              <span>{step.EXECUTION_SECONDS}s</span>
            </div>
          </div>
          {/* Connector arrow */}
          {idx < steps.length - 1 && (
            <div className="flex items-center justify-center w-4 text-muted-foreground/30">
              {/* visual space - vertical line in the flow */}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
