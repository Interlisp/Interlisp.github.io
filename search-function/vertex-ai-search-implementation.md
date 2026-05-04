# Vertex AI Search Integration with Hugo (Docsy)
## Implementation Guide for Interlisp.org

This document captures the complete steps taken to replace Google Custom Search (GCS) with a Vertex AI Search (Agent Search) powered search engine on a Hugo/Docsy site hosted on GitHub Pages.

---

## Architecture Overview

```
Browser → Hugo Search Page → Cloud Function (proxy) → Vertex AI Search (Agent Search)
                                      ↑        ↑
                              Service Account  Firestore (rate limiting)
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
| Firestore | `rate_limits` collection | Per-IP and global request rate limiting |

---

## Part 1 — GCP Project Setup

### 1.1 Enable Required APIs

```bash
gcloud services enable discoveryengine.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable orgpolicy.googleapis.com
gcloud services enable firestore.googleapis.com
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

# Allow Firestore read/write for rate limiting
gcloud projects add-iam-policy-binding interlispsearch \
  --member="serviceAccount:vertex-search-sa@interlispsearch.iam.gserviceaccount.com" \
  --role="roles/datastore.user"
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
    ├── rateLimiter.js
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
    "@google-cloud/firestore": "^7.0.0",
    "google-auth-library": "^9.0.0"
  }
}
```

### 4.3 `index.js`

The function uses the raw REST API (not the Node.js SDK) to avoid SDK auto-pagination which strips the `summary` field from responses. It includes Firestore-based rate limiting and resolves citation URLs by matching document IDs from results.

```javascript
'use strict';

const { GoogleAuth }    = require('google-auth-library');
const { isRateLimited } = require('./rateLimiter');

const PROJECT_ID = process.env.PROJECT_ID;
const ENGINE_ID  = process.env.ENGINE_ID;
const LOCATION   = 'global';

const auth = new GoogleAuth({
  scopes: ['https://www.googleapis.com/auth/cloud-platform']
});

