# TMHCCI POC -- Snowflake Data Loading Runbook

**Database:** `TMHCCI_UW_POC`
**Schema:** `STAGING`
**Stage:** `SYNTHETIC_DATA`
**Warehouse:** `TMHCCI_POC_WH`

---

## Step 0: Setup (run once)

```sql
USE DATABASE TMHCCI_UW_POC;
USE SCHEMA STAGING;
USE WAREHOUSE TMHCCI_POC_WH;

-- Create the internal stage with subdirectories
CREATE STAGE IF NOT EXISTS SYNTHETIC_DATA
  DIRECTORY = (ENABLE = TRUE)
  COMMENT = 'Synthetic data for TMHCCI UW POC - 10 source folders';
```

---

## Step 1: Upload files to stage (run from SnowSQL or Snowsight)

Upload each folder into a subfolder within the stage. Run these PUT commands
from **SnowSQL** (not Snowsight -- Snowsight can upload files via UI instead).

```sql
-- ============================================================
-- 01: SUBMISSION EMAILS (.eml)
-- ============================================================
PUT file://C:/Users/bharg/Downloads/OneDrive_2026-04-07/Tokio Marine/Tokio Marine POC - London/synthetic_data/01_submission_emails/*.eml
    @SYNTHETIC_DATA/01_submission_emails
    AUTO_COMPRESS = FALSE
    OVERWRITE = TRUE;

-- ============================================================
-- 02: SOV SCHEDULES (.xlsx)
-- ============================================================
PUT file://C:/Users/bharg/Downloads/OneDrive_2026-04-07/Tokio Marine/Tokio Marine POC - London/synthetic_data/02_sov_schedules/*.xlsx
    @SYNTHETIC_DATA/02_sov_schedules
    AUTO_COMPRESS = FALSE
    OVERWRITE = TRUE;

-- ============================================================
-- 03: APPLICATIONS (.pdf)
-- ============================================================
PUT file://C:/Users/bharg/Downloads/OneDrive_2026-04-07/Tokio Marine/Tokio Marine POC - London/synthetic_data/03_applications/*.pdf
    @SYNTHETIC_DATA/03_applications
    AUTO_COMPRESS = FALSE
    OVERWRITE = TRUE;

-- ============================================================
-- 04: LOSS RUNS (.pdf)
-- ============================================================
PUT file://C:/Users/bharg/Downloads/OneDrive_2026-04-07/Tokio Marine/Tokio Marine POC - London/synthetic_data/04_loss_runs/*.pdf
    @SYNTHETIC_DATA/04_loss_runs
    AUTO_COMPRESS = FALSE
    OVERWRITE = TRUE;

-- ============================================================
-- 05: PROMISED LINES (.csv)
-- ============================================================
PUT file://C:/Users/bharg/Downloads/OneDrive_2026-04-07/Tokio Marine/Tokio Marine POC - London/synthetic_data/05_promised_lines/promised_lines.csv
    @SYNTHETIC_DATA/05_promised_lines
    AUTO_COMPRESS = TRUE
    OVERWRITE = TRUE;

-- ============================================================
-- 06: RATING DATA ERS (.csv)
-- ============================================================
PUT file://C:/Users/bharg/Downloads/OneDrive_2026-04-07/Tokio Marine/Tokio Marine POC - London/synthetic_data/06_rating_data_ers/rating_data.csv
    @SYNTHETIC_DATA/06_rating_data_ers
    AUTO_COMPRESS = TRUE
    OVERWRITE = TRUE;

-- ============================================================
-- 07: RATING DATA SHEETS (.xlsx)
-- ============================================================
PUT file://C:/Users/bharg/Downloads/OneDrive_2026-04-07/Tokio Marine/Tokio Marine POC - London/synthetic_data/07_rating_data_sheets/*.xlsx
    @SYNTHETIC_DATA/07_rating_data_sheets
    AUTO_COMPRESS = FALSE
    OVERWRITE = TRUE;

-- ============================================================
-- 08: CLAIMS DATA (.csv)
-- ============================================================
PUT file://C:/Users/bharg/Downloads/OneDrive_2026-04-07/Tokio Marine/Tokio Marine POC - London/synthetic_data/08_claims_data/claims.csv
    @SYNTHETIC_DATA/08_claims_data
    AUTO_COMPRESS = TRUE
    OVERWRITE = TRUE;

-- ============================================================
-- 09: UW GUIDELINES (.pdf)
-- ============================================================
PUT file://C:/Users/bharg/Downloads/OneDrive_2026-04-07/Tokio Marine/Tokio Marine POC - London/synthetic_data/09_uw_guidelines/*.pdf
    @SYNTHETIC_DATA/09_uw_guidelines
    AUTO_COMPRESS = FALSE
    OVERWRITE = TRUE;

-- ============================================================
-- 10: AUTHORITY LETTERS (.pdf)
-- ============================================================
PUT file://C:/Users/bharg/Downloads/OneDrive_2026-04-07/Tokio Marine/Tokio Marine POC - London/synthetic_data/10_authority_letters/*.pdf
    @SYNTHETIC_DATA/10_authority_letters
    AUTO_COMPRESS = FALSE
    OVERWRITE = TRUE;
```

---

## Step 2: Verify uploads

```sql
-- List everything in stage
LIST @SYNTHETIC_DATA;

-- Count files per subfolder
SELECT
    SPLIT_PART(name, '/', 1) AS folder,
    COUNT(*) AS file_count,
    SUM(size) AS total_bytes
FROM DIRECTORY(@SYNTHETIC_DATA)
GROUP BY folder
ORDER BY folder;
```

---

## Step 3: Create RAW schema tables and load structured CSVs

```sql
CREATE SCHEMA IF NOT EXISTS RAW;
USE SCHEMA RAW;

-- ============================================================
-- 05: PROMISED LINES (750 rows)
-- ============================================================
CREATE OR REPLACE TABLE RAW.PROMISED_LINES (
    promised_line_id            VARCHAR,
    submission_id               VARCHAR,
    submission_date             DATE,
    insured_name                VARCHAR,
    broker_name                 VARCHAR,
    broker_contact              VARCHAR,
    coverage_type               VARCHAR,
    effective_date              DATE,
    expiry_date                 DATE,
    total_insured_value         NUMBER(15,0),
    limit_requested             NUMBER(15,0),
    deductible                  NUMBER(12,0),
    lead_follow                 VARCHAR,
    our_line_pct                NUMBER(5,0),
    our_premium                 NUMBER(12,0),
    technical_premium           NUMBER(12,0),
    rate_per_million            FLOAT,
    deviation_from_technical_pct FLOAT,
    decision                    VARCHAR,
    decision_date               DATE,
    decision_reason             VARCHAR,
    underwriter_name            VARCHAR,
    authority_level             VARCHAR,
    referral_required           BOOLEAN,
    decline_reason              VARCHAR,
    ntu_reason                  VARCHAR,
    bound_premium               NUMBER(12,0),
    bound_date                  DATE,
    renewal_of                  VARCHAR,
    fac_reinsurance_purchased   BOOLEAN,
    fac_premium                 NUMBER(12,0),
    number_of_locations         NUMBER(5,0),
    primary_state               VARCHAR,
    occupancy_class             VARCHAR
);

COPY INTO RAW.PROMISED_LINES
FROM @STAGING.SYNTHETIC_DATA/05_promised_lines/promised_lines.csv
FILE_FORMAT = (
    TYPE = 'CSV'
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    SKIP_HEADER = 1
    NULL_IF = ('', 'NULL')
    EMPTY_FIELD_AS_NULL = TRUE
)
ON_ERROR = 'CONTINUE';

-- Verify
SELECT COUNT(*) AS row_count, 'PROMISED_LINES' AS table_name FROM RAW.PROMISED_LINES;


-- ============================================================
-- 06: RATING DATA (426 rows)
-- ============================================================
CREATE OR REPLACE TABLE RAW.RATING_DATA (
    rating_id                   VARCHAR,
    promised_line_id            VARCHAR,
    submission_id               VARCHAR,
    insured_name                VARCHAR,
    effective_date              DATE,
    coverage_type               VARCHAR,
    total_insured_value         NUMBER(15,0),
    number_of_locations         NUMBER(5,0),
    primary_occupancy           VARCHAR,
    primary_construction        VARCHAR,
    primary_protection_class    NUMBER(3,0),
    avg_year_built              NUMBER(4,0),
    pct_sprinklered             NUMBER(3,0),
    base_rate                   FLOAT,
    territory_factor            FLOAT,
    occupancy_factor            FLOAT,
    construction_factor         FLOAT,
    protection_factor           FLOAT,
    experience_mod              FLOAT,
    schedule_mod                FLOAT,
    uw_judgment_factor          FLOAT,
    package_credit              FLOAT,
    technical_rate              FLOAT,
    technical_premium           NUMBER(12,0),
    quoted_rate                 FLOAT,
    quoted_premium              NUMBER(12,0),
    deviation_pct               FLOAT,
    cat_load_wind               FLOAT,
    cat_load_earthquake         FLOAT,
    cat_load_flood              FLOAT,
    expense_ratio               FLOAT,
    profit_margin               FLOAT,
    layer_attachment            NUMBER(12,0),
    layer_limit                 NUMBER(15,0),
    layer_premium               NUMBER(12,0)
);

COPY INTO RAW.RATING_DATA
FROM @STAGING.SYNTHETIC_DATA/06_rating_data_ers/rating_data.csv
FILE_FORMAT = (
    TYPE = 'CSV'
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    SKIP_HEADER = 1
    NULL_IF = ('', 'NULL')
    EMPTY_FIELD_AS_NULL = TRUE
)
ON_ERROR = 'CONTINUE';

SELECT COUNT(*) AS row_count, 'RATING_DATA' AS table_name FROM RAW.RATING_DATA;


-- ============================================================
-- 08: CLAIMS (375 rows)
-- ============================================================
CREATE OR REPLACE TABLE RAW.CLAIMS (
    claim_id                    VARCHAR,
    policy_id                   VARCHAR,
    promised_line_id            VARCHAR,
    insured_name                VARCHAR,
    loss_date                   DATE,
    report_date                 DATE,
    close_date                  DATE,
    claim_status                VARCHAR,
    loss_type                   VARCHAR,
    loss_description            VARCHAR,
    location_state              VARCHAR,
    paid_amount                 NUMBER(12,0),
    reserved_amount             NUMBER(12,0),
    total_incurred              NUMBER(12,0),
    deductible_applied          NUMBER(12,0),
    recovery_amount             NUMBER(12,0),
    net_incurred                NUMBER(12,0),
    cause_of_loss               VARCHAR,
    cat_event_flag              BOOLEAN,
    cat_event_name              VARCHAR,
    large_loss_flag             BOOLEAN
);

COPY INTO RAW.CLAIMS
FROM @STAGING.SYNTHETIC_DATA/08_claims_data/claims.csv
FILE_FORMAT = (
    TYPE = 'CSV'
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    SKIP_HEADER = 1
    NULL_IF = ('', 'NULL')
    EMPTY_FIELD_AS_NULL = TRUE
)
ON_ERROR = 'CONTINUE';

SELECT COUNT(*) AS row_count, 'CLAIMS' AS table_name FROM RAW.CLAIMS;
```

---

## Step 4: Create RAW tables for unstructured documents

```sql
-- ============================================================
-- 01: EMAILS (parsed via AI_COMPLETE)
-- ============================================================
CREATE OR REPLACE TABLE RAW.EMAILS (
    file_name                   VARCHAR,
    file_url                    VARCHAR,
    raw_content                 VARCHAR,
    parsed_at                   TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

INSERT INTO RAW.EMAILS (file_name, file_url, raw_content)
SELECT
    RELATIVE_PATH AS file_name,
    BUILD_SCOPED_FILE_URL(@STAGING.SYNTHETIC_DATA, RELATIVE_PATH) AS file_url,
    NULL AS raw_content  -- will be populated by parser pipeline
FROM DIRECTORY(@STAGING.SYNTHETIC_DATA)
WHERE RELATIVE_PATH LIKE '01_submission_emails/%'
  AND RELATIVE_PATH LIKE '%.eml';


-- ============================================================
-- 02: SOV SCHEDULES (parsed via PARSE_DOCUMENT)
-- ============================================================
CREATE OR REPLACE TABLE RAW.SOV_SCHEDULES (
    file_name                   VARCHAR,
    file_url                    VARCHAR,
    scoped_url                  VARCHAR,
    parsed_content              VARIANT,
    parsed_at                   TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

INSERT INTO RAW.SOV_SCHEDULES (file_name, file_url, scoped_url)
SELECT
    RELATIVE_PATH,
    BUILD_SCOPED_FILE_URL(@STAGING.SYNTHETIC_DATA, RELATIVE_PATH),
    BUILD_SCOPED_FILE_URL(@STAGING.SYNTHETIC_DATA, RELATIVE_PATH)
FROM DIRECTORY(@STAGING.SYNTHETIC_DATA)
WHERE RELATIVE_PATH LIKE '02_sov_schedules/%.xlsx';


-- ============================================================
-- 03: APPLICATIONS (parsed via PARSE_DOCUMENT)
-- ============================================================
CREATE OR REPLACE TABLE RAW.APPLICATIONS (
    file_name                   VARCHAR,
    file_url                    VARCHAR,
    scoped_url                  VARCHAR,
    parsed_content              VARIANT,
    parsed_at                   TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

INSERT INTO RAW.APPLICATIONS (file_name, file_url, scoped_url)
SELECT
    RELATIVE_PATH,
    BUILD_SCOPED_FILE_URL(@STAGING.SYNTHETIC_DATA, RELATIVE_PATH),
    BUILD_SCOPED_FILE_URL(@STAGING.SYNTHETIC_DATA, RELATIVE_PATH)
FROM DIRECTORY(@STAGING.SYNTHETIC_DATA)
WHERE RELATIVE_PATH LIKE '03_applications/%.pdf';


-- ============================================================
-- 04: LOSS RUNS (parsed via PARSE_DOCUMENT)
-- ============================================================
CREATE OR REPLACE TABLE RAW.LOSS_RUNS (
    file_name                   VARCHAR,
    file_url                    VARCHAR,
    scoped_url                  VARCHAR,
    parsed_content              VARIANT,
    parsed_at                   TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

INSERT INTO RAW.LOSS_RUNS (file_name, file_url, scoped_url)
SELECT
    RELATIVE_PATH,
    BUILD_SCOPED_FILE_URL(@STAGING.SYNTHETIC_DATA, RELATIVE_PATH),
    BUILD_SCOPED_FILE_URL(@STAGING.SYNTHETIC_DATA, RELATIVE_PATH)
FROM DIRECTORY(@STAGING.SYNTHETIC_DATA)
WHERE RELATIVE_PATH LIKE '04_loss_runs/%.pdf';


-- ============================================================
-- 07: RATING DATA SHEETS (parsed via PARSE_DOCUMENT)
-- ============================================================
CREATE OR REPLACE TABLE RAW.RATING_SHEETS (
    file_name                   VARCHAR,
    file_url                    VARCHAR,
    scoped_url                  VARCHAR,
    parsed_content              VARIANT,
    parsed_at                   TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

INSERT INTO RAW.RATING_SHEETS (file_name, file_url, scoped_url)
SELECT
    RELATIVE_PATH,
    BUILD_SCOPED_FILE_URL(@STAGING.SYNTHETIC_DATA, RELATIVE_PATH),
    BUILD_SCOPED_FILE_URL(@STAGING.SYNTHETIC_DATA, RELATIVE_PATH)
FROM DIRECTORY(@STAGING.SYNTHETIC_DATA)
WHERE RELATIVE_PATH LIKE '07_rating_data_sheets/%.xlsx';


-- ============================================================
-- 09: UW GUIDELINES (parsed via PARSE_DOCUMENT)
-- ============================================================
CREATE OR REPLACE TABLE RAW.UW_GUIDELINES (
    file_name                   VARCHAR,
    file_url                    VARCHAR,
    scoped_url                  VARCHAR,
    parsed_content              VARIANT,
    parsed_at                   TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

INSERT INTO RAW.UW_GUIDELINES (file_name, file_url, scoped_url)
SELECT
    RELATIVE_PATH,
    BUILD_SCOPED_FILE_URL(@STAGING.SYNTHETIC_DATA, RELATIVE_PATH),
    BUILD_SCOPED_FILE_URL(@STAGING.SYNTHETIC_DATA, RELATIVE_PATH)
FROM DIRECTORY(@STAGING.SYNTHETIC_DATA)
WHERE RELATIVE_PATH LIKE '09_uw_guidelines/%.pdf';


-- ============================================================
-- 10: AUTHORITY LETTERS (parsed via PARSE_DOCUMENT)
-- ============================================================
CREATE OR REPLACE TABLE RAW.AUTHORITY_LETTERS (
    file_name                   VARCHAR,
    file_url                    VARCHAR,
    scoped_url                  VARCHAR,
    parsed_content              VARIANT,
    parsed_at                   TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

INSERT INTO RAW.AUTHORITY_LETTERS (file_name, file_url, scoped_url)
SELECT
    RELATIVE_PATH,
    BUILD_SCOPED_FILE_URL(@STAGING.SYNTHETIC_DATA, RELATIVE_PATH),
    BUILD_SCOPED_FILE_URL(@STAGING.SYNTHETIC_DATA, RELATIVE_PATH)
FROM DIRECTORY(@STAGING.SYNTHETIC_DATA)
WHERE RELATIVE_PATH LIKE '10_authority_letters/%.pdf';
```

