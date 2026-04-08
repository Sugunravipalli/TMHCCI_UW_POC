import { NextResponse } from "next/server";
import { query } from "@/lib/snowflake";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const [classification, completeness, entityResolution] = await Promise.all([
      query<{ TOTAL: number; MATCHES: number }>(
        `SELECT COUNT(*) AS TOTAL,
                SUM(CASE WHEN CLASSIFICATION_MATCH THEN 1 ELSE 0 END) AS MATCHES
         FROM TMHCCI_UW_POC.CURATED.EMAIL_CLASSIFICATION`
      ),
      query<{ GRADE: string; CNT: number }>(
        `SELECT COMPLETENESS_GRADE AS GRADE, COUNT(*) AS CNT
         FROM TMHCCI_UW_POC.CURATED.SUBMISSION_COMPLETENESS
         GROUP BY COMPLETENESS_GRADE ORDER BY CNT DESC`
      ),
      query<{
        TOTAL_VARIANTS: number;
        UNIQUE_FIRMS: number;
        AVG_CONFIDENCE: number;
      }>(
        `SELECT COUNT(*) AS TOTAL_VARIANTS,
                COUNT(DISTINCT CANONICAL_FIRM_NAME) AS UNIQUE_FIRMS,
                AVG(MATCH_CONFIDENCE) AS AVG_CONFIDENCE
         FROM TMHCCI_UW_POC.CURATED.BROKER_MASTER_MAP`
      ),
    ]);

    const total = classification[0]?.TOTAL || 0;
    const matches = classification[0]?.MATCHES || 0;
    const classificationAccuracy =
      total > 0 ? Math.round((matches / total) * 100) : 0;

    return NextResponse.json({
      classification: {
        total,
        matches,
        accuracy: classificationAccuracy,
      },
      completenessDistribution: completeness.map((c) => ({
        grade: c.GRADE,
        count: c.CNT,
      })),
      entityResolution: {
        totalVariants: entityResolution[0]?.TOTAL_VARIANTS || 0,
        uniqueFirms: entityResolution[0]?.UNIQUE_FIRMS || 0,
        avgConfidence: Number(
          entityResolution[0]?.AVG_CONFIDENCE?.toFixed(1)
        ) || 0,
      },
    });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
