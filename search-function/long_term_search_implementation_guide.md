# Long-Term Search Implementation Guide
## Complete Step-by-Step Instructions with Scripts

**Document Version:** 1.1  
**Date:** September 02, 2026  
**Status:** Implemented — Dual-Engine Blended (verified live `search-00037-xas` 2026-09-02; `0 Untitled` across github/medley/screenshots matrix)

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Phase 1: Create Unified Search (Data Store + Engine)](#phase-1-create-unified-search-data-store--engine)
4. [Phase 2: Update Cloud Function](#phase-2-update-cloud-function)
5. [Phase 3: Deploy & Test](#phase-3-deploy--test)
6. [Phase 4: Set Up Automation](#phase-4-set-up-automation)
7. [Testing Checklist](#testing-checklist)
8. [Rollback Procedures](#rollback-procedures)
9. [Monitoring & Troubleshooting](#monitoring--troubleshooting)
10. [Phase 7: Cleanup — Pare to In-Use Resources](#phase-7-cleanup--pare-interlispsearch-to-in-use-resources-only)
11. [Appendix: Script Reference](#appendix-script-reference)

---

## Overview

This guide walks you through implementing the unified data store architecture with automated refresh pipeline.

### What You're Building — Implemented

```
interlisp-web-sites_1741606671710 (proven)    interlisp-github-v2 (NO_CONTENT, branches/0)
  PUBLIC_WEBSITE *.interlisp.org/* SUCCEEDED   structured GitHub issues/PRs/markdown
         \                                          /
          \   interlisp-website-only      interlisp-github-only
           \  [interlisp-web-sites_…]      [interlisp-github-v2]  (fallback engine
            \        \                         /                  interlisp-search-unified
             \        \--→ Cloud Function search (dual-fetch blended) ←--/
                      ↓  WEBSITE_ENGINE_ID + GITHUB_ENGINE_ID
                   website-primary (1) → website-secondary (2) → github (3)
                   parallel fetch 20 each, blended 70/30 (50/50 for github|issue|pr|discussion)
                   dedup by url, priority→semanticRelevanceScore, citations sorted
                   title: derived.title || structData.title (schema retrievable:true)
                      ↓
                   Cloud Scheduler (automation, local one-off until isolated deploy)
                   · Weekly GitHub JSONL → interlisp-github-v2 branches/0 (source/priority/last_indexed)
                   · Website crawl managed by existing *.interlisp.org targetSites (no recreation)
```

Fallback `interlisp-search-unified` (`[interlisp-web-sites_1741606671710, interlisp-github-v2]`) retained; fresh `interlisp-search-unified` website store (`interlisp.org/*` + `files.interlisp.org/*`) `SUCCEEDED` but not used for serving (returned only `files` for `history`/`Medley`).

### Timeline

- **Phase 1:** Data store setup (2-4 hours)
- **Phase 2:** Cloud Function updates (1-2 hours)
- **Phase 3:** Testing & deployment (1-2 hours)
- **Phase 4:** Automation setup (2-3 hours)

**Total:** 6-11 hours

---

## Prerequisites

Before starting, verify you have:

- ✅ gcloud CLI installed and authenticated
- ✅ Access to `interlispsearch` GCP project
- ✅ Service account `vertex-search-sa@interlispsearch.iam.gserviceaccount.com` exists
- ✅ Cloud Function `search` deployed and working
- ✅ `interlisp-search-v3` data store exists (will clone from this)
- ✅ GitHub token (for reimport function)
- ✅ Node.js 24+ (for Cloud Function testing)

**Verify access:**

```bash
gcloud config set project interlispsearch
gcloud auth application-default login

# Test project access
gcloud projects describe interlispsearch

createTime: '2025-03-09T12:06:51.391531Z'
lifecycleState: ACTIVE
name: InterlispSearch
parent:
  id: '513691321000'
  type: organization
projectId: interlispsearch
projectNumber: '191169864763'

# Check existing data stores — Discovery Engine has NO gcloud CLI (REST API only)
# Use curl with Discovery Engine API instead:
TOKEN=$(gcloud auth application-default print-access-token)
curl -s -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: interlispsearch" \
  "https://discoveryengine.googleapis.com/v1/projects/interlispsearch/locations/global/collections/default_collection/dataStores" \
  | python3 -m json.tool

# We need to prune this list -- which data stores are no longer in use?  And, which ones become obsolete
# when this work is done?
    "dataStores": [
        {
            "name": "projects/191169864763/locations/global/collections/default_collection/dataStores/interlisp-document-bucket_1741737147622",
            "displayName": "interlisp document bucket",
            "industryVertical": "GENERIC",
            "createTime": "2025-03-11T23:52:48.241959Z",
            "solutionTypes": [
                "SOLUTION_TYPE_SEARCH"
            ],
            "contentConfig": "CONTENT_REQUIRED",
            "defaultSchemaId": "default_schema",
            "billingEstimation": {
                "unstructuredDataSize": "4512314",
                "unstructuredDataUpdateTime": "2026-08-28T05:04:14.419426546Z"
            },
            "documentProcessingConfig": {
                "name": "projects/191169864763/locations/global/collections/default_collection/dataStores/interlisp-document-bucket_1741737147622/documentProcessingConfig",
                "defaultParsingConfig": {
                    "digitalParsingConfig": {}
                }
            },
            "servingConfigDataStore": {}
        },
        {
            "name": "projects/191169864763/locations/global/collections/default_collection/dataStores/interlisp-github",
            "displayName": "Interlisp GitHub Content",
            "industryVertical": "GENERIC",
            "createTime": "2026-05-05T03:59:14.530998Z",
            "solutionTypes": [
                "SOLUTION_TYPE_SEARCH"
            ],
            "contentConfig": "CONTENT_REQUIRED",
            "defaultSchemaId": "default_schema",
            "documentProcessingConfig": {
                "name": "projects/191169864763/locations/global/collections/default_collection/dataStores/interlisp-github/documentProcessingConfig",
                "defaultParsingConfig": {
                    "digitalParsingConfig": {}
                }
            },
            "servingConfigDataStore": {}
        },
        {
            "name": "projects/191169864763/locations/global/collections/default_collection/dataStores/interlisp-github-v2",
            "displayName": "Interlisp GitHub Content",
            "industryVertical": "GENERIC",
            "createTime": "2026-05-13T03:30:54.827835Z",
            "solutionTypes": [
                "SOLUTION_TYPE_SEARCH"
            ],
            "contentConfig": "NO_CONTENT",
            "defaultSchemaId": "default_schema",
            "billingEstimation": {
                "structuredDataSize": "5107743",
                "structuredDataUpdateTime": "2026-08-28T08:40:17.553964358Z"
            },
            "servingConfigDataStore": {},
            "naturalLanguageQueryUnderstandingConfig": {
                "mode": "ENABLED"
            }
        },
        {
            "name": "projects/191169864763/locations/global/collections/default_collection/dataStores/interlisp-site-search",
            "displayName": "Interlisp Site Search",
            "industryVertical": "GENERIC",
            "createTime": "2026-04-29T11:34:57.642327Z",
            "solutionTypes": [
                "SOLUTION_TYPE_SEARCH"
            ],
            "contentConfig": "PUBLIC_WEBSITE",
            "defaultSchemaId": "default_schema",
            "advancedSiteSearchConfig": {
                "disableAutomaticRefresh": false
            },
            "billingEstimation": {
                "websiteDataSize": "1224192000",
                "websiteDataUpdateTime": "2026-08-28T10:10:53.793689149Z"
            },
            "servingConfigDataStore": {}
        },
        {
            "name": "projects/191169864763/locations/global/collections/default_collection/dataStores/interlisp-web-sites_1741606671710",
            "displayName": "Interlisp Web Sites",
            "industryVertical": "GENERIC",
            "createTime": "2025-03-10T11:40:25.475329Z",
            "solutionTypes": [
                "SOLUTION_TYPE_SEARCH"
            ],
            "contentConfig": "PUBLIC_WEBSITE",
            "defaultSchemaId": "default_schema",
            "advancedSiteSearchConfig": {
                "disableInitialIndex": true,
                "disableAutomaticRefresh": true
            },
            "billingEstimation": {
                "websiteDataSize": "407040000",
                "websiteDataUpdateTime": "2026-08-28T10:10:53.793689149Z"
            },
            "documentProcessingConfig": {
                "name": "projects/191169864763/locations/global/collections/default_collection/dataStores/interlisp-web-sites_1741606671710/documentProcessingConfig",
                "chunkingConfig": {
                    "layoutBasedChunkingConfig": {
                        "chunkSize": 500
                    }
                },
                "defaultParsingConfig": {
                    "layoutParsingConfig": {}
                }
            },
            "servingConfigDataStore": {},
            "naturalLanguageQueryUnderstandingConfig": {}
        },
        {
            "name": "projects/191169864763/locations/global/collections/default_collection/dataStores/lispcore_1742267831416",
            "displayName": "LispCore",
            "industryVertical": "GENERIC",
            "createTime": "2025-03-18T03:17:18.742179Z",
            "solutionTypes": [
                "SOLUTION_TYPE_SEARCH"
            ],
            "contentConfig": "GOOGLE_WORKSPACE",
            "aclEnabled": true,
            "workspaceConfig": {
                "type": "GOOGLE_GROUPS"
            },
            "servingConfigDataStore": {}
        },
        {
            "name": "projects/191169864763/locations/global/collections/default_collection/dataStores/medley-interlisp-core_1741735842821",
            "displayName": "Medley Interlisp Core",
            "industryVertical": "GENERIC",
            "createTime": "2025-03-11T23:31:01.436125Z",
            "solutionTypes": [
                "SOLUTION_TYPE_SEARCH"
            ],
            "contentConfig": "GOOGLE_WORKSPACE",
            "aclEnabled": true,
            "workspaceConfig": {
                "type": "GOOGLE_GROUPS"
            },
            "servingConfigDataStore": {}
        }
    ]
}

```

---

## Phase 1: Create Unified Search (Data Store + Engine)

Production unified search uses two focused engines blended in the Cloud Function:

* `interlisp-website-only` (`[interlisp-web-sites_1741606671710]` `PUBLIC_WEBSITE`, `GENERIC`, `*.interlisp.org/*` `SUCCEEDED` — proven to return `https://interlisp.org/...` for `history`/`software`/`Medley` where `interlisp-search-unified` returned only `files`/`online`/`primer`)
* `interlisp-github-v2` (`NO_CONTENT`, `GENERIC`) — structured GitHub issues / PRs / markdown via `interlisp-github-only` (`[interlisp-github-v2]`)
* Fallback `interlisp-search-unified` (`[interlisp-web-sites_1741606671710, interlisp-github-v2]`) retained for single-engine callers; the freshly created `interlisp-search-unified` website store (`PUBLIC_WEBSITE` `interlisp.org/*` + `files.interlisp.org/*`) is retained but not used for serving (its crawl returned only `files`).

All Discovery Engine operations use the REST API (`https://discoveryengine.googleapis.com/v1/...` with `x-goog-user-project`); there is no `gcloud discoveryengine` group (SDK 568.0.0).

### Step 1.1: Inventory Existing Resources

Document current state before creating new resources:

```bash
TOKEN=$(gcloud auth application-default print-access-token)

# All data stores and engines (for reference)
curl -s -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: interlispsearch" \
  "https://discoveryengine.googleapis.com/v1/projects/interlispsearch/locations/global/collections/default_collection/dataStores?pageSize=100" \
  | python3 -m json.tool > /tmp/datastores_backup.json

curl -s -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: interlispsearch" \
  "https://discoveryengine.googleapis.com/v1/projects/interlispsearch/locations/global/collections/default_collection/engines?pageSize=100" \
  | python3 -m json.tool > /tmp/engines_backup.json

# Reference engine — shows expected multi-store pattern and industryVertical
curl -s -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: interlispsearch" \
  "https://discoveryengine.googleapis.com/v1/projects/interlispsearch/locations/global/collections/default_collection/engines/interlisp-search-v3" \
  | python3 -m json.tool > /tmp/interlisp-search-v3.json

echo "Backups saved to /tmp/datastores_backup.json, /tmp/engines_backup.json, /tmp/interlisp-search-v3.json"
```

### Step 1.2: Create the Unified Website Data Store — Retained, Not Used for Serving (its crawl returned only `files` for `history`/`Medley`)

> **Implemented note (2026-09-02):** This fresh `interlisp-search-unified` `PUBLIC_WEBSITE` store (`interlisp.org/*` + `files.interlisp.org/*`) is `SUCCEEDED` but not used for serving; proven `interlisp-web-sites_1741606671710` (`*.interlisp.org/*` `SUCCEEDED`) is primary. Steps 1.2–1.5 retained for inventory/reproducibility; Phase 1.7 fallback engine `interlisp-search-unified` (`[interlisp-web-sites_1741606671710, interlisp-github-v2]`) is the kept unified engine.

### Step 1.2 (historical): Create the Unified Website Data Store

```bash
#!/bin/bash
# File: create-unified-datastore.sh
PROJECT_ID="interlispsearch"
DATA_STORE_ID="interlisp-search-unified"
DISPLAY_NAME="Interlisp Unified Search"
LOCATION="global"
TOKEN=$(gcloud auth application-default print-access-token)

curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "x-goog-user-project: $PROJECT_ID" \
  "https://discoveryengine.googleapis.com/v1/projects/$PROJECT_ID/locations/$LOCATION/collections/default_collection/dataStores?dataStoreId=$DATA_STORE_ID" \
  -d '{
    "displayName": "'"$DISPLAY_NAME"'",
    "industryVertical": "GENERIC",
    "solutionTypes": ["SOLUTION_TYPE_SEARCH"],
    "contentConfig": "PUBLIC_WEBSITE"
  }'
sleep 5
curl -s -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: $PROJECT_ID" \
  "https://discoveryengine.googleapis.com/v1/projects/$PROJECT_ID/locations/$LOCATION/collections/default_collection/dataStores/$DATA_STORE_ID" \
  | python3 -m json.tool
```

```bash
chmod +x create-unified-datastore.sh && ./create-unified-datastore.sh
```

### Step 1.3: Add Target Sites

```bash
#!/bin/bash
# File: add-target-sites.sh
PROJECT_ID="interlispsearch"
DATA_STORE_ID="interlisp-search-unified"
LOCATION="global"
TOKEN=$(gcloud auth application-default print-access-token)

for pattern in "interlisp.org/*" "files.interlisp.org/*"; do
  echo "Adding target site: $pattern"
  curl -X POST \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -H "x-goog-user-project: $PROJECT_ID" \
    "https://discoveryengine.googleapis.com/v1/projects/$PROJECT_ID/locations/$LOCATION/collections/default_collection/dataStores/$DATA_STORE_ID/siteSearchEngine/targetSites" \
    -d "{\"providedUriPattern\": \"$pattern\", \"type\": \"INCLUDE\", \"exactMatch\": false}"
  sleep 2
done

curl -s -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: $PROJECT_ID" \
  "https://discoveryengine.googleapis.com/v1/projects/$PROJECT_ID/locations/$LOCATION/collections/default_collection/dataStores/$DATA_STORE_ID/siteSearchEngine/targetSites" \
  | python3 -m json.tool
```

```bash
chmod +x add-target-sites.sh && ./add-target-sites.sh
```

### Step 1.4: Upgrade to Advanced Indexing (Console)

1. Cloud Console → **AI Applications → Data Stores → `interlisp-search-unified` → Data tab**
2. For each target site, click **Upgrade to Advanced**
3. Wait 4–8 hours for indexing to reach `SUCCEEDED`

There is no REST/`gcloud` API for this step.

### Step 1.5: Verify Indexing Status

```bash
#!/bin/bash
# File: check-indexing-status.sh
PROJECT_ID="interlispsearch"
DATA_STORE_ID="interlisp-search-unified"
LOCATION="global"
TOKEN=$(gcloud auth application-default print-access-token)
curl -s -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: $PROJECT_ID" \
  "https://discoveryengine.googleapis.com/v1/projects/$PROJECT_ID/locations/$LOCATION/collections/default_collection/dataStores/$DATA_STORE_ID/siteSearchEngine/targetSites" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for site in data.get('targetSites', []):
    print(f\"{site.get('providedUriPattern')}: {site.get('indexingStatus','UNKNOWN')}\")
"
```

```bash
chmod +x check-indexing-status.sh && ./check-indexing-status.sh
# watch -n 1800 ./check-indexing-status.sh  # during initial crawl
```

### Step 1.6: Initial GitHub Import into `interlisp-github-v2`

The website crawl (Steps 1.2–1.5) does not include GitHub. Import structured GitHub content into the `NO_CONTENT` store `interlisp-github-v2` before creating the unified engine so ranking can be validated in Phase 2.

Documents are stored as `Document.structData` (not top-level `title`/`url`); `document.id` must match `^[a-zA-Z0-9-_]+$` (sanitize `.` → `-`) and use `branches/0` (not `branches/default`). Metadata `source`/`priority`/`last_indexed` is additive to existing `repo`/`type`/`created_date`.

**Option A — via Cloud Function (recommended for repeatability):**

```bash
export GITHUB_TOKEN=ghp_...  # from https://github.com/settings/tokens (repo read)

# Pub/Sub topic must exist before deploy
gcloud pubsub topics create reimport-github --project=interlispsearch 2>/dev/null || true

# Deploy from repo root (or --source=. if inside search-function/)
gcloud functions deploy github-reimport \
  --gen2 --runtime=nodejs24 --region=us-central1 \
  --source=./search-function --entry-point=reimportGithub --trigger-topic=reimport-github \
  --service-account=vertex-search-sa@interlispsearch.iam.gserviceaccount.com \
  --set-env-vars GITHUB_TOKEN=$GITHUB_TOKEN --memory=512Mi --timeout=300s \
  --project=interlispsearch

# Trigger one initial import
gcloud pubsub topics publish reimport-github --message='{"action":"reimport","reason":"initial-seed-unified"}' --project=interlispsearch
gcloud functions logs read github-reimport --gen2 --region=us-central1 --limit=50 --project=interlispsearch

# Verify import operation
TOKEN=$(gcloud auth application-default print-access-token)
curl -s -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: interlispsearch" \
  "https://discoveryengine.googleapis.com/v1/projects/interlispsearch/locations/global/collections/default_collection/dataStores/interlisp-github-v2/branches/0/documents?pageSize=1" \
  | python3 -m json.tool
```

**Option B — local one-off (no function deploy):**

```bash
cd search-function && npm install
# Writes /tmp/github-initial-*.jsonl, uploads to gs://interlispsearch-search-imports/, POST .../branches/0/documents:import
node github-initial-import.js            # anonymous GitHub API (60 req/h) or with GITHUB_TOKEN
GITHUB_TOKEN=$GITHUB_TOKEN node github-initial-import.js  # authenticated (higher quota)
# Dry run only:
node github-initial-import.js --dry-run
```

Both options produce JSONL lines `{"id":"github-issue-medley-123","structData":{"id":"...","title":"...","url":"...","content":"...","source":"github","priority":3,...}}`, sanitize IDs (`Interlisp.github.io` → `Interlisp-github-io`), upload to `gs://interlispsearch-search-imports/github-initial-*.jsonl`, and `POST .../branches/0/documents:import`.

Verify `successCount == totalCount` in the returned `operations/import-documents-*` (e.g. `successCount: 350, done: true`).

### Step 1.7: Create Engines (two focused + one unified fallback)

`interlisp-web-sites_1741606671710` (`PUBLIC_WEBSITE` `*.interlisp.org/*` `SUCCEEDED`) is the proven website crawl — `interlisp-search-unified` website store created in 1.2 returned only `files`/`online`/`primer` for `history`/`interlisp` and is retained but not used for serving. `industryVertical: GENERIC` is required for multi-store engines.

```bash
TOKEN=$(gcloud auth application-default print-access-token)

# Website-only (primary, used for dual fetch)
curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -H "x-goog-user-project: interlispsearch" \
  "https://discoveryengine.googleapis.com/v1/projects/interlispsearch/locations/global/collections/default_collection/engines?engineId=interlisp-website-only" \
  -d '{
    "displayName": "Interlisp Website Only",
    "dataStoreIds": ["interlisp-web-sites_1741606671710"],
    "solutionType": "SOLUTION_TYPE_SEARCH",
    "industryVertical": "GENERIC",
    "searchEngineConfig": {"searchTier":"SEARCH_TIER_ENTERPRISE","searchAddOns":["SEARCH_ADD_ON_LLM"]}
  }' | python3 -m json.tool

# GitHub-only (secondary)
curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -H "x-goog-user-project: interlispsearch" \
  "https://discoveryengine.googleapis.com/v1/projects/interlispsearch/locations/global/collections/default_collection/engines?engineId=interlisp-github-only" \
  -d '{
    "displayName": "Interlisp GitHub Only",
    "dataStoreIds": ["interlisp-github-v2"],
    "solutionType": "SOLUTION_TYPE_SEARCH",
    "industryVertical": "GENERIC",
    "searchEngineConfig": {"searchTier":"SEARCH_TIER_ENTERPRISE","searchAddOns":["SEARCH_ADD_ON_LLM"]}
  }' | python3 -m json.tool

# Unified fallback (website + GitHub)
curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -H "x-goog-user-project: interlispsearch" \
  "https://discoveryengine.googleapis.com/v1/projects/interlispsearch/locations/global/collections/default_collection/engines?engineId=interlisp-search-unified" \
  -d '{
    "displayName": "Interlisp Unified Search",
    "dataStoreIds": ["interlisp-web-sites_1741606671710","interlisp-github-v2"],
    "solutionType": "SOLUTION_TYPE_SEARCH",
    "industryVertical": "GENERIC",
    "searchEngineConfig": {"searchTier":"SEARCH_TIER_ENTERPRISE","searchAddOns":["SEARCH_ADD_ON_LLM"]}
  }' | python3 -m json.tool

# Verify
curl -s -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: interlispsearch" \
  "https://discoveryengine.googleapis.com/v1/projects/interlispsearch/locations/global/collections/default_collection/engines/interlisp-website-only" | python3 -m json.tool
curl -s -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: interlispsearch" \
  "https://discoveryengine.googleapis.com/v1/projects/interlispsearch/locations/global/collections/default_collection/engines/interlisp-search-unified" | python3 -m json.tool
# Phase 2 uses WEBSITE_ENGINE_ID=interlisp-website-only, GITHUB_ENGINE_ID=interlisp-github-only (fallback ENGINE_ID=interlisp-search-unified)
```

**Phase 1 complete when:** `GET .../engines/interlisp-website-only` and `interlisp-github-only` exist, `GET .../engines/interlisp-search-unified` returns `["interlisp-web-sites_1741606671710","interlisp-github-v2"]`, and GitHub import `successCount == totalCount` (350).

---

## Phase 2: Update Cloud Function

### Step 2.1: Create Updated `index.js`

This implements dual-engine blended ranking: `website-primary` (`interlisp.org`/`www.interlisp.org` →1) over `website-secondary` (`*.interlisp.org` →2) over `github` →3, with guaranteed GitHub representation (70/30, 50/50 for GitHub queries).

**File: `search-function/index.js`** (deployed as `search-00037-xas` 2026-09-02 with `WEBSITE_ENGINE_ID=interlisp-website-only`, `GITHUB_ENGINE_ID=interlisp-github-only`; verified `0 Untitled`)

```javascript
'use strict';
const { GoogleAuth } = require('google-auth-library');
const { isRateLimited } = require('./rateLimiter');
const PROJECT_ID = process.env.PROJECT_ID;
const WEBSITE_ENGINE_ID = process.env.WEBSITE_ENGINE_ID || process.env.ENGINE_ID;
const GITHUB_ENGINE_ID = process.env.GITHUB_ENGINE_ID || null;
const LOCATION = 'global';
const auth = new GoogleAuth({ scopes: ['https://www.googleapis.com/auth/cloud-platform'] });
exports.search = async (req, res) => {
  // ... CORS + rate limiting (see repo) ...
  const query = req.query.q || req.body?.q || '';
  const pageSize = parseInt(req.query.pageSize) || 10;
  const stripHtml = str => str ? str.replace(/<[^>]*>/g, '') : null;
  const getSource = (url) => {
    if (!url) return 'unknown';
    try {
      const u = new URL(url); const host = u.hostname.toLowerCase();
      if (host === 'www.interlisp.org' || host === 'interlisp.org') return 'website-primary';
      if (host.endsWith('.interlisp.org')) return 'website-secondary';
      if (host.includes('github.com') || url.includes('github.com')) return 'github';
      return 'other';
    } catch (_) { return url.includes('github.com') ? 'github' : url.includes('interlisp.org') ? 'website-secondary' : 'other'; }
  };
  const sourcePriorityMap = { 'website-primary':1,'website-secondary':2,'github':3,'other':4,'unknown':999 };
  const fetchPageSize = 20;
  const searchEngine = async (engineId, withSummary) => {
    const endpoint = `https://discoveryengine.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION}/collections/default_collection/engines/${engineId}/servingConfigs/default_config:search`;
    const body = { query, pageSize: fetchPageSize, contentSearchSpec: { snippetSpec:{returnSnippet:true}, extractiveContentSpec:{maxExtractiveAnswerCount:3} } };
    if (withSummary) body.contentSearchSpec.summarySpec = { summaryResultCount:5, includeCitations:true, useSemanticChunks:true, languageCode:'en-US', modelPromptSpec:{preamble:buildPreamble(context)}, modelSpec:{version:'stable'} };
    const resp = await fetch(endpoint, { method:'POST', headers:{'Authorization':`Bearer ${(await (await auth.getClient()).getAccessToken()).token}`,'Content-Type':'application/json','x-goog-user-project':PROJECT_ID}, body:JSON.stringify(body) });
    if (!resp.ok) throw new Error(`Vertex API error ${resp.status} on ${engineId}: ${await resp.text()}`);
    return resp.json();
  };
  let [websiteData, githubData] = GITHUB_ENGINE_ID ? await Promise.all([searchEngine(WEBSITE_ENGINE_ID,true), searchEngine(GITHUB_ENGINE_ID,false)]) : [await searchEngine(WEBSITE_ENGINE_ID,true), null];
  // Blended merge: guarantee GitHub despite website priority
  const isGithubQuery = /github|issue|pull\s*request|\bpr\b|discussion/i.test(query);
  const websiteTake = isGithubQuery ? Math.ceil(pageSize*0.5) : Math.ceil(pageSize*0.7);
  const githubTake = pageSize - websiteTake;
  const toItems = (data, hint) => (data?.results||[]).map(r=>{ const d=r.document?.derivedStructData, s=r.document?.structData, url=d?.link||d?.url||s?.url||s?.link||null, src=hint||getSource(url); return {raw:r, url, source:src, priority:sourcePriorityMap[src]||999, derived:d, structData:s, score:r.retrievalSignals?.semanticRelevanceScore||0}; }).filter(i=>i.url);
  let websiteItems = toItems(websiteData,null).sort((a,b)=>a.priority-b.priority||b.score-a.score);
  let githubItems = toItems(githubData,'github').sort((a,b)=>b.score-a.score);
  const seen=new Set(); websiteItems=websiteItems.filter(i=>!seen.has(i.url)&&seen.add(i.url)); githubItems=githubItems.filter(i=>!seen.has(i.url)&&seen.add(i.url));
  let allResults = [...websiteItems.slice(0,websiteTake), ...githubItems.slice(0,githubTake)];
  if (allResults.length < pageSize) { const rem=[...websiteItems.slice(websiteTake),...githubItems.slice(githubTake)].sort((a,b)=>a.priority-b.priority||b.score-a.score); allResults=[...allResults,...rem].slice(0,pageSize); }
  allResults.sort((a,b)=>a.priority-b.priority||b.score-a.score);
  const docIdToUrl={}; [...websiteItems,...githubItems].forEach(i=>{ if(i.raw.document?.id) docIdToUrl[i.raw.document.id]=i.url; });
  let references = (websiteData?.summary?.summaryWithMetadata?.references||[]).map(ref=>{ const docId=ref.document?.split('/').pop(), uri=docIdToUrl[docId]||null, src=getSource(uri); return {title:ref.title,uri,docId,source:src,priority:sourcePriorityMap[src]||999}; }).sort((a,b)=>a.priority-b.priority);
  const results = allResults.map(i=>({ id:i.raw.document?.id, title:i.derived?.title||i.structData?.title||null, url:i.url, snippet:stripHtml(i.derived?.snippets?.[0]?.snippet||i.structData?.content?.slice(0,300)||null), source:i.source, priority:i.priority, section:i.url.replace(/^https:\/\/[^\/]+\//,'').split('/')?.[0]||'', type:i.structData?.type||null, repo:i.structData?.repo||null, state:i.structData?.state||null })).slice(0,pageSize);
  res.json({ summary: (websiteData?.summary?.summaryText ? {summaryText:websiteData.summary.summaryText, citations:references} : null), results });
};
function buildPreamble(context) {
  const base = `You are a search assistant for Interlisp.org. ... Citation Priorities: 1. www.interlisp.org/interlisp.org →2. *.interlisp.org (files/primer/online) →3. GitHub (issues/PRs/discussions) →4. source files. When both cover topic, cite www. ... Answer in Markdown only.`;
  return context ? `${base}\n\n## Current Context\nThe user is browsing the "${context}" section of www.interlisp.org — prioritize results from that section.` : base;
}
```

### Step 2.2: Test Cloud Function Locally (Optional)

```bash
# Copy updated code to search-function directory
cp index.js search-function/index.js

# Run npm install to ensure dependencies are up to date
cd search-function
npm install

# Test with local function emulator (if you have Google Cloud Functions emulator)
# Or manually test by reviewing the code for syntax errors
node -c index.js  # Check syntax
```

---

## Phase 3: Deploy & Test

### Step 3.1: Deploy Updated Cloud Function (dual-engine blended)

Deployed as `search-00037-xas` (2026-09-02) with two engines for guaranteed website primary + GitHub secondary (70/30, 50/50 for GitHub queries); `0 Untitled` verified.

```bash
#!/bin/bash
# File: deploy-search-function.sh
PROJECT_ID="interlispsearch"
REGION="us-central1"
WEBSITE_ENGINE_ID="interlisp-website-only"   # [interlisp-web-sites_1741606671710] — proven www history/medley
GITHUB_ENGINE_ID="interlisp-github-only"     # [interlisp-github-v2] — issues/PRs/markdown
# Verify engines exist (REST, no gcloud discoveryengine):
# TOKEN=$(gcloud auth application-default print-access-token); curl -s -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: interlispsearch" "https://discoveryengine.googleapis.com/v1/projects/interlispsearch/locations/global/collections/default_collection/engines" | python3 -m json.tool | grep -E '"name"|interlisp-website-only|interlisp-github-only'

echo "Deploying search function to $REGION..."
echo "WEBSITE_ENGINE_ID=$WEBSITE_ENGINE_ID GITHUB_ENGINE_ID=$GITHUB_ENGINE_ID"

gcloud functions deploy search \
  --gen2 \
  --runtime=nodejs24 \
  --region=$REGION \
  --source=. \
  --entry-point=search \
  --trigger-http \
  --allow-unauthenticated \
  --service-account=vertex-search-sa@interlispsearch.iam.gserviceaccount.com \
  --set-env-vars PROJECT_ID=$PROJECT_ID,WEBSITE_ENGINE_ID=$WEBSITE_ENGINE_ID,GITHUB_ENGINE_ID=$GITHUB_ENGINE_ID,ENGINE_ID=$WEBSITE_ENGINE_ID \
  --memory=256Mi \
  --timeout=30s \
  --project=$PROJECT_ID

echo "Deployed: https://$REGION-$PROJECT_ID.cloudfunctions.net/search"
echo "Env: WEBSITE_ENGINE_ID=$WEBSITE_ENGINE_ID GITHUB_ENGINE_ID=$GITHUB_ENGINE_ID"
```

**Then run:**

```bash
chmod +x deploy-search-function.sh
./deploy-search-function.sh
```

### Step 3.2: Verify Deployment

```bash
#!/bin/bash
# File: verify-deployment.sh

PROJECT_ID="interlispsearch"
REGION="us-central1"

echo "Verifying Cloud Function deployment..."
echo ""

gcloud functions describe search \
  --gen2 \
  --region=$REGION \
  --project=$PROJECT_ID \
  --format=json | python3 -m json.tool

echo ""
echo "Function URL: https://$REGION-$PROJECT_ID.cloudfunctions.net/search"
echo ""
echo "Testing function with sample query..."
curl -s "https://$REGION-$PROJECT_ID.cloudfunctions.net/search?q=interlisp&pageSize=5" \
  | python3 -m json.tool | head -50
```

**Run it:**

```bash
chmod +x verify-deployment.sh
./verify-deployment.sh
```

### Step 3.3: Test Citation Preference

```bash
#!/bin/bash
# File: test-citations.sh

FUNCTION_URL="https://us-central1-interlispsearch.cloudfunctions.net/search"

echo "Testing citation preference..."
echo ""

# Test 1: General query (should cite interlisp.org first)
echo "Test 1: Query 'interlisp' (should cite website first)"
echo "=========================================="
curl -s "$FUNCTION_URL?q=interlisp&pageSize=10" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('summary') and data['summary'].get('citations'):
    for i, citation in enumerate(data['summary']['citations'][:3], 1):
        print(f\"[{i}] {citation.get('title', 'Untitled')}\")
        print(f\"    URI: {citation.get('uri', 'N/A')}\")
        print()
else:
    print('No citations found')
"
echo ""

# Test 2: Check first result URL
echo "Test 2: First result should be from interlisp.org"
echo "=========================================="
curl -s "$FUNCTION_URL?q=medley&pageSize=5" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('results'):
    result = data['results'][0]
    print(f\"Title: {result.get('title')}\")
    print(f\"URL: {result.get('url')}\")
    print(f\"Source: {result.get('source')}\")
    print(f\"Priority: {result.get('priority')}\")
else:
    print('No results found')
"
echo ""

# Test 3: Verify GitHub content still appears
echo "Test 3: GitHub content should still appear in results"
echo "=========================================="
curl -s "$FUNCTION_URL?q=github&pageSize=20" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('results'):
    github_results = [r for r in data['results'] if 'github' in r.get('url', '')]
    print(f\"Found {len(github_results)} GitHub results\")
    for r in github_results[:2]:
        print(f\"  - {r.get('title')}\")
        print(f\"    {r.get('url')}\")
else:
    print('No results found')
"
```

**Run it:**

```bash
chmod +x test-citations.sh
./test-citations.sh
```

---

## Phase 4: Set Up Automation

### Step 4.1: Create Website Recrawl Function

**File: `search-function/trigger-website-recrawl.js`** (targets proven website store — not the fresh `interlisp-search-unified` crawl)

```javascript
'use strict';

const { GoogleAuth } = require('google-auth-library');

const PROJECT_ID = 'interlispsearch';
const LOCATION = 'global';
const DATA_STORE_ID = 'interlisp-web-sites_1741606671710'; // proven *.interlisp.org/* SUCCEEDED; NOT interlisp-search-unified

const auth = new GoogleAuth({
  scopes: ['https://www.googleapis.com/auth/cloud-platform']
});

exports.recrawlWebsite = async (message, context) => {
  console.log(`[${new Date().toISOString()}] Starting website recrawl...`);
  
  try {
    const client = await auth.getClient();
    const token = await client.getAccessToken();
    
    // Get target sites
    const targetSitesUrl = `https://discoveryengine.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION}/collections/default_collection/dataStores/${DATA_STORE_ID}/siteSearchEngine/targetSites`;
    
    console.log(`Fetching target sites from: ${targetSitesUrl}`);
    
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
    
    console.log(`Found ${targetSites.length} target sites`);
    
    if (targetSites.length === 0) {
      console.warn('No target sites found. Data store may not be initialized.');
      return;
    }
    
    // Trigger recrawl for each target site
    const recrawlResults = [];
    
    for (const site of targetSites) {
      try {
        console.log(`Triggering recrawl for: ${site.providedUriPattern}`);
        
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
          const errorText = await recrawlResponse.text();
          console.error(`Recrawl failed for ${site.providedUriPattern}: ${recrawlResponse.statusText}`);
          console.error(`Error details: ${errorText}`);
          recrawlResults.push({
            pattern: site.providedUriPattern,
            status: 'FAILED',
            error: recrawlResponse.statusText
          });
        } else {
          const recrawlData = await recrawlResponse.json();
          console.log(`Recrawl triggered for ${site.providedUriPattern}`);
          console.log(`Operation: ${recrawlData.name}`);
          recrawlResults.push({
            pattern: site.providedUriPattern,
            status: 'SUCCESS',
            operation: recrawlData.name
          });
        }
      } catch (siteError) {
        console.error(`Error recrawling ${site.providedUriPattern}:`, siteError.message);
        recrawlResults.push({
          pattern: site.providedUriPattern,
          status: 'ERROR',
          error: siteError.message
        });
      }
    }
    
    console.log(`[${new Date().toISOString()}] Website recrawl completed`);
    console.log(JSON.stringify(recrawlResults, null, 2));
    
    return recrawlResults;
    
  } catch (err) {
    console.error(`[${new Date().toISOString()}] Recrawl error:`, err);
    throw err;
  }
};
```

**Deploy recrawl function:**

```bash
gcloud functions deploy trigger-website-recrawl \
  --gen2 \
  --runtime=nodejs24 \
  --region=us-central1 \
  --source=./search-function \
  --entry-point=recrawlWebsite \
  --trigger-topic=recrawl-website \
  --service-account=vertex-search-sa@interlispsearch.iam.gserviceaccount.com \
  --memory=256Mi \
  --timeout=60s \
  --project=interlispsearch
```

### Step 4.2: Create GitHub Reimport Function — Implemented (future-proof schema, `branches/0`, sanitized ids)

**File: `search-function/github-reimport.js`** (structured GitHub store `interlisp-github-v2`, NOT website store)

```javascript
'use strict';

const { GoogleAuth } = require('google-auth-library');
const { Storage } = require('@google-cloud/storage');

const PROJECT_ID = 'interlispsearch';
const LOCATION = 'global';
// Structured GitHub store — NOT the website store. Keeps website crawl separate
// and is consumed via interlisp-github-only engine (blended 70/30 in search function).
// Fallback engine interlisp-search-unified ([interlisp-web-sites_1741606671710, interlisp-github-v2]) retained.
const DATA_STORE_ID = 'interlisp-github-v2';
const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const GITHUB_ORG = 'Interlisp';
const GITHUB_REPOS = ['medley', 'maiko', 'Interlisp.github.io'];

// Schema (future-proof, patched 2026-09-02): default_schema title/url/repo/type/state/author/number etc. all retrievable:true
// so search-function/index.js:193-195 title: derived.title || structData.title resolves and frontend never shows "Untitled".
// JSONL shape: {"id": sanitized, "structData":{id,title,url,content,source,priority,repo,type,state,number,created_at,last_indexed,…}}
// sanitized id: Interlisp.github.io → Interlisp-github-io, branches/0 not default

// Shared-source re-export: search-function/index.js re-exports reimportGithub so same dir can serve both entry-points:
// try { exports.reimportGithub = require('./github-reimport').reimportGithub; } catch(_) {}

const auth = new GoogleAuth({
  scopes: ['https://www.googleapis.com/auth/cloud-platform']
});

const storage = new Storage({ projectId: PROJECT_ID });

exports.reimportGithub = async (message, context) => {
  console.log(`[${new Date().toISOString()}] Starting GitHub reimport...`);
  
  try {
    // 1. Fetch GitHub content
    const gitHubDocuments = [];
    
    console.log('Fetching GitHub Issues...');
    const issues = await fetchGitHubIssues();
    gitHubDocuments.push(...issues);
    console.log(`Fetched ${issues.length} GitHub issues`);
    
    console.log('Fetching GitHub Pull Requests...');
    const prs = await fetchGitHubPullRequests();
    gitHubDocuments.push(...prs);
    console.log(`Fetched ${prs.length} GitHub pull requests`);
    
    console.log('Fetching GitHub Markdown files...');
    const markdownFiles = await fetchGitHubMarkdown();
    gitHubDocuments.push(...markdownFiles);
    console.log(`Fetched ${markdownFiles.length} GitHub markdown files`);
    
    if (gitHubDocuments.length === 0) {
      console.warn('No GitHub documents fetched. Check GitHub token and repo access.');
      return { status: 'NO_DOCUMENTS', count: 0 };
    }
    
    // 2. Convert to JSONL format — interlisp-github-v2 is NO_CONTENT: each line is
    // {id, structData:{...}} with sanitized id ^[a-zA-Z0-9-_]+$ on branches/0 (see guide 1.6). Future-proof: all display fields retrievable.
    const sanitizeId = (id) => id.replace(/\./g, '-').replace(/[^a-zA-Z0-9-_]/g, '-');
    console.log(`Converting ${gitHubDocuments.length} documents to JSONL (structData, branches/0, sanitized ids, future-proof schema)...`);
    const jsonlLines = gitHubDocuments.map(doc => {
      const rawId = doc.id; const sid = sanitizeId(rawId);
      const m = doc.metadata || {};
      const structData = { id: sid, title: doc.title||'', url: doc.url||'', content: doc.content||'', source: m.source||'github', priority: m.priority||3, type: m.content_type||null, content_type: m.content_type||null, repo: m.repo||null, state: m.state||null, number: m.issue_number||m.pr_number||m.number||null, issue_number: m.issue_number||null, pr_number: m.pr_number||null, file: m.file||null, created_at: m.created_date||null, updated_at: m.updated_date||null, created_date: m.created_date||null, updated_date: m.updated_date||null, last_indexed: m.last_indexed||new Date().toISOString() };
      Object.keys(structData).forEach(k => structData[k]==null && delete structData[k]);
      return JSON.stringify({ id: sid, structData });
    });
    const jsonlContent = jsonlLines.join('\n');
    
    // 3. Upload JSONL to Cloud Storage
    const bucketName = `${PROJECT_ID}-search-imports`;
    const fileName = `github-import-${Date.now()}.jsonl`;
    
    console.log(`Creating Cloud Storage bucket if needed: ${bucketName}`);
    const bucket = storage.bucket(bucketName);
    
    try {
      await bucket.exists();
    } catch (e) {
      console.log(`Creating bucket: ${bucketName}`);
      await storage.createBucket(bucketName, { location: 'US' });
    }
    
    console.log(`Uploading JSONL to gs://${bucketName}/${fileName}`);
    const file = bucket.file(fileName);
    await file.save(jsonlContent);
    
    // 4. Call Vertex AI importDocuments API
    const client = await auth.getClient();
    const token = await client.getAccessToken();
    
    const importUrl = `https://discoveryengine.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION}/collections/default_collection/dataStores/${DATA_STORE_ID}/branches/0/documents:import`; // branches/0, not default
    
    console.log(`Calling Vertex AI import API: ${importUrl}`);
    
    const importResponse = await fetch(importUrl, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token.token}`,
        'Content-Type': 'application/json',
        'x-goog-user-project': PROJECT_ID
      },
      body: JSON.stringify({
        gcsSource: {
          inputUris: [`gs://${bucketName}/${fileName}`]
        }
      })
    });
    
    if (!importResponse.ok) {
      const errorText = await importResponse.text();
      throw new Error(`Import failed: ${importResponse.statusText} - ${errorText}`);
    }
    
    const importData = await importResponse.json();
    console.log(`Import operation started: ${importData.name}`);
    console.log(`[${new Date().toISOString()}] GitHub reimport completed successfully`);
    
    return {
      status: 'SUCCESS',
      documentsImported: gitHubDocuments.length,
      operation: importData.name,
      gcsLocation: `gs://${bucketName}/${fileName}`
    };
    
  } catch (err) {
    console.error(`[${new Date().toISOString()}] GitHub reimport error:`, err);
    throw err;
  }
};

async function fetchGitHubIssues() {
  const issues = [];
  
  for (const repo of GITHUB_REPOS) {
    try {
      const url = `https://api.github.com/repos/${GITHUB_ORG}/${repo}/issues?state=all&per_page=100`;
      const response = await fetch(url, {
        headers: {
          'Authorization': `token ${GITHUB_TOKEN}`,
          'Accept': 'application/vnd.github.v3+json'
        }
      });
      
      if (!response.ok) {
        console.warn(`Failed to fetch issues from ${GITHUB_ORG}/${repo}: ${response.statusText}`);
        continue;
      }
      
      const repoIssues = await response.json();
      
      for (const issue of repoIssues) {
        issues.push({
          id: `github-issue-${repo}-${issue.number}`,
          title: issue.title,
          url: issue.html_url,
          content: issue.body || '',
          metadata: {
            source: 'github',
            priority: 3,
            content_type: 'issue',
            repo: `${GITHUB_ORG}/${repo}`,
            issue_number: issue.number,
            state: issue.state,
            created_date: issue.created_at,
            updated_date: issue.updated_at,
            last_indexed: new Date().toISOString()
          }
        });
      }
    } catch (err) {
      console.error(`Error fetching issues from ${GITHUB_ORG}/${repo}:`, err.message);
    }
  }
  
  return issues;
}

async function fetchGitHubPullRequests() {
  const prs = [];
  
  for (const repo of GITHUB_REPOS) {
    try {
      const url = `https://api.github.com/repos/${GITHUB_ORG}/${repo}/pulls?state=all&per_page=100`;
      const response = await fetch(url, {
        headers: {
          'Authorization': `token ${GITHUB_TOKEN}`,
          'Accept': 'application/vnd.github.v3+json'
        }
      });
      
      if (!response.ok) {
        console.warn(`Failed to fetch PRs from ${GITHUB_ORG}/${repo}: ${response.statusText}`);
        continue;
      }
      
      const repoPrs = await response.json();
      
      for (const pr of repoPrs) {
        prs.push({
          id: `github-pr-${repo}-${pr.number}`,
          title: pr.title,
          url: pr.html_url,
          content: (pr.body || '') + '\n' + (pr.title || ''),
          metadata: {
            source: 'github',
            priority: 3,
            content_type: 'pull_request',
            repo: `${GITHUB_ORG}/${repo}`,
            pr_number: pr.number,
            state: pr.state,
            created_date: pr.created_at,
            updated_date: pr.updated_at,
            last_indexed: new Date().toISOString()
          }
        });
      }
    } catch (err) {
      console.error(`Error fetching PRs from ${GITHUB_ORG}/${repo}:`, err.message);
    }
  }
  
  return prs;
}

async function fetchGitHubMarkdown() {
  const markdownFiles = [];
  
  for (const repo of GITHUB_REPOS) {
    try {
      // Fetch README
      const readmeUrl = `https://api.github.com/repos/${GITHUB_ORG}/${repo}/readme`;
      const readmeResponse = await fetch(readmeUrl, {
        headers: {
          'Authorization': `token ${GITHUB_TOKEN}`,
          'Accept': 'application/vnd.github.v3.raw'
        }
      });
      
      if (readmeResponse.ok) {
        const content = await readmeResponse.text();
        markdownFiles.push({
          id: `github-markdown-${repo}-README`,
          title: `${repo} README`,
          url: `https://github.com/${GITHUB_ORG}/${repo}/blob/main/README.md`,
          content: content,
          metadata: {
            source: 'github',
            priority: 3,
            content_type: 'markdown',
            repo: `${GITHUB_ORG}/${repo}`,
            file: 'README.md',
            last_indexed: new Date().toISOString()
          }
        });
      }
    } catch (err) {
      console.warn(`No README found in ${GITHUB_ORG}/${repo}`);
    }
  }
  
  return markdownFiles;
}
```

**Deploy GitHub reimport function:**

First, create or get a GitHub token:

```bash
# You can generate one at: https://github.com/settings/tokens
# Needs: repo (full), read:org permissions

export GITHUB_TOKEN="your_github_token_here"

gcloud functions deploy github-reimport \
  --gen2 \
  --runtime=nodejs24 \
  --region=us-central1 \
  --source=./search-function \
  --entry-point=reimportGithub \
  --trigger-topic=reimport-github \
  --service-account=vertex-search-sa@interlispsearch.iam.gserviceaccount.com \
  --set-env-vars GITHUB_TOKEN=$GITHUB_TOKEN \
  --memory=512Mi \
  --timeout=300s \
  --project=interlispsearch
```

### Step 4.3: Create Cloud Scheduler Jobs

**Daily Website Recrawl (2 AM UTC):**

```bash
gcloud scheduler jobs create pubsub recrawl-website-daily \
  --location=us-central1 \
  --schedule="0 2 * * *" \
  --timezone="UTC" \
  --topic=recrawl-website \
  --message-body='{"action":"recrawl","timestamp":"$(date -u +%Y-%m-%dT%H:%M:%SZ)"}' \
  --project=interlispsearch
```

**Weekly GitHub Reimport (Monday 3 AM UTC):**

```bash
gcloud scheduler jobs create pubsub reimport-github-weekly \
  --location=us-central1 \
  --schedule="0 3 * * 1" \
  --timezone="UTC" \
  --topic=reimport-github \
  --message-body='{"action":"reimport","timestamp":"$(date -u +%Y-%m-%dT%H:%M:%SZ)"}' \
  --project=interlispsearch
```

**Verify jobs created:**

```bash
gcloud scheduler jobs list --location=us-central1 --project=interlispsearch
```

### Step 4.4: Test Automation (Optional)

**Manually trigger recrawl:**

```bash
gcloud scheduler jobs run recrawl-website-daily \
  --location=us-central1 \
  --project=interlispsearch
```

**Manually trigger GitHub reimport:**

```bash
gcloud scheduler jobs run reimport-github-weekly \
  --location=us-central1 \
  --project=interlispsearch
```

**Check logs:**

```bash
gcloud functions logs read trigger-website-recrawl \
  --gen2 \
  --region=us-central1 \
  --limit=20 \
  --project=interlispsearch

gcloud functions logs read github-reimport \
  --gen2 \
  --region=us-central1 \
  --limit=20 \
  --project=interlispsearch
```

---

## Testing Checklist — Implemented (dual-engine blended, 0 Untitled verified 2026-09-02)

Use this checklist to validate the implementation at each phase.

### Before Deployment

- [x] Proven website store `interlisp-web-sites_1741606671710` (`*.interlisp.org/*` `SUCCEEDED`) confirmed — fresh `interlisp-search-unified` website store (`interlisp.org/*`+`files`) also `SUCCEEDED` but not used for serving
- [x] GitHub store `interlisp-github-v2` schema patched future-proof (`title/url/repo/type/state/author/number` `retrievable:true`; `PATCH …/schemas/default_schema`)
- [x] Target sites `*.interlisp.org/*` verified `SUCCEEDED` (proven store)
- [x] GitHub import `branches/0` `structData` sanitized (`Interlisp.github.io`→`Interlisp-github-io`) `successCount 350/350` via local one-off `GITHUB_TOKEN=$(gh auth token) node /tmp/local_import_simple.js` → `gs://interlispsearch-search-imports/github-import-*.jsonl`
- [x] Engines `interlisp-website-only` `[interlisp-web-sites_…]` + `interlisp-github-only` `[interlisp-github-v2]` + fallback `interlisp-search-unified` `[both]` exist
- [x] Cloud Function `search-00037-xas` dual-fetch blended (70/30, 50/50 for `github|issue|pr|discussion`) with `website-primary:1 → website-secondary:2 → github:3`, dedup by `url`, `priority→semanticRelevanceScore`
- [x] No syntax errors (`node -c index.js`, `npm run lint` — 5 warnings allowed)

### After Cloud Function Deployment — Verified 2026-09-02

**Test URL:** `https://us-central1-interlispsearch.cloudfunctions.net/search` (`search-00037-xas` `WEBSITE_ENGINE_ID=interlisp-website-only` `GITHUB_ENGINE_ID=interlisp-github-only`)

- [x] **Health check:** `?q=test` returns results without errors
- [x] **Website prioritization:** First result is `website-primary` `interlisp.org` (not github.com)
- [x] **Citation preference:** First citation is `website-primary` `interlisp.org` (not github.com)
- [x] **GitHub still present (blended):** `?q=github` 5+5 (50/50), `?q=interlisp` 7+3 (70/30) — `github|issue|pr|discussion` triggers 50/50
- [x] **No Untitled:** `github/medley/pull request/issue/screenshots/FONTSAVAILABLE` all `title` non-null (schema patch `retrievable:true` + `derived.title || structData.title`)
- [x] **Repo/type/state chips:** `Interlisp/medley` etc. visible (structData retrievable)
- [x] **Summary quality:** Summaries accurate with `www` preamble preference
- [x] **Response time:** Queries complete in <5 seconds (fetch 20 each, parallel)
- [x] **Error handling:** Errors return proper HTTP status codes

**Sample test queries:**

```bash
# Test 1: Basic query
curl -s "https://us-central1-interlispsearch.cloudfunctions.net/search?q=interlisp&pageSize=10" | jq '.results[0]'

# Test 2: Citation preference
curl -s "https://us-central1-interlispsearch.cloudfunctions.net/search?q=medley&pageSize=10" | jq '.summary.citations[0]'

# Test 3: GitHub content availability
curl -s "https://us-central1-interlispsearch.cloudfunctions.net/search?q=github&pageSize=20" | jq '.results | map(.url) | map(select(contains("github")))'

# Test 4: Error handling (missing query)
curl -s "https://us-central1-interlispsearch.cloudfunctions.net/search?q=" | jq '.'

# Test 5: Rate limiting (run 25 times quickly)
for i in {1..25}; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://us-central1-interlispsearch.cloudfunctions.net/search?q=test")
  echo "Request $i: $STATUS"
done
```

### After Automation Deployment

- [ ] **Recrawl function deployed:** `trigger-website-recrawl` is active
- [ ] **GitHub reimport function deployed:** `github-reimport` is active
- [ ] **Cloud Scheduler jobs created:** Both jobs listed in scheduler
- [ ] **Manual trigger test:** Recrawl can be triggered manually and succeeds
- [ ] **Manual trigger test:** GitHub reimport can be triggered manually and succeeds
- [ ] **Function logs:** No errors in recrawl/reimport function logs
- [ ] **Scheduled execution:** Jobs execute at scheduled times

**Check scheduled job status:**

```bash
gcloud scheduler jobs describe recrawl-website-daily --location=us-central1 --project=interlispsearch
gcloud scheduler jobs describe reimport-github-weekly --location=us-central1 --project=interlispsearch
```

---

## Rollback Procedures

If issues arise, use these procedures to roll back to a known good state.

### Rollback Cloud Function to Previous Version

**Option 1: Restore from Git**

```bash
cd search-function

# Restore previous index.js
git checkout HEAD~1 index.js

# Redeploy
gcloud functions deploy search \
  --gen2 \
  --runtime=nodejs24 \
  --region=us-central1 \
  --source=. \
  --entry-point=search \
  --trigger-http \
  --allow-unauthenticated \
  --service-account=vertex-search-sa@interlispsearch.iam.gserviceaccount.com \
  --set-env-vars PROJECT_ID=interlispsearch,ENGINE_ID=interlisp-org-search_1768860477660 \
  --memory=256Mi \
  --timeout=30s \
  --project=interlispsearch
```

**Option 2: Switch Engine Back to Previous Data Store**

```bash
# Deploy current code but point to old engine
gcloud functions deploy search \
  --gen2 \
  --runtime=nodejs24 \
  --region=us-central1 \
  --source=./search-function \
  --entry-point=search \
  --trigger-http \
  --allow-unauthenticated \
  --service-account=vertex-search-sa@interlispsearch.iam.gserviceaccount.com \
  --set-env-vars PROJECT_ID=interlispsearch,ENGINE_ID=interlisp-org-search_1768860477660 \
  --memory=256Mi \
  --timeout=30s \
  --project=interlispsearch
```

### Disable Automation (if causing issues)

```bash
# Pause scheduler jobs
gcloud scheduler jobs pause recrawl-website-daily --location=us-central1 --project=interlispsearch
gcloud scheduler jobs pause reimport-github-weekly --location=us-central1 --project=interlispsearch

# Resume when ready
gcloud scheduler jobs resume recrawl-website-daily --location=us-central1 --project=interlispsearch
gcloud scheduler jobs resume reimport-github-weekly --location=us-central1 --project=interlispsearch
```

### Delete and Recreate Automation Functions

```bash
# Delete functions if broken
gcloud functions delete trigger-website-recrawl --gen2 --region=us-central1 --project=interlispsearch --quiet
gcloud functions delete github-reimport --gen2 --region=us-central1 --project=interlispsearch --quiet

# Then redeploy with corrected code
# (See Phase 4 deployment steps)
```

---

## Monitoring & Troubleshooting

### View Cloud Function Logs

```bash
# Search function logs (real-time)
gcloud functions logs read search --gen2 --region=us-central1 --limit=50 --follow --project=interlispsearch

# Recrawl function logs
gcloud functions logs read trigger-website-recrawl --gen2 --region=us-central1 --limit=50 --project=interlispsearch

# GitHub reimport logs
gcloud functions logs read github-reimport --gen2 --region=us-central1 --limit=50 --project=interlispsearch
```

### Check Data Store Indexing Status

```bash
#!/bin/bash
# File: check-datastore-status.sh

PROJECT_ID="interlispsearch"
DATA_STORE_ID="interlisp-search-unified"
LOCATION="global"

TOKEN=$(gcloud auth application-default print-access-token)

curl -s -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: $PROJECT_ID" \
  "https://discoveryengine.googleapis.com/v1/projects/$PROJECT_ID/locations/$LOCATION/collections/default_collection/dataStores/$DATA_STORE_ID/siteSearchEngine/targetSites" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
print('Data Store: interlisp-search-unified')
print('='*50)
if 'targetSites' in data:
    for site in data['targetSites']:
        print(f\"URI Pattern: {site.get('providedUriPattern')}\")
        print(f\"Status: {site.get('indexingStatus', 'UNKNOWN')}\")
        print(f\"Type: {site.get('type')}\")
        if site.get('failureReasons'):
            print(f\"Failures: {site['failureReasons']}\")
        print()
else:
    print('No target sites found')
    print(json.dumps(data, indent=2))
"
```

### Common Issues & Fixes

#### Issue: "indexingStatus: FAILED"

**Cause:** Website structure incompatible with crawler

**Fix:**
1. Check if robots.txt is blocking crawler
2. Verify URL patterns are correct (no `https://` prefix needed)
3. Check GCP Console logs for specific errors
4. Retry upgrade to Advanced indexing

#### Issue: "403 Forbidden" on API calls

**Cause:** Service account lacks permissions

**Fix:**
```bash
# Verify service account has required roles
gcloud projects get-iam-policy interlispsearch \
  --flatten="bindings[].members" \
  --format='table(bindings.role)' \
  --filter="bindings.members:vertex-search-sa*"
```

#### Issue: Cloud Function returns empty results

**Cause:** ENGINE_ID points to data store that hasn't finished indexing

**Fix:**
1. Wait for indexing to complete (check target sites status)
2. Verify ENGINE_ID matches actual engine ID
3. Test with sample query via GCP Console first

#### Issue: GitHub documents not appearing

**Cause:** GitHub reimport function failed or GitHub token expired

**Fix:**
```bash
# Check recent logs
gcloud functions logs read github-reimport --gen2 --region=us-central1 --limit=30 --project=interlispsearch

# Manually trigger to see detailed error
gcloud scheduler jobs run reimport-github-weekly --location=us-central1 --project=interlispsearch

# Verify GitHub token is still valid
# Regenerate at: https://github.com/settings/tokens
```

### Monitoring Setup (Optional)

Create Cloud Monitoring alerts for failures:

```bash
# Create alert for Cloud Function errors
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="Search Function Errors" \
  --condition-display-name="Search function error rate > 5%" \
  --condition-threshold-value=0.05 \
  --condition-threshold-duration=300s
```

---

## Appendix: Script Reference

All scripts mentioned in this guide are collected here for easy reference.

### Complete Deployment Checklist Script

```bash
#!/bin/bash
# File: deployment-checklist.sh

echo "==============================================="
echo "INTERLISP SEARCH - UNIFIED DATA STORE CHECKLIST"
echo "==============================================="
echo ""

PROJECT_ID="interlispsearch"
DATA_STORE_ID="interlisp-search-unified"
LOCATION="global"
REGION="us-central1"

# Check 1: Unified data store exists (REST API — no gcloud CLI)
echo "[1/8] Checking unified data store..."
TOKEN=$(gcloud auth application-default print-access-token 2>/dev/null)
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: $PROJECT_ID" "https://discoveryengine.googleapis.com/v1/projects/$PROJECT_ID/locations/$LOCATION/collections/default_collection/dataStores/$DATA_STORE_ID")
if [ "$HTTP_CODE" = "200" ]; then
    echo "  ✓ Data store exists"
else
    echo "  ✗ Data store not found (HTTP $HTTP_CODE)"
fi
echo ""

# Check 2: Target sites configured
echo "[2/8] Checking target sites..."
TOKEN=$(gcloud auth application-default print-access-token)
RESPONSE=$(curl -s -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: $PROJECT_ID" \
  "https://discoveryengine.googleapis.com/v1/projects/$PROJECT_ID/locations/$LOCATION/collections/default_collection/dataStores/$DATA_STORE_ID/siteSearchEngine/targetSites")
SITE_COUNT=$(echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('targetSites', [])))")
echo "  Found $SITE_COUNT target sites"
echo ""

# Check 3: Cloud Function deployed
echo "[3/8] Checking search Cloud Function..."
if gcloud functions describe search --gen2 --region=$REGION --project=$PROJECT_ID &>/dev/null; then
    ENGINE_ID=$(gcloud functions describe search --gen2 --region=$REGION --project=$PROJECT_ID --format='value(environmentVariables.ENGINE_ID)')
    echo "  ✓ Function deployed"
    echo "  ENGINE_ID: $ENGINE_ID"
else
    echo "  ✗ Function not deployed"
fi
echo ""

# Check 4: Recrawl function deployed
echo "[4/8] Checking website recrawl function..."
if gcloud functions describe trigger-website-recrawl --gen2 --region=$REGION --project=$PROJECT_ID &>/dev/null; then
    echo "  ✓ Function deployed"
else
    echo "  ✗ Function not deployed"
fi
echo ""

# Check 5: GitHub reimport function deployed
echo "[5/8] Checking GitHub reimport function..."
if gcloud functions describe github-reimport --gen2 --region=$REGION --project=$PROJECT_ID &>/dev/null; then
    echo "  ✓ Function deployed"
else
    echo "  ✗ Function not deployed"
fi
echo ""

# Check 6: Scheduler jobs configured
echo "[6/8] Checking Cloud Scheduler jobs..."
RECRAWL_EXISTS=$(gcloud scheduler jobs list --location=us-central1 --filter="name:recrawl-website-daily" --project=$PROJECT_ID --format='value(name)' 2>/dev/null)
REIMPORT_EXISTS=$(gcloud scheduler jobs list --location=us-central1 --filter="name:reimport-github-weekly" --project=$PROJECT_ID --format='value(name)' 2>/dev/null)

[ -n "$RECRAWL_EXISTS" ] && echo "  ✓ Recrawl job exists" || echo "  ✗ Recrawl job missing"
[ -n "$REIMPORT_EXISTS" ] && echo "  ✓ Reimport job exists" || echo "  ✗ Reimport job missing"
echo ""

# Check 7: Service account permissions
echo "[7/8] Checking service account permissions..."
SA_EMAIL="vertex-search-sa@interlispsearch.iam.gserviceaccount.com"
ROLES=$(gcloud projects get-iam-policy $PROJECT_ID \
  --flatten="bindings[].members" \
  --format='value(bindings.role)' \
  --filter="bindings.members:$SA_EMAIL" 2>/dev/null | wc -l)
echo "  Service account has $ROLES roles assigned"
echo ""

# Check 8: Test search function
echo "[8/8] Testing search function..."
FUNCTION_URL="https://$REGION-$PROJECT_ID.cloudfunctions.net/search"
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$FUNCTION_URL?q=test&pageSize=5")
if [ "$HTTP_STATUS" = "200" ]; then
    echo "  ✓ Function responsive (HTTP $HTTP_STATUS)"
else
    echo "  ✗ Function returned HTTP $HTTP_STATUS"
fi
echo ""

echo "==============================================="
echo "CHECKLIST COMPLETE"
echo "==============================================="
```

**Run it:**

```bash
chmod +x deployment-checklist.sh
./deployment-checklist.sh
```

---

## Phase 7: Cleanup — Pare interlispsearch to In-Use Resources Only

**Goal:** After dual-engine blended (`interlisp-website-only` + `interlisp-github-only` + fallback `interlisp-search-unified`) is validated in production (≥48h serving traffic, verified 2026-09-02 `search-00037-xas`), delete the “large collection of data stores” and any other stale resources so `interlispsearch` contains only the keep-list below. Run only after Phases 1–4 are complete and `0 Untitled` matrix passes.

**Keep list (do NOT delete):**

| Type | Name |
|---|---|
| Data store | `interlisp-web-sites_1741606671710` (proven website `*.interlisp.org/*` SUCCEEDED) |
| Data store | `interlisp-github-v2` (structured `NO_CONTENT` `branches/0` future-proof schema) |
| Data store | `interlisp-search-unified` (fresh website store `PUBLIC_WEBSITE` interlisp.org/*+files — retained, not used for serving) |
| Engine | `interlisp-website-only` (`[interlisp-web-sites_1741606671710]`) — primary |
| Engine | `interlisp-github-only` (`[interlisp-github-v2]`) — secondary |
| Engine | `interlisp-search-unified` (`[interlisp-web-sites_1741606671710, interlisp-github-v2]`) — fallback |
| Cloud Functions (Gen2, us-central1) | `search` (`search-00037-xas`), `github-reimport` (needs isolated source dir for Pub/Sub; re-export via `index.js`) |
| Cloud Scheduler (us-central1) | `reimport-github-weekly` (deferred weekly until isolated deploy; manual local one-off active), `recrawl-website-daily` if kept |
| Firestore | Database + `rate_limits` collection (TTL on `updatedAt`) |
| Cloud Storage | `interlispsearch-search-imports` bucket (prune old `github-import-*.jsonl` objects only) |
| IAM | `vertex-search-sa@` service account + org-policy overrides |

Everything else — `interlisp-search-v3`, `interlisp-org-search_1768860477660`, `interlisp-site-search`, `interlisp-document-bucket_1741737147622`, `lispcore_…`, `medley-interlisp-core_…` if superseded, `interlisp-github` (old `CONTENT_REQUIRED`), test engines/stores, stale functions/jobs, old import objects — is a **delete candidate**. Keep `interlisp-github-v2` and `interlisp-web-sites_1741606671710` plus the three engines above.

### Step 7.1: Inventory (read-only, save for review)

```bash
#!/bin/bash
# File: inventory-interlispsearch.sh — run BEFORE any deletes
set -e
PROJECT_ID="interlispsearch"
LOCATION="global"
REGION="us-central1"
OUTDIR="/tmp/interlispsearch-inventory-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$OUTDIR"
TOKEN=$(gcloud auth application-default print-access-token)

echo "Inventory -> $OUTDIR"

# 1. Data stores (REST — no gcloud CLI)
curl -s -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: $PROJECT_ID" \
  "https://discoveryengine.googleapis.com/v1/projects/$PROJECT_ID/locations/$LOCATION/collections/default_collection/dataStores?pageSize=100" \
  | python3 -m json.tool > "$OUTDIR/datastores.json"
echo "dataStores -> $OUTDIR/datastores.json"
cat "$OUTDIR/datastores.json" | python3 -c "import json; d=json.load(open('$OUTDIR/datastores.json')); print(f\"  {len(d.get('dataStores',[]))} data stores\")"

# 2. Engines / search apps
curl -s -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: $PROJECT_ID" \
  "https://discoveryengine.googleapis.com/v1/projects/$PROJECT_ID/locations/$LOCATION/collections/default_collection/engines?pageSize=100" \
  | python3 -m json.tool > "$OUTDIR/engines.json"
cat "$OUTDIR/engines.json" | python3 -c "import json; d=json.load(open('$OUTDIR/engines.json')); print(f\"  {len(d.get('engines',[]))} engines\")"

# 3. Target sites for each data store (helps decide what to keep)
python3 -c "
import json
d=json.load(open('$OUTDIR/datastores.json'))
for ds in d.get('dataStores',[]):
    print(ds['name'].split('/')[-1], '—', ds.get('displayName',''))
" > "$OUTDIR/datastore-names.txt"
cat "$OUTDIR/datastore-names.txt"

# 4. Cloud Functions
gcloud functions list --gen2 --region=$REGION --project=$PROJECT_ID --format=json > "$OUTDIR/functions.json" 2>&1 || true
python3 -c "import json; d=json.load(open('$OUTDIR/functions.json')); print(f\"  {len(d)} functions\")" 2>/dev/null || echo "  (functions list requires permissions)"

# 5. Scheduler jobs
gcloud scheduler jobs list --location=$REGION --project=$PROJECT_ID --format=json > "$OUTDIR/scheduler.json" 2>&1 || true

# 6. Storage buckets
gcloud storage ls --project=$PROJECT_ID > "$OUTDIR/storage-ls.txt" 2>&1 || gsutil ls -p $PROJECT_ID > "$OUTDIR/storage-ls.txt" 2>&1 || true
cat "$OUTDIR/storage-ls.txt"

# 7. Firestore collections (console is authoritative)
echo "Firestore: check console -> Firestore -> Data, or: gcloud firestore databases describe --project=$PROJECT_ID"

echo ""
echo "REVIEW $OUTDIR/datastores.json and $OUTDIR/engines.json"
echo "Mark KEEP vs DELETE before running Step 7.2. Commit $OUTDIR to git or share for review."
```

**Review gate:** Open `$OUTDIR/datastores.json` and `$OUTDIR/engines.json`, build a `KEEP = {interlisp-search-unified}` list, and get a second reviewer before any `DELETE`.

### Step 7.2: Delete in Safe Order (engines → data stores → functions → scheduler → storage)

> **Safety:** Each `DELETE` is irreversible. Re-run inventory after each sub-step and verify `curl "https://us-central1-interlispsearch.cloudfunctions.net/search?q=interlisp"` still returns `200`.

```bash
#!/bin/bash
# File: cleanup-interlispsearch.sh — DESTRUCTIVE. Run only after inventory review.
set -e
PROJECT_ID="interlispsearch"
LOCATION="global"
REGION="us-central1"
TOKEN=$(gcloud auth application-default print-access-token)

# KEEP — edit if your unified engine ID differs
KEEP_DATASTORE="interlisp-search-unified"

# --- 1. Engines first (depend on data stores) ---
echo "=== 1. Deleting stale engines (keeping only *$KEEP_DATASTORE*) ==="
ENGINES_JSON=$(curl -s -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: $PROJECT_ID" \
  "https://discoveryengine.googleapis.com/v1/projects/$PROJECT_ID/locations/$LOCATION/collections/default_collection/engines?pageSize=100")
python3 -c "
import json, sys
d=json.loads('''$ENGINES_JSON'''.replace(\"'\", \"'\"))  # placeholder
" 2>&1 | head
# Preferred: iterate with jq/python in a loop:
# For each engine where dataStoreIds != ["interlisp-search-unified"]:
curl -s -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: $PROJECT_ID" \
  "https://discoveryengine.googleapis.com/v1/projects/$PROJECT_ID/locations/$LOCATION/collections/default_collection/engines" \
  | python3 -c "
import json, subprocess, shlex, sys
import json as j
data=json.load(sys.stdin)
for e in data.get('engines',[]):
    name=e['name']
    ds_ids=e.get('dataStoreIds',[])
    eng_id=name.split('/')[-1]
    if ds_ids != ['interlisp-search-unified']:
        print(f'DELETE engine {eng_id} (dataStoreIds={ds_ids})')
        # Uncomment to actually delete:
        # subprocess.run(['curl','-X','DELETE','-H',f'Authorization: Bearer {TOKEN}','-H',f'x-goog-user-project: {PROJECT_ID}',f'https://discoveryengine.googleapis.com/v1/{name}'], check=False)
    else:
        print(f'KEEP   engine {eng_id}')
"

# --- 2. Data stores second (cascades to documents/targetSites) ---
echo ""
echo "=== 2. Deleting stale data stores (keeping $KEEP_DATASTORE) ==="
curl -s -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: $PROJECT_ID" \
  "https://discoveryengine.googleapis.com/v1/projects/$PROJECT_ID/locations/$LOCATION/collections/default_collection/dataStores" \
  | python3 -c "
import json, sys
data=json.load(sys.stdin)
for ds in data.get('dataStores',[]):
    ds_id=ds['name'].split('/')[-1]
    if ds_id != 'interlisp-search-unified':
        print(f'DELETE dataStore {ds_id} ({ds.get(\"displayName\",\"\")})')
        # Uncomment to actually delete:
        # import subprocess, os
        # subprocess.run(['curl','-X','DELETE','-H',f'Authorization: Bearer {os.environ[\"TOKEN\"]}','-H','x-goog-user-project: interlispsearch',f'https://discoveryengine.googleapis.com/v1/projects/interlispsearch/locations/global/collections/default_collection/dataStores/{ds_id}'])
    else:
        print(f'KEEP   dataStore {ds_id}')
"
# Actual delete command for one data store (run after review):
# curl -X DELETE -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: $PROJECT_ID" \
#   "https://discoveryengine.googleapis.com/v1/projects/$PROJECT_ID/locations/$LOCATION/collections/default_collection/dataStores/interlisp-search-v3"
# curl -X DELETE -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: $PROJECT_ID" \
#   "https://discoveryengine.googleapis.com/v1/projects/$PROJECT_ID/locations/$LOCATION/collections/default_collection/dataStores/interlisp-org-search_1768860477660"

# --- 3. Cloud Functions third (not in keep list) ---
echo ""
echo "=== 3. Stale Cloud Functions (review then delete) ==="
gcloud functions list --gen2 --region=$REGION --project=$PROJECT_ID --format="value(name)" 2>/dev/null | while read f; do
  base=$(basename "$f")
  case "$base" in search|trigger-website-recrawl|github-reimport) echo "KEEP   function $base" ;; *) echo "DELETE function $base — run: gcloud functions delete $base --gen2 --region=$REGION --project=$PROJECT_ID" ;; esac
done

# --- 4. Scheduler fourth ---
echo ""
echo "=== 4. Stale Scheduler jobs ==="
gcloud scheduler jobs list --location=$REGION --project=$PROJECT_ID --format="value(name)" 2>/dev/null | while read j; do
  base=$(basename "$j")
  case "$base" in recrawl-website-daily|reimport-github-weekly) echo "KEEP   scheduler $base" ;; *) echo "DELETE scheduler $base — run: gcloud scheduler jobs delete $base --location=$REGION --project=$PROJECT_ID" ;; esac
done

# --- 5. Storage fifth (prune old JSONL only) ---
echo ""
echo "=== 5. Storage — prune old import artifacts (keep bucket) ==="
echo "List: gcloud storage ls gs://interlispsearch-search-imports/ 2>/dev/null || gsutil ls gs://interlispsearch-search-imports/"
echo "Prune older than last successful import:"
echo "  gcloud storage rm gs://interlispsearch-search-imports/github-import-*.jsonl --project=$PROJECT_ID  # add --dry-run first if supported"
echo "  (Do NOT delete the bucket itself)"

# --- 6. Firestore sixth ---
echo ""
echo "=== 6. Firestore — TTL handles rate_limits; delete only ad-hoc test collections via console ==="

# --- 7. IAM last (do not delete SA) ---
echo ""
echo "=== 7. IAM — do NOT delete vertex-search-sa; only delete unused keys: gcloud iam service-accounts keys list --iam-account=vertex-search-sa@interlispsearch.iam.gserviceaccount.com --project=$PROJECT_ID ==="
```

**Important:** The script above prints `DELETE` lines first. Uncomment the `curl -X DELETE` / `gcloud delete` lines only after you have saved inventory and confirmed the keep list.

Single-store/engine delete examples for manual use:

```bash
TOKEN=$(gcloud auth application-default print-access-token)
# Delete one engine
curl -X DELETE -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: interlispsearch" \
  "https://discoveryengine.googleapis.com/v1/projects/interlispsearch/locations/global/collections/default_collection/engines/ENGINE_ID_TO_DELETE"

# Delete one data store (cascades — wait 5-10 min, then verify GET returns 404)
curl -X DELETE -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: interlispsearch" \
  "https://discoveryengine.googleapis.com/v1/projects/interlispsearch/locations/global/collections/default_collection/dataStores/DATASTORE_ID_TO_DELETE"

# Verify deletion
curl -s -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: interlispsearch" \
  "https://discoveryengine.googleapis.com/v1/projects/interlispsearch/locations/global/collections/default_collection/dataStores/DATASTORE_ID_TO_DELETE" | python3 -m json.tool
# Expected: 404 Not Found
```

### Step 7.3: Validate After Cleanup

```bash
./inventory-interlispsearch.sh
# Expected: 1 dataStore (interlisp-search-unified), 1 engine, 3 functions, 2 scheduler jobs

curl -s "https://us-central1-interlispsearch.cloudfunctions.net/search?q=interlisp&pageSize=5" | python3 -m json.tool | head -40
# Expected: 200, results with source:website first, citations from interlisp.org

gcloud functions logs read search --gen2 --region=us-central1 --limit=20 --project=interlispsearch
# Expected: no discoveryengine quota errors
```

---

## Summary

You now have a complete implementation guide for:

1. ✅ Creating a unified data store with website + GitHub content
2. ✅ Implementing request-time filtering + post-processing in the Cloud Function
3. ✅ Deploying with proper citation preferences
4. ✅ Setting up automated daily website recrawls
5. ✅ Setting up automated weekly GitHub reimports
6. ✅ Testing and validating the deployment
7. ✅ Monitoring and troubleshooting procedures
8. ✅ **Cleanup — paring interlispsearch to in-use resources only (Phase 7)**

**Next Steps:**

1. Review this guide completely
2. Ensure all prerequisites are met
3. Follow Phase 1-4 in order
4. Use the testing checklist to validate each phase
5. Keep this document handy for troubleshooting
6. **Only after production validation (Phase 7): run inventory → review keep/delete list → delete in safe order (engines→dataStores→functions→scheduler→storage)**

---

**Document Version:** 1.1  
**Last Updated:** September 02, 2026  
**Status:** Implemented — see Testing Checklist verified 2026-09-02; Phase 7 still gated (≥48h production) and scheduled `github-reimport` Pub/Sub requires isolated source dir
