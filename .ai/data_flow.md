# TMHCCI UW POC -- Data Flow Registry

## Stage -> RAW Flows
| Flow ID | Source | Target Table | Method | Cortex Function | Notes |
|---------|--------|-------------|--------|-----------------|-------|
| F01 | 01_submission_emails/*.eml | RAW.EMAILS | DIRECTORY() + AI_EXTRACT | AI_EXTRACT | 50 .eml files, 12 structured fields extracted per email |
| F02 | 02_sov_schedules/*.xlsx | RAW.SOV_LOCATIONS | Python openpyxl -> CSV -> COPY INTO | None | Superset schema (35 cols) handles heterogeneous XLSX headers |
| F03 | 03_applications/*.pdf | RAW.APPLICATIONS_PARSED | DIRECTORY() + AI_PARSE_DOCUMENT | AI_PARSE_DOCUMENT (LAYOUT) | 8 PDFs -> markdown content |
| F04 | 04_loss_runs/*.pdf | RAW.LOSS_RUNS_PARSED | DIRECTORY() + AI_PARSE_DOCUMENT | AI_PARSE_DOCUMENT (LAYOUT) | 10 PDFs -> markdown content |
| F05 | 05_promised_lines/*.csv | RAW.PROMISED_LINES | COPY INTO | None | 750 rows, 34 columns |
| F06 | 06_rating_data_ers/*.csv | RAW.RATING_DATA | COPY INTO | None | 426 rows |
| F07a | 07_rating_data_sheets/*.xlsx | RAW.RATING_SHEETS_SUMMARY | Python openpyxl -> CSV -> COPY INTO | None | Summary sheet key-value pairs, 50 rows, 14 cols |
| F07b | 07_rating_data_sheets/*.xlsx | RAW.RATING_SHEETS_FACTORS | Python openpyxl -> CSV -> COPY INTO | None | Rating sheet key-value pairs, 50 rows, 20 cols |
| F07c | 07_rating_data_sheets/*.xlsx | RAW.RATING_SHEETS_LOSS_ANALYSIS | Python openpyxl -> CSV -> COPY INTO | None | Loss Analysis tabular data, 448 rows, 5 cols |
| F07d | 07_rating_data_sheets/*.xlsx | RAW.RATING_SHEETS_UW_NOTES | Python openpyxl -> CSV -> COPY INTO | None | UW Notes free text, 50 rows, 2 cols |
| F08 | 08_claims_data/*.csv | RAW.CLAIMS | COPY INTO | None | 375 rows, 21 columns |
| F09 | 09_uw_guidelines/*.pdf | RAW.UW_GUIDELINES_PARSED | DIRECTORY() + AI_PARSE_DOCUMENT | AI_PARSE_DOCUMENT (LAYOUT) | 3 guideline PDFs -> markdown |
| F10 | 10_authority_letters/*.pdf | RAW.AUTHORITY_LETTERS_PARSED | DIRECTORY() + AI_PARSE_DOCUMENT | AI_PARSE_DOCUMENT (LAYOUT) | 3 authority letter PDFs -> markdown |

## RAW -> CURATED Flows
| Flow ID | Source Table(s) | Target Table | Transformation | Notes |
|---------|----------------|-------------|----------------|-------|
| C01 | RAW.PROMISED_LINES, RAW.RATING_DATA, RAW.CLAIMS, RAW.EMAILS, RAW.RATING_SHEETS_SUMMARY | CURATED.INSURED_NAME_VARIANTS | UPPER + REGEXP_REPLACE suffix stripping | 321 name-source pairs |
| C02 | CURATED.INSURED_NAME_VARIANTS | CURATED.INSURED_ENTITY_MAP | JAROWINKLER_SIMILARITY (>= 92) + manual fixes | 138 canonical entities from 167 variants |
| C03 | CURATED.INSURED_ENTITY_MAP | CURATED.DIM_INSURED | GROUP BY canonical, LISTAGG variants | 138 rows, 14 merged clusters |
| C04 | RAW.PROMISED_LINES, RAW.EMAILS, RAW.RATING_SHEETS_SUMMARY | CURATED.DIM_BROKER | UPPER + suffix stripping, GROUP BY | ~30 canonical brokers |
| C05 | RAW.EMAILS + DIM_INSURED + DIM_BROKER | CURATED.FACT_SUBMISSIONS | Entity linkage via deduped entity map | 50 rows, 100% linkage |
| C06 | RAW.RATING_SHEETS_SUMMARY + RAW.RATING_SHEETS_FACTORS + DIM_INSURED | CURATED.FACT_RATING | JOIN on source_file + entity linkage | 50 rows with full rating factors |
| C07 | CURATED.FACT_SUBMISSIONS + multiple RAW tables | CURATED.SUBMISSION_COMPLETENESS | Weighted scoring across 7 document types | 35 submissions, 9 A-grade |
| C08 | CURATED.FACT_SUBMISSIONS + FACT_RATING + RAW.CLAIMS + DIM_BROKER | CURATED.BROKER_SCORECARD | Composite scoring (hit rate, volume, claims, pricing) | 13 brokers scored |
| C09 | CURATED.FACT_SUBMISSIONS | CURATED.EMAIL_CLASSIFICATION | AI_COMPLETE (llama3.1-8b) content classification | 6 categories, 50 emails |
| C10 | N/A | CURATED.WORKBOOK_FIELD_CATALOG | Manual catalog of 41 rating sheet fields | INPUT/OUTPUT/CALCULATED roles |

## RAW -> SEARCH Flows
| Flow ID | Source Table(s) | Target Table/Service | Transformation | Notes |
|---------|----------------|---------------------|----------------|-------|
| S01 | RAW.RATING_SHEETS_UW_NOTES, RAW.UW_GUIDELINES_PARSED, RAW.APPLICATIONS_PARSED, RAW.LOSS_RUNS_PARSED, RAW.AUTHORITY_LETTERS_PARSED | SEARCH.UW_NOTES_CORPUS | UNION ALL + insured name enrichment | 74 docs, 119KB text |
| S02 | SEARCH.UW_NOTES_CORPUS | SEARCH.UW_KNOWLEDGE_SEARCH | CREATE CORTEX SEARCH SERVICE | Semantic + keyword hybrid search, 1hr target lag |
