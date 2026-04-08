import { NextResponse } from "next/server";
import { query } from "@/lib/snowflake";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const rows = await query<{
      EMAIL_ID: number;
      FILE_NAME: string;
      SUBMISSION_ID: string;
      FILENAME_BASED_TYPE: string;
      CANONICAL_INSURED_NAME: string;
      SUBJECT: string;
      DATE_SENT: string;
      AI_CLASSIFICATION: string;
      CLASSIFICATION_MATCH: boolean;
    }>(
      `SELECT ec.EMAIL_ID, ec.FILE_NAME, ec.SUBMISSION_ID, ec.FILENAME_BASED_TYPE,
              ec.CANONICAL_INSURED_NAME, ec.SUBJECT, ec.DATE_SENT,
              ec.AI_CLASSIFICATION, ec.CLASSIFICATION_MATCH
       FROM TMHCCI_UW_POC.CURATED.EMAIL_CLASSIFICATION ec
       ORDER BY ec.AI_CLASSIFICATION, ec.DATE_SENT DESC`
    );

    const grouped: Record<string, typeof rows> = {};
    for (const row of rows) {
      const cat = row.AI_CLASSIFICATION;
      if (!grouped[cat]) grouped[cat] = [];
      grouped[cat].push(row);
    }

    return NextResponse.json({ emails: rows, grouped });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
