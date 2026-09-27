/*
Copyright 2018 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

// Local override of Docsy's search.js. Adds dual-mode support: the
// pre-search mode picker (see layouts/_partials/search-input.html) stores
// the user's choice, and the Enter-to-search redirect below carries it as
// ?mode=ai so the results page opens directly in AI-assisted mode.
// Standard search remains the default when nothing is stored.

(function ($) {
  'use strict';

  var STORAGE_KEY = 'interlisp-search-mode';

  function getPreferredMode() {
    try {
      return window.localStorage.getItem(STORAGE_KEY) === 'ai' ? 'ai' : 'standard';
    } catch (_) {
      return 'standard';
    }
  }

  function setPreferredMode(mode, skipEvent) {
    try {
      window.localStorage.setItem(STORAGE_KEY, mode === 'ai' ? 'ai' : 'standard');
    } catch (_) {}
    syncPickers(mode);
    if (!skipEvent) {
      // Notify the results-page toggle (vertex-search.js) on the same page.
      try {
        window.dispatchEvent(new CustomEvent('interlisp:search-mode-change', {
          detail: { mode: mode }
        }));
      } catch (_) {}
    }
  }

  function syncPickers(mode) {
    var useAi = mode === 'ai';
    var pickers = document.querySelectorAll('input.td-search-mode');
    for (var i = 0; i < pickers.length; i++) {
      pickers[i].checked = useAi;
      var group = pickers[i].closest('.td-search-mode-switch');
      if (group) {
        var labels = group.querySelectorAll('.td-search-mode-label');
        for (var j = 0; j < labels.length; j++) {
          var active = labels[j].getAttribute('data-search-mode') === mode;
          if (active) {
            labels[j].classList.add('is-active');
          } else {
            labels[j].classList.remove('is-active');
          }
        }
      }
    }
  }

  var Search = {
    init: function () {
      $(document).ready(function () {
        // Reflect the stored preference in every pre-search picker.
        syncPickers(getPreferredMode());

        $(document).on('change', 'input.td-search-mode', function () {
          setPreferredMode($(this).is(':checked') ? 'ai' : 'standard');
        });

        // Side labels set an explicit mode (they must not merely toggle).
        $(document).on('click', '.td-search-mode-label', function () {
          setPreferredMode($(this).data('search-mode') === 'ai' ? 'ai' : 'standard');
        });

        $(document).on('keypress', '.td-search input', function (e) {
          if (e.keyCode !== 13) {
            return;
          }

          var query = $(this).val();
          var params = new URLSearchParams();
          params.set('q', query);
          if (getPreferredMode() === 'ai') {
            params.set('mode', 'ai');
          }
          var searchPage = '{{ "search/" | absURL }}?' + params.toString();
          document.location = searchPage;

          return false;
        });
      });
    },
  };

  Search.init();

  // Shared with vertex-search.js (results-page toggle).
  window.interlispSearchMode = {
    get: getPreferredMode,
    set: setPreferredMode
  };
})(jQuery);
