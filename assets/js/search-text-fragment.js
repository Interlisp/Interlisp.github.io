/**
 * Text Fragment Enhancement for Google Programmable Search Engine
 * 
 * This script intercepts clicks on GCSE search result links and adds
 * text fragment highlighting (#:~:text=...) to navigate users directly
 * to the relevant content on the target page.
 * 
 * Text fragments are supported in Chrome 80+, Edge 80+, and other
 * Chromium-based browsers. Firefox and Safari have limited support.
 */

(function() {
  'use strict';

  // Get the search query from the URL
  function getSearchQuery() {
    const params = new URLSearchParams(window.location.search);
    return params.get('q') || '';
  }

  // Create a text fragment from search terms
  function createTextFragment(query) {
    if (!query) return '';
    
    // Clean and encode the query for use in text fragment
    // Use the first few significant words (avoid very long fragments)
    const words = query.trim().split(/\s+/).slice(0, 5);
    const fragment = words.join(' ');
    
    return '#:~:text=' + encodeURIComponent(fragment);
  }

  // Check if browser supports text fragments
  function supportsTextFragments() {
    return 'fragmentDirective' in document || 
           // Chrome/Edge support detection
           (navigator.userAgent.includes('Chrome') || navigator.userAgent.includes('Edg'));
  }

  // Intercept clicks on GCSE result links
  function setupLinkInterception() {
    const query = getSearchQuery();
    if (!query || !supportsTextFragments()) return;

    const textFragment = createTextFragment(query);

    // Use event delegation since GCSE results are loaded dynamically
    document.addEventListener('click', function(event) {
      // Find if click was on a GCSE result link
      const link = event.target.closest('.gs-title a, a.gs-title');
      if (!link) return;

      const href = link.getAttribute('href');
      if (!href) return;

      // Only modify links to our own site
      const currentHost = window.location.hostname;
      try {
        const linkUrl = new URL(href, window.location.origin);
        if (linkUrl.hostname !== currentHost) return;
        
        // Don't add fragment if one already exists
        if (linkUrl.hash && !linkUrl.hash.startsWith('#:~:text=')) return;
        
        // Modify the link to include text fragment
        event.preventDefault();
        const newUrl = href.split('#')[0] + textFragment;
        window.location.href = newUrl;
      } catch (e) {
        // Invalid URL, let it proceed normally
      }
    }, true);
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupLinkInterception);
  } else {
    setupLinkInterception();
  }
})();
