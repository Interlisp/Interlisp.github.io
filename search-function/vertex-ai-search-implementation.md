# Vertex AI Search Integration with Hugo (Docsy)
## Implementation Guide for Interlisp.org

This document captures the complete steps taken to replace Google Custom Search (GCS) with a Vertex AI Search (Agent Search) powered search engine on a Hugo/Docsy site hosted on GitHub Pages.

---

## Architecture Overview

```
Browser → Hugo Search Page → Cloud Function (proxy) → Vertex AI Search (Agent Search)
                                      ↑
                              Service Account (auth)
                                      ↑
                              Data Store (interlisp.org crawl)
```

### Components

| Component | Name/ID | Purpose |
|---|---|---|
| GCP Project | `interlispsearch` (191169864763) | Container for all resources |
| Service Account | `vertex-search-sa@interlispsearch.iam.gserviceaccount.com` | Auth identity for Cloud Function |
| Data Store | `interlisp-site-search` | Crawled and indexed site content |
| Search Engine | `interlisp-site-search-v2_1777510147931` | Search app with LLM add-on |
| Cloud Function | `search` (us-central1) | Proxy between Hugo frontend and Vertex AI |

---

## Part 1 — GCP Project Setup

### 1.1 Enable Required APIs

```bash
gcloud services enable discoveryengine.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable orgpolicy.googleapis.com
```

### 1.2 Create Service Account

```bash
gcloud iam service-accounts create vertex-search-sa \
  --display-name="Vertex Search Service Account" \
  --project=interlispsearch
```

### 1.3 Grant Service Account Roles

```bash
# Core role for Vertex AI Search access
gcloud projects add-iam-policy-binding interlispsearch \
  --member="serviceAccount:vertex-search-sa@interlispsearch.iam.gserviceaccount.com" \
  --role="roles/discoveryengine.editor"

# Allow reading from Cloud Storage (for future JSONL imports)
gcloud projects add-iam-policy-binding interlispsearch \
  --member="serviceAccount:vertex-search-sa@interlispsearch.iam.gserviceaccount.com" \
  --role="roles/storage.objectViewer"
```

### 1.4 Override Org Policies (Project Level)

The interlisp.org GCP organization had two restrictive org policies that blocked key creation and public function invocation. These were overridden at the project level without affecting the org-wide policy.

```bash
# Allow allUsers IAM bindings in this project (needed for public Cloud Function)
cat > allow-all-users.yaml << 'EOF'
name: projects/interlispsearch/policies/iam.allowedPolicyMemberDomains
spec:
  inheritFromParent: false
  rules:
  - allowAll: true
EOF

gcloud org-policies set-policy allow-all-users.yaml --project=interlispsearch

# Allow service account key creation in this project
cat > allow-sa-keys.yaml << 'EOF'
name: projects/interlispsearch/policies/iam.disableServiceAccountKeyCreation
spec:
  inheritFromParent: false
  rules:
  - enforce: false
EOF

gcloud org-policies set-policy allow-sa-keys.yaml --project=interlispsearch
```

### 1.5 Set Up Local Authentication

```bash
# Authenticate with Application Default Credentials
gcloud auth application-default login

# Set quota project (required for Discovery Engine API calls)
gcloud auth application-default set-quota-project interlispsearch

# Set default project
gcloud config set project interlispsearch
```

**Important:** All `curl` calls to the Discovery Engine API require the `x-goog-user-project` header:

```bash
-H "x-goog-user-project: interlispsearch"
```

---

## Part 2 — Vertex AI Data Store

### 2.1 Create the Data Store

```bash
TOKEN=$(gcloud auth application-default print-access-token)

curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "x-goog-user-project: interlispsearch" \
  "https://discoveryengine.googleapis.com/v1/projects/interlispsearch/locations/global/collections/default_collection/dataStores?dataStoreId=interlisp-site-search" \
  -d '{
    "displayName": "Interlisp Site Search",
    "industryVertical": "GENERIC",
    "solutionTypes": ["SOLUTION_TYPE_SEARCH"],
    "contentConfig": "PUBLIC_WEBSITE"
  }'
```

**Key parameters:**
- `contentConfig: PUBLIC_WEBSITE` — enables website crawling
- `industryVertical: GENERIC` — required for non-Workspace data stores
- Location must be `global` for AI summarization features

### 2.2 Add Target Site

