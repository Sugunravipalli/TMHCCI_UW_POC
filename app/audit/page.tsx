"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { AuditTimeline } from "@/components/AuditTimeline";
import {
  ClipboardList,
  Search,
  FileText,
} from "lucide-react";
import { Input } from "@/components/ui/input";
import { gradeBg, formatCurrency } from "@/components/FormatUtils";

interface Submission {
  SUBMISSION_ID: string;
  CANONICAL_INSURED_NAME: string;
  CANONICAL_BROKER_NAME: string;
  TOTAL_INSURED_VALUE: number;
  COMPLETENESS_GRADE: string;
  COMPLETENESS_SCORE: number;
  TOTAL_EMAILS: number;
  [key: string]: unknown;
}

interface AuditStep {
  step: number;
  name: string;
  function: string;
  result: string;
  executionMs: number;
  missingDocs?: string;
  followUpText?: string;
}

interface AuditData {
  emailId: number;
  steps: AuditStep[];
  totalProcessingMs: number;
  totalProcessingSeconds: string;
  manualEquivalentMinutes: number;
}

export default function AuditTrail() {
  const [submissions, setSubmissions] = useState<Submission[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedAudit, setSelectedAudit] = useState<AuditData | null>(null);
  const [auditLoading, setAuditLoading] = useState(false);
  const [selectedSubmission, setSelectedSubmission] = useState<Submission | null>(null);
  const [emails, setEmails] = useState<{ EMAIL_ID: number; SUBMISSION_ID: string }[]>([]);

  useEffect(() => {
    async function fetchData() {
      try {
        const [subRes, emailRes] = await Promise.all([
          fetch("/api/completeness"),
          fetch("/api/emails"),
        ]);
        const subData = await subRes.json();
        const emailData = await emailRes.json();

        setSubmissions(subData.submissions || []);
        setEmails(
          (emailData.emails || []).map((e: Record<string, unknown>) => ({
            EMAIL_ID: e.EMAIL_ID,
            SUBMISSION_ID: e.SUBMISSION_ID,
          }))
        );
      } catch (err) {
        console.error("Failed to fetch audit data:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  async function handleSubmissionClick(sub: Submission) {
    setSelectedSubmission(sub);
    setAuditLoading(true);
    setSelectedAudit(null);

    // Find an email for this submission to get the audit trail
    const email = emails.find((e) => e.SUBMISSION_ID === sub.SUBMISSION_ID);
    if (!email) {
      setAuditLoading(false);
      return;
    }

    try {
      const res = await fetch(`/api/emails/${email.EMAIL_ID}/audit`);
      const data = await res.json();
      setSelectedAudit(data);
    } catch (err) {
      console.error("Failed to fetch audit trail:", err);
    } finally {
      setAuditLoading(false);
    }
  }

  const filtered = submissions.filter((s) => {
    const term = searchTerm.toLowerCase();
    return (
      s.SUBMISSION_ID.toLowerCase().includes(term) ||
      (s.CANONICAL_INSURED_NAME || "").toLowerCase().includes(term) ||
      (s.CANONICAL_BROKER_NAME || "").toLowerCase().includes(term)
    );
  });

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
        <h1 className="text-2xl font-bold">Audit Trail</h1>
        <p className="text-sm text-muted-foreground mt-1">
          Per-submission explainability timeline — see every processing step for each submission
        </p>
      </div>

      {/* Search */}
      <div className="relative max-w-md">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Search by submission ID, insured, or broker..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="pl-9 bg-card border-border"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Submission list */}
        <div className="lg:col-span-1 space-y-2 max-h-[calc(100vh-300px)] overflow-y-auto pr-1">
          {filtered.map((sub) => (
            <button
              key={sub.SUBMISSION_ID}
              onClick={() => handleSubmissionClick(sub)}
              className={`w-full text-left rounded-lg border border-border/50 p-3 hover:border-primary/30 transition-colors ${
                selectedSubmission?.SUBMISSION_ID === sub.SUBMISSION_ID
                  ? "border-primary/50 bg-primary/5"
                  : "bg-card/50"
              }`}
            >
              <div className="flex items-center gap-2 mb-1">
                <FileText className="h-3.5 w-3.5 text-muted-foreground" />
                <span className="text-xs font-mono text-muted-foreground">
                  {sub.SUBMISSION_ID}
                </span>
                <Badge
                  variant="outline"
                  className={`text-[10px] ml-auto ${gradeBg(sub.COMPLETENESS_GRADE)}`}
                >
                  {sub.COMPLETENESS_GRADE} ({sub.COMPLETENESS_SCORE}%)
                </Badge>
              </div>
              <p className="text-sm font-medium text-foreground truncate">
                {sub.CANONICAL_INSURED_NAME || "—"}
              </p>
              <div className="flex items-center justify-between mt-1">
                <p className="text-xs text-muted-foreground truncate">
                  {sub.CANONICAL_BROKER_NAME || "—"}
                </p>
                <span className="text-xs font-mono text-muted-foreground">
                  {sub.TOTAL_INSURED_VALUE
                    ? formatCurrency(sub.TOTAL_INSURED_VALUE)
                    : "—"}
                </span>
              </div>
            </button>
          ))}
        </div>

        {/* Audit timeline */}
        <div className="lg:col-span-2">
          {auditLoading ? (
            <Skeleton className="h-96 rounded-lg" />
          ) : selectedAudit && selectedAudit.steps.length > 0 ? (
            <Card className="border-border/50">
              <CardHeader className="pb-2">
                <div className="flex items-center gap-2">
                  <ClipboardList className="h-4 w-4 text-primary" />
                  <CardTitle className="text-sm">
                    Processing Timeline —{" "}
                    {selectedSubmission?.CANONICAL_INSURED_NAME}
                  </CardTitle>
                </div>
                <p className="text-xs text-muted-foreground">
                  {selectedSubmission?.SUBMISSION_ID} ·{" "}
                  {selectedSubmission?.CANONICAL_BROKER_NAME}
                </p>
              </CardHeader>
              <CardContent>
                <AuditTimeline
                  steps={selectedAudit.steps}
                  totalProcessingSeconds={selectedAudit.totalProcessingSeconds}
                  manualEquivalentMinutes={selectedAudit.manualEquivalentMinutes}
                />
              </CardContent>
            </Card>
          ) : selectedSubmission ? (
            <Card className="border-border/50 border-dashed">
              <CardContent className="p-8 text-center text-muted-foreground">
                <ClipboardList className="h-8 w-8 mx-auto mb-2 opacity-30" />
                <p className="text-sm">No audit trail available for this submission</p>
                <p className="text-xs mt-1">No linked email found</p>
              </CardContent>
            </Card>
          ) : (
            <Card className="border-border/50 border-dashed">
              <CardContent className="p-8 text-center text-muted-foreground">
                <ClipboardList className="h-8 w-8 mx-auto mb-2 opacity-30" />
                <p className="text-sm">
                  Select a submission to view its processing audit trail
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
