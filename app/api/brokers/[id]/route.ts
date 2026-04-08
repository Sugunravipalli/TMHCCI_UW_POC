import { NextResponse } from "next/server";
import { query } from "@/lib/snowflake";

export const dynamic = "force-dynamic";

export async function GET(
  _req: Request,
  { params }: { params: { id: string } }
) {
  try {
    const brokerId = parseInt(params.id, 10);
    if (isNaN(brokerId)) {
      return NextResponse.json({ error: "Invalid broker ID" }, { status: 400 });
    }

    const [scorecard, ratings, variants] = await Promise.all([
      query<Record<string, unknown>>(
        `SELECT * FROM TMHCCI_UW_POC.CURATED.BROKER_SCORECARD WHERE BROKER_ID = ?`,
        [brokerId]
      ),
      query<Record<string, unknown>>(
        `SELECT RATING_ID, CANONICAL_INSURED_NAME, EFFECTIVE_DATE, COVERAGE_TYPE,
                TOTAL_INSURED_VALUE, OUR_LINE_PCT, OUR_PREMIUM, TECHNICAL_PREMIUM,
                DECISION, DEVIATION_PCT, UNDERWRITER
         FROM TMHCCI_UW_POC.CURATED.FACT_RATING
         WHERE BROKER_ID = ?
         ORDER BY EFFECTIVE_DATE DESC`,
        [brokerId]
      ),
      query<Record<string, unknown>>(
        `SELECT VARIANT_NAME, SOURCE, MATCH_METHOD, MATCH_CONFIDENCE, CONTACT_PERSON, EMAIL_DOMAIN
         FROM TMHCCI_UW_POC.CURATED.BROKER_MASTER_MAP
         WHERE CANONICAL_FIRM_NAME = (
           SELECT CANONICAL_BROKER_NAME FROM TMHCCI_UW_POC.CURATED.BROKER_SCORECARD WHERE BROKER_ID = ?
         )
         ORDER BY SOURCE, VARIANT_NAME`,
        [brokerId]
      ),
    ]);

    if (scorecard.length === 0) {
      return NextResponse.json({ error: "Broker not found" }, { status: 404 });
    }

    return NextResponse.json({
      scorecard: scorecard[0],
      ratings,
      variants,
    });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
