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
      if (!derived) return null;
    
      const url = derived.link || null;
      const snippet = derived.snippets?.[0]?.snippet || null;
      // Strip angle brackets to prevent HTML/script tag injection in display text
      const stripHtml = (str) => str ? str.replace(/[<>]/g, '') : null;
      
      return {
        id:      result.document?.id,
        title:   derived.title || null,
        url,
        snippet: stripHtml(derived.snippets?.[0]?.snippet || null),
        section: url?.replace('https://interlisp.org/', '')?.split('/')?.[0] || '',
      };
    }).filter(r => r?.url);

    // Build a map of document ID to URL from search results
    const docIdToUrl = {};
    (data.results || []).forEach(result => {
      const id  = result.document?.id;
      const url = result.document?.derivedStructData?.link;
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
  const base = `You are a search assistant for the Interlisp documentation site.
Answer questions clearly and concisely. Always cite the sources you used.
If no relevant results exist, say so directly rather than guessing.`;

  if (context) {
    return `${base}\nThe user is currently browsing the "${context}" section — prioritize results from that section where relevant.`;
  }
  return base;
}