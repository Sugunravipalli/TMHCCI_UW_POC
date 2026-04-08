"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { ArrowUpDown, ArrowLeft } from "lucide-react";
import { formatCurrency, formatPct, decisionColor } from "@/components/FormatUtils";
interface Broker {
  BROKER_ID: number;
  DISPLAY_NAME: string;
  CANONICAL_BROKER_NAME: string;
  PRESENT_IN_SOURCES: string;
  TOTAL_SUBMISSIONS: number;
  HIT_RATE_PCT: number;
  AVG_PREMIUM: number;
  TOTAL_PREMIUM: number;
  BOUND_COUNT: number;
  DECLINED_COUNT: number;
  NTU_COUNT: number;
  AVG_COMPLETENESS_SCORE: number;
  BROKER_SCORE: number;
  [key: string]: unknown;
}

interface BrokerDetail {
  scorecard: Record<string, unknown>;
  ratings: Record<string, unknown>[];
  variants: Record<string, unknown>[];
}

type SortField = "BROKER_SCORE" | "TOTAL_SUBMISSIONS" | "HIT_RATE_PCT" | "TOTAL_PREMIUM";

export default function BrokerIntelligence() {
  const [brokers, setBrokers] = useState<Broker[]>([]);
  const [loading, setLoading] = useState(true);
  const [sortField, setSortField] = useState<SortField>("BROKER_SCORE");
  const [sortAsc, setSortAsc] = useState(false);
  const [selectedBroker, setSelectedBroker] = useState<BrokerDetail | null>(null);

  useEffect(() => {
    async function fetchBrokers() {
      try {
        const res = await fetch("/api/brokers");
        const data = await res.json();
        setBrokers(data.brokers || []);
      } catch (err) {
        console.error("Failed to fetch brokers:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchBrokers();
  }, []);

  async function handleBrokerClick(brokerId: number) {
    try {
      const res = await fetch(`/api/brokers/${brokerId}`);
      const data = await res.json();
      setSelectedBroker(data);
    } catch (err) {
      console.error("Failed to fetch broker detail:", err);
    }
  }

  function handleSort(field: SortField) {
    if (sortField === field) {
      setSortAsc(!sortAsc);
    } else {
      setSortField(field);
      setSortAsc(false);
    }
  }

  const sorted = [...brokers].sort((a, b) => {
    const aVal = Number(a[sortField]) || 0;
    const bVal = Number(b[sortField]) || 0;
    return sortAsc ? aVal - bVal : bVal - aVal;
  });

  if (loading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-8 w-64" />
        <Skeleton className="h-96" />
      </div>
    );
  }

  // Broker detail view
  if (selectedBroker) {
    const sc = selectedBroker.scorecard;
    return (
      <div className="space-y-6">
        <button
          onClick={() => setSelectedBroker(null)}
          className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors"
        >
          <ArrowLeft className="h-4 w-4" /> Back to Broker List
        </button>

        <div>
          <h1 className="text-2xl font-bold">{String(sc.DISPLAY_NAME)}</h1>
          <p className="text-sm text-muted-foreground mt-1">
            {String(sc.CANONICAL_BROKER_NAME)} — Sources: {String(sc.PRESENT_IN_SOURCES)}
          </p>
        </div>

        {/* Scorecard KPIs */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <MetricCard label="Broker Score" value={String(sc.BROKER_SCORE)} accent />
          <MetricCard label="Hit Rate" value={formatPct(Number(sc.HIT_RATE_PCT))} />
          <MetricCard label="Total Premium" value={formatCurrency(Number(sc.TOTAL_PREMIUM))} />
          <MetricCard label="Submissions" value={String(sc.TOTAL_SUBMISSIONS)} />
          <MetricCard label="Bound" value={String(sc.BOUND_COUNT)} />
          <MetricCard label="Declined" value={String(sc.DECLINED_COUNT)} />
          <MetricCard label="NTU" value={String(sc.NTU_COUNT)} />
          <MetricCard label="Completeness" value={formatPct(Number(sc.AVG_COMPLETENESS_SCORE))} />
        </div>

        {/* Ratings table */}
        {selectedBroker.ratings.length > 0 && (
          <Card className="border-border/50">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm">Rating History ({selectedBroker.ratings.length})</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="rounded-lg border border-border/50 overflow-auto max-h-80">
                <Table>
                  <TableHeader>
                    <TableRow className="border-border/50">
                      <TableHead className="text-xs">Insured</TableHead>
                      <TableHead className="text-xs">Coverage</TableHead>
                      <TableHead className="text-xs text-right">TIV</TableHead>
                      <TableHead className="text-xs text-right">Premium</TableHead>
                      <TableHead className="text-xs text-right">Deviation</TableHead>
                      <TableHead className="text-xs text-right">Decision</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {selectedBroker.ratings.map((r, i) => (
                      <TableRow key={i} className="border-border/30">
                        <TableCell className="text-xs max-w-40 truncate">
                          {String(r.CANONICAL_INSURED_NAME || "—")}
                        </TableCell>
                        <TableCell className="text-xs">{String(r.COVERAGE_TYPE || "—")}</TableCell>
                        <TableCell className="text-xs text-right font-mono">
                          {r.TOTAL_INSURED_VALUE ? formatCurrency(Number(r.TOTAL_INSURED_VALUE)) : "—"}
                        </TableCell>
                        <TableCell className="text-xs text-right font-mono">
                          {r.OUR_PREMIUM ? formatCurrency(Number(r.OUR_PREMIUM)) : "—"}
                        </TableCell>
                        <TableCell className="text-xs text-right font-mono">
                          {r.DEVIATION_PCT ? formatPct(Number(r.DEVIATION_PCT)) : "—"}
                        </TableCell>
                        <TableCell className="text-right">
                          <Badge variant="outline" className={`text-[10px] ${decisionColor(String(r.DECISION || ""))}`}>
                            {String(r.DECISION || "—")}
                          </Badge>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Name variants */}
        {selectedBroker.variants.length > 0 && (
          <Card className="border-border/50">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm">
                Name Variants ({selectedBroker.variants.length})
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-1.5">
                {selectedBroker.variants.map((v, i) => (
                  <div
                    key={i}
                    className="flex items-center justify-between text-xs rounded border border-border/30 px-3 py-1.5"
                  >
                    <span className="font-mono">{String(v.VARIANT_NAME)}</span>
                    <div className="flex items-center gap-2">
                      <Badge variant="outline" className="text-[10px]">
                        {String(v.SOURCE)}
                      </Badge>
                      <span className="text-muted-foreground">
                        {String(v.MATCH_METHOD)} ({Number(v.MATCH_CONFIDENCE)}%)
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    );
  }

  // Broker list view
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Broker Intelligence</h1>
        <p className="text-sm text-muted-foreground mt-1">
          A2 — Performance scorecard across {brokers.length} broker firms. Click any broker to drill down.
        </p>
      </div>

      <Card className="border-border/50">
        <CardContent className="p-0">
          <div className="rounded-lg overflow-auto">
            <Table>
              <TableHeader>
                <TableRow className="border-border/50">
                  <TableHead className="text-xs">#</TableHead>
                  <TableHead className="text-xs">Broker</TableHead>
                  <SortableHead label="Score" field="BROKER_SCORE" current={sortField} onClick={handleSort} />
                  <SortableHead label="Submissions" field="TOTAL_SUBMISSIONS" current={sortField} onClick={handleSort} />
                  <SortableHead label="Hit Rate" field="HIT_RATE_PCT" current={sortField} onClick={handleSort} />
                  <SortableHead label="Total Premium" field="TOTAL_PREMIUM" current={sortField} onClick={handleSort} />
                  <TableHead className="text-xs text-right">B/D/N</TableHead>
                  <TableHead className="text-xs text-right">Completeness</TableHead>
                  <TableHead className="text-xs">Sources</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {sorted.map((b, idx) => (
                  <TableRow
                    key={b.BROKER_ID}
                    className="border-border/30 cursor-pointer hover:bg-primary/5 transition-colors"
                    onClick={() => handleBrokerClick(b.BROKER_ID)}
                  >
                    <TableCell className="text-xs text-muted-foreground">
                      {idx + 1}
                    </TableCell>
                    <TableCell className="text-sm font-medium max-w-48 truncate">
                      {b.DISPLAY_NAME}
                    </TableCell>
                    <TableCell className="text-right">
                      <span className="text-sm font-bold text-primary">
                        {b.BROKER_SCORE}
                      </span>
                    </TableCell>
                    <TableCell className="text-xs text-right font-mono">
                      {b.TOTAL_SUBMISSIONS}
                    </TableCell>
                    <TableCell className="text-xs text-right font-mono">
                      {formatPct(b.HIT_RATE_PCT)}
                    </TableCell>
                    <TableCell className="text-xs text-right font-mono">
                      {formatCurrency(b.TOTAL_PREMIUM)}
                    </TableCell>
                    <TableCell className="text-xs text-right font-mono">
                      {b.BOUND_COUNT}/{b.DECLINED_COUNT}/{b.NTU_COUNT}
                    </TableCell>
                    <TableCell className="text-xs text-right font-mono">
                      {formatPct(b.AVG_COMPLETENESS_SCORE)}
                    </TableCell>
                    <TableCell className="text-xs text-muted-foreground max-w-24 truncate">
                      {b.PRESENT_IN_SOURCES}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function SortableHead({
  label,
  field,
  current,
  onClick,
}: {
  label: string;
  field: SortField;
  current: SortField;
  onClick: (f: SortField) => void;
}) {
  return (
    <TableHead className="text-xs text-right">
      <button
        onClick={() => onClick(field)}
        className="flex items-center gap-1 ml-auto hover:text-foreground transition-colors"
      >
        {label}
        <ArrowUpDown
          className={`h-3 w-3 ${current === field ? "text-primary" : "text-muted-foreground/30"}`}
        />
      </button>
    </TableHead>
  );
}

function MetricCard({
  label,
  value,
  accent = false,
}: {
  label: string;
  value: string;
  accent?: boolean;
}) {
  return (
    <div className="rounded-lg border border-border bg-card p-3">
      <p className="text-xs text-muted-foreground">{label}</p>
      <p className={`text-lg font-bold ${accent ? "text-primary" : ""}`}>
        {value}
      </p>
    </div>
  );
}