The URL pattern does **not** include the `https://` protocol prefix:

```bash
TOKEN=$(gcloud auth application-default print-access-token)

curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "x-goog-user-project: interlispsearch" \
  "https://discoveryengine.googleapis.com/v1/projects/interlispsearch/locations/global/collections/default_collection/dataStores/interlisp-site-search/siteSearchEngine/targetSites" \
  -d '{
    "providedUriPattern": "interlisp.org/*",
    "type": "INCLUDE",
    "exactMatch": false
  }'
```

### 2.3 Upgrade to Advanced Website Indexing

Advanced indexing is required for AI summarization features. This is done in the GCP console:

1. Go to **AI Applications → Data Stores → interlisp-site-search**
2. Click the **Data** tab
3. Click **Upgrade to Advanced** next to the URL pattern

Upgrading takes 4-8 hours for a site the size of interlisp.org. Check status:

```bash
TOKEN=$(gcloud auth application-default print-access-token)

curl -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: interlispsearch" \
  "https://discoveryengine.googleapis.com/v1/projects/interlispsearch/locations/global/collections/default_collection/dataStores/interlisp-site-search/siteSearchEngine/targetSites" \
  | python3 -m json.tool
```

Look for `indexingStatus: SUCCEEDED` to confirm completion.

---

## Part 3 — Vertex AI Search Engine (App)

### 3.1 Important: App Type Selection

The search engine must be created as **"Site search with AI mode"** in the console — NOT as "Gemini Enterprise" or "Custom Search (general)".

- **Gemini Enterprise** — for internal workspace knowledge bases, incompatible with website data stores
- **Custom Search (general)** — for structured document/JSONL data, not website crawling
- **Site search with AI mode** ✓ — correct type for public website crawling with AI summaries

### 3.2 Create via Console

1. Go to **AI Applications → Apps → Create App**
2. Select **Search → Site search with AI mode**
3. Fill in details:
   - App name: `interlisp-site-search-v2`
   - Company name: `interlisp.org`
   - Location: `global`
4. Select data store: `interlisp-site-search`
5. Note the generated engine ID: `interlisp-site-search-v2_1777510147931`

### 3.3 Verify Engine Configuration

```bash
TOKEN=$(gcloud auth application-default print-access-token)

curl -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: interlispsearch" \
  "https://discoveryengine.googleapis.com/v1/projects/interlispsearch/locations/global/collections/default_collection/engines/interlisp-site-search-v2_1777510147931" \
  | python3 -m json.tool
```

Confirm the response contains:
```json
{
  "searchEngineConfig": {
    "searchTier": "SEARCH_TIER_ENTERPRISE",
    "searchAddOns": ["SEARCH_ADD_ON_LLM"]
  }
}
```

`SEARCH_ADD_ON_LLM` is required for AI summaries.

---

## Part 4 — Cloud Function (Search Proxy)

The Cloud Function acts as a secure proxy between the public Hugo frontend and the authenticated Vertex AI Search API. It also builds the AI prompt context.

### 4.1 Project Structure

```
hugo-site/
└── search-function/
    ├── index.js
    ├── package.json
    └── .gcloudignore
```

### 4.2 `package.json`

```json
{
  "name": "search-function",
  "version": "1.0.0",
  "main": "index.js",
  "dependencies": {
    "@google-cloud/discoveryengine": "^1.0.0",
    "google-auth-library": "^9.0.0"
  }
}
```

### 4.3 `index.js`

The function uses the raw REST API (not the Node.js SDK) to avoid SDK auto-pagination which strips the `summary` field from responses.

