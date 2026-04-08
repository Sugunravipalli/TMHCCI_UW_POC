# TMHCCI Underwriting Intelligence Platform

## Project Overview

POC to compress the insurance quote cycle from ~20 days to 1-2 days using Snowflake-native AI and a Next.js frontend. Built for Tokio Marine HCC International (London).

**Design philosophy**: "An insurance executive doesn't care about dashboards. They care about three things: Can I trust this? Does it save me time? Can I act on it right now?"

## Tech Stack

- **Framework**: Next.js 14.2.35 (App Router) — NOT v15 (requires Node 20+, we use Node 18.20.8)
- **UI**: shadcn/ui v3 (Radix-based) + Tailwind CSS v3 — NOT shadcn v4 or Tailwind v4
- **Charts**: Recharts 2.15.4 (BarChart, PieChart with Cell)
- **Icons**: lucide-react
- **Snowflake**: snowflake-sdk (server-side only via API routes)
- **Fonts**: Geist Sans/Mono (local .woff files)

## Architecture

- **Server Components + API Routes** — Snowflake SDK is server-side only, frontend fetches `/api/*`
- **READ-ONLY** — All API endpoints only SELECT or CALL stored procedures
- **globalThis connection pooling** — `globalThis.__sfConn` survives Next.js dev-mode hot reloads
- **Dual auth** — ExternalBrowser for local dev, OAuth for SPCS production (`/snowflake/session/token`)
- **SPCS-ready** — `output: "standalone"` in next.config.mjs

## Snowflake Connection

- **Account**: qsb28595.us-east-1
- **User**: SUGUN@SQUADRONDATA.COM
- **Role**: SYSADMIN
- **Database**: TMHCCI_UW_POC
- **Warehouse**: TMHCCI_POC_WH (MEDIUM, auto-suspend 300s)
- **Schemas**: PUBLIC, STAGING, RAW, CURATED, SEARCH
- **Key tables (CURATED)**: BROKER_SCORECARD (11), EMAIL_CLASSIFICATION (50), SUBMISSION_COMPLETENESS (30), FACT_RATING (50), FACT_SUBMISSIONS (50), DATA_FLOW (7), BROKER_MASTER_MAP (50), DIM_BROKER (11)
- **Stored proc**: RUN_REGRESSION_TESTS() — 20 tests

## Theme / Branding (Tokio Marine Light + Navy Blue)

Fully converted from dark+red to light+navy blue:

| Token | Value | Usage |
|---|---|---|
| Primary | `#0B3B6E` (navy) | Headings, KPI values, active states |
| Accent | `#1E63B5` (blue) | Buttons, active sidebar links |
| Background | `#F4F6F8` | Page background |
| Card | `#FFFFFF` | Card surfaces, `#E5E7EB` borders |
| Text Primary | `#0F172A` | Body text |
| Text Secondary | `#475569` | Labels, axis ticks |
| Text Muted | `#9CA3AF` | Hints, timestamps |
| Success | `#1BAA73` / emerald-600 | Pass, complete, bound |
| Warning | `#F5A623` / amber-600 | Warnings, NTU, quoted |
| Danger | `#D64545` / red-600 | Fail, declined |
| Sidebar | `#0B3B6E` bg, white text | Navy with `#1E63B5` active |
| Charts | `#0B3B6E`, `#1BAA73`, `#1E63B5`, `#F5A623`, `#7C3AED`, `#0D9488` | Six-color palette |

**Status badge pattern**: `bg-*-50 text-*-700 border-*-200` (light theme)  
**Accent text pattern**: `-600` variants for readability on light backgrounds

CSS uses hsl custom properties consumed via `hsl(var(--...))` in tailwind.config.ts.

## Pages (5)

1. **/** — Command Center: KPIs, submission volume chart, class-of-business pie chart, pipeline health
2. **/inbox** — Smart Inbox: AI-classified emails with confidence scores, search, email detail view
3. **/brokers** — Broker Analytics: Scorecard table, broker detail drill-down with metrics
4. **/quality** — Data Quality: Pipeline lineage, quality metrics, live regression test runner (20 tests)
5. **/audit** — Audit Trail: Submission timeline, per-step audit with execution time, follow-up text

## API Routes (12)

All under `app/api/`:
- `command-center/stats` — Dashboard KPIs + chart data
- `emails` — Email list with classification
- `emails/[id]` — Single email detail
- `emails/[id]/audit` — Audit trail for an email
- `brokers` — Broker scorecard list
- `brokers/[id]` — Single broker detail
- `completeness` — Submission completeness scores
- `completeness/[id]/followup` — Follow-up generation
- `quality/metrics` — Quality metric summary
- `quality/regression` — Run regression tests (calls RUN_REGRESSION_TESTS())
- `quality/lineage` — Data flow lineage
- `deliverables` — Deliverable checklist status

## Key Components

- `NavSidebar.tsx` — Navy sidebar with nav links
- `KPICard.tsx` — Token-based KPI display cards
- `StatusBadge.tsx` — Color-coded status pills
- `FormatUtils.ts` — Grade/classification/decision color utilities
- `AuditTimeline.tsx` — Step-by-step audit visualization
- `DataLineageFlow.tsx` — Pipeline lineage diagram
- `RegressionResults.tsx` — Test results with pass/fail summary
- `DeliverableChecklist.tsx` — Deliverable status list

## Data Engineering (Completed)

- **D1-D5 deliverables**: Email classification, submission completeness, broker scoring, rating analysis, data lineage
- **A1-A3 deliverables**: Cortex AI classification, document intelligence, completeness scoring
- **20/20 regression tests passing**

## Important Patterns

- Colors use hsl in CSS vars, NOT oklch (incompatible with Tailwind v3)
- Recharts Tooltip formatter params typed as `any` with eslint-disable
- AuditStep interface uses explicit optional props (not unknown)
- `next.config.mjs` uses `experimental.serverComponentsExternalPackages` (Next.js 14 syntax)
