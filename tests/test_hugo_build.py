"""
tests/test_hugo_build.py
========================
Validates that the production Hugo build succeeds and produces well-formed
output.  These tests focus on *build quality* — exit code, absence of errors,
presence of critical output files, and sitemap integrity.

They complement test_bibliography_jsonld.py (which validates template output
correctness) and test_html_validation.py (which validates HTML conformance).

The ``production_build`` fixture (defined in conftest.py) runs
``hugo --cleanDestinationDir --logLevel warn`` when the ``public/`` directory
is stale and caches the result for the session.

Usage
-----
    pytest tests/test_hugo_build.py -v

    # Force a fresh production build first:
    PYTEST_FORCE_HUGO_BUILD=1 pytest tests/test_hugo_build.py -v
"""

import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

import pytest
import yaml

from conftest import PROD_PUBLIC, REPO_ROOT


def _get_baseurl_path() -> str:
    """Return the path component of the Hugo baseURL for the active environment.

    When ``baseURL`` contains a path prefix (e.g.
    ``https://interlisp.github.io/interlisp-staging/``), Hugo prepends
    that path (``/interlisp-staging``) to every site-root-relative
    ``href``.  This helper extracts just the path component so link checks
    can strip it before resolving to the filesystem.
    """
    env = os.environ.get("HUGO_ENVIRONMENT", "production")
    env_config = REPO_ROOT / "config" / env / "hugo.yaml"
    if not env_config.exists():
        env_config = REPO_ROOT / "config" / "_default" / "hugo.yaml"
    if env_config.exists():
        with open(env_config) as f:
            cfg = yaml.safe_load(f)
            if cfg and "baseURL" in cfg:
                return urlparse(cfg["baseURL"]).path.rstrip("/") or ""
    return ""


# ---------------------------------------------------------------------------
# Build process tests
# ---------------------------------------------------------------------------


class TestHugoBuildProcess:
    """The Hugo build must complete cleanly."""

    @pytest.fixture(autouse=True)
    def build(self, production_build):
        self.result = production_build

    def test_exits_with_zero(self):
        """Hugo must exit 0; any non-zero exit indicates a build failure."""
        assert self.result.returncode == 0, (
            f"Hugo exited {self.result.returncode}:\n{self.result.stderr}"
        )

    def test_no_error_lines_in_output(self):
        """Hugo must not emit any ERROR-level log lines."""
        error_lines = [
            line for line in self.result.stderr.splitlines()
            if line.strip().startswith("ERROR")
        ]
        assert not error_lines, (
            "Hugo produced ERROR lines:\n" + "\n".join(error_lines)
        )

    def test_no_broken_ref_links(self):
        """Hugo must not report REF_NOT_FOUND — every internal page reference
        used in content must resolve to an existing page."""
        assert "REF_NOT_FOUND" not in self.result.stderr, (
            "Hugo reported unresolved page references (REF_NOT_FOUND).\n"
            "Check content files for broken {{< ref >}} shortcodes:\n"
            + "\n".join(
                l for l in self.result.stderr.splitlines()
                if "REF_NOT_FOUND" in l
            )
        )


# ---------------------------------------------------------------------------
# Output structure tests
# ---------------------------------------------------------------------------


class TestCriticalPagesExist:
    """Key pages must be present in the built output."""

    REQUIRED_PATHS = (
        # Site root
        "index.html",
        # Bibliography section
        "history/bibliography/index.html",
        # Sitemap and robots
        "sitemap.xml",
        "robots.txt",
    )

    @pytest.mark.parametrize("path", REQUIRED_PATHS)
    def test_page_exists(self, path: str) -> None:
        assert (PROD_PUBLIC / path).exists(), (
            f"Required output file missing: public/{path}"
        )