```javascript
const { GoogleAuth } = require('google-auth-library');

const PROJECT_ID = process.env.PROJECT_ID;
const ENGINE_ID  = process.env.ENGINE_ID;
const LOCATION   = 'global';

const auth = new GoogleAuth({
  scopes: ['https://www.googleapis.com/auth/cloud-platform']
});

exports.search = async (req, res) => {

  // CORS — allow specific origins only
  const allowedOrigins = [
    'https://interlisp.org',
    'https://www.interlisp.org',
    'https://stumbo.github.io',
    'http://localhost:1313',
    'http://localhost:8080',
  ];

  const origin = req.headers.origin || '';
  const allowedOrigin = allowedOrigins.includes(origin) ? origin : 'https://interlisp.org';

  res.set('Access-Control-Allow-Origin', allowedOrigin);
  res.set('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.set('Access-Control-Allow-Headers', 'Content-Type');
  res.set('Access-Control-Max-Age', '3600');

  if (req.method === 'OPTIONS') {
    res.status(204).send('');
    return;
  }

  const query    = req.query.q || req.body?.q || '';
  const context  = req.query.context || req.body?.context || '';
  const pageSize = parseInt(req.query.pageSize) || 10;

  if (!query.trim()) {
    res.status(400).json({ error: 'Missing query parameter q' });
    return;
  }

  try {
    const client = await auth.getClient();
    const token  = await client.getAccessToken();

    const endpoint = `https://discoveryengine.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION}/collections/default_collection/engines/${ENGINE_ID}/servingConfigs/default_config:search`;

    const requestBody = {
      query,
      pageSize,
      contentSearchSpec: {
        summarySpec: {
          summaryResultCount: 5,
          includeCitations: true,
          modelPromptSpec: {
            preamble: buildPreamble(context)
          }
        },
        snippetSpec: {
          returnSnippet: true
        },
        extractiveContentSpec: {
          maxExtractiveAnswerCount: 3
        }
      }
    };

    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token.token}`,
        'Content-Type': 'application/json',
        'x-goog-user-project': PROJECT_ID
      },
      body: JSON.stringify(requestBody)
    });

    if (!response.ok) {
      const errText = await response.text();
      throw new Error(`Vertex API error ${response.status}: ${errText}`);
    }

    const data = await response.json();

    // REST API returns derivedStructData as flat object (not nested under .fields)
    const results = (data.results || []).map(result => {
      const derived = result.document?.derivedStructData;
      if (!derived) return null;

      const url     = derived.link || null;
      const snippet = derived.snippets?.[0]?.snippet || null;

      return {
        id:      result.document?.id,
        title:   derived.title || null,
        url,
        snippet,
        section: url?.replace('https://interlisp.org/', '')?.split('/')?.[0] || '',
      };
    }).filter(r => r?.url);

    const summaryText = data.summary?.summaryText || null;

    res.json({
      summary: summaryText ? {
        summaryText,
        citations: data.summary?.summaryWithMetadata?.references || []
      } : null,
      results
    });

  } catch (err) {
    console.error('Search error:', err);
    res.status(500).json({ error: 'Search failed', detail: err.message });
  }
};

function buildPreamble(context) {
  const base = `You are a search assistant for the Interlisp documentation site.
Answer questions clearly and concisely. Always cite the sources you used.
If no relevant results exist, say so directly rather than guessing.`;

  if (context) {
    return `${base}\nThe user is currently browsing the "${context}" section — prioritize results from that section where relevant.`;
  }
  return base;
}
```

### 4.4 `.gcloudignore`

```
node_modules/
.git/
*.md
```

### 4.5 Deploy

```bash
cd search-function
npm install

gcloud functions deploy search \
  --gen2 \
  --runtime=nodejs24 \
  --region=us-central1 \
  --source=. \
  --entry-point=search \
  --trigger-http \
  --allow-unauthenticated \
  --service-account=vertex-search-sa@interlispsearch.iam.gserviceaccount.com \
  --set-env-vars PROJECT_ID=interlispsearch,ENGINE_ID=interlisp-site-search-v2_1777510147931,ALLOWED_ORIGIN=https://interlisp.org \
  --memory=256Mi \
  --timeout=30s \
  --project=interlispsearch
```

**Key deployment decisions:**
- `--gen2` — required for Cloud Run-based functions with better performance
- `--allow-unauthenticated` — public endpoint, CORS restricts access by domain in function code
- `--service-account` — function runs as the service account, which has Discovery Engine access
- No key file needed — the service account is attached at deploy time

### 4.6 Verify Deployment

```bash
# Test without auth token (should return results)
curl -s "https://us-central1-interlispsearch.cloudfunctions.net/search?q=interlisp" \
  | python3 -m json.tool | head -30
```

---

## Part 5 — Hugo / Docsy Integration

The site uses Hugo with the **Docsy** theme (v0.14.3) loaded as a Hugo module. Docsy renders its search box only when `gcs_engine_id` is set in params — this param is kept to preserve the search UI, while the results page is completely overridden.

### 5.1 How Docsy Search Works

