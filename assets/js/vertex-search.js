import { marked } from 'marked';
import DOMPurify from 'dompurify';

(function () {
  'use strict';

  marked.setOptions({
    gfm: true,
    breaks: true
  });

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

  function renderSummaryMarkdown(summaryText, citationCount) {
    const linkedMarkdown = (summaryText || '').replace(/\[(\d+)\]/g, (_, num) => {
      const index = Number(num);
      if (!Number.isInteger(index) || index < 1 || index > citationCount) return `[${num}]`;
      return `[${num}](#source-row-${index})`;
    });

    const html = marked.parse(linkedMarkdown);
    return DOMPurify.sanitize(html, {
      ALLOWED_TAGS: [
        'a', 'p', 'ul', 'ol', 'li', 'strong', 'em', 'code', 'pre',
        'blockquote', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'br'
      ],
      ALLOWED_ATTR: ['href', 'title', 'target', 'rel', 'id', 'class']
    });
  }

  function renderResultSnippet(snippetText, result) {
    if (!snippetText) return '';
    const normalized = normalizeSnippetText(snippetText, result);
    const html = marked.parse(normalized);
    return DOMPurify.sanitize(html, {
      ALLOWED_TAGS: ['p', 'b', 'strong', 'em', 'code', 'pre', 'br', 'ul', 'ol', 'li', 'a'],
      ALLOWED_ATTR: ['href', 'title', 'target', 'rel']
    });
  }

  function decodeHtmlEntities(text) {
    const textarea = document.createElement('textarea');
    textarea.innerHTML = String(text || '');
    return textarea.value;
  }

  function normalizeSnippetText(text, result) {
    let output = decodeHtmlEntities(text);

    // Repair malformed highlight markers like "bIssue/b" or "bmedley issues/b".
    output = output.replace(/(^|[\s(\[{])b([^\n]{1,120}?)\/b(?=[\s)\]}.,;:!?]|$)/gi,
      (match, prefix, value) => `${prefix}<strong>${value.trim()}</strong>`);

    // Repair malformed URLs where emphasis markers leak into the URL text.
    output = output
      .replace(/https?:\/\/b/gi, 'https://')
      .replace(/\bb([a-z0-9.-]+)\/b/gi, '$1')
      .replace(/\/(b)([a-z0-9._-]+)/gi, '/$2')
      .replace(/([a-z0-9._-]+)\/b(?=\/|\b)/gi, '$1')
      .replace(/\s*\.\.\.\s*/g, ' ');

    output = normalizeGithubIssueMentions(output, result);

    // Drop noisy raw URL tails often appended by snippet extraction.
    output = output.replace(/https?:\/\/\S+$/i, '');

    // Normalize whitespace for cleaner one-line snippets.
    output = output.replace(/\s+/g, ' ').trim();
    return output;
  }

  function normalizeGithubIssueMentions(text, result) {
    const repo = result?.repo;
    if (!repo) return text;

    // Fix malformed markdown links like: [Issue 609](https://bgithub/b.com/Interlisp/bmedley/b/bissues/b/609)
    let output = text.replace(
      /\[(Issue\s+#?\d+)\]\((https?:\/\/[^)]+)\)/gi,
      (match, label, rawUrl) => {
        const issueNumberMatch = label.match(/(\d+)/);
        if (!issueNumberMatch) return match;
        const issueNumber = issueNumberMatch[1];
        const cleanUrl = `https://github.com/Interlisp/${repo}/issues/${issueNumber}`;
        return `[${label}](${cleanUrl})`;
      }
    );

    // Convert plain text mentions like "Issue 609" or "Issue #609" into links.
    output = output.replace(/\bIssue\s+#?(\d+)\b/g, (match, num) => {
      const issueUrl = `https://github.com/Interlisp/${repo}/issues/${num}`;
      return `[Issue ${num}](${issueUrl})`;
    });

    return output;
  }

  function formatDisplayUrl(rawUrl) {
    if (!rawUrl) return '';

    try {
      const parsed = new URL(rawUrl);
      const host = parsed.host.replace(/^www\./, '');
      const pathSegments = parsed.pathname.split('/').filter(Boolean);
      const path = pathSegments.length > 0 ? ` › ${pathSegments.join(' › ')}` : '';
      return `${host}${path}`;
    } catch (_) {
      return rawUrl;
    }
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
        const refs = data.summary?.citations || [];
        const validRefs = refs.filter(r => r.title || r.uri);

        summaryTxt.innerHTML = renderSummaryMarkdown(data.summary.summaryText, validRefs.length);

        const inlineRefs = summaryTxt.querySelectorAll('a[href^="#source-row-"]');
        inlineRefs.forEach((el) => {
          el.classList.add('summary-inline-citation');
          el.setAttribute('aria-label', `Jump to source ${el.textContent}`);
        });

        summaryEl.style.display = 'block';

        // Remove stale source rows before rendering the latest list.
        const previousCitations = summaryEl.querySelector('.search-citations');
        if (previousCitations) previousCitations.remove();

        if (validRefs.length > 0) {
          const citationHtml = validRefs.map((ref, i) => `
            <div id="source-row-${i + 1}" class="search-citation">
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
      } else {
        summaryTxt.innerHTML = '';
        summaryEl.style.display = 'none';
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
          <h5 class="td-search-hit__title mb-1">
            <a href="${escapeHtml(r.url)}">${escapeHtml(r.title || 'Untitled')}</a>
          </h5>
          <p class="td-search-hit__url mb-1"><small>${escapeHtml(formatDisplayUrl(r.url))}</small></p>
          ${r.snippet ? `<div class="td-search-hit__snippet mb-1 text-muted small">${renderResultSnippet(r.snippet, r)}</div>` : ''}
          ${(r.type || r.repo || r.state)
            ? `<p class="td-search-hit__meta mb-0">
                ${r.type ? `<span class="search-meta-chip">${escapeHtml(r.type)}</span>` : ''}
                ${r.repo ? `<span class="search-meta-chip">${escapeHtml(r.repo)}</span>` : ''}
                ${r.state ? `<span class="search-meta-chip">${escapeHtml(r.state)}</span>` : ''}
              </p>`
            : ''}
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