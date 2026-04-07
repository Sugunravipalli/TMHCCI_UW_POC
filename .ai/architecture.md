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
- **Schemas:** `STAGING` (with stages: `SYNTHETIC_DATA`, `TMHCCI_REAL_DATA`)
- **Schemas to create during build:** `RAW`, `CURATED`, `SEARCH`

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