When a user types in the search box and presses Enter, Docsy's `search.js` redirects to `/search/?q=query`. The results page (`layouts/search.html`) is where we intercept and replace GCS with Vertex AI.

### 5.2 `config/_default/params.yaml` Changes

```yaml
# Keep this — Docsy won't render the search box without it
gcs_engine_id: 33ef4cbe0703b4f3a

# Add Vertex AI Search Cloud Function URL
vertex_search_url: "https://us-central1-interlispsearch.cloudfunctions.net/search"
```

### 5.3 Override Search Results Page

Create `layouts/search.html` (overrides Docsy's GCS results page):

```html
{{ define "main" }}
<section class="row td-search-result">
  <div class="col-12 col-md-8 offset-md-2">
    <h2 class="ms-4">Search Results</h2>

    <div id="vertex-search-container" class="ms-4 mt-4">

      <div id="vertex-search-config"
        data-search-url="{{ .Site.Params.vertex_search_url }}"
        style="display:none">
      </div>

      <div id="vertex-search-summary" style="display:none">
        <div class="ai-summary mb-4">
          <span class="ai-badge">
            <i class="fas fa-robot"></i> AI Summary
          </span>
          <p id="summary-text" class="mt-2 mb-0"></p>
        </div>
      </div>

      <div id="vertex-search-status" class="text-muted">
        <i class="fas fa-spinner fa-spin"></i> Searching...
      </div>

      <div id="vertex-search-hits"></div>

    </div>
  </div>
</section>
{{ end }}
```

### 5.4 Search Widget JavaScript

Create `assets/js/vertex-search.js`:

```javascript
(function () {
  'use strict';

  const config = document.getElementById('vertex-search-config');
  if (!config) return;

  const FUNCTION_URL = config.dataset.searchUrl;
  if (!FUNCTION_URL) return;

  const urlParams  = new URLSearchParams(window.location.search);
  const query      = urlParams.get('q') || '';

  const statusEl   = document.getElementById('vertex-search-status');
  const hitsEl     = document.getElementById('vertex-search-hits');
  const summaryEl  = document.getElementById('vertex-search-summary');
  const summaryTxt = document.getElementById('summary-text');

  function escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  async function doSearch(q) {
    if (!q) {
      statusEl.textContent = 'Enter a search query above.';
      return;
    }

    document.title = `Search: ${q}`;
    statusEl.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Searching for <strong>' +
      escapeHtml(q) + '</strong>…';

    try {
      const url = new URL(FUNCTION_URL);
      url.searchParams.set('q', q);

      // Pass referring section as context
      const ref = document.referrer;
      if (ref) {
        try {
          const refPath = new URL(ref).pathname.split('/').filter(Boolean);
          if (refPath.length > 0) url.searchParams.set('context', refPath[0]);
        } catch (_) {}
      }

      const resp = await fetch(url.toString());
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const data = await resp.json();

      statusEl.style.display = 'none';

      // Show AI summary if available
      if (data.summary?.summaryText) {
        summaryTxt.textContent = data.summary.summaryText;
        summaryEl.style.display = 'block';
      }

      if (!data.results || data.results.length === 0) {
        hitsEl.innerHTML = `<p>No results found for <strong>${escapeHtml(q)}</strong>.</p>`;
        return;
      }

      hitsEl.innerHTML =
        `<p class="text-muted mb-3">${data.results.length} results for <strong>${escapeHtml(q)}</strong></p>` +
        data.results.map(r => `
          <div class="td-search-hit mb-4">
            <h5 class="mb-1">
              <a href="${escapeHtml(r.url)}">${escapeHtml(r.title || 'Untitled')}</a>
            </h5>
            ${r.snippet ? `<p class="mb-1 text-muted small">${escapeHtml(r.snippet)}</p>` : ''}
            <p class="mb-0"><small class="text-success">${escapeHtml(r.url)}</small></p>
          </div>
        `).join('');

    } catch (err) {
      statusEl.textContent = 'Search error: ' + err.message;
      console.error('Vertex search error:', err);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => doSearch(query));
  } else {
    doSearch(query);
  }

})();
```

### 5.5 Load JS and Pass Config via `head-end.html`

Update `layouts/_partials/hooks/head-end.html`:

```html
<link rel="canonical" href="{{ .Permalink }}">
<link rel="me" href="https://fosstodon.org/@interlisp">

{{ $searchJS := resources.Get "js/vertex-search.js" | js.Build | fingerprint }}
<script src="{{ $searchJS.RelPermalink }}" defer></script>
```

### 5.6 Add Styles

Add to `assets/scss/_styles_project.scss`:

```scss
// Vertex AI Search styles
.ai-summary {
  background: #f0f7ff;
  border-left: 4px solid #1a73e8;
  padding: 1rem 1.25rem;
  margin-bottom: 1.5rem;
  border-radius: 0 4px 4px 0;

  .ai-badge {
    font-size: 0.75rem;
    font-weight: 600;
    color: #1a73e8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    display: block;
    margin-bottom: 0.5rem;
  }

  p { margin: 0; }
}

.td-search-hit {
  padding: 1rem 0;
  border-bottom: 1px solid #e8e8e8;

  &:last-child { border-bottom: none; }

  &__title {
    margin: 0 0 0.25rem;
    font-size: 1rem;
    a { color: #1a0dab; }
  }

  &__snippet {
    font-size: 0.875rem;
    color: #545454;
    margin: 0.25rem 0;
  }

  &__url {
    color: #006621;
    margin: 0;
  }
}
```

---

## Part 6 — File Summary

### New Files Created

| File | Purpose |
|---|---|
| `search-function/index.js` | Cloud Function — proxy to Vertex AI Search |
| `search-function/package.json` | Node.js dependencies |
| `search-function/.gcloudignore` | Excludes node_modules from deploy |
| `layouts/search.html` | Overrides Docsy's GCS results page |
| `assets/js/vertex-search.js` | Frontend search widget JS |

### Modified Files

| File | Change |
|---|---|
| `config/_default/params.yaml` | Added `vertex_search_url`, kept `gcs_engine_id` |
| `layouts/_partials/hooks/head-end.html` | Added JS bundle load |
| `assets/scss/_styles_project.scss` | Added search result styles |

---

## Part 7 — Key Lessons Learned

### Authentication
- Local `curl` testing requires the `x-goog-user-project: interlispsearch` header with ADC credentials — without it, requests are billed against a Google-internal project and fail with 403
- Cloud Functions authenticate via the attached service account at runtime — no key file needed
- Browser JS cannot call authenticated Cloud Functions directly — the function must be public (`--allow-unauthenticated`) with CORS restricting by origin in code

### Vertex AI SDK vs REST API
- The Node.js `@google-cloud/discoveryengine` SDK uses auto-pagination by default, which flattens the response into a plain array of results and **strips the `summary` field**
- Using the raw REST API via `fetch` preserves the full response structure including `summary`, `totalSize`, `attributionToken`, and `semanticState`
- The REST API also returns `derivedStructData` as a flat object (e.g. `derived.title`) rather than nested under `fields` as the SDK does (e.g. `fields.title.stringValue`)

### Org Policies
- `constraints/iam.allowedPolicyMemberDomains` blocked `allUsers` invocation
- `constraints/iam.disableServiceAccountKeyCreation` blocked service account key files
- Both were overridden at the project level using `gcloud org-policies set-policy` — requires `roles/owner` on the project but not org-level admin access

### Docsy Search Integration
- Docsy only renders the search box when `gcs_engine_id` is set in params
- The search box redirects to `/search/?q=query` on Enter — this is handled by Docsy's own `search.js`
- Override `layouts/search.html` to replace GCS results with Vertex AI results
- Do not try to intercept the search input directly — work with Docsy's redirect behavior

### Data Store Type
- Must be created as **"Site search with AI mode"** in the AI Applications console
- **"Gemini Enterprise"** app type is incompatible with website data stores
- URL patterns for target sites must **not** include `https://` protocol prefix
- Advanced website indexing (upgrade from Basic) is required for AI summarization — takes 4-8 hours

---

## Part 8 — Pending Items

- [ ] Confirm Advanced indexing completes (`indexingStatus: SUCCEEDED`)
- [ ] Verify AI summary appears in search results once indexing is complete
- [ ] Deploy to staging site (`stumbo.github.io/InterlispDraft.github.io`)
- [ ] Test CORS from staging domain
- [ ] Deploy to production (`interlisp.org`)
- [ ] Set up CI/CD to re-index when site content changes (JSONL approach)
- [ ] Remove debug `console.log` statements from `index.js`
- [ ] Consider rate limiting on the Cloud Function for production
