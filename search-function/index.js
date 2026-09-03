'use strict';

const { GoogleAuth }    = require('google-auth-library');
const { isRateLimited } = require('./rateLimiter');

const PROJECT_ID = process.env.PROJECT_ID;
const WEBSITE_ENGINE_ID = process.env.WEBSITE_ENGINE_ID || process.env.ENGINE_ID;
const GITHUB_ENGINE_ID = process.env.GITHUB_ENGINE_ID || null;
const LOCATION   = 'global';

const auth = new GoogleAuth({
  scopes: ['https://www.googleapis.com/auth/cloud-platform']
});

exports.search = async (req, res) => {

  const allowedOrigins = [
    'https://interlisp.org',
    'https://www.interlisp.org',
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
  const pageSize = parseInt(req.query.pageSize, 10) || 10;

  if (!query.trim()) {
    res.status(400).json({ error: 'Missing query parameter q' });
    return;
  }

  try {
    const client = await auth.getClient();
    const token  = await client.getAccessToken();

    const stripHtml = str => str ? str.replace(/<[^>]*>/g, '') : null;

    const getSource = (url) => {
      if (!url) return 'unknown';
      try {
        const u = new URL(url);
        const host = u.hostname.toLowerCase();
        if (host === 'www.interlisp.org' || host === 'interlisp.org') return 'website-primary';
        if (host.endsWith('.interlisp.org')) return 'website-secondary';
        if (host.includes('github.com') || url.includes('github.com')) return 'github';
        return 'other';
      } catch (_) {
        if (url.includes('github.com')) return 'github';
        if (url.includes('interlisp.org')) return 'website-secondary';
        return 'other';
      }
    };

    const sourcePriorityMap = {
      'website-primary': 1,
      'website-secondary': 2,
      'github': 3,
      'other': 4,
      'unknown': 999
    };

    const fetchPageSize = 20;

    const searchEngine = async (engineId, withSummary) => {
      const endpoint = `https://discoveryengine.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION}/collections/default_collection/engines/${engineId}/servingConfigs/default_config:search`;
      const body = {
        query,
        pageSize: fetchPageSize,
        contentSearchSpec: {
          snippetSpec: { returnSnippet: true },
          extractiveContentSpec: { maxExtractiveAnswerCount: 3 }
        }
      };
      if (withSummary) {
        body.contentSearchSpec.summarySpec = {
          summaryResultCount: 5,
          includeCitations: true,
          useSemanticChunks: true,
          languageCode: 'en-US',
          modelPromptSpec: { preamble: buildPreamble(context) },
          modelSpec: { version: 'stable' }
        };
      }
      const resp = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token.token}`,
          'Content-Type': 'application/json',
          'x-goog-user-project': PROJECT_ID
        },
        body: JSON.stringify(body)
      });
      if (!resp.ok) {
        const errText = await resp.text();
        throw new Error(`Vertex API error ${resp.status} on ${engineId}: ${errText}`);
      }
      return resp.json();
    };

    let websiteData;
    let githubData;
    if (GITHUB_ENGINE_ID) {
      [websiteData, githubData] = await Promise.all([
        searchEngine(WEBSITE_ENGINE_ID, true),
        searchEngine(GITHUB_ENGINE_ID, false)
      ]);
    } else {
      websiteData = await searchEngine(WEBSITE_ENGINE_ID, true);
      githubData = null;
    }

    // Blended merge: guarantee GitHub despite website priority (70/30, 50/50 for GitHub queries)
    const isGithubQuery = /github|issue|pull\s*request|\bpr\b|discussion/i.test(query);
    const websiteTake = isGithubQuery ? Math.ceil(pageSize * 0.5) : Math.ceil(pageSize * 0.7);
    const githubTake = pageSize - websiteTake;

    const toItems = (data, hint) => (data?.results || []).map(r => {
      const d = r.document?.derivedStructData;
      const s = r.document?.structData;
      const url = d?.link || d?.url || s?.url || s?.link || null;
      const src = hint || getSource(url);
      return {
        raw: r,
        url,
        source: src,
        priority: sourcePriorityMap[src] || 999,
        derived: d,
        structData: s,
        score: r.retrievalSignals?.semanticRelevanceScore || 0
      };
    }).filter(i => i.url);

    let websiteItems = toItems(websiteData, null).sort((a, b) => a.priority - b.priority || b.score - a.score);
    let githubItems = toItems(githubData, 'github').sort((a, b) => b.score - a.score);

    // Dedup by URL
    const seen = new Set();
    websiteItems = websiteItems.filter(i => !seen.has(i.url) && seen.add(i.url));
    githubItems = githubItems.filter(i => !seen.has(i.url) && seen.add(i.url));

    let allResults = [...websiteItems.slice(0, websiteTake), ...githubItems.slice(0, githubTake)];
    if (allResults.length < pageSize) {
      const rem = [...websiteItems.slice(websiteTake), ...githubItems.slice(githubTake)].sort((a, b) => a.priority - b.priority || b.score - a.score);
      allResults = [...allResults, ...rem].slice(0, pageSize);
    }
    allResults.sort((a, b) => a.priority - b.priority || b.score - a.score);

    // docId → URL map for citations (from both engines)
    const docIdToUrl = {};
    [...websiteItems, ...githubItems].forEach(i => {
      if (i.raw.document?.id) docIdToUrl[i.raw.document.id] = i.url;
    });

    let references = (websiteData?.summary?.summaryWithMetadata?.references || []).map(ref => {
      const docId = ref.document?.split('/').pop();
      const uri = docIdToUrl[docId] || null;
      const src = getSource(uri);
      return {
        title: ref.title,
        uri,
        docId,
        source: src,
        priority: sourcePriorityMap[src] || 999
      };
    }).sort((a, b) => a.priority - b.priority);

    const results = allResults.map(i => ({
      id: i.raw.document?.id,
      title: i.derived?.title || i.structData?.title || null,
      url: i.url,
      snippet: stripHtml(i.derived?.snippets?.[0]?.snippet || i.structData?.content?.slice(0, 300) || null),
      source: i.source,
      priority: i.priority,
      section: i.url.replace(/^https:\/\/[^/]+\//, '').split('/')?.[0] || '',
      type: i.structData?.type || null,
      repo: i.structData?.repo || null,
      state: i.structData?.state || null
    })).slice(0, pageSize);

    res.json({
      summary: (websiteData?.summary?.summaryText ? {
        summaryText: websiteData.summary.summaryText,
        citations: references
      } : null),
      results
    });

  } catch (err) {
    console.error('Search error:', err);
    res.status(500).json({ error: 'Search failed', detail: err.message });
  }
};

// Re-export for github-reimport Cloud Function (shares same source dir but different entry-point)
try {
  exports.reimportGithub = require('./github-reimport').reimportGithub;
} catch (e) {
  // ignore if github-reimport not available during search deploy
  void e;
}

function buildPreamble(context) {
  const base = `You are a search assistant for Interlisp.org. You answer questions about the Interlisp project using indexed documentation, code examples, historical information, and GitHub content (issues, PRs, discussions).

## Core Principles
- Answer clearly and concisely. Always cite sources.
- If unsure, say "I don't know" — never guess.
- Prefer authoritative primary sources (Interlisp Reference Manual, official docs) over secondary sources.
- When multiple sources cover the same topic, cite the most authoritative one first.

## Citation Priorities (in order)
1. **Interlisp.org website** (documentation, guides, examples) — preferred for general questions
2. **Official PDFs** (files.interlisp.org) — Medley documentation, release notes, reference manuals
3. **GitHub content** (issues, PRs, discussions, project status) — use when discussing development, maintenance, or community feedback
4. GitHub repository source files — use only if no better source exists

When a topic is covered by both the website AND GitHub (e.g., release notes on interlisp.org vs GitHub issues), cite the website version.

## Content Guidance
- **General Interlisp questions:** Use interlisp.org docs and PDFs as primary sources
- **Code examples:** Provide Interlisp examples; note Common Lisp differences when relevant; cite source docs
- **Development/maintenance:** Include GitHub issue/PR references; cite discussions that show community input
- **Historical context:** Use interlisp.org history section and official documents

## Response Format (always use this structure)
- Opening paragraph (1-2 sentences)
- "## Key Points" with bullet points
- "## Details" for additional context (only if needed)
- "## Caveats" (only when needed for safety/accuracy)
- Citations at the end as [1], [2], [3]

## Critical Notes
- Answer in Markdown only — no HTML
- When citing sources, include the direct link, not GitHub repo paths
- If the user is browsing a specific website section, prioritize results from that section`;

  if (context) {
    return `${base}\n\n## Current Context\nThe user is browsing the "${context}" section of interlisp.org — prioritize results from that section when relevant.`;
  }
  return base;
}