---

## Step 5: Parse unstructured documents with Cortex AI

```sql
-- ============================================================
-- Parse PDFs with PARSE_DOCUMENT (applications, loss runs, guidelines, authority)
-- ============================================================

-- Applications
UPDATE RAW.APPLICATIONS
SET parsed_content = SNOWFLAKE.CORTEX.PARSE_DOCUMENT(
    @STAGING.SYNTHETIC_DATA,
    RELATIVE_PATH,
    {'mode': 'LAYOUT'}
)
FROM (SELECT RELATIVE_PATH FROM DIRECTORY(@STAGING.SYNTHETIC_DATA)
      WHERE RELATIVE_PATH LIKE '03_applications/%.pdf') d
WHERE RAW.APPLICATIONS.file_name = d.RELATIVE_PATH;

-- Loss Runs
UPDATE RAW.LOSS_RUNS
SET parsed_content = SNOWFLAKE.CORTEX.PARSE_DOCUMENT(
    @STAGING.SYNTHETIC_DATA,
    RELATIVE_PATH,
    {'mode': 'LAYOUT'}
)
FROM (SELECT RELATIVE_PATH FROM DIRECTORY(@STAGING.SYNTHETIC_DATA)
      WHERE RELATIVE_PATH LIKE '04_loss_runs/%.pdf') d
WHERE RAW.LOSS_RUNS.file_name = d.RELATIVE_PATH;

-- UW Guidelines
UPDATE RAW.UW_GUIDELINES
SET parsed_content = SNOWFLAKE.CORTEX.PARSE_DOCUMENT(
    @STAGING.SYNTHETIC_DATA,
    RELATIVE_PATH,
    {'mode': 'LAYOUT'}
)
FROM (SELECT RELATIVE_PATH FROM DIRECTORY(@STAGING.SYNTHETIC_DATA)
      WHERE RELATIVE_PATH LIKE '09_uw_guidelines/%.pdf') d
WHERE RAW.UW_GUIDELINES.file_name = d.RELATIVE_PATH;

-- Authority Letters
UPDATE RAW.AUTHORITY_LETTERS
SET parsed_content = SNOWFLAKE.CORTEX.PARSE_DOCUMENT(
    @STAGING.SYNTHETIC_DATA,
    RELATIVE_PATH,
    {'mode': 'LAYOUT'}
)
FROM (SELECT RELATIVE_PATH FROM DIRECTORY(@STAGING.SYNTHETIC_DATA)
      WHERE RELATIVE_PATH LIKE '10_authority_letters/%.pdf') d
WHERE RAW.AUTHORITY_LETTERS.file_name = d.RELATIVE_PATH;

-- Rating Sheets (Excel)
UPDATE RAW.RATING_SHEETS
SET parsed_content = SNOWFLAKE.CORTEX.PARSE_DOCUMENT(
    @STAGING.SYNTHETIC_DATA,
    RELATIVE_PATH,
    {'mode': 'LAYOUT'}
)
FROM (SELECT RELATIVE_PATH FROM DIRECTORY(@STAGING.SYNTHETIC_DATA)
      WHERE RELATIVE_PATH LIKE '07_rating_data_sheets/%.xlsx') d
WHERE RAW.RATING_SHEETS.file_name = d.RELATIVE_PATH;

-- SOV Schedules (Excel)
UPDATE RAW.SOV_SCHEDULES
SET parsed_content = SNOWFLAKE.CORTEX.PARSE_DOCUMENT(
    @STAGING.SYNTHETIC_DATA,
    RELATIVE_PATH,
    {'mode': 'LAYOUT'}
)
FROM (SELECT RELATIVE_PATH FROM DIRECTORY(@STAGING.SYNTHETIC_DATA)
      WHERE RELATIVE_PATH LIKE '02_sov_schedules/%.xlsx') d
WHERE RAW.SOV_SCHEDULES.file_name = d.RELATIVE_PATH;
```

