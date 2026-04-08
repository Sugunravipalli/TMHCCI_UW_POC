import { NextResponse } from "next/server";
import { query } from "@/lib/snowflake";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const rows = await query<Record<string, unknown>>(
      `SELECT SUBMISSION_ID, INSURED_ID, CANONICAL_INSURED_NAME,
              BROKER_ID, CANONICAL_BROKER_NAME, SUBMISSION_DATE,
              TOTAL_INSURED_VALUE, EFFECTIVE_DATE, COVERAGE_TYPE,
              HAS_INITIAL_EMAIL, IS_RENEWAL, FOLLOWUP_COUNT,
              HAS_BINDING_ORDER, UW_QUERY_COUNT, TOTAL_EMAILS,
              HAS_SOV, HAS_APPLICATION, HAS_LOSS_RUN, HAS_RATING_SHEET,
              CLAIMS_COUNT, PROMISED_LINES_COUNT,
              COMPLETENESS_SCORE, COMPLETENESS_GRADE,
              MISSING_DOCUMENTS, FOLLOW_UP_REQUEST
       FROM TMHCCI_UW_POC.CURATED.SUBMISSION_COMPLETENESS
       ORDER BY COMPLETENESS_SCORE DESC`
    );

    return NextResponse.json({ submissions: rows });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
