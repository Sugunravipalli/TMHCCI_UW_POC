# TMHCCI UW POC -- Runbook

| Step | Phase | Action | Owner | Date | Status |
|------|-------|--------|-------|------|--------|
| 1 | PRE-BUILD | Generate synthetic data (emails, SOVs, loss runs, notes, entities, claims) | Barga | April 7 | COMPLETED |
| 2 | PRE-BUILD | Create database skeleton and project context (this step) | Sai | April 7 | COMPLETED |
| 3 | BUILD | Upload synthetic data to Snowflake stage | Barga | April 7 | COMPLETED |
| 4 | BUILD | D1 -- Load all raw data into RAW schema (13 tables, 2,353 rows) | Barga | April 7 | COMPLETED |
| 5 | BUILD | D2 -- Build entity resolution (138 canonical entities, JW similarity) | Barga | April 7 | COMPLETED |
| 6 | BUILD | D3 -- Build UW notes corpus + Cortex Search (74 docs, service live) | Barga | April 7 | COMPLETED |
| 7 | BUILD | D4 -- Build email parser (AI_EXTRACT on 50 .eml, FACT_SUBMISSIONS) | Barga | April 7 | COMPLETED |
| 8 | BUILD | D5 -- Build workbook mapping catalog (41 fields, FACT_RATING) | Barga | April 7 | COMPLETED |
| 9 | BUILD | A1 -- Submission completeness scoring (35 submissions scored) | Barga | April 7 | COMPLETED |
| 10 | BUILD | A2 -- Broker scorecard (13 brokers, composite scoring) | Barga | April 7 | COMPLETED |
| 11 | BUILD | A3 -- Email classification (6 AI categories, renewals discovered) | Barga | April 7 | COMPLETED |
| 12 | TEST | End-to-end dry run on synthetic data | Both | April 10 | NOT_STARTED |
| 13 | ONSITE | Demo Canonical Brain + synthetic pipeline (Day 1) | Sai | April 13 | NOT_STARTED |
| 14 | ONSITE | Get real submissions + start loading (Day 2) | Both | April 14 | NOT_STARTED |
| 15 | ONSITE | Full build on real data (Day 3) | Both | April 15 | NOT_STARTED |
| 16 | ONSITE | Demo on real TMHCCI data (Day 4) | Both | April 16 | NOT_STARTED |
