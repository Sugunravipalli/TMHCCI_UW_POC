"use client";

import { StatusBadge } from "./StatusBadge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

interface Test {
  TEST_NAME: string;
  EXPECTED: string;
  ACTUAL: string;
  STATUS: string;
}

interface RegressionResultsProps {
  tests: Test[];
  summary: { total: number; passed: number; failed: number };
}

export function RegressionResults({
  tests,
  summary,
}: RegressionResultsProps) {
  return (
    <div className="space-y-4">
      {/* Summary bar */}
      <div className="flex items-center gap-4 rounded-lg border border-border bg-card p-3">
        <div className="flex items-center gap-2">
          <span className="text-sm text-muted-foreground">Total:</span>
          <span className="text-sm font-bold">{summary.total}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-sm text-muted-foreground">Passed:</span>
          <span className="text-sm font-bold text-emerald-600">
            {summary.passed}
          </span>
        </div>
        {summary.failed > 0 && (
          <div className="flex items-center gap-2">
            <span className="text-sm text-muted-foreground">Failed:</span>
            <span className="text-sm font-bold text-red-600">
              {summary.failed}
            </span>
          </div>
        )}
        <div className="flex-1" />
        <StatusBadge
          status={summary.failed === 0 ? "PASS" : "FAIL"}
        />
      </div>

      {/* Test table */}
      <div className="rounded-lg border border-border/50 overflow-hidden">
        <Table>
          <TableHeader>
            <TableRow className="border-border/50">
              <TableHead className="text-xs">Test Name</TableHead>
              <TableHead className="text-xs">Expected</TableHead>
              <TableHead className="text-xs">Actual</TableHead>
              <TableHead className="text-xs text-right">Status</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {tests.map((t) => (
              <TableRow key={t.TEST_NAME} className="border-border/30">
                <TableCell className="text-xs font-mono">
                  {t.TEST_NAME}
                </TableCell>
                <TableCell className="text-xs text-muted-foreground">
                  {t.EXPECTED}
                </TableCell>
                <TableCell className="text-xs text-muted-foreground">
                  {t.ACTUAL}
                </TableCell>
                <TableCell className="text-right">
                  <StatusBadge status={t.STATUS} />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