---

## Step 6: Verify everything loaded

```sql
-- Final verification
SELECT 'PROMISED_LINES' AS source, COUNT(*) AS rows FROM RAW.PROMISED_LINES
UNION ALL SELECT 'RATING_DATA', COUNT(*) FROM RAW.RATING_DATA
UNION ALL SELECT 'CLAIMS', COUNT(*) FROM RAW.CLAIMS
UNION ALL SELECT 'EMAILS', COUNT(*) FROM RAW.EMAILS
UNION ALL SELECT 'SOV_SCHEDULES', COUNT(*) FROM RAW.SOV_SCHEDULES
UNION ALL SELECT 'APPLICATIONS', COUNT(*) FROM RAW.APPLICATIONS
UNION ALL SELECT 'LOSS_RUNS', COUNT(*) FROM RAW.LOSS_RUNS
UNION ALL SELECT 'RATING_SHEETS', COUNT(*) FROM RAW.RATING_SHEETS
UNION ALL SELECT 'UW_GUIDELINES', COUNT(*) FROM RAW.UW_GUIDELINES
UNION ALL SELECT 'AUTHORITY_LETTERS', COUNT(*) FROM RAW.AUTHORITY_LETTERS
ORDER BY source;

-- Expected output:
-- APPLICATIONS        8
-- AUTHORITY_LETTERS    3
-- CLAIMS             375
-- EMAILS              50
-- LOSS_RUNS           10
-- PROMISED_LINES     750
-- RATING_DATA        426
-- RATING_SHEETS       50
-- SOV_SCHEDULES       12
-- UW_GUIDELINES        3
```

---

## File Format Summary

| Folder | Format | Snowflake Method | RAW Table |
|--------|--------|------------------|-----------|
| 01_submission_emails | .eml | DIRECTORY + text read | RAW.EMAILS |
| 02_sov_schedules | .xlsx | PARSE_DOCUMENT | RAW.SOV_SCHEDULES |
| 03_applications | .pdf | PARSE_DOCUMENT | RAW.APPLICATIONS |
| 04_loss_runs | .pdf | PARSE_DOCUMENT | RAW.LOSS_RUNS |
| 05_promised_lines | .csv | COPY INTO | RAW.PROMISED_LINES |
| 06_rating_data_ers | .csv | COPY INTO | RAW.RATING_DATA |
| 07_rating_data_sheets | .xlsx | PARSE_DOCUMENT | RAW.RATING_SHEETS |
| 08_claims_data | .csv | COPY INTO | RAW.CLAIMS |
| 09_uw_guidelines | .pdf | PARSE_DOCUMENT | RAW.UW_GUIDELINES |
| 10_authority_letters | .pdf | PARSE_DOCUMENT | RAW.AUTHORITY_LETTERS |
