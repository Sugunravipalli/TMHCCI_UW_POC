# TMHCCI UW POC -- Architecture Layers

| Order | Layer | Function Used | Description | Swap Strategy (Synthetic -> Real) |
|-------|-------|---------------|-------------|-----------------------------------|
| 1 | Snowflake Stage | Stage + PUT/COPY INTO | Raw files land here. Synthetic now, real TMHCCI files onsite. | Create new stage TMHCCI_REAL_DATA, upload real files, re-run same pipeline |
| 2 | Document Parser | AI_PARSE_DOCUMENT | Turns PDFs, Excel, scanned docs into structured text. LAYOUT mode for tables, OCR for scans. | Same function -- works on any document format |
| 3 | Field Extraction | AI_COMPLETE / AI_EXTRACT | Extracts specific fields into structured JSON. Two tracks: targeted (cheap/fast) + full aggregation (thorough). | May need prompt tuning for TMHCCI terminology |
| 4 | Knowledge Search | Cortex Search Service | Makes UW notes searchable via natural language. Hybrid search: semantic + keyword. | Drop and recreate search service on real notes table |
| 5 | Curated Output | SQL Views + Tables | Clean structured data ready for mapping and demo. | Same schema regardless of data source |

## Snowflake Objects

- **Database:** `TMHCCI_UW_POC`
- **Warehouse:** `TMHCCI_POC_WH` (MEDIUM, auto-suspend 300s, auto-resume)
- **Connection:** `Banking_demo` | **Role:** `SYSADMIN`

### STAGING Schema
- **Stage:** `SYNTHETIC_DATA` (directory-enabled internal stage)
- Extracted CSVs at: `02_sov_parsed/`, `07_rs_extracted/`

### RAW Schema (13 tables, 2,353 rows)
| Table | Rows | Source Method |
|-------|------|-------------|
| PROMISED_LINES | 750 | COPY INTO from CSV |
| RATING_DATA | 426 | COPY INTO from CSV |
| CLAIMS | 375 | COPY INTO from CSV |
| EMAILS | 50 | AI_EXTRACT on .eml files |
| APPLICATIONS_PARSED | 8 | AI_PARSE_DOCUMENT on PDFs |
| LOSS_RUNS_PARSED | 10 | AI_PARSE_DOCUMENT on PDFs |
| UW_GUIDELINES_PARSED | 3 | AI_PARSE_DOCUMENT on PDFs |
| AUTHORITY_LETTERS_PARSED | 3 | AI_PARSE_DOCUMENT on PDFs |
| SOV_LOCATIONS | 130 | Python openpyxl -> CSV -> COPY INTO (superset schema, 35 cols) |
| RATING_SHEETS_SUMMARY | 50 | Python openpyxl -> CSV -> COPY INTO |
| RATING_SHEETS_FACTORS | 50 | Python openpyxl -> CSV -> COPY INTO |
| RATING_SHEETS_LOSS_ANALYSIS | 448 | Python openpyxl -> CSV -> COPY INTO |
| RATING_SHEETS_UW_NOTES | 50 | Python openpyxl -> CSV -> COPY INTO |

### CURATED Schema (8 tables)
| Table | Rows | Purpose |
|-------|------|---------|
| INSURED_NAME_VARIANTS | ~321 | All name variants with normalized names across 5 sources |
| INSURED_ENTITY_MAP | ~321 | Maps original -> canonical insured name |
| DIM_INSURED | 138 | Canonical insured dimension (14 merged entity clusters) |
| DIM_BROKER | ~30 | Canonical broker dimension |
| FACT_SUBMISSIONS | 50 | Email submissions linked to DIM_INSURED + DIM_BROKER |
| FACT_RATING | 50 | Rating sheet data joined with factors, linked to entities |
| WORKBOOK_FIELD_CATALOG | 41 | Metadata catalog of rating sheet fields (input/output/calculated) |
| SUBMISSION_COMPLETENESS | 35 | Weighted completeness scores per submission |
| BROKER_SCORECARD | 13 | Composite broker performance scores |
| EMAIL_CLASSIFICATION | 50 | AI-classified email categories (6 types) |

### SEARCH Schema (1 table, 1 service)
| Object | Type | Description |
|--------|------|-------------|
| UW_NOTES_CORPUS | TABLE | 74 documents from 5 sources with insured enrichment |
| UW_KNOWLEDGE_SEARCH | CORTEX SEARCH SERVICE | Semantic search on UW corpus, filterable by doc_type and insured_name |

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Data Storage & Processing | Snowflake (tables, stages) |
| Document Intelligence | Cortex AI Functions (PARSE_DOCUMENT, AI_EXTRACT) |
| Semantic Search (notes, similar risks) | Cortex Search Service |
| Agent Orchestration | Cortex Agent |
| UW Synthesis & Reasoning | Cortex AI (LLM completions) |
| Rating Model Execution | Historical validation approach for POC |
| CAT Model Integration | Stubbed with historical outputs for POC |
| Presentation Layer | Notebook / simple Streamlit for POC |
| Guidelines Rule Engine | SQL / Python stored procedures |
