"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Separator } from "@/components/ui/separator";
import { Mail, ArrowRight, Filter } from "lucide-react";
import { classificationColor, classificationLabel, formatDate } from "@/components/FormatUtils";
import { StatusBadge } from "@/components/StatusBadge";

interface Email {
  EMAIL_ID: number;
  FILE_NAME: string;
  SUBMISSION_ID: string;
  FILENAME_BASED_TYPE: string;
  CANONICAL_INSURED_NAME: string;
  SUBJECT: string;
  DATE_SENT: string;
  AI_CLASSIFICATION: string;
  CLASSIFICATION_MATCH: boolean;
}

interface EmailDetail {
  classification: Email;
  submission: Record<string, unknown> | null;
}

export default function InboxTriage() {
  const [emails, setEmails] = useState<Email[]>([]);
  const [grouped, setGrouped] = useState<Record<string, Email[]>>({});
  const [loading, setLoading] = useState(true);
  const [selectedEmail, setSelectedEmail] = useState<EmailDetail | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);
  const [activeCategory, setActiveCategory] = useState<string | null>(null);

  useEffect(() => {
    async function fetchEmails() {
      try {
        const res = await fetch("/api/emails");
        const data = await res.json();
        setEmails(data.emails || []);
        setGrouped(data.grouped || {});
      } catch (err) {
        console.error("Failed to fetch emails:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchEmails();
  }, []);

  async function handleEmailClick(emailId: number) {
    setDetailLoading(true);
    try {
      const res = await fetch(`/api/emails/${emailId}`);
      const data = await res.json();
      setSelectedEmail(data);
    } catch (err) {
      console.error("Failed to fetch email detail:", err);
    } finally {
      setDetailLoading(false);
    }
  }

  const categories = Object.keys(grouped);
  const displayedEmails = activeCategory
    ? grouped[activeCategory] || []
    : emails;

  if (loading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-8 w-64" />
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <Skeleton className="h-96 col-span-2" />
          <Skeleton className="h-96" />
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold">Inbox Triage</h1>
        <p className="text-sm text-muted-foreground mt-1">
          A3 — AI-classified submission emails. {emails.length} emails across{" "}
          {categories.length} categories.
        </p>
      </div>

      {/* Category filter chips */}
      <div className="flex items-center gap-2 flex-wrap">
        <Filter className="h-4 w-4 text-muted-foreground" />
        <button
          onClick={() => setActiveCategory(null)}
          className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
            activeCategory === null
              ? "bg-primary text-primary-foreground"
              : "bg-secondary text-secondary-foreground hover:bg-secondary/80"
          }`}
        >
          All ({emails.length})
        </button>
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setActiveCategory(cat)}
            className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
              activeCategory === cat
                ? "bg-primary text-primary-foreground"
                : "bg-secondary text-secondary-foreground hover:bg-secondary/80"
            }`}
          >
            {classificationLabel(cat)} ({grouped[cat].length})
          </button>
        ))}
      </div>

      {/* Main content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Email list */}
        <div className="lg:col-span-2 space-y-2 max-h-[calc(100vh-280px)] overflow-y-auto pr-1">
          {displayedEmails.map((email) => (
            <button
              key={email.EMAIL_ID}
              onClick={() => handleEmailClick(email.EMAIL_ID)}
              className={`w-full text-left rounded-lg border border-border/50 p-3 hover:border-primary/30 transition-colors ${
                selectedEmail?.classification?.EMAIL_ID === email.EMAIL_ID
                  ? "border-primary/50 bg-primary/5"
                  : "bg-card/50"
              }`}
            >
              <div className="flex items-center gap-2 mb-1">
                <Mail className="h-3.5 w-3.5 text-muted-foreground" />
                <span className="text-xs font-mono text-muted-foreground">
                  #{email.EMAIL_ID}
                </span>
                <Badge
                  variant="outline"
                  className={`text-[10px] ${classificationColor(email.AI_CLASSIFICATION)}`}
                >
                  {classificationLabel(email.AI_CLASSIFICATION)}
                </Badge>
                {email.CLASSIFICATION_MATCH && (
                  <span className="text-[10px] text-emerald-600">✓ match</span>
                )}
                <span className="ml-auto text-[10px] text-muted-foreground">
                  {formatDate(email.DATE_SENT)}
                </span>
              </div>
              <p className="text-sm font-medium text-foreground truncate">
                {email.CANONICAL_INSURED_NAME || email.FILE_NAME}
              </p>
              <p className="text-xs text-muted-foreground truncate">
                {email.SUBJECT || email.FILE_NAME}
              </p>
            </button>
          ))}
        </div>

        {/* Detail panel */}
        <div>
          {detailLoading ? (
            <Skeleton className="h-96 rounded-lg" />
          ) : selectedEmail ? (
            <Card className="border-border/50 sticky top-6">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm flex items-center gap-2">
                  <ArrowRight className="h-4 w-4 text-primary" />
                  Email Detail
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <DetailRow
                    label="Email ID"
                    value={`#${selectedEmail.classification.EMAIL_ID}`}
                  />
                  <DetailRow
                    label="File"
                    value={selectedEmail.classification.FILE_NAME}
                  />
                  <DetailRow
                    label="Submission"
                    value={selectedEmail.classification.SUBMISSION_ID}
                  />
                  <DetailRow
                    label="Insured"
                    value={selectedEmail.classification.CANONICAL_INSURED_NAME || "—"}
                  />
                  <DetailRow
                    label="Date Sent"
                    value={formatDate(selectedEmail.classification.DATE_SENT)}
                  />
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-muted-foreground">
                      AI Classification
                    </span>
                    <Badge
                      variant="outline"
                      className={classificationColor(
                        selectedEmail.classification.AI_CLASSIFICATION
                      )}
                    >
                      {classificationLabel(
                        selectedEmail.classification.AI_CLASSIFICATION
                      )}
                    </Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-muted-foreground">
                      Filename Type
                    </span>
                    <span className="text-xs font-mono">
                      {selectedEmail.classification.FILENAME_BASED_TYPE}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-muted-foreground">
                      Match
                    </span>
                    <StatusBadge
                      status={
                        selectedEmail.classification.CLASSIFICATION_MATCH
                          ? "PASS"
                          : "FAIL"
                      }
                    />
                  </div>
                </div>

                {selectedEmail.submission && (
                  <>
                    <Separator className="bg-border/30" />
                    <div className="space-y-2">
                      <p className="text-xs font-medium text-primary">
                        Linked Submission
                      </p>
                      <DetailRow
                        label="Broker"
                        value={
                          String(
                            selectedEmail.submission.CANONICAL_BROKER_NAME || "—"
                          )
                        }
                      />
                      <DetailRow
                        label="TIV"
                        value={
                          selectedEmail.submission.TOTAL_INSURED_VALUE
                            ? `$${Number(selectedEmail.submission.TOTAL_INSURED_VALUE).toLocaleString()}`
                            : "—"
                        }
                      />
                      <DetailRow
                        label="Coverage"
                        value={String(
                          selectedEmail.submission.COVERAGE_TYPE || "—"
                        )}
                      />
                    </div>
                  </>
                )}
              </CardContent>
            </Card>
          ) : (
            <Card className="border-border/50 border-dashed">
              <CardContent className="p-8 text-center text-muted-foreground">
                <Mail className="h-8 w-8 mx-auto mb-2 opacity-30" />
                <p className="text-sm">Select an email to view details</p>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}

function DetailRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between">
      <span className="text-xs text-muted-foreground">{label}</span>
      <span className="text-xs font-medium text-foreground max-w-[60%] text-right truncate">
        {value}
      </span>
    </div>
  );
}
