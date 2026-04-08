import { NextResponse } from "next/server";
import { query } from "@/lib/snowflake";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const rows = await query<Record<string, unknown>>(
      `SELECT BROKER_ID, CANONICAL_BROKER_NAME, DISPLAY_NAME, PRESENT_IN_SOURCES,
              TOTAL_SUBMISSIONS, INITIAL_SUBMISSIONS, RENEWALS, FOLLOW_UPS, BINDING_ORDERS,
              AVG_TIV, UNIQUE_INSUREDS, TOTAL_RATED, BOUND_COUNT, DECLINED_COUNT, NTU_COUNT,
              HIT_RATE_PCT, AVG_PREMIUM, TOTAL_PREMIUM, AVG_DEVIATION_PCT,
              TOTAL_CLAIMS, TOTAL_INCURRED, AVG_CLAIM_SIZE,
              TOTAL_PROMISED_LINES, TOTAL_PREMIUM_PLACED,
              AVG_COMPLETENESS_SCORE, COMPLETENESS_RATE_PCT, BROKER_SCORE
       FROM TMHCCI_UW_POC.CURATED.BROKER_SCORECARD
       ORDER BY BROKER_SCORE DESC`
    );

    return NextResponse.json({ brokers: rows });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