class TestSitemapIntegrity:
    """The sitemap must be valid XML and reference only absolute URLs."""

    @pytest.fixture(autouse=True)
    def sitemap(self):
        path = PROD_PUBLIC / "sitemap.xml"
        if not path.exists():
            pytest.skip("sitemap.xml not found — run a production build first")
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()
        # Strip XML namespace for simpler XPath queries
        self.ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    def test_is_valid_xml(self):
        """sitemap.xml must parse as well-formed XML."""
        assert self.root is not None

    def test_has_url_entries(self):
        """sitemap.xml must contain at least one <url> entry."""
        urls = self.root.findall("sm:url", self.ns)
        assert len(urls) > 0, "sitemap.xml contains no <url> entries"

    def test_all_locs_are_absolute_https(self):
        """Every <loc> in the sitemap must be an absolute https:// URL."""
        bad = []
        for loc in self.root.findall(".//sm:loc", self.ns):
            if not (loc.text or "").startswith("https://"):
                bad.append(loc.text)
        assert not bad, (
            f"{len(bad)} sitemap <loc> values are not absolute https:// URLs:\n"
            + "\n".join(bad[:10])
        )

    def test_bibliography_section_present(self):
        """The bibliography section index must appear in the sitemap."""
        locs = {loc.text for loc in self.root.findall(".//sm:loc", self.ns)}
        assert any("bibliography" in (loc or "") for loc in locs), (
            "No bibliography URL found in sitemap.xml"
        )


class TestHistorySidebarNavigation:
    """The Bibliography section must be reachable from History navigation.

    Regression tests for PR #347: setting only ``cascade.toc_hide`` hid the
    Bibliography entry itself from the History sidebar (Hugo merges a
    section's own cascade into its own Params). The empty
    ``layouts/_partials/section-index.html`` override is intentional and
    must keep suppressing the subpage cards. Either deviation must break
    the build tests.
    """

    @pytest.fixture(autouse=True)
    def history_page(self, production_build):
        self.build_result = production_build
        path = PROD_PUBLIC / "history" / "index.html"
        if not path.exists():
            pytest.skip("history/index.html not found — run a production build first")
        self.content = path.read_text(encoding="utf-8", errors="ignore")

    def test_bibliography_in_sidebar_nav(self) -> None:
        """The sidebar nav on /history/ must link to /history/bibliography/."""
        nav = re.search(
            r'<nav[^>]*id="td-section-nav".*?</nav>',
            self.content,
            re.DOTALL,
        )
        assert nav, "sidebar nav #td-section-nav not found on history page"
        assert "/history/bibliography/" in nav.group(0), (
            "Bibliography entry missing from the History sidebar navigation"
        )

    def test_intake_guide_in_sidebar_nav(self) -> None:
        """The Intake Guide must be listed under Bibliography, while the
        hundreds of generated entries must stay out of the nav."""
        nav = re.search(
            r'<nav[^>]*id="td-section-nav".*?</nav>',
            self.content,
            re.DOTALL,
        )
        assert nav, "sidebar nav #td-section-nav not found on history page"
        nav_html = nav.group(0)
        assert "/history/bibliography/intake/" in nav_html, (
            "Intake Guide entry missing from the sidebar navigation"
        )
        stray_entries = re.findall(
            r'href="/history/bibliography/(?!intake/)[a-z0-9]+/"', nav_html
        )
        assert not stray_entries, (
            "Generated bibliography entries leaking into sidebar navigation:\n"
            + "\n".join(stray_entries[:10])
        )

    def test_no_subpage_cards(self) -> None:
        """The History page must not render section-index subpage cards;
        subpage navigation lives in the sidebar. The empty
        ``layouts/_partials/section-index.html`` override suppresses them."""
        assert '<div class="section-index">' not in self.content, (
            "section-index subpage list should be suppressed on the History page"
        )

    def test_no_sidebar_truncation_warning(self) -> None:
        """Hugo must not truncate sidebar entries — a flood of unhidden
        bibliography entries (e.g. from a stale Zotero cache without
        ``toc_hide``) would trigger this Docsy warning."""
        assert "sidebar entries have been truncated" not in (
            self.build_result.stderr or ""
        ), "Sidebar entries were truncated — bibliography entries may be leaking into navigation"


