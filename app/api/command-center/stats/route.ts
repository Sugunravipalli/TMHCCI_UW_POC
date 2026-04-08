import { NextResponse } from "next/server";
import { query } from "@/lib/snowflake";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const [submissions, grades, emailStats, brokerStats, pipelineHealth] =
      await Promise.all([
        query<{ CNT: number }>(
          `SELECT COUNT(*) AS CNT FROM TMHCCI_UW_POC.CURATED.SUBMISSION_COMPLETENESS`
        ),
        query<{
          COMPLETENESS_GRADE: string;
          CNT: number;
          AVG_SCORE: number;
        }>(
          `SELECT COMPLETENESS_GRADE, COUNT(*) AS CNT, AVG(COMPLETENESS_SCORE) AS AVG_SCORE
           FROM TMHCCI_UW_POC.CURATED.SUBMISSION_COMPLETENESS
           GROUP BY COMPLETENESS_GRADE ORDER BY AVG_SCORE DESC`
        ),
        query<{ AI_CLASSIFICATION: string; CNT: number; MATCHES: number }>(
          `SELECT AI_CLASSIFICATION, COUNT(*) AS CNT,
                  SUM(CASE WHEN CLASSIFICATION_MATCH THEN 1 ELSE 0 END) AS MATCHES
           FROM TMHCCI_UW_POC.CURATED.EMAIL_CLASSIFICATION
           GROUP BY AI_CLASSIFICATION ORDER BY CNT DESC`
        ),
        query<{ BROKER_COUNT: number; AVG_SCORE: number; TOP_BROKER: string; TOP_SCORE: number }>(
          `SELECT COUNT(*) AS BROKER_COUNT,
                  AVG(BROKER_SCORE) AS AVG_SCORE,
                  MAX_BY(DISPLAY_NAME, BROKER_SCORE) AS TOP_BROKER,
                  MAX(BROKER_SCORE) AS TOP_SCORE
           FROM TMHCCI_UW_POC.CURATED.BROKER_SCORECARD`
        ),
        query<{ STEP_COUNT: number; TOTAL_ROWS: number; TOTAL_SECONDS: number; ALL_SUCCESS: boolean }>(
          `SELECT COUNT(*) AS STEP_COUNT,
                  SUM(ROWS_AFFECTED) AS TOTAL_ROWS,
                  SUM(EXECUTION_SECONDS) AS TOTAL_SECONDS,
                  MIN(CASE WHEN STATUS = 'SUCCESS' THEN 1 ELSE 0 END) = 1 AS ALL_SUCCESS
           FROM TMHCCI_UW_POC.CURATED.DATA_FLOW`
        ),
      ]);

    const totalSubmissions = submissions[0]?.CNT || 0;
    const totalEmails = emailStats.reduce((sum, e) => sum + e.CNT, 0);
    const totalMatches = emailStats.reduce((sum, e) => sum + e.MATCHES, 0);
    const classificationAccuracy =
      totalEmails > 0 ? Math.round((totalMatches / totalEmails) * 100) : 0;

    const completeCount =
      grades.find((g) => g.COMPLETENESS_GRADE.startsWith("A"))?.CNT || 0;
    const incompleteCount = totalSubmissions - completeCount;

    return NextResponse.json({
      kpis: {
        totalSubmissions,
        totalEmails,
        completeCount,
        incompleteCount,
        classificationAccuracy,
        brokerCount: brokerStats[0]?.BROKER_COUNT || 0,
        avgBrokerScore: Number(brokerStats[0]?.AVG_SCORE?.toFixed(1)) || 0,
        topBroker: brokerStats[0]?.TOP_BROKER || "",
        topBrokerScore: Number(brokerStats[0]?.TOP_SCORE) || 0,
        pipelineSteps: pipelineHealth[0]?.STEP_COUNT || 0,
        pipelineRowsProcessed: pipelineHealth[0]?.TOTAL_ROWS || 0,
        pipelineSeconds: Number(pipelineHealth[0]?.TOTAL_SECONDS) || 0,
        pipelineHealthy: pipelineHealth[0]?.ALL_SUCCESS ?? false,
      },
      completenessDistribution: grades.map((g) => ({
        grade: g.COMPLETENESS_GRADE,
        count: g.CNT,
        avgScore: Number(g.AVG_SCORE.toFixed(1)),
      })),
      emailClassification: emailStats.map((e) => ({
        category: e.AI_CLASSIFICATION,
        count: e.CNT,
        matches: e.MATCHES,
      })),
    });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
