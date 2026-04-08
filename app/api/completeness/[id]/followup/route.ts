import { NextResponse } from "next/server";
import { query } from "@/lib/snowflake";

export const dynamic = "force-dynamic";

export async function GET(
  _req: Request,
  { params }: { params: { id: string } }
) {
  try {
    const submissionId = params.id;

    const rows = await query<{
      FOLLOW_UP_REQUEST: string;
      MISSING_DOCUMENTS: string;
      COMPLETENESS_GRADE: string;
      COMPLETENESS_SCORE: number;
      CANONICAL_INSURED_NAME: string;
    }>(
      `SELECT FOLLOW_UP_REQUEST, MISSING_DOCUMENTS, COMPLETENESS_GRADE,
              COMPLETENESS_SCORE, CANONICAL_INSURED_NAME
       FROM TMHCCI_UW_POC.CURATED.SUBMISSION_COMPLETENESS
       WHERE SUBMISSION_ID = ?`,
      [submissionId]
    );

    if (rows.length === 0) {
      return NextResponse.json(
        { error: "Submission not found" },
        { status: 404 }
      );
    }

    return NextResponse.json(rows[0]);
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
