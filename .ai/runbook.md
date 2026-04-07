# TMHCCI UW POC -- Runbook

| Step | Phase | Action | Owner | Date | Status |
|------|-------|--------|-------|------|--------|
| 1 | PRE-BUILD | Generate synthetic data (emails, SOVs, loss runs, notes, entities, claims) | Barga | April 7 | IN_PROGRESS |
| 2 | PRE-BUILD | Create database skeleton and project context (this step) | Sai | April 7 | COMPLETED |
| 3 | BUILD | Upload synthetic data to Snowflake stage | Barga | April 8 | NOT_STARTED |
| 4 | BUILD | D1 -- Load all raw data into RAW schema | Barga | April 8 | NOT_STARTED |
| 5 | BUILD | D2 -- Build entity resolution matching | Barga | April 9 | NOT_STARTED |
| 6 | BUILD | D3 -- Build UW notes corpus + Cortex Search | Barga | April 9 | NOT_STARTED |
| 7 | BUILD | D4 -- Build email parser (Track 1 + Track 2 + router) | Sai | April 9 | NOT_STARTED |
| 8 | BUILD | D5 -- Build workbook mapping catalog | Sai | April 9 | NOT_STARTED |
| 9 | BUILD | A1 -- Submission completeness scoring | Sai | April 10 | NOT_STARTED |
| 10 | BUILD | A2 -- Broker scorecard | Barga | April 10 | NOT_STARTED |
| 11 | BUILD | A3 -- Email classification | Sai | April 10 | NOT_STARTED |
| 12 | TEST | End-to-end dry run on synthetic data | Both | April 10 | NOT_STARTED |
| 13 | ONSITE | Demo Canonical Brain + synthetic pipeline (Day 1) | Sai | April 13 | NOT_STARTED |
| 14 | ONSITE | Get real submissions + start loading (Day 2) | Both | April 14 | NOT_STARTED |
| 15 | ONSITE | Full build on real data (Day 3) | Both | April 15 | NOT_STARTED |
| 16 | ONSITE | Demo on real TMHCCI data (Day 4) | Both | April 16 | NOT_STARTED |
