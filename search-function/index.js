const { GoogleAuth } = require('google-auth-library');

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
    // Use raw REST API to avoid SDK auto-pagination swallowing the summary
    const client = await auth.getClient();
    const token = await client.getAccessToken();

    const endpoint = `https://discoveryengine.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION}/collections/default_collection/engines/${ENGINE_ID}/servingConfigs/default_config:search`;

    const requestBody = {
      query,
      pageSize,
      contentSearchSpec: {
        summarySpec: {
          summaryResultCount: 5,
          includeCitations: true,
          useSemanticChunks: true,
          languageCode: 'en-US',
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

    // Add this right after const data = await response.json();
    console.log('FIRST RESULT:', JSON.stringify(data.results?.[0], null, 2));
    console.log('SUMMARY FULL:', JSON.stringify(data.summary, null, 2));
    console.log('CITATIONS:', JSON.stringify(data.summary?.summaryWithMetadata?.references?.[0]));

    console.log('RESPONSE KEYS:', Object.keys(data));
    console.log('SUMMARY:', JSON.stringify(data.summary));
    console.log('RESULT COUNT:', (data.results || []).length);

    const results = (data.results || []).map(result => {
      const derived = result.document?.derivedStructData;
      const struct  = result.document?.structData;

      // Some documents expose URL as derivedStructData.link, others as derivedStructData.url.
      // Support both so GitHub issues/PRs/discussions are surfaced as clickable results.
      const url = derived?.link || derived?.url || struct?.url || null;

      // title: website crawl uses derivedStructData.title; structured docs use keyPropertyMapping:"title"
      // which also maps to derivedStructData.title — fall back to structData.title if missing.
      const title = derived?.title || struct?.title || null;

      // snippets: generated from content field when keyPropertyMapping:"body" is set in the schema.
      // Falls back to structData.content substring for structured docs without body mapping.
      const rawSnippet = derived?.snippets?.[0]?.snippet || struct?.content?.slice(0, 300) || null;

      return {
        id:      result.document?.id,
        title,
        url,
        snippet: rawSnippet,
        type: struct?.type || null,
        repo: struct?.repo || null,
        state: struct?.state || null,
        section: url?.replace('https://interlisp.org/', '')?.split('/')?.[0] || '',
      };
    }).filter(r => r?.url);

    // Build a map of document ID to URL from search results
    const docIdToUrl = {};
    (data.results || []).forEach(result => {
      const id  = result.document?.id;
      const derived = result.document?.derivedStructData;
      const url = derived?.link || derived?.url || result.document?.structData?.url;
      if (id && url) docIdToUrl[id] = url;
    });
    
    // Enrich references with URLs by matching document IDs
    const references = (data.summary?.summaryWithMetadata?.references || []).map(ref => {
      // Extract document ID from the full document path
      const docId = ref.document?.split('/').pop();
      return {
        title: ref.title,
        uri:   docIdToUrl[docId] || null,
        docId
      };
    });
    
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