class TestSearchModeToggle:
    """The Standard / AI-assisted search controls must reach the built site.

    Regression test: ``layouts/_partials/search-input.html`` — the Docsy
    override that renders the pre-search "Standard [switch] AI" picker below
    the search box — was left untracked when the toggle feature was
    committed.  Its JavaScript (``assets/js/search.js``), styles
    (``assets/scss/_styles_project.scss``) and results-page controls
    (``layouts/search.html``) were all committed, so local ``hugo server``
    runs showed the picker while every build from a clean checkout fell back
    to Docsy's ``search-input`` partial, which has none.  The control was
    thus missing from CI builds and the deployed site with its handlers and
    styles still shipping.  These tests assert on rendered markup, because
    the JavaScript and CSS are inert without it.
    """

    @pytest.fixture(autouse=True)
    def dual_mode(self, production_build):
        self.build_result = production_build

        params_file = REPO_ROOT / "config" / "_default" / "params.yaml"
        if not params_file.exists():
            pytest.skip("config/_default/params.yaml not found")
        with open(params_file) as f:
            params = yaml.safe_load(f) or {}

        # Both backends must be configured for either control to render.
        if not (params.get("gcs_engine_id") and params.get("vertex_search_url")):
            pytest.skip(
                "dual search mode not configured — both gcs_engine_id and "
                "vertex_search_url are required"
            )

        index = PROD_PUBLIC / "index.html"
        search = PROD_PUBLIC / "search" / "index.html"
        if not (index.exists() and search.exists()):
            pytest.skip("index.html or search/index.html not built")

        self.index_html = index.read_text(encoding="utf-8", errors="ignore")
        self.search_html = search.read_text(encoding="utf-8", errors="ignore")

    def test_presearch_picker_rendered(self) -> None:
        """The "Standard [switch] AI" picker must render under the search box.

        Its presence proves the local ``search-input.html`` override is part
        of the repository; without it Hugo silently falls back to Docsy's
        version and the picker disappears.
        """
        assert 'class="td-search-mode-switch"' in self.index_html, (
            "Pre-search mode picker missing from index.html — "
            "layouts/_partials/search-input.html is not being used"
        )
        for selector in ('data-search-mode="standard"', 'data-search-mode="ai"'):
            assert selector in self.index_html, (
                f"Picker label {selector} missing from index.html"
            )
        assert 'class="form-check-input td-search-mode"' in self.index_html, (
            "Picker switch input missing from index.html"
        )

    def test_picker_script_shipped(self) -> None:
        """A bundled script must reference the picker selectors, so the
        control is wired to localStorage and the ``?mode=ai`` redirect."""
        js_dir = PROD_PUBLIC / "js"
        if not js_dir.is_dir():
            pytest.skip("public/js not built")
        wired = any(
            "td-search-mode-switch" in path.read_text(encoding="utf-8", errors="ignore")
            for path in js_dir.rglob("*.js")
        )
        assert wired, (
            "No bundled script references td-search-mode-switch — "
            "assets/js/search.js was not built into the site"
        )

    def test_results_page_toggle_rendered(self) -> None:
        """The results page must render both mode radios and the container
        that assets/js/vertex-search.js binds to before doing anything."""
        for fragment in (
            'id="search-mode-standard"',
            'id="search-mode-ai"',
            'id="vertex-search-container"',
        ):
            assert fragment in self.search_html, (
                f"{fragment} missing from search/index.html"
            )

    def test_results_page_toggle_has_one_radiogroup(self) -> None:
        """The mode radios must sit in a single ``role="radiogroup"``.

        The toggle was originally wrapped in a radiogroup nested inside a
        second one, which exposes the radios to assistive technology as a
        group within a group.
        """
        groups = self.search_html.count('role="radiogroup"')
        assert groups == 1, (
            f"Expected exactly 1 role=\"radiogroup\" on search/index.html, "
            f"found {groups} — the mode toggle radiogroups are nested"
        )


class TestInternalLinks:
    """All internal href links in the built HTML must resolve to existing pages."""

    def test_no_broken_internal_links(self) -> None:
        if not PROD_PUBLIC.exists():
            pytest.skip("public/ not built — run hugo first")

        prefix = _get_baseurl_path()
        broken: list[tuple[str, str]] = []

        for html_file in PROD_PUBLIC.rglob("*.html"):
            content = html_file.read_text(encoding="utf-8", errors="ignore")
            # Match href values that start with / (site-root-relative)
            for href in re.findall(r'href="(/[^"#?]*?)"', content):
                # If baseURL has a path component (e.g., /interlisp-staging),
                # Hugo prepends it to site-root-relative links. Strip it before
                # resolving to the filesystem.
                resolved = href
                if prefix and href.startswith(prefix + "/"):
                    resolved = href[len(prefix):]
                target = PROD_PUBLIC / resolved.lstrip("/")
                if not target.exists() and not (target / "index.html").exists():
                    broken.append((str(html_file.relative_to(PROD_PUBLIC)), href))

        assert not broken, (
            f"{len(broken)} broken internal links found:\n"
            + "\n".join(f"  {page} → {link}" for page, link in broken[:20])
        )
