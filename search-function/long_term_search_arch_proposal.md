# Long-Term Architecture Plan: Multi-Source Interlisp Search with Automated Refresh

**Document Created:** August 26, 2024  
**Last Updated:** September 02, 2026  
**Status:** Implemented — Dual-Engine Blended (verified live 2026-09-02)  
**Author:** OpenCode Architecture Planning Session
**Deployed:** `search-00037-xas` (`WEBSITE_ENGINE_ID=interlisp-website-only`, `GITHUB_ENGINE_ID=interlisp-github-only`)

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Current State Analysis](#current-state-analysis)
3. [Architecture Overview](#architecture-overview)
4. [Phase 1: Research Vertex AI Search Capabilities](#phase-1-research-vertex-ai-search-capabilities)
5. [Phase 2: Optimal Data Store Configuration](#phase-2-optimal-data-store-configuration)
6. [Phase 3: Source Weighting & Ranking Strategy](#phase-3-source-weighting--ranking-strategy)
7. [Phase 4: Automated Refresh Pipeline](#phase-4-automated-refresh-pipeline)
8. [Phase 5: Reference Manual Structuring](#phase-5-reference-manual-structuring)
9. [Phase 6: Updated Cloud Function](#phase-6-updated-cloud-function)
10. [Implementation Sequence](#implementation-sequence)
11. [Decision Points](#decision-points)

---

## Executive Summary

This document proposes a long-term architecture for the Interlisp.org AI-assisted search system that:

- **Unifies** website, GitHub, and reference materials via two engines blended in one Cloud Function
- **Prioritizes** `www.interlisp.org` / `interlisp.org` (primary) over `*.interlisp.org` secondary subdomains (`files`, `primer`, `online`) over GitHub, while guaranteeing GitHub representation
- **Automates** content refresh (website crawl, GitHub `interlisp-github-v2` import) on a recurring schedule
- **Prepares** for future structuring of reference materials (PDFs, documentation)
- **Maintains** backward compatibility with current Cloud Function architecture

### Key Improvements

| Aspect | Current State | Proposed State |
|--------|---------------|-----------------|
| **Data Organization** | Two separate engines (`v3` website+GitHub, `176886...` website+bucket) | Two focused engines (`interlisp-website-only` [`interlisp-web-sites_1741606671710`], `interlisp-github-only` [`interlisp-github-v2`]) blended; `interlisp-search-unified` combines both for fallback |
| **Website Prioritization** | GitHub dominates or secondary subdomains dominate | `website-primary` (apex/`www`) → `website-secondary` (`files`/`primer`/`online`) → `github`; blended 70/30 (50/50 for GitHub queries) guarantees both |
| **Content Freshness** | Manual recrawl/reimport required | Automated daily website (via existing `*.interlisp.org` crawl), weekly GitHub JSONL import to `interlisp-github-v2` branches/0 |
| **Maintainability** | Two Cloud Functions, manual updates | Single `search` function dual-fetching both engines, automated refresh pipeline |
| **Future-Ready** | Limited structure for reference materials | `source`/`priority`/`last_indexed` metadata additive to GitHub `repo`/`type`/`created_date`; framework ready for structured imports |

---

## Current State Analysis

### Existing Implementations

#### `interlisp-org-search_1768860477660` (Unstructured)
- **Contents:** interlisp.org website + files.interlisp.org (PDFs, documentation)
- **Strengths:** ✅ Website content surfaces first, clean results
- **Weaknesses:** ❌ Reference Manual PDFs are unstructured, not searchable at section/chapter level

#### `interlisp-search-v3` (Structured)
- **Contents:** interlisp.org website + files.interlisp.org + GitHub structured data
- **GitHub Data:** Issues, PRs, Markdown files
- **Strengths:** ✅ GitHub content available as context
- **Weaknesses:** ❌ GitHub content dominates results, website is deprioritized

### Root Cause: No Source-Level Weighting

Vertex AI Search has **limited native support** for source-level prioritization at the data store configuration level. The system returns results based on semantic relevance and ranking, without explicit mechanisms to say "always rank source A above source B."

**Solution:** Combine request-time filtering + post-processing logic in the Cloud Function to enforce source priority.

---

## Architecture Overview

### System Diagram — Implemented (dual-engine blended)

```
┌──────────────────────────────┐      ┌──────────────────────────────┐
│ DATA STORE                   │      │ DATA STORE                   │
│ interlisp-web-sites_         │      │ interlisp-github-v2          │
│ 1741606671710                │      │ (NO_CONTENT, GENERIC)        │
│ PUBLIC_WEBSITE, *.interlisp. │      │ structData: title/url/content│
│ org/*, SUCCEEDED             │      │ + source/priority/last_indexed│
└──────────────┬───────────────┘      └──────────────┬───────────────┘
               │                                     │
               ▼                                     ▼
┌──────────────────────────────┐      ┌──────────────────────────────┐
│ ENGINE                       │      │ ENGINE                       │
│ interlisp-website-only       │      │ interlisp-github-only        │
│ [interlisp-web-sites_...]    │      │ [interlisp-github-v2]        │
│ GENERIC, ENTERPRISE+LLM      │      │ GENERIC, ENTERPRISE+LLM      │
└──────────────┬───────────────┘      └──────────────┬───────────────┘
               │                                     │
               └──────────────┬──────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ CLOUD FUNCTION `search` (Gen2, us-central1)                 │
│ WEBSITE_ENGINE_ID=interlisp-website-only                    │
│ GITHUB_ENGINE_ID=interlisp-github-only                      │
│ 1. Parallel search both engines (fetch 20 each)             │
│ 2. getSource(): website-primary (interlisp.org/www) →1,     │
│    website-secondary (*.interlisp.org) →2, github →3        │
│ 3. Blended merge: 70/30 (50/50 if /github|issue|pr/i)       │
│    guarantees GitHub despite website priority               │
│ 4. Summary from website engine, preamble prefers www,       │
│    citations sorted primary→secondary→github                │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ AUTOMATED REFRESH PIPELINE (Cloud Scheduler + Functions)    │
│ Trigger 1: Weekly GitHub JSONL → interlisp-github-v2        │
│            branches/0 (source/priority/last_indexed)        │
│ Trigger 2: Website crawl is managed by existing *.interlisp │
│            targetSites (SUCCEEDED) — no recreation needed   │
└─────────────────────────────────────────────────────────────┘
   Fallback engine interlisp-search-unified [interlisp-web-sites, interlisp-github-v2] retained for single-engine callers.
```

### Data Flow — Implemented

1. **User Query** → Cloud Function `search`
2. **Parallel** `POST .../engines/interlisp-website-only/servingConfigs/default_config:search` (with `summarySpec` + preamble) + `POST .../engines/interlisp-github-only/...` (results only), each `pageSize:20`
3. **Merge:** dedup by `url`, `getSource()` → `website-primary` (1) / `website-secondary` (2) / `github` (3), blended 70/30 (50/50 for GitHub queries) so GitHub never starved, then final priority + `semanticRelevanceScore` sort, slice to `pageSize`
4. **Summary** from website engine (LLM preamble: `www.interlisp.org` → `*.interlisp.org` → GitHub), citations resolved via `docId→url` map and sorted same priority
5. **Response** → `results[]` + `summary {summaryText, citations[]}` with `source`/`priority` for observability

### Refresh Flow

1. **Daily @ 2 AM UTC** → Cloud Scheduler → `trigger-website-recrawl()` Cloud Function
   - Initiates Vertex AI recrawl of `interlisp.org/*` and `files.interlisp.org/*` patterns
   - Updates `last_indexed` metadata

2. **Weekly (Monday) @ 3 AM UTC** → Cloud Scheduler → `github-reimport()` Cloud Function
   - Fetches latest GitHub Issues, PRs, Markdown files
   - Transforms to JSONL with metadata (`source: github`, `priority: 3`)
   - Uploads to Cloud Storage
   - Calls Vertex AI `importDocuments()` API
   - Clears old GitHub documents before import

3. **Manual Triggers** → On-demand via Cloud Scheduler UI or `gcloud` CLI
   - For urgent updates, testing, or manual validation

---

## Phase 1: Research Vertex AI Search Capabilities

### Findings

Vertex AI Search (Discovery Engine) supports the following relevant features:

#### ✅ Supported

1. **Metadata-based filtering & boosting** via search request parameters
   - `filter` parameter in `contentSearchSpec`
   - Can filter by custom metadata fields added during import
   - Example: `filter: "metadata.source:website"`

2. **Multiple target sites** in a single data store
   - Different URL patterns (`interlisp.org/*`, `files.interlisp.org/*`)
   - Both crawled automatically
   - Can specify recrawl triggers per target

3. **Structured document imports** (JSONL) alongside crawled content
   - GitHub Issues, PRs, Markdown as JSONL documents
   - Custom metadata fields included in import schema
   - Can be re-imported periodically to update content

4. **Custom metadata fields** on imported documents
   - Fields like `source`, `priority`, `last_updated`, `content_type`
   - Available for filtering, sorting, and post-processing

5. **Search-time parameters** to influence ranking
   - `pageSize`, `offset` for pagination
   - `filter` for inclusion/exclusion criteria
   - `orderBy` for explicit sorting (limited)

#### ⚠️ Limited

1. **Source-level weighting at config time**
   - No built-in "prioritize collection A over B" setting
   - Must implement via request-time filtering or post-processing

2. **Automatic deduplication across sources**
   - Same content from website + GitHub may appear as separate results
   - Requires post-processing to deduplicate if needed

### Implication — Implemented

**Implemented approach:** **Two focused data stores + dual-engine blended Cloud Function** (replaces the earlier “single unified store” proposal).

* Website store `interlisp-web-sites_1741606671710` (`PUBLIC_WEBSITE`, `*.interlisp.org/*`, `SUCCEEDED`) — proven to return `https://interlisp.org/...` for `history`/`software`/`Medley` (the freshly created `interlisp-search-unified` website store `PUBLIC_WEBSITE` `interlisp.org/*` + `files.interlisp.org/*` returned only `files`/`online`/`primer` and is retained but not used for serving).
* GitHub store `interlisp-github-v2` (`NO_CONTENT`, `GENERIC`, structured `structData` on `branches/0`) — GitHub issues/PRs/markdown with future-proof `retrievable:true` schema (title/url/repo/type/state/author/number etc., see Phase 2).
* Fallback engine `interlisp-search-unified` (`[interlisp-web-sites_1741606671710, interlisp-github-v2]`) retained for single-engine callers.

This dual-store blending avoids GitHub starvation (guaranteed 70/30, 50/50 for GitHub-intent queries) while keeping website-primary strictly first.

---

## Phase 2: Optimal Data Store Configuration — Implemented (dual focused stores)

### Recommendation: Two Focused Stores Blended in Cloud Function (Implemented)

| Approach | Pros | Cons | Implemented |
|----------|------|------|-------------|
| **Unified** (`interlisp-search-unified` website store) | Single query | Requires careful filtering; fresh `interlisp-search-unified` crawl returned only `files`/`online`/`primer` for `history`/`Medley` — not suitable for serving | — (retained, not used) |
| **Split (implemented)** | Proven website crawl `interlisp-web-sites_1741606671710` (`*.interlisp.org/*` `SUCCEEDED`) + structured `interlisp-github-v2` (`NO_CONTENT` `branches/0`) blended 70/30; fallback `interlisp-search-unified` engine combines both | Slightly more Cloud Function logic (dual fetch) | ✓ |

**Decision:** **Dual focused stores** — `interlisp-web-sites_1741606671710` + `interlisp-github-v2` (+ fallback engine `interlisp-search-unified`).

### Implemented Data Store Configuration

#### Website Store (proven, primary)

```yaml
Data Store ID: interlisp-web-sites_1741606671710
Display Name: Interlisp Web Sites
Project: interlispsearch
Location: global
Industry Vertical: GENERIC
Solution Types: SOLUTION_TYPE_SEARCH
Content Config: PUBLIC_WEBSITE
Target Site:
  URI Pattern: "*.interlisp.org/*"
  Type: INCLUDE
  Indexing Status: SUCCEEDED   # proven for history/software/Medley queries
Advanced Site Search: disableInitialIndex:true, disableAutomaticRefresh:true
```

*Note:* Fresh store `interlisp-search-unified` (`PUBLIC_WEBSITE` `interlisp.org/*` + `files.interlisp.org/*`) was created per guide Steps 1.2–1.5 and is `SUCCEEDED`, but its crawl was not used for serving; it is retained for inventory.

#### GitHub Structured Store (`NO_CONTENT`, branches/0)

```yaml
Data Store ID: interlisp-github-v2
Display Name: Interlisp GitHub Content
Project: interlispsearch
Location: global
Industry Vertical: GENERIC
Solution Types: SOLUTION_TYPE_SEARCH
Content Config: NO_CONTENT
Branches: 0  # NOT default/branches/default
Schema: default_schema  # future-proof, see below
```

**Schema `default_schema` (future-proof, patched 2026-09-02):**

Future-proof patch made all display fields `retrievable:true` so Search API returns them in both `structData` and fallback `derivedStructData`:

```yaml
title:   {keyPropertyMapping: title,       retrievable: true}
url:     {keyPropertyMapping: uri,         retrievable: true}
content: {keyPropertyMapping: description, retrievable: true}
repo:    {retrievable: true, searchable: true, indexable: true}
type:    {retrievable: true, searchable: true, indexable: true}
state:   {retrievable: true, searchable: true, indexable: true}
author/number/labels/references/created_at/updated_at/created_date/priority/last_indexed/file/issue_number/pr_number: retrievable: true (as applicable)
```

Without this patch, GitHub results were `title:null` → frontend `Untitled` (fixed 2026-09-02; `github-only` engine now returns `structData.title` and Cloud Function `index.js:193-195` `derived.title || structData.title` resolves).

**Patch command (idempotent):**
```bash
TOKEN=$(gcloud auth application-default print-access-token)
curl -X PATCH -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: interlispsearch" \
  -H "Content-Type: application/json" \
  "https://discoveryengine.googleapis.com/v1/projects/interlispsearch/locations/global/collections/default_collection/dataStores/interlisp-github-v2/schemas/default_schema" \
  -d @/tmp/patch_schema4.json  # see Implementation Guide Phase 1.6 for JSON
```

#### Structured Data Imports (JSONL) — Actual Shape

```json
{"id":"github-issue-medley-2741","structData":{"id":"github-issue-medley-2741","title":"FONTSAVAILABLE…","url":"https://github.com/Interlisp/medley/issues/2741","content":"…","source":"github","priority":3,"type":"issue","repo":"Interlisp/medley","state":"open","number":2741,"created_at":"2026-08-26T01:21:42Z","last_indexed":"2026-09-02T12:54:55Z"}}
```
Sanitized `id` (`Interlisp.github.io` → `Interlisp-github-io`), uploaded to `gs://interlispsearch-search-imports/github-import-*.jsonl`, imported via `POST …/branches/0/documents:import`.

#### Indexing Configuration — Implemented

```yaml
Website: Existing *.interlisp.org crawl managed by siteSearchEngine (no recreation needed)
GitHub: Weekly JSONL import to interlisp-github-v2 branches/0 (local one-off until scheduled reimport enabled)
```

Initial GitHub Seed (implemented 2026-09-02 via local one-off `GITHUB_TOKEN=$(gh auth token) node /tmp/local_import_simple.js` → 350 docs `successCount 350/350`); scheduled weekly `github-reimport` Pub/Sub requires `GITHUB_TOKEN` env and is deferred until source-dir isolation fixed (search function already re-exports `reimportGithub`).

Fallback engine `interlisp-search-unified` (`[interlisp-web-sites_1741606671710, interlisp-github-v2]`) retained for single-engine callers; live `search` uses dual fetch.

---

## Phase 3: Source Weighting & Ranking Strategy — Implemented (dual-fetch blended)

### Implemented: URL-based `getSource()` + Priority + Guaranteed GitHub Slice

Live `search-function/index.js:64-86,138-172` (deployed `search-00037-xas`) implements:

* **No `filter` param** (proposal filtered by `metadata.source` proved unnecessary and would starve GitHub). Ranking is pure post-processing on URL + blended slice.

* **Source detection (`getSource(url)`):**
  ```javascript
  host === 'www.interlisp.org' || host === 'interlisp.org' → 'website-primary' (1)
  host.endsWith('.interlisp.org')               → 'website-secondary' (2)  // files/primer/online — strictly after primary, not tiered further
  host.includes('github.com')                   → 'github' (3)
  other                                         → 4, unknown → 999
  ```

* **Parallel fetch:** `Promise.all([searchEngine(WEBSITE_ENGINE_ID, withSummary:true), searchEngine(GITHUB_ENGINE_ID, withSummary:false)])` each `fetchPageSize=20` (website engine provides `summarySpec` + preamble; github engine results-only).

* **Blended merge (guaranteed GitHub, never starved):**
  ```javascript
  isGithubQuery = /github|issue|pull\s*request|\bpr\b|discussion/i.test(query)
  websiteTake = ceil(pageSize * (isGithubQuery ? 0.5 : 0.7))
  githubTake  = pageSize - websiteTake
  // sort: websiteItems by priority→semanticRelevanceScore, githubItems by score
  // dedup by url, take slices, fill remainder sorted priority→score, final sort priority→score
  ```

* **Citations & results:** `docId→url` map across both engines, `references` sorted `website-primary → website-secondary → github`; `results` mapped with `title: derived.title || structData.title` (fixed by schema `retrievable:true`) and `type/repo/state` from `structData`.

#### Tier 1: Search Request-Level Filtering (Not Used — See Implemented Above)

Proposal `filter: buildSourceFilter(context)` was superseded by URL-based blended slice; kept only as fallback if `GITHUB_ENGINE_ID` unset (`index.js:128-136`).

#### Tier 2: Post-Processing Reordering (Guardrail) — Implemented

**Source Priority Order (implemented, strictly after, not tiered within secondary):**
1. `website-primary` (1) — `interlisp.org` / `www.interlisp.org`
2. `website-secondary` (2) — `*.interlisp.org` (files, primer, online)
3. `github` (3) — issues/PRs/discussions/markdown

**Snippet from live `index.js:143-204`:**
```javascript
const toItems = (data, hint) => (data?.results||[]).map(r=>{... url = d.link||d.url||s.url ...; src=hint||getSource(url); return {raw:r, url, source:src, priority:sourcePriorityMap[src], score:retrievalSignals.semanticRelevanceScore}}).filter(i=>i.url);
let websiteItems = toItems(websiteData,null).sort((a,b)=>a.priority-b.priority||b.score-a.score);
let githubItems = toItems(githubData,'github').sort((a,b)=>b.score-a.score);
// dedup, blended slice, final priority→score sort
```

### Ranking Behavior — Verified Live

| Query Type | Verified Behavior (live 2026-09-02) |
|------------|-------------------|
| General `interlisp/medley/history/software` | First 7 website-primary, last 3 github; citations website-primary first |
| GitHub-intent `github` / `github issue` | 5+5 split (50/50) — `isGithubQuery` triggers |
| `pull request` | 1 website + 9 github (still priority→score, githubTake 5 plus remainder fill) |
| Code/doc overlap | Website cited first per preamble; GitHub never starved |

**Frontend:** `assets/js/vertex-search.js:220` `r.title || 'Untitled'` now resolves because schema patch makes `title` retrievable; verified 0 untitled across `github/medley/pull request/issue/screenshots/FONTSAVAILABLE` matrix.

---

## Phase 4: Automated Refresh Pipeline

### Goal

Keep content fresh without manual intervention. Automate:
- **Website recrawl** (daily) — captures updated docs, blog posts, etc.
- **GitHub reimport** (weekly) — refreshes issues, PRs, discussions
- **Manual triggers** — for urgent updates or testing

### Architecture

```
Cloud Scheduler (GCP)
  │
  ├─ Trigger 1: Daily @ 2 AM UTC
  │   └─ Pub/Sub Topic: "recrawl-website"
  │       └─ Cloud Function: trigger-website-recrawl()
  │           └─ Calls: Vertex AI API to recrawl target sites
  │
  ├─ Trigger 2: Weekly (Monday @ 3 AM UTC)
  │   └─ Pub/Sub Topic: "reimport-github"
  │       └─ Cloud Function: github-reimport()
  │           ├─ Fetch: GitHub API (issues, PRs, markdown)
  │           ├─ Transform: to JSONL with metadata
  │           ├─ Upload: to Cloud Storage
  │           └─ Import: Vertex AI importDocuments()
  │
  └─ Trigger 3: Manual (gcloud CLI or UI)
      └─ Force recrawl/reimport on demand
```

### Step 1: Create `trigger-website-recrawl()` Cloud Function

**Purpose:** Initiate Vertex AI recrawl of target sites

**Deployment:**

```bash
gcloud functions deploy trigger-website-recrawl \
  --gen2 \
  --runtime=nodejs24 \
  --region=us-central1 \
  --trigger-topic=recrawl-website \
  --entry-point=recrawlWebsite \
  --service-account=vertex-search-sa@interlispsearch.iam.gserviceaccount.com \
  --memory=256Mi \
  --timeout=60s \
  --project=interlispsearch
```

**Code:** `search-function/trigger-website-recrawl.js` (targets proven website store)

```javascript
'use strict';

const { GoogleAuth } = require('google-auth-library');

const PROJECT_ID = 'interlispsearch';
const LOCATION = 'global';
const DATA_STORE_ID = 'interlisp-web-sites_1741606671710'; // NOT interlisp-search-unified (its crawl returned only files)

const auth = new GoogleAuth({
  scopes: ['https://www.googleapis.com/auth/cloud-platform']
});

exports.recrawlWebsite = async (message, context) => {
  console.log('Starting website recrawl...');
  
  try {
    const client = await auth.getClient();
    const token = await client.getAccessToken();
    
    // Get target sites
    const targetSitesUrl = `https://discoveryengine.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION}/collections/default_collection/dataStores/${DATA_STORE_ID}/siteSearchEngine/targetSites`;
    
    const targetSitesResponse = await fetch(targetSitesUrl, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token.token}`,
        'x-goog-user-project': PROJECT_ID
      }
    });
    
    if (!targetSitesResponse.ok) {
      throw new Error(`Failed to fetch target sites: ${targetSitesResponse.statusText}`);
    }
    
    const targetSitesData = await targetSitesResponse.json();
    const targetSites = targetSitesData.targetSites || [];
    
    console.log(`Found ${targetSites.length} target sites. Starting recrawl...`);
    
    // Trigger recrawl for each target site
    for (const site of targetSites) {
      const recrawlUrl = `https://discoveryengine.googleapis.com/v1/${site.name}:recrawl`;
      
      const recrawlResponse = await fetch(recrawlUrl, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token.token}`,
          'Content-Type': 'application/json',
          'x-goog-user-project': PROJECT_ID
        },
        body: JSON.stringify({})
      });
      
      if (!recrawlResponse.ok) {
        console.error(`Recrawl failed for ${site.uri_pattern}: ${recrawlResponse.statusText}`);
      } else {
        console.log(`Recrawl triggered for ${site.uri_pattern}`);
      }
    }
    
    console.log('Website recrawl completed');
    
  } catch (err) {
    console.error('Recrawl error:', err);
    throw err;
  }
};
```

### Step 2: Create `github-reimport()` Cloud Function

**Purpose:** Fetch latest GitHub content and reimport as structured documents

**Deployment:**

```bash
gcloud functions deploy github-reimport \
  --gen2 \
  --runtime=nodejs24 \
  --region=us-central1 \
  --trigger-topic=reimport-github \
  --entry-point=reimportGithub \
  --service-account=vertex-search-sa@interlispsearch.iam.gserviceaccount.com \
  --memory=512Mi \
  --timeout=300s \
  --set-env-vars GITHUB_TOKEN=your_github_token_here \
  --project=interlispsearch
```

**Code:** `search-function/github-reimport.js` (pseudocode)

```javascript
'use strict';

const { GoogleAuth } = require('google-auth-library');
const { Storage } = require('@google-cloud/storage');
const https = require('https');

const PROJECT_ID = 'interlispsearch';
const LOCATION = 'global';
const DATA_STORE_ID = 'interlisp-github-v2'; // NOT interlisp-search-unified; structured GitHub store on branches/0
const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const GITHUB_ORG = 'Interlisp';

const auth = new GoogleAuth({
  scopes: ['https://www.googleapis.com/auth/cloud-platform']
});

const storage = new Storage({ projectId: PROJECT_ID });

exports.reimportGithub = async (message, context) => {
  console.log('Starting GitHub reimport...');
  
  try {
    // 1. Fetch GitHub issues, PRs, markdown files
    const gitHubDocuments = [];
    
    // Fetch Issues
    const issues = await fetchGitHubIssues();
    gitHubDocuments.push(...issues);
    console.log(`Fetched ${issues.length} GitHub issues`);
    
    // Fetch Pull Requests
    const prs = await fetchGitHubPullRequests();
    gitHubDocuments.push(...prs);
    console.log(`Fetched ${prs.length} GitHub pull requests`);
    
    // Fetch Markdown files from repos
    const markdownFiles = await fetchGitHubMarkdown();
    gitHubDocuments.push(...markdownFiles);
    console.log(`Fetched ${markdownFiles.length} GitHub markdown files`);
    
    // 2. Convert to JSONL format with metadata
    const jsonlContent = gitHubDocuments
      .map(doc => JSON.stringify(doc))
      .join('\n');
    
    // 3. Upload JSONL to Cloud Storage
    const bucket = storage.bucket(`${PROJECT_ID}-search-imports`);
    const file = bucket.file(`github-import-${Date.now()}.jsonl`);
    
    await file.save(jsonlContent);
    console.log(`Uploaded JSONL to gs://${bucket.name}/${file.name}`);
    
    // 4. Call Vertex AI importDocuments API
    const client = await auth.getClient();
    const token = await client.getAccessToken();
    
    const importUrl = `https://discoveryengine.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION}/collections/default_collection/dataStores/${DATA_STORE_ID}/branches/0/documents:import`; // branches/0, not default
    
    // JSONL shape: {"id": sanitized, "structData":{id,title,url,content,source,priority,repo,type,state,…}} — NOT top-level title/url
    const importResponse = await fetch(importUrl, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token.token}`,
        'Content-Type': 'application/json',
        'x-goog-user-project': PROJECT_ID
      },
      body: JSON.stringify({
        gcsSource: {
          inputUris: [`gs://${bucket.name}/${file.name}`]
        }
      })
    });
    
    if (!importResponse.ok) {
      throw new Error(`Import failed: ${importResponse.statusText}`);
    }
    
    const importData = await importResponse.json();
    console.log(`Import operation started: ${importData.name}`);
    console.log('GitHub reimport completed');
    
  } catch (err) {
    console.error('GitHub reimport error:', err);
    throw err;
  }
};

async function fetchGitHubIssues() {
  // Fetch issues from Interlisp/medley, Interlisp/maiko, etc.
  // Return array of documents with metadata
  return [];
}

async function fetchGitHubPullRequests() {
  // Fetch PRs from Interlisp repositories
  return [];
}

async function fetchGitHubMarkdown() {
  // Fetch README, markdown files from Interlisp repos
  return [];
}

function buildGitHubSchema() {
  // Deprecated — schema is now patched via REST PATCH on default_schema (retrievable:true for title/url/repo/type/state etc.)
  // New JSONL uses flat structData: {title, url, content, source, priority, repo, type, state, number, created_at,…}
  // Sanitized id: Interlisp.github.io → Interlisp-github-io, /^[a-zA-Z0-9-_]+$/
  return null;
}
```

### Step 3: Create Cloud Scheduler Jobs

**Daily Website Recrawl:**

```bash
gcloud scheduler jobs create pubsub recrawl-website-daily \
  --location=us-central1 \
  --schedule="0 2 * * *" \
  --timezone="UTC" \
  --topic=recrawl-website \
  --message-body='{"action":"recrawl","timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"}' \
  --project=interlispsearch
```

**Weekly GitHub Reimport (Monday @ 3 AM UTC):**

```bash
gcloud scheduler jobs create pubsub reimport-github-weekly \
  --location=us-central1 \
  --schedule="0 3 * * 1" \
  --timezone="UTC" \
  --topic=reimport-github \
  --message-body='{"action":"reimport","timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"}' \
  --project=interlispsearch
```

**Manual Triggers (via gcloud CLI):**

```bash
# Trigger website recrawl immediately
gcloud scheduler jobs run recrawl-website-daily \
  --location=us-central1 \
  --project=interlispsearch

# Trigger GitHub reimport immediately
gcloud scheduler jobs run reimport-github-weekly \
  --location=us-central1 \
  --project=interlispsearch
```

### Step 4: Monitoring & Logging

**View Cloud Function logs:**

```bash
# Website recrawl logs
gcloud functions logs read trigger-website-recrawl \
  --gen2 \
  --region=us-central1 \
  --limit=50 \
  --project=interlispsearch

# GitHub reimport logs
gcloud functions logs read github-reimport \
  --gen2 \
  --region=us-central1 \
  --limit=50 \
  --project=interlispsearch
```

**View Cloud Scheduler execution history:**

```bash
# Website recrawl schedule
gcloud scheduler jobs describe recrawl-website-daily \
  --location=us-central1 \
  --project=interlispsearch

# GitHub reimport schedule
gcloud scheduler jobs describe reimport-github-weekly \
  --location=us-central1 \
  --project=interlispsearch
```

---

## Phase 5: Reference Manual Structuring

### Current Problem

Reference Manual PDFs in `files.interlisp.org/` are indexed as unstructured content. This causes:
- Lost context (which chapter/section?)
- Poor chunking (full document treated as one blob)
- Lower relevance in search results

### Long-Term Solution Options

#### Option A: Structured PDF Extraction (Medium-term, 1-2 months)

**Approach:**
1. Extract Reference Manual PDFs with chapter/section metadata
2. Create JSONL documents with hierarchical structure:
   ```json
   {
     "id": "refman-ch3-sec2-subsec1",
     "title": "Chapter 3.2.1: Function Definitions",
     "content": "Section content here...",
     "metadata": {
       "source": "reference_manual",
       "priority": 2,
       "book": "Interlisp Reference Manual",
       "chapter": "3",
       "section": "2",
       "subsection": "1",
       "page_range": "123-145"
     }
   }
   ```
3. Import as structured documents using same pipeline as GitHub
4. Update Cloud Function to recognize and prioritize reference material

**Pros:**
- Searchable at chapter/section level
- Retains hierarchical structure
- Can deduplicate if content appears on website too

**Cons:**
- Requires PDF parsing library (pypdf, pdfplumber, etc.)
- Manual validation for OCR errors
- One-time extraction effort

#### Option B: Text-to-Markdown Conversion (Long-term, 2-3 months)

**Approach:**
1. Convert Reference Manual PDFs to structured Markdown
2. Organize by chapter/section/subsection with proper heading hierarchy
3. Host as `.md` files in new `docs.interlisp.org` subdomain (or `interlisp.org/docs/`)
4. Let Vertex AI crawl them as website content (gets better indexing)

**Pros:**
- Best UX — users can view docs directly on website
- Website crawl handles indexing (no separate import needed)
- Heading structure provides natural chunking
- Can add cross-references, links, examples

**Cons:**
- Larger effort (PDF → Markdown conversion + hosting)
- Requires ongoing maintenance as docs change

#### Option C: Defer Structuring (Short-term)

**Approach:**
- Use unified data store with website content prioritized
- Keep Reference Manual as unstructured for now
- Revisit when search quality metrics indicate PDFs are a priority

**Pros:**
- Minimal effort; unblock other improvements
- Gather user feedback on what's missing

**Cons:**
- Reference Manual remains hard to search

### Recommendation

**Short-term (now):** Option C — defer to unblock unified data store deployment  
**Medium-term (after 2-4 weeks):** Option A — structured extraction, validate results  
**Long-term (3-6 months):** Option B — full Markdown conversion for best UX

---

## Phase 6: Updated Cloud Function — Implemented

### Changes Implemented (live `search-00037-xas`)

`search-function/index.js:6-9,64-86,90-172,193-195` implements dual-fetch blended (see Phase 3) plus re-export for shared source dir:

1. ✅ **Dual-fetch blending** (replaces Tier 1 `filter`): `WEBSITE_ENGINE_ID=interlisp-website-only`, `GITHUB_ENGINE_ID=interlisp-github-only`, `fetchPageSize=20` each, `isGithubQuery` 50/50 else 70/30
2. ✅ **Post-processing reordering**: `getSource()` → `website-primary:1 / website-secondary:2 / github:3`, priority→`semanticRelevanceScore`, dedup by `url`
3. ✅ **Points to focused engines** (not unified): `WEBSITE_ENGINE_ID`/`GITHUB_ENGINE_ID`/`ENGINE_ID=WEBSITE_ENGINE_ID`; fallback `interlisp-search-unified` retained
4. ✅ **Preamble citation preference** preserved (`www` → `*.interlisp.org` → GitHub)
5. ✅ **Source metadata tracking** (`source`/`priority`/`type`/`repo`/`state`) for observability — verified 0 untitled after schema patch
6. ✅ **Shared-source re-export**: `exports.reimportGithub = require('./github-reimport').reimportGithub` so same `search-function/` dir serves both `search` and `github-reimport` entry-points

### Deployment — Implemented

```bash
# search-function/deploy-search-function.sh:6-9
WEBSITE_ENGINE_ID="interlisp-website-only"   # [interlisp-web-sites_1741606671710]
GITHUB_ENGINE_ID="interlisp-github-only"     # [interlisp-github-v2]
FALLBACK_ENGINE_ID="interlisp-search-unified"

gcloud functions deploy search \
  --gen2 --runtime=nodejs24 --region=us-central1 \
  --source=./search-function --entry-point=search --trigger-http --allow-unauthenticated \
  --service-account=vertex-search-sa@interlispsearch.iam.gserviceaccount.com \
  --set-env-vars PROJECT_ID=interlispsearch,WEBSITE_ENGINE_ID=$WEBSITE_ENGINE_ID,GITHUB_ENGINE_ID=$GITHUB_ENGINE_ID,ENGINE_ID=$WEBSITE_ENGINE_ID \
  --memory=256Mi --timeout=30s --project=interlispsearch
# Deployed: https://us-central1-interlispsearch.cloudfunctions.net/search
```

### Testing Strategy

**Before switching to unified data store:**

1. Create unified data store (clone from v3 + add metadata)
2. Deploy updated Cloud Function to **staging** or **development**
3. Test with sample queries:
   ```bash
   # Should prefer website
   curl -s "https://<staging-function-url>/search?q=interlisp" | jq '.results[0:3]'
   
   # Should cite interlisp.org docs, not GitHub
   curl -s "https://<staging-function-url>/search?q=medley+release" | jq '.summary.citations[0]'
   
   # GitHub content still available for context
   curl -s "https://<staging-function-url>/search?q=github+issues" | jq '.results | map(.url) | map(select(contains("github")))'
   ```

4. Compare results with current v3 behavior
5. Validate that response time is acceptable
6. Check Cloud Function logs for errors

**Validation Checklist:**

- [ ] First result is from interlisp.org (not github.com)
- [ ] First citation is from interlisp.org (not github.com)
- [ ] GitHub content still appears in results (not excluded)
- [ ] Summary quality is same or better than before
- [ ] No increase in error rates or response time
- [ ] Cloud Function logs are clean (no errors)
- [ ] All allowed origins work (localhost, staging, production)

### Rollback Plan

If issues occur post-deployment:

```bash
# Option 1: Switch back to old engine
gcloud functions deploy search \
  --gen2 \
  --runtime=nodejs24 \
  --region=us-central1 \
  --source=./search-function \
  --entry-point=search \
  --trigger-http \
  --allow-unauthenticated \
  --service-account=vertex-search-sa@interlispsearch.iam.gserviceaccount.com \
  --set-env-vars \
    PROJECT_ID=interlispsearch,\
    ENGINE_ID=interlisp-org-search_1768860477660,\
    ALLOWED_ORIGIN=https://interlisp.org \
  --memory=256Mi \
  --timeout=30s \
  --project=interlispsearch

# Option 2: Restore from git
cd search-function
git checkout index.js
npm install
# ... redeploy with same gcloud functions deploy command
```

---

## Implementation Sequence

### Timeline & Effort Estimates

| Phase | Task | Effort | Priority | Dependencies |
|-------|------|--------|----------|--------------|
| **2** | Create/verify dual focused stores (`interlisp-web-sites_1741606671710` proven, `interlisp-github-v2` schema patched future-proof) | 2-4 hrs | HIGH | None |
| **3** | Update Cloud Function with dual-fetch blended logic (70/30, 50/50, website-primary→secondary→github) | 1-2 hrs | HIGH | Phase 2 |
| **6** | Deploy + test updated function (staging → production, verify 0 untitled) | 1-2 hrs | HIGH | Phase 3 |
| **4** | Set up Cloud Scheduler + recrawl/reimport functions (website via existing crawl, github via local one-off until scheduled) | 2-3 hrs | MEDIUM | Phase 2 |
| **5** | Plan Reference Manual structuring strategy | 1 hr | LOW | None |
| **7** | **Cleanup — pare interlispsearch to in-use resources only** | 1-2 hrs | HIGH | Phases 2,3,6 |

**Total Estimated Time:** 8-14 hours

### Recommended Execution Order

**Week 1: Core Implementation**

1. ✅ **Phase 2** — Verify dual stores + patch schema
   - Confirm `interlisp-web-sites_1741606671710` (`*.interlisp.org/*` `SUCCEEDED`) proven
   - Patch `interlisp-github-v2` default_schema (title/url/repo/type/state → `retrievable:true`) future-proof
   - Import GitHub JSONL via local one-off (`GITHUB_TOKEN=$(gh auth token) node /tmp/local_import_simple.js` → 350 `branches/0` `successCount 350`)

2. ✅ **Phase 3** — Update Cloud Function (dual-fetch blended)
   - Replace `filter` with `getSource()` + `website-primary:1 → website-secondary:2 → github:3` + 70/30 (50/50 for github queries)
   - Add `stripHtml`, `semanticRelevanceScore` tie-break, dedup, citation sorting
   - Test locally `node -c index.js` + `npm run lint`

3. ✅ **Phase 6** — Deploy & test
   - Deploy to staging first (`search-00037-xas`)
   - Run test queries from Testing Strategy (verify 0 untitled across github/medley/screenshots/FONTSAVAILABLE)
   - Compare results with current v3
   - Deploy to production once validated

**Week 2: Automation**

4. ✅ **Phase 4** — Set up Cloud Scheduler + automation functions
   - `trigger-website-recrawl` targets `interlisp-web-sites_1741606671710` (existing crawl, no recreation)
   - `github-reimport` targets `interlisp-github-v2` `branches/0` (local one-off until isolated source dir for scheduled Pub/Sub; re-exports via `index.js`)
   - Create Cloud Scheduler jobs (daily website, weekly GitHub — deferred weekly until isolated deploy)
   - Test manual trigger to verify end-to-end flow

5. ⏳ **Phase 5** — Plan Reference Manual structuring (defer to later sprint)
   - Document Option A (structured extraction)
   - Identify PDF parsing tools
   - Plan manual validation approach

**Week 3: Cleanup (after unified stack validated in production)**

6. ✅ **Phase 7** — Pare interlispsearch to in-use resources only
   - Inventory all data stores, engines, functions, scheduler jobs, storage buckets, Firestore collections
   - Mark `interlisp-web-sites_1741606671710`, `interlisp-github-v2`, engines `interlisp-website-only`/`interlisp-github-only`/`interlisp-search-unified` (fallback), `search`/`github-reimport` (`trigger-website-recrawl` if kept) + scheduler jobs as **KEEP**
   - Delete all other Discovery Engine data stores/engines (e.g. `interlisp-search-v3`, `interlisp-org-search_1768860477660`, `interlisp-site-search`, document-bucket if superseded), stale functions, and `interlispsearch-search-imports` staging artifacts — see Implementation Guide Phase 7 for safe-delete sequence

---

## Decision Points

Before proceeding with implementation, please confirm:

### Decision 1: Unified Data Store Approach

**Question:** Does a single unified data store (with metadata-based ranking) make sense for your use case?

**Alternatives:**
- Keep two separate data stores; update Cloud Function routing logic
- Create three data stores (website-only, website+github, website+github+reference)

**Recommendation:** ✅ Single unified data store

**Your Decision:** [ ] Approve [ ] Request modifications [ ] Choose alternative

---

### Decision 2: Metadata Tagging

**Question:** Should we tag all existing documents with `source` and `priority` metadata?

**Approach:**
- Website-crawled documents: automatically tagged `source:website, priority:1`
- GitHub imported documents: manually tagged in JSONL `source:github, priority:3`
- Reference manual (future): tagged `source:reference_manual, priority:2`

**Implementation:**
- Website documents may not have explicit metadata (use URL pattern to infer)
- GitHub documents get metadata during JSONL import
- Reference docs get tagged during PDF extraction

**Your Decision:** [ ] Approve [ ] Request modifications

---

### Decision 3: Refresh Frequency

**Question:** Does the proposed refresh schedule work for your needs?

**Proposed:**
- Website: Daily @ 2 AM UTC (captures doc updates within 24 hours)
- GitHub: Weekly, Monday @ 3 AM UTC (captures issues/PRs within 7 days)

**Alternatives:**
- Website: Every 6 hours (more frequent, higher API costs)
- GitHub: Every 3 days (faster feedback on issues)
- Manual only (no automation)

**Your Decision:** [ ] Approve [ ] Request modifications (specify frequency)

---

### Decision 4: Reference Manual Priority

**Question:** When should we tackle Reference Manual structuring?

**Options:**
- A. Defer until after unified data store is live and stable (4-6 weeks)
- B. Start immediately (parallel with data store setup, +3-4 weeks)
- C. Defer indefinitely; revisit based on user feedback

**Recommendation:** ✅ Option A (defer to unblock core improvements)

**Your Decision:** [ ] Option A (defer) [ ] Option B (start now) [ ] Option C (indefinite)

---

### Decision 5: Architecture Style Preference

**Question:** Any changes to the proposed architecture?

- Single unified data store with metadata-based ranking
- Cloud Scheduler automation for refresh
- Post-processing logic in Cloud Function for result reordering
- Preamble guidance for citation preference

**Your Decision:** [ ] Approved as-is [ ] Request modifications (describe)

---

## Phase 7 — Cleanup: Pare interlispsearch to In-Use Resources Only

**Goal:** After the unified stack (`interlisp-search-unified` + its engine + updated `search` function + automation) is validated in production, delete every other resource in `interlispsearch` so the project contains only what is actively used. This removes the “large collection of data stores” discovered via the REST `list` call and prevents quota/cost drift.

**Triggers:** Do NOT run until Phases 2–4 and 6 are complete and `interlisp-search-unified` serves production traffic for ≥ 48h.

### Keep List (explicit) — Updated

| Resource type | Name / ID | Why kept |
|---|---|---|
| Data store | `interlisp-web-sites_1741606671710` | Proven website crawl (`*.interlisp.org/*` `SUCCEEDED`) — primary |
| Data store | `interlisp-github-v2` | Structured GitHub store (`NO_CONTENT` `branches/0`, future-proof schema `retrievable:true`) |
| Data store | `interlisp-search-unified` | Fresh website store (`PUBLIC_WEBSITE` interlisp.org/*+files) retained, not used for serving (fallback) |
| Engine (search app) | `interlisp-website-only` / `interlisp-github-only` | Focused engines blended in live `search` |
| Engine (search app) | `interlisp-search-unified` (`[interlisp-web-sites_1741606671710,interlisp-github-v2]`) | Fallback for single-engine callers |
| Cloud Functions (Gen2) | `search` (`search-00037-xas`), `github-reimport` (needs isolated source dir for Pub/Sub) | Production + GitHub import |
| Cloud Scheduler | `reimport-github-weekly` (deferred weekly), `recrawl-website-daily` if kept | Refresh |
| Firestore | `rate_limits` collection (TTL on `updatedAt`) | Rate limiting |
| Cloud Storage | `interlispsearch-search-imports` (or current import bucket) | GitHub JSONL staging — keep bucket, prune old objects |
| IAM | `vertex-search-sa@interlispsearch.iam.gserviceaccount.com` + org-policy overrides | Runtime identity |
| Project | `interlispsearch` itself | Container |

Everything else in `interlispsearch` is **candidate for deletion**.

### Inventory First (read-only)

Run the inventory script from the Implementation Guide (§ Phase 7, `inventory-interlispsearch.sh`) — it `GET`s:

* `GET /v1/projects/INTERLISPSEARCH/locations/global/collections/default_collection/dataStores` — all data stores
* `GET /v1/projects/INTERLISPSEARCH/locations/global/collections/default_collection/engines` — all engines
* `gcloud functions list --gen2 --region=us-central1`
* `gcloud scheduler jobs list --location=us-central1`
* `gcloud storage ls` / `gsutil ls`
* `gcloud firestore collections list` (or console)

Save JSON output to `/tmp/interlispsearch-inventory-YYYYMMDD/` and commit the keep/delete decision list for review. Require a second pair of eyes before any `DELETE`.

### Safe-Delete Sequence

Order matters — engines depend on data stores, functions depend on service account:

1. **Engines first** — `DELETE /v1/projects/…/engines/{engineId}` for every engine whose `dataStoreIds` is not `["interlisp-search-unified"]`. Engines are cheap to recreate; data stores are not.
2. **Data stores second** — `DELETE /v1/projects/…/dataStores/{dataStoreId}` for stale stores (`interlisp-search-v3`, `interlisp-org-search_1768860477660`, `interlisp-site-search` if superseded, and any `test-*`/`tmp-*`). Each delete cascades to its documents/targetSites; allow 5–10 min per store and verify `404` on subsequent `GET`.
3. **Cloud Functions third** — `gcloud functions delete {name} --gen2 --region=us-central1` for any function not in the keep list (e.g. old `search-v2`, staging clones).
4. **Cloud Scheduler fourth** — `gcloud scheduler jobs delete {name} --location=us-central1` for stale jobs.
5. **Cloud Storage fifth** — `gcloud storage rm gs://BUCKET/github-import-*.jsonl` for import artifacts older than the last successful import; do not delete the bucket itself.
6. **Firestore sixth** — prune `rate_limits` documents only via TTL (do not delete the database); remove any ad-hoc `test-*` collections.
7. **IAM last** — do not delete the service account; only remove unused keys (`gcloud iam service-accounts keys delete`).

All deletes use the REST `DELETE` with `x-goog-user-project: interlispsearch` and `Authorization: Bearer $(gcloud auth application-default print-access-token)` — there is no `gcloud beta discoveryengine` CLI (verified SDK 568.0.0; see Phase 7 scripts).

### Validation After Cleanup

* Re-run the inventory script — expected counts: `dataStores=1`, `engines=1`, `functions=3`, `schedulerJobs=2`.
* `curl "https://us-central1-interlispsearch.cloudfunctions.net/search?q=interlisp"` still returns `200` with unified-store citations (`source:website` first).
* No `discoveryengine.googleapis.com` quota errors in Cloud Logging.

---

## Next Steps

Once you approve the decision points above:

1. **I will create detailed implementation scripts** for each phase
2. **I will provide exact gcloud commands** for data store setup
3. **I will write complete Cloud Function code** (with error handling, logging)
4. **I will create testing checklist** and validation steps
5. **I will provide monitoring/observability setup** (logging, alerts)
6. **Phase 7 will be executed only after production validation** — inventory → review → delete in the order above

---

## Appendix: References

### Vertex AI Search Documentation

- [Vertex AI Search Overview](https://cloud.google.com/generative-ai-app-builder/docs/unified-overview)
- [Data Store Configuration](https://cloud.google.com/generative-ai-app-builder/docs/manage-data-stores)
- [Search API Reference](https://cloud.google.com/generative-ai-app-builder/docs/search-reference)
- [Document Import (JSONL)](https://cloud.google.com/generative-ai-app-builder/docs/import-data)
- [Filter Syntax](https://cloud.google.com/generative-ai-app-builder/docs/filter-results)

### Google Cloud Platform Resources

- [Cloud Scheduler Documentation](https://cloud.google.com/scheduler/docs)
- [Cloud Functions Documentation](https://cloud.google.com/functions/docs)
- [Cloud Storage Documentation](https://cloud.google.com/storage/docs)
- [Discovery Engine API](https://cloud.google.com/python/docs/reference/google-cloud-discoveryengine/latest)

### Related Files in This Repository

- `search-function/index.js` — Current Cloud Function implementation
- `search-function/rateLimiter.js` — Firestore-based rate limiting
- `vertex-ai-search-implementation.md` — Current implementation guide
- `search-function/package.json` — Dependencies

---

**Document Version:** 1.1  
**Last Updated:** September 02, 2026  
**Status:** Implemented — see Implementation Guide Phase 7 still pending (gated ≥48h production)

