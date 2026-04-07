# TMHCCI UW POC -- Deliverable Scope

| ID | Deliverable | Description | Status | Owner | Target Date | Notes |
|----|-------------|-------------|--------|-------|-------------|-------|
| D1 | Data Landing | Bulk load all data into Snowflake -- emails, rating sheets, claims, guidelines. Stages + COPY INTO for structured, AI_PARSE_DOCUMENT for unstructured. | NOT_STARTED | Barga | April 9 | Synthetic set: 50 emails, 10 SOVs, 10 loss runs |
| D2 | Entity Resolution | Fuzzy matching (JAROWINKLER_SIMILARITY) on insured name + date + broker to link submissions -> ratings -> claims. 70-80% match rate fine for demo. | NOT_STARTED | Barga | April 9 | Highest-risk item -- depends on naming messiness |
| D3 | UW Notes Corpus | Extract UW notes and decline reasons, clean with AI_COMPLETE, load into Cortex Search Service. Highest-signal deliverable. | NOT_STARTED | Barga | April 10 | Surfaces institutional knowledge UWs cant find today |
| D4 | Email Submission Parser | Three-stage pipeline: PARSE_DOCUMENT -> AI_COMPLETE structured output -> AI_EXTRACT. Two-track: targeted extraction (fast) + full aggregation (thorough) with smart router. | NOT_STARTED | Sai | April 10 | Building against 10 synthetic broker emails |
| D5 | Workbook Mapping | Catalog the rating workbook: input cells, output cells, allowed values, sheet dependencies. PARSE_DOCUMENT + COMPLETE to auto-generate catalog. | NOT_STARTED | Sai | April 10 | Validate with UWs onsite Day 1-2 |
| A1 | Submission Completeness Scoring | Auto-score whether submission has enough info to rate. Flag gaps, generate broker follow-up request. | NOT_STARTED | Sai | April 10 | Aspirational -- unlock after D4 works reliably |
| A2 | Broker Scorecard | Profile brokers by historical submission quality, completeness rates, win rates. | NOT_STARTED | Barga | April 10 | Aspirational -- unlock after D2 entity resolution |
| A3 | Email Classification | Classify 15k emails into initial submissions vs follow-ups vs mid-journey. | NOT_STARTED | Sai | April 10 | Aspirational -- unlock after D1 + D4 |
