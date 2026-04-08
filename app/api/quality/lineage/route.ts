import { NextResponse } from "next/server";
import { query } from "@/lib/snowflake";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const rows = await query<{
      STEP_ORDER: number;
      STEP_NAME: string;
      SOURCE_SCHEMA: string;
      SOURCE_TABLES: string;
      TARGET_TABLE: string;
      DESCRIPTION: string;
      ROWS_AFFECTED: number;
      EXECUTION_SECONDS: number;
      EXECUTED_AT: string;
      STATUS: string;
    }>(
      `SELECT * FROM TMHCCI_UW_POC.CURATED.DATA_FLOW ORDER BY STEP_ORDER`
    );

    return NextResponse.json({ steps: rows });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
