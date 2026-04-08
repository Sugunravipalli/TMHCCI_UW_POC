"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { KPICard } from "@/components/KPICard";
import { DeliverableChecklist } from "@/components/DeliverableChecklist";
import { Skeleton } from "@/components/ui/skeleton";
import {
  FileText,
  Mail,
  Users,
  Activity,
  Timer,
  Target,
  TrendingUp,
  CheckCircle2,
} from "lucide-react";
import { formatPct } from "@/components/FormatUtils";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";

interface KPIData {
  totalSubmissions: number;
  totalEmails: number;
  completeCount: number;
  incompleteCount: number;
  classificationAccuracy: number;
  brokerCount: number;
  avgBrokerScore: number;
  topBroker: string;
  topBrokerScore: number;
  pipelineSteps: number;
  pipelineRowsProcessed: number;
  pipelineSeconds: number;
  pipelineHealthy: boolean;
}

interface Deliverable {
  id: string;
  name: string;
  description: string;
  status: string;
  detail: string;
}

const CHART_COLORS = [
  "#0B3B6E",
  "#1BAA73",
  "#1E63B5",
  "#F5A623",
  "#7C3AED",
  "#0D9488",
];

export default function CommandCenter() {
  const [kpis, setKpis] = useState<KPIData | null>(null);
  const [completenessDistribution, setCompletenessDistribution] = useState<
    { grade: string; count: number; avgScore: number }[]
  >([]);
  const [emailClassification, setEmailClassification] = useState<
    { category: string; count: number; matches: number }[]
  >([]);
  const [deliverables, setDeliverables] = useState<Deliverable[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [statsRes, delRes] = await Promise.all([
          fetch("/api/command-center/stats"),
          fetch("/api/deliverables"),
        ]);
        const stats = await statsRes.json();
        const dels = await delRes.json();

        setKpis(stats.kpis);
        setCompletenessDistribution(stats.completenessDistribution || []);
        setEmailClassification(stats.emailClassification || []);
        setDeliverables(dels.deliverables || []);
      } catch (err) {
        console.error("Failed to fetch command center data:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {[...Array(4)].map((_, i) => (
            <Skeleton key={i} className="h-28 rounded-lg" />
          ))}
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {[...Array(3)].map((_, i) => (
            <Skeleton key={i} className="h-64 rounded-lg" />
          ))}
        </div>
      </div>
    );
  }

  if (!kpis) {
    return (
      <div className="flex items-center justify-center h-64 text-muted-foreground">
        Failed to load data. Check Snowflake connection.
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold">Command Center</h1>
        <p className="text-sm text-muted-foreground mt-1">
          TMHCCI Underwriting Intelligence — Pipeline health, deliverable compliance, and AI analytics overview
        </p>
      </div>

      {/* KPI Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard
          title="Submissions"
          value={kpis.totalSubmissions}
          subtitle={`${kpis.completeCount} complete, ${kpis.incompleteCount} incomplete`}
          icon={FileText}
        />
        <KPICard
          title="Emails Classified"
          value={kpis.totalEmails}
          subtitle={`${kpis.classificationAccuracy}% accuracy`}
          icon={Mail}
        />
        <KPICard
          title="Brokers Scored"
          value={kpis.brokerCount}
          subtitle={`Top: ${kpis.topBroker} (${kpis.topBrokerScore})`}
          icon={Users}
        />
        <KPICard
          title="Pipeline Health"
          value={kpis.pipelineHealthy ? "Healthy" : "Issues"}
          subtitle={`${kpis.pipelineSteps} steps, ${kpis.pipelineRowsProcessed.toLocaleString()} rows, ${kpis.pipelineSeconds}s`}
          icon={Activity}
          accentColor={kpis.pipelineHealthy ? "text-emerald-600" : "text-red-600"}
        />
      </div>

      {/* Three-column analytics */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* A1 — Completeness Distribution */}
        <Card className="border-border/50">
          <CardHeader className="pb-2">
            <div className="flex items-center gap-2">
              <Target className="h-4 w-4 text-primary" />
              <CardTitle className="text-sm">A1 — Completeness Grades</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={180}>
              <BarChart data={completenessDistribution}>
                <XAxis
                  dataKey="grade"
                  tick={{ fill: "#475569", fontSize: 12 }}
                  axisLine={false}
                  tickLine={false}
                />
                <YAxis
                  tick={{ fill: "#475569", fontSize: 11 }}
                  axisLine={false}
                  tickLine={false}
                />
                <Tooltip
                  contentStyle={{
                    background: "#FFFFFF",
                    border: "1px solid #E5E7EB",
                    borderRadius: "8px",
                    color: "#0F172A",
                    fontSize: 12,
                  }}
                  // eslint-disable-next-line @typescript-eslint/no-explicit-any
                  formatter={(value: any, _name: any, props: any) => [
                    `${value} submissions (avg ${props?.payload?.avgScore ?? 0}%)`,
                    "Count",
                  ]}
                />
                <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                  {completenessDistribution.map((_, i) => (
                    <Cell key={i} fill={CHART_COLORS[i % CHART_COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* A3 — Email Classification */}
        <Card className="border-border/50">
          <CardHeader className="pb-2">
            <div className="flex items-center gap-2">
              <Mail className="h-4 w-4 text-primary" />
              <CardTitle className="text-sm">A3 — Email Classification</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={180}>
              <PieChart>
                <Pie
                  data={emailClassification}
                  dataKey="count"
                  nameKey="category"
                  cx="50%"
                  cy="50%"
                  outerRadius={70}
                  innerRadius={35}
                  paddingAngle={2}
                  stroke="none"
                >
                  {emailClassification.map((_, i) => (
                    <Cell key={i} fill={CHART_COLORS[i % CHART_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    background: "#FFFFFF",
                    border: "1px solid #E5E7EB",
                    borderRadius: "8px",
                    color: "#0F172A",
                    fontSize: 12,
                  }}
                  formatter={(value: number, name: string) => [
                    `${value} emails`,
                    name.replace(/_/g, " "),
                  ]}
                />
              </PieChart>
            </ResponsiveContainer>
            <div className="flex flex-wrap gap-2 mt-2">
              {emailClassification.map((e, i) => (
                <div key={e.category} className="flex items-center gap-1.5 text-xs">
                  <div
                    className="h-2.5 w-2.5 rounded-full"
                    style={{ background: CHART_COLORS[i % CHART_COLORS.length] }}
                  />
                  <span className="text-muted-foreground">
                    {e.category.replace(/_/g, " ")} ({e.count})
                  </span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* A2 — Broker Summary */}
        <Card className="border-border/50">
          <CardHeader className="pb-2">
            <div className="flex items-center gap-2">
              <TrendingUp className="h-4 w-4 text-primary" />
              <CardTitle className="text-sm">A2 — Broker Intelligence</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs text-muted-foreground">Broker firms scored</span>
              <span className="text-lg font-bold">{kpis.brokerCount}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xs text-muted-foreground">Avg broker score</span>
              <span className="text-lg font-bold">
                {formatPct(kpis.avgBrokerScore)}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xs text-muted-foreground">Top performer</span>
              <span className="text-sm font-medium text-primary">
                {kpis.topBroker}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xs text-muted-foreground">Top score</span>
              <span className="text-lg font-bold text-primary">
                {kpis.topBrokerScore}
              </span>
            </div>
            <div className="flex items-center justify-between border-t border-border/30 pt-3 mt-3">
              <span className="text-xs text-muted-foreground">Pipeline time</span>
              <div className="flex items-center gap-1.5">
                <Timer className="h-3.5 w-3.5 text-muted-foreground" />
                <span className="text-sm">{kpis.pipelineSeconds}s</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Deliverables Compliance */}
      <Card className="border-border/50">
        <CardHeader className="pb-2">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="h-4 w-4 text-primary" />
            <CardTitle className="text-sm">Deliverable Compliance — Week 1</CardTitle>
          </div>
          <p className="text-xs text-muted-foreground">
            D1-D5 core deliverables + A1-A3 advanced analytics
          </p>
        </CardHeader>
        <CardContent>
          <DeliverableChecklist deliverables={deliverables} />
        </CardContent>
      </Card>
    </div>
  );
}
