import { NextResponse } from "next/server";
import { query } from "@/lib/snowflake";

export const dynamic = "force-dynamic";

export async function GET(
  _req: Request,
  { params }: { params: { id: string } }
) {
  try {
    const emailId = parseInt(params.id, 10);
    if (isNaN(emailId)) {
      return NextResponse.json({ error: "Invalid email ID" }, { status: 400 });
    }

    const [classification, submission] = await Promise.all([
      query<{
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
        `SELECT * FROM TMHCCI_UW_POC.CURATED.EMAIL_CLASSIFICATION WHERE EMAIL_ID = ?`,
        [emailId]
      ),
      query<Record<string, unknown>>(
        `SELECT * FROM TMHCCI_UW_POC.CURATED.FACT_SUBMISSIONS WHERE EMAIL_ID = ?`,
        [emailId]
      ),
    ]);

    if (classification.length === 0) {
      return NextResponse.json({ error: "Email not found" }, { status: 404 });
    }

    return NextResponse.json({
      classification: classification[0],
      submission: submission[0] || null,
    });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
