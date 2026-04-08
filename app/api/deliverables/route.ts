import { NextResponse } from "next/server";
import { query } from "@/lib/snowflake";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    // Check row counts across RAW and CURATED to determine deliverable status
    const [rawCounts, curatedCounts, fieldCatalog, searchCorpus] =
      await Promise.all([
        query<{ TABLE_NAME: string; ROW_COUNT: number }>(
          `SELECT TABLE_NAME, ROW_COUNT
           FROM TMHCCI_UW_POC.INFORMATION_SCHEMA.TABLES
           WHERE TABLE_SCHEMA = 'RAW'
           ORDER BY TABLE_NAME`
        ),
        query<{ TABLE_NAME: string; ROW_COUNT: number }>(
          `SELECT TABLE_NAME, ROW_COUNT
           FROM TMHCCI_UW_POC.INFORMATION_SCHEMA.TABLES
           WHERE TABLE_SCHEMA = 'CURATED'
           ORDER BY TABLE_NAME`
        ),
        query<{ CNT: number }>(
          `SELECT COUNT(*) AS CNT FROM TMHCCI_UW_POC.CURATED.WORKBOOK_FIELD_CATALOG`
        ),
        query<{ CNT: number }>(
          `SELECT COUNT(*) AS CNT FROM TMHCCI_UW_POC.SEARCH.UW_NOTES_CORPUS`
        ),
      ]);

    const curatedMap = Object.fromEntries(
      curatedCounts.map((r) => [r.TABLE_NAME, r.ROW_COUNT])
    );

    const deliverables = [
      {
        id: "D1",
        name: "Raw Data Ingestion",
        description: "13 raw tables loaded from CSV/Excel/PDF sources",
        status: rawCounts.length >= 13 ? "COMPLETE" : "INCOMPLETE",
        detail: `${rawCounts.length} tables, ${rawCounts.reduce((s, r) => s + r.ROW_COUNT, 0)} rows`,
      },
      {
        id: "D2",
        name: "Entity Resolution",
        description: "Broker & insured name normalization across sources",
        status:
          (curatedMap["BROKER_MASTER_MAP"] || 0) > 0 &&
          (curatedMap["INSURED_ENTITY_MAP"] || 0) > 0
            ? "COMPLETE"
            : "INCOMPLETE",
        detail: `${curatedMap["BROKER_MASTER_MAP"] || 0} broker variants, ${curatedMap["INSURED_ENTITY_MAP"] || 0} insured variants`,
      },
      {
        id: "D3",
        name: "Curated Fact Tables",
        description: "FACT_SUBMISSIONS + FACT_RATING with resolved foreign keys",
        status:
          (curatedMap["FACT_SUBMISSIONS"] || 0) > 0 &&
          (curatedMap["FACT_RATING"] || 0) > 0
            ? "COMPLETE"
            : "INCOMPLETE",
        detail: `${curatedMap["FACT_SUBMISSIONS"] || 0} submissions, ${curatedMap["FACT_RATING"] || 0} ratings`,
      },
      {
        id: "D4",
        name: "Data Quality Framework",
        description: "20 regression tests + pipeline lineage tracking",
        status: (curatedMap["DATA_FLOW"] || 0) > 0 ? "COMPLETE" : "INCOMPLETE",
        detail: `${curatedMap["DATA_FLOW"] || 0} pipeline steps tracked`,
      },
      {
        id: "D5",
        name: "Rating Workbook Field Catalog",
        description: "Structured field mapping for rating sheet ingestion",
        status: (fieldCatalog[0]?.CNT || 0) > 0 ? "COMPLETE" : "INCOMPLETE",
        detail: `${fieldCatalog[0]?.CNT || 0} fields cataloged`,
      },
      {
        id: "A1",
        name: "Submission Completeness Scoring",
        description: "Auto-scored completeness grades with missing doc detection",
        status:
          (curatedMap["SUBMISSION_COMPLETENESS"] || 0) > 0
            ? "COMPLETE"
            : "INCOMPLETE",
        detail: `${curatedMap["SUBMISSION_COMPLETENESS"] || 0} submissions scored`,
      },
      {
        id: "A2",
        name: "Broker Performance Scorecard",
        description: "Cross-source broker intelligence with 27 metrics",
        status:
          (curatedMap["BROKER_SCORECARD"] || 0) > 0
            ? "COMPLETE"
            : "INCOMPLETE",
        detail: `${curatedMap["BROKER_SCORECARD"] || 0} brokers scored`,
      },
      {
        id: "A3",
        name: "Email AI Classification",
        description: "Cortex AI_CLASSIFY for submission email triage",
        status:
          (curatedMap["EMAIL_CLASSIFICATION"] || 0) > 0
            ? "COMPLETE"
            : "INCOMPLETE",
        detail: `${curatedMap["EMAIL_CLASSIFICATION"] || 0} emails classified`,
      },
    ];

    return NextResponse.json({
      deliverables,
      rawTables: rawCounts,
      curatedTables: curatedCounts,
      searchCorpusSize: searchCorpus[0]?.CNT || 0,
    });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
