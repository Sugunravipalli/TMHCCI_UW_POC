import { NextResponse } from "next/server";
import { query } from "@/lib/snowflake";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const rows = await query<{
      TEST_NAME: string;
      EXPECTED: string;
      ACTUAL: string;
      STATUS: string;
    }>(`SELECT * FROM TABLE(TMHCCI_UW_POC.CURATED.RUN_REGRESSION_TESTS())`);

    const total = rows.length;
    const passed = rows.filter((r) => r.STATUS === "PASS").length;
    const failed = rows.filter((r) => r.STATUS !== "PASS").length;

    return NextResponse.json({
      tests: rows,
      summary: { total, passed, failed },
    });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