exports.search = async (req, res) => {

  const allowedOrigins = [
    'https://interlisp.org',
    'https://www.interlisp.org',
    'https://stumbo.github.io',
    'http://localhost:1313',
    'http://localhost:8080',
  ];

  const origin        = req.headers.origin || '';
  const allowedOrigin = allowedOrigins.includes(origin)
    ? origin
    : 'https://interlisp.org';

  res.set('Access-Control-Allow-Origin',  allowedOrigin);
  res.set('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.set('Access-Control-Allow-Headers', 'Content-Type');
  res.set('Access-Control-Max-Age',       '3600');

  if (req.method === 'OPTIONS') {
    res.status(204).send('');
    return;
  }

  // Rate limiting
  const rateLimitResult = await isRateLimited(req);
  if (rateLimitResult.limited) {
    res.set('Retry-After', String(rateLimitResult.retryAfter));
    res.status(429).json({
      error:      'Rate limit exceeded',
      message:    rateLimitResult.reason,
      retryAfter: rateLimitResult.retryAfter
    });
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
          includeCitations:   true,
          useSemanticChunks:  true,
          languageCode:       'en-US',
          modelPromptSpec: {
            preamble: buildPreamble(context)
          },
          modelSpec: {
            version: 'stable'
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
      method:  'POST',
      headers: {
        'Authorization':       `Bearer ${token.token}`,
        'Content-Type':        'application/json',
        'x-goog-user-project': PROJECT_ID
      },
      body: JSON.stringify(requestBody)
    });

    if (!response.ok) {
      const errText = await response.text();
      throw new Error(`Vertex API error ${response.status}: ${errText}`);
    }

    const data = await response.json();

    // Strip HTML tags from snippet text
    const stripHtml = str => str ? str.replace(/<[^>]*>/g, '') : null;

    // Build document ID → URL map for citation linking
    const docIdToUrl = {};
    (data.results || []).forEach(result => {
      const id  = result.document?.id;
      const url = result.document?.derivedStructData?.link;
      if (id && url) docIdToUrl[id] = url;
    });

    // Map references to include resolved URLs by matching document IDs
    const references = (data.summary?.summaryWithMetadata?.references || [])
      .map(ref => {
        const docId = ref.document?.split('/').pop();
        return {
          title: ref.title,
          uri:   docIdToUrl[docId] || null,
        };
      });

    // REST API returns derivedStructData as flat object (not nested under .fields)
    const results = (data.results || []).map(result => {
      const derived = result.document?.derivedStructData;
      if (!derived) return null;

      const url = derived.link || null;

      return {
        id:      result.document?.id,
        title:   derived.title || null,
        url,
        snippet: stripHtml(derived.snippets?.[0]?.snippet || null),
        section: url?.replace('https://interlisp.org/', '')
                     ?.split('/')?.[0] || '',
      };
    }).filter(r => r?.url);

    const summaryText = data.summary?.summaryText || null;

    res.json({
      summary: summaryText ? {
        summaryText,
        citations: references
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
- `--service-account` — function runs as the service account, which has Discovery Engine and Firestore access
- No key file needed — the service account is attached at deploy time

### 4.6 Verify Deployment

```bash
# Test without auth token (should return results)
curl -s "https://us-central1-interlispsearch.cloudfunctions.net/search?q=interlisp" \
  | python3 -m json.tool | head -30
```

---

## Part 5 — Firestore Rate Limiting

Rate limiting is implemented using Firestore to track request counts across all function instances. In-memory counters cannot be used because Cloud Functions can scale to multiple instances.

### 5.1 Create the Firestore Database

```bash
gcloud firestore databases create \
  --location=us-central1 \
  --project=interlispsearch
```

### 5.2 Set Up TTL to Auto-Clean Expired Documents

This prevents the `rate_limits` collection from growing indefinitely:

```bash
gcloud firestore fields ttls update updatedAt \
  --collection-group=rate_limits \
  --enable-ttl \
  --project=interlispsearch
```

This operation takes 5-15 minutes to propagate. Check status:

```bash
gcloud firestore fields describe updatedAt \
  --collection-group=rate_limits \
  --project=interlispsearch
```

Look for `ttlConfig.state: ACTIVE` to confirm completion.

### 5.3 `rateLimiter.js`

Create `search-function/rateLimiter.js`:

```javascript
'use strict';

const { Firestore } = require('@google-cloud/firestore');

const db = new Firestore({ projectId: process.env.PROJECT_ID });

const LIMITS = {
  perIp: {
    requests: 20,    // max 20 requests per IP
    windowSec: 60,   // per 60 second window
  },
  global: {
    requests: 500,   // max 500 total requests
    windowSec: 60,   // per 60 second window
  }
};

async function checkLimit(key, limit) {
  const ref      = db.collection('rate_limits').doc(key);
  const now      = Date.now();
  const windowMs = limit.windowSec * 1000;

  try {
    const result = await db.runTransaction(async t => {
      const doc  = await t.get(ref);
      const data = doc.exists ? doc.data() : null;

      if (!data || (now - data.windowStart) > windowMs) {
        t.set(ref, { count: 1, windowStart: now, updatedAt: now });
        return { allowed: true, count: 1 };
      }

      if (data.count >= limit.requests) {
        return { allowed: false, count: data.count };
      }

      t.update(ref, {
        count:     Firestore.FieldValue.increment(1),
        updatedAt: now
      });
      return { allowed: true, count: data.count + 1 };
    });

    return result;

  } catch (err) {
    // Fail open — don't block searches if Firestore is unavailable
    console.error('Rate limiter error:', err.message);
    return { allowed: true, count: 0 };
  }
}

async function isRateLimited(req) {
  const ip = req.headers['x-forwarded-for']
    ?.split(',')[0]?.trim() || 'unknown';

  const [ipCheck, globalCheck] = await Promise.all([
    checkLimit(`ip:${ip}`, LIMITS.perIp),
    checkLimit('global',   LIMITS.global),
  ]);

  if (!ipCheck.allowed) {
    return {
      limited:    true,
      reason:     'Too many requests. Please wait a moment before searching again.',
      retryAfter: LIMITS.perIp.windowSec
    };
  }

  if (!globalCheck.allowed) {
    return {
      limited:    true,
      reason:     'Search service is temporarily busy. Please try again shortly.',
      retryAfter: LIMITS.global.windowSec
    };
  }

  return { limited: false };
}

module.exports = { isRateLimited };
```

### 5.4 Rate Limit Configuration

| Limit | Value | Notes |
|---|---|---|
| Per IP | 20 requests / 60 seconds | Prevents individual abuse |
| Global | 500 requests / 60 seconds | Protects against aggregate overload |
| Fail behavior | Open (allow) | If Firestore unavailable, searches proceed |

### 5.5 Verify Rate Limiting

```bash
# Check Firestore documents are created after searches
gcloud firestore documents list \
  --collection=rate_limits \
  --project=interlispsearch

# Test that 429 is returned after limit is exceeded
for i in {1..25}; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    "https://us-central1-interlispsearch.cloudfunctions.net/search?q=test")
  echo "Request $i: $STATUS"
done
```

Requests 1-20 return `200`, requests 21+ return `429`.

---

## Part 6 — Hugo / Docsy Integration

The site uses Hugo with the **Docsy** theme (v0.14.3) loaded as a Hugo module. Docsy renders its search box only when `gcs_engine_id` is set in params — this param is kept to preserve the search UI, while the results page is completely overridden.

### 6.1 How Docsy Search Works

When a user types in the search box and presses Enter, Docsy's `search.js` redirects to `/search/?q=query`. The results page (`layouts/search.html`) is where we intercept and replace GCS with Vertex AI.

### 6.2 `config/_default/params.yaml` Changes

```yaml
# Keep this — Docsy won't render the search box without it
gcs_engine_id: 33ef4cbe0703b4f3a

# Add Vertex AI Search Cloud Function URL
vertex_search_url: "https://us-central1-interlispsearch.cloudfunctions.net/search"
```

### 6.3 Override Search Results Page

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

### 6.4 Search Widget JavaScript

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

      // Show AI summary and citations if available
      if (data.summary?.summaryText) {
        summaryTxt.textContent = data.summary.summaryText;
        summaryEl.style.display = 'block';

        const refs = data.summary?.citations || [];
        const validRefs = refs.filter(r => r.title || r.uri);
        if (validRefs.length > 0) {
          const citationHtml = validRefs.map((ref, i) => `
            <div class="search-citation">
              <span class="citation-number">[${i + 1}]</span>
              ${ref.uri
                ? `<a href="${escapeHtml(ref.uri)}" target="_blank" rel="noopener">${escapeHtml(ref.title || ref.uri)}</a>`
                : `<span>${escapeHtml(ref.title || 'Unknown source')}</span>`
              }
            </div>
          `).join('');
          const citationsDiv = document.createElement('div');
          citationsDiv.className = 'search-citations mt-3';
          citationsDiv.innerHTML = '<p class="citations-label">Sources</p>' + citationHtml;
          summaryEl.querySelector('.ai-summary').appendChild(citationsDiv);
        }
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

### 6.5 Load JS via `head-end.html`

Update `layouts/_partials/hooks/head-end.html`:

```html
<link rel="canonical" href="{{ .Permalink }}">
<link rel="me" href="https://fosstodon.org/@interlisp">

{{ $searchJS := resources.Get "js/vertex-search.js" | js.Build | fingerprint }}
<script src="{{ $searchJS.RelPermalink }}" defer></script>
```

### 6.6 Add Styles

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
}

.search-citations {
  border-top: 1px solid #d0e4ff;
  padding-top: 0.75rem;
  margin-top: 0.75rem;

  .citations-label {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #1a73e8;
    margin-bottom: 0.4rem;
  }
}

.search-citation {
  font-size: 0.8rem;
  margin-bottom: 0.25rem;

  .citation-number {
    color: #1a73e8;
    font-weight: 600;
    margin-right: 0.4rem;
  }

  a { color: #444; }
}
```

---

## Part 7 — File Summary

### New Files Created

| File | Purpose |
|---|---|
| `search-function/index.js` | Cloud Function — proxy to Vertex AI Search |
| `search-function/rateLimiter.js` | Firestore-based rate limiting |
| `search-function/package.json` | Node.js dependencies |
| `search-function/.gcloudignore` | Excludes node_modules from deploy |
| `layouts/search.html` | Overrides Docsy's GCS results page |
| `assets/js/vertex-search.js` | Frontend search widget JS |

### Modified Files

| File | Change |
|---|---|
| `config/_default/params.yaml` | Added `vertex_search_url`, kept `gcs_engine_id` |
| `layouts/_partials/hooks/head-end.html` | Added JS bundle load |
| `assets/scss/_styles_project.scss` | Added search result and citation styles |

---

## Part 8 — Key Lessons Learned

### Authentication
- Local `curl` testing requires the `x-goog-user-project: interlispsearch` header with ADC credentials — without it, requests are billed against a Google-internal project and fail with 403
- Cloud Functions authenticate via the attached service account at runtime — no key file needed
- Browser JS cannot call authenticated Cloud Functions directly — the function must be public (`--allow-unauthenticated`) with CORS restricting by origin in code

### Vertex AI SDK vs REST API
- The Node.js `@google-cloud/discoveryengine` SDK uses auto-pagination by default, which flattens the response into a plain array of results and **strips the `summary` field**
- Using the raw REST API via `fetch` preserves the full response structure including `summary`, `totalSize`, `attributionToken`, and `semanticState`
- The REST API returns `derivedStructData` as a flat object (e.g. `derived.title`) rather than nested under `fields` as the SDK does (e.g. `fields.title.stringValue`)

### Citations
- The `references` array in `summaryWithMetadata` contains document paths, not URLs
- URLs must be resolved by cross-referencing document IDs from the `results` array against the document path suffix in each reference
- `useSemanticChunks: true` in `summarySpec` improves citation accuracy

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

### Rate Limiting
- Cloud Functions are stateless — in-memory rate limit counters don't work across scaled instances
- Firestore transactions provide atomic counter increments safe for concurrent access
- The rate limiter fails open — if Firestore is unavailable, searches proceed rather than being blocked
- Firestore TTL policies auto-clean expired rate limit documents — set on the `updatedAt` field

---

## Part 9 — Deployment Status

| Environment | URL | Status |
|---|---|---|
| Local dev | `http://localhost:1313` | ✅ Working |
| Staging | `https://stumbo.github.io/InterlispDraft.github.io/` | ✅ Deployed and verified |
| Production | `https://interlisp.org` | ⏳ Pending |

### What is working end to end

- Search box renders in Docsy navbar and sidebar
- Typing a query and pressing Enter redirects to `/search/?q=query`
- Vertex AI Search returns relevant results from the indexed interlisp.org site
- AI-generated summary appears at the top of results with `[n]` citation markers
- Citation sources are listed below the summary with links to source pages
- Snippets are plain text (HTML stripped)
- CORS is correctly scoped to allowed origins
- Rate limiting is active — 20 requests/minute per IP, 500/minute global
- Firestore TTL auto-cleans expired rate limit documents

---

## Part 10 — Remaining Items

- [ ] Deploy to production (`interlisp.org`)
- [ ] Set up CI/CD to re-index when site content changes (JSONL approach or scheduled recrawl)
- [ ] Remove any remaining debug `console.log` statements from `index.js`
- [ ] Monitor Firestore `rate_limits` collection and adjust limits based on real traffic
- [ ] Consider adding query logging to Firestore for search analytics
- [ ] Review and tune the AI preamble prompt based on real query patterns
- [ ] Add `interlisp.org` to the CORS `allowedOrigins` list in `index.js` before production deploy (already present, verify it matches exact production domain)
