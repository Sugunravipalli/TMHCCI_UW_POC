"use client";

import { useEffect, useState, useCallback } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { DataLineageFlow } from "@/components/DataLineageFlow";
import { RegressionResults } from "@/components/RegressionResults";
import {
  ShieldCheck,
  GitBranch,
  TestTube2,
  BarChart3,
  RefreshCw,
} from "lucide-react";
import { formatPct } from "@/components/FormatUtils";

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

interface Test {
  TEST_NAME: string;
  EXPECTED: string;
  ACTUAL: string;
  STATUS: string;
}

interface QualityMetrics {
  classification: { total: number; matches: number; accuracy: number };
  completenessDistribution: { grade: string; count: number }[];
  entityResolution: {
    totalVariants: number;
    uniqueFirms: number;
    avgConfidence: number;
  };
}

export default function DataQuality() {
  const [lineage, setLineage] = useState<LineageStep[]>([]);
  const [tests, setTests] = useState<Test[]>([]);
  const [testSummary, setTestSummary] = useState({ total: 0, passed: 0, failed: 0 });
  const [metrics, setMetrics] = useState<QualityMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [testRunning, setTestRunning] = useState(false);

  useEffect(() => {
    async function fetchData() {
      try {
        const [lineageRes, metricsRes] = await Promise.all([
          fetch("/api/quality/lineage"),
          fetch("/api/quality/metrics"),
        ]);
        const lineageData = await lineageRes.json();
        const metricsData = await metricsRes.json();

        setLineage(lineageData.steps || []);
        setMetrics(metricsData);
      } catch (err) {
        console.error("Failed to fetch quality data:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  const runTests = useCallback(async () => {
    setTestRunning(true);
    try {
      const res = await fetch("/api/quality/regression");
      const data = await res.json();
      setTests(data.tests || []);
      setTestSummary(data.summary || { total: 0, passed: 0, failed: 0 });
    } catch (err) {
      console.error("Failed to run regression tests:", err);
    } finally {
      setTestRunning(false);
    }
  }, []);

  if (loading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-8 w-64" />
        <Skeleton className="h-96" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Data Quality & Integrity</h1>
        <p className="text-sm text-muted-foreground mt-1">
          Pipeline lineage, quality metrics, and live regression test execution
        </p>
      </div>

      <Tabs defaultValue="lineage" className="space-y-4">
        <TabsList className="bg-secondary">
          <TabsTrigger value="lineage" className="text-xs gap-1.5">
            <GitBranch className="h-3.5 w-3.5" />
            Data Lineage
          </TabsTrigger>
          <TabsTrigger value="metrics" className="text-xs gap-1.5">
            <BarChart3 className="h-3.5 w-3.5" />
            Quality Metrics
          </TabsTrigger>
          <TabsTrigger value="tests" className="text-xs gap-1.5">
            <TestTube2 className="h-3.5 w-3.5" />
            Regression Tests
          </TabsTrigger>
        </TabsList>

        {/* Lineage Tab */}
        <TabsContent value="lineage">
          <Card className="border-border/50">
            <CardHeader className="pb-2">
              <div className="flex items-center gap-2">
                <GitBranch className="h-4 w-4 text-primary" />
                <CardTitle className="text-sm">
                  Pipeline Lineage — {lineage.length} Steps
                </CardTitle>
              </div>
              <p className="text-xs text-muted-foreground">
                End-to-end data flow from RAW ingestion to CURATED analytics
              </p>
            </CardHeader>
            <CardContent>
              <DataLineageFlow steps={lineage} />
            </CardContent>
          </Card>
        </TabsContent>

        {/* Metrics Tab */}
        <TabsContent value="metrics">
          {metrics && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Classification accuracy */}
              <Card className="border-border/50">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm">A3 — Classification</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="text-center">
                    <p className="text-4xl font-bold text-primary">
                      {metrics.classification.accuracy}%
                    </p>
                    <p className="text-xs text-muted-foreground">
                      AI classification accuracy
                    </p>
                  </div>
                  <div className="flex items-center justify-between text-xs text-muted-foreground">
                    <span>Total emails</span>
                    <span className="font-mono">{metrics.classification.total}</span>
                  </div>
                  <div className="flex items-center justify-between text-xs text-muted-foreground">
                    <span>Correct matches</span>
                    <span className="font-mono">{metrics.classification.matches}</span>
                  </div>
                </CardContent>
              </Card>

              {/* Completeness distribution */}
              <Card className="border-border/50">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm">A1 — Completeness</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {metrics.completenessDistribution.map((d) => (
                      <div
                        key={d.grade}
                        className="flex items-center justify-between rounded border border-border/30 px-3 py-1.5"
                      >
                        <span className="text-sm font-bold">{d.grade}</span>
                        <span className="text-xs font-mono text-muted-foreground">
                          {d.count} submissions
                        </span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Entity resolution */}
              <Card className="border-border/50">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm">D2 — Entity Resolution</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-muted-foreground">Total variants</span>
                    <span className="font-mono font-bold">
                      {metrics.entityResolution.totalVariants}
                    </span>
                  </div>
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-muted-foreground">Unique firms</span>
                    <span className="font-mono font-bold">
                      {metrics.entityResolution.uniqueFirms}
                    </span>
                  </div>
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-muted-foreground">Avg confidence</span>
                    <span className="font-mono font-bold">
                      {formatPct(metrics.entityResolution.avgConfidence)}
                    </span>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </TabsContent>

        {/* Tests Tab */}
        <TabsContent value="tests">
          <Card className="border-border/50">
            <CardHeader className="pb-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <ShieldCheck className="h-4 w-4 text-primary" />
                  <CardTitle className="text-sm">
                    Live Regression Tests
                  </CardTitle>
                </div>
                <button
                  onClick={runTests}
                  disabled={testRunning}
                  className="flex items-center gap-1.5 rounded-lg bg-primary px-3 py-1.5 text-xs font-medium text-primary-foreground hover:bg-primary/90 transition-colors disabled:opacity-50"
                >
                  <RefreshCw
                    className={`h-3.5 w-3.5 ${testRunning ? "animate-spin" : ""}`}
                  />
                  {testRunning ? "Running..." : "Run Tests"}
                </button>
              </div>
              <p className="text-xs text-muted-foreground">
                Execute RUN_REGRESSION_TESTS() live against Snowflake
              </p>
            </CardHeader>
            <CardContent>
              {tests.length > 0 ? (
                <RegressionResults tests={tests} summary={testSummary} />
              ) : (
                <div className="py-12 text-center text-muted-foreground">
                  <TestTube2 className="h-8 w-8 mx-auto mb-2 opacity-30" />
                  <p className="text-sm">
                    Click &quot;Run Tests&quot; to execute 20 regression tests live
                  </p>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
