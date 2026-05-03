(function () {
  'use strict';

  // Only run on the search results page
  const config = document.getElementById('vertex-search-config');
  if (!config) return;

  const FUNCTION_URL = config.dataset.searchUrl;
  if (!FUNCTION_URL) {
    console.warn('Vertex search URL not configured');
    return;
  }

  // Get query from URL params (?q=...)
  const urlParams = new URLSearchParams(window.location.search);
  const query = urlParams.get('q') || '';

  const statusEl  = document.getElementById('vertex-search-status');
  const hitsEl    = document.getElementById('vertex-search-hits');
  const summaryEl = document.getElementById('vertex-search-summary');
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

    // Update page title to reflect query
    document.title = `Search: ${q}`;
    statusEl.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Searching for <strong>' +
      escapeHtml(q) + '</strong>…';

    try {
      const url = new URL(FUNCTION_URL);
      url.searchParams.set('q', q);

      // Pass referring section as context if coming from a content page
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

      // Hide spinner
      statusEl.style.display = 'none';

      // Show AI summary if available
      if (data.summary?.summaryText) {
        summaryTxt.textContent = data.summary.summaryText;
        summaryEl.style.display = 'block';
      
        // Render numbered citation list
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

      // Show results
      if (!data.results || data.results.length === 0) {
        hitsEl.innerHTML = `<p>No results found for <strong>${escapeHtml(q)}</strong>.</p>`;
        return;
      }

      // Show result count
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

  // Run search on page load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => doSearch(query));
  } else {
    doSearch(query);
  }

})();