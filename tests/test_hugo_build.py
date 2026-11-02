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

import html
import json
import os
import re
import subprocess
import uuid
import shutil
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


def _run_404_script(content: str, path: str, tmp_path: Path) -> dict:
    """Execute the built 404 page script in Node with a minimal fake DOM.

    Returns the visible state and rewritten links for ``path``.
    """
    node = shutil.which("node")
    if not node:
        pytest.skip("Node.js is required to exercise the 404 page script")

    script_match = re.search(
        r'<script id="not-found-script">(.*?)</script>', content, re.DOTALL
    )
    assert script_match, "not-found-script block not found in 404.html"

    data_match = re.search(
        r'<script type="application/json" id="bibliography-removed-data">(.*?)</script>',
        content,
        re.DOTALL,
    )
    assert data_match, "bibliography removed data not found in 404.html"

    harness = "\n".join(
        [
            "function makeElement(id) {",
            "  const classes = new Set();",
            "  return {",
            "    id,",
            '    textContent: "",',
            '    href: "",',
            "    classes,",
            "    classList: {",
            "      add: (c) => classes.add(c),",
            "      remove: (c) => classes.delete(c),",
            "      contains: (c) => classes.has(c),",
            "    },",
            "  };",
            "}",
            "const ids = [",
            '  "not-found-generic", "not-found-bibliography",',
            '  "not-found-bib-key", "not-found-bib-title",',
            '  "not-found-bib-title-wrap", "not-found-bib-zotero",',
            '  "not-found-bib-browse", "not-found-bib-intake",',
            '  "not-found-bib-home",',
            "];",
            "const elements = Object.fromEntries(ids.map((id) => [id, makeElement(id)]));",
            'elements["not-found-bibliography"].classList.add("d-none");',
            'elements["not-found-bib-title-wrap"].classList.add("d-none");',
            "const removedData = { textContent: "
            + json.dumps(data_match.group(1))
            + " };",
            "const byId = Object.assign({}, elements, {",
            '  "bibliography-removed-data": removedData,',
            "});",
            "const window = { location: { pathname: "
            + json.dumps(path)
            + " } };",
            'const document = { title: "", getElementById: (id) => byId[id] || null };',
            script_match.group(1),
            "console.log(JSON.stringify({",
            '  visible: !elements["not-found-bibliography"].classes.has("d-none"),',
            '  key: elements["not-found-bib-key"].textContent,',
            '  browse: elements["not-found-bib-browse"].href,',
            '  intake: elements["not-found-bib-intake"].href,',
            '  home: elements["not-found-bib-home"].href,',
            '  title: document.title,',
            "}));",
        ]
    )

    script_file = tmp_path / "check-404.js"
    script_file.write_text(harness, encoding="utf-8")
    result = subprocess.run(
        [node, str(script_file)],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout.strip().splitlines()[-1])


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


class TestNotFoundPage:
    """The custom 404 page must handle removed bibliography entries."""

    @pytest.fixture(autouse=True)
    def page(self):
        path = PROD_PUBLIC / "404.html"
        if not path.exists():
            pytest.skip("404.html not found — run a production build first")
        self.content = path.read_text(encoding="utf-8", errors="ignore")

    def test_has_bibliography_fallback(self) -> None:
        assert 'id="not-found-bibliography"' in self.content
        assert "/history/bibliography/" in self.content
        assert "bibliography-removed-data" in self.content

    def test_embeds_removed_entries_as_json(self) -> None:
        match = re.search(
            r'<script type="application/json" id="bibliography-removed-data">(.*?)</script>',
            self.content,
            re.DOTALL,
        )
        assert match, "Removed-bibliography data block not found in 404.html"
        removed = json.loads(match.group(1))
        assert isinstance(removed, list)
        for entry in removed:
            assert isinstance(entry.get("key"), str) and entry["key"]
            assert isinstance(entry.get("title"), str)

    def test_is_noindex(self) -> None:
        assert re.search(
            r'<meta name="robots" content="[^"]*noindex',
            self.content,
        ), "404 page must be marked noindex"

    def test_bibliography_match_ignores_site_prefix(self) -> None:
        """Staging previews live under /Interlisp.staging/pr-<N>/ and are
        served by the domain-level 404 page, so detection must match the end
        of the path rather than a build-time baseURL prefix."""
        assert r"/\/history\/bibliography\/([^/?#]+(?:\/[^/?#]+)*)\/?(?:[?#]|$)/" in self.content
        assert "startsWith(bibRoot)" not in self.content
        for element_id in (
            "not-found-bib-browse",
            "not-found-bib-intake",
            "not-found-bib-home",
        ):
            assert f'id="{element_id}"' in self.content

    @pytest.mark.parametrize(
        ("path", "expected_root"),
        (
            ("/history/bibliography/wxmqhqnz/", "/"),
            ("/history/bibliography/WXMQHQNZ", "/"),
            (
                "/Interlisp.staging/pr-355/history/bibliography/wxmqhqnz/",
                "/Interlisp.staging/pr-355/",
            ),
        ),
    )
    def test_bibliography_links_follow_site_prefix(
        self, path: str, expected_root: str, tmp_path: Path
    ) -> None:
        result = _run_404_script(self.content, path, tmp_path)
        assert result["visible"] is True
        assert result["key"] == "WXMQHQNZ"
        assert result["browse"] == expected_root + "history/bibliography/"
        assert result["intake"] == expected_root + "history/bibliography/intake/"
        assert result["home"] == expected_root

    @pytest.mark.parametrize(
        "path",
        (
            "/history/bibliography/",
            "/some/other/page/",
            "/Interlisp.staging/pr-355/history/bibliography/",
        ),
    )
    def test_non_entry_paths_stay_generic(self, path: str, tmp_path: Path) -> None:
        result = _run_404_script(self.content, path, tmp_path)
        assert result["visible"] is False


class TestLegacyRedirects:
    """Aliases and static redirects must exist for known legacy URLs."""

    REDIRECTS = (
        ("doc/info/history.html", "/history/"),
        ("about/partners/index.html", "/project/partners/"),
        ("running/running-with-docker/index.html", "/software/install-and-run/"),
        (
            "running/online/usingonline/index.html",
            "/software/using-medley/online-using/",
        ),
        (
            "medley/using/running/runnning-on-win/index.html",
            "/software/install-and-run/windows/",
        ),
        ("IRM_files/content.htm", "/documentation/IRM.pdf"),
    )

    @pytest.mark.parametrize(("path", "target"), REDIRECTS)
    def test_redirect_exists(self, path: str, target: str) -> None:
        redirect = PROD_PUBLIC / path
        if not redirect.exists():
            pytest.skip("public/ not built — run hugo first")
        content = redirect.read_text(encoding="utf-8", errors="ignore")
        assert target in content, (
            f"Redirect {path} does not point at {target}:\n{content[:200]}"
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


class TestGlossaryTooltips:
    """Timeline glossary links must expose a non-empty Bootstrap tooltip and
    resolve to a rendered glossary anchor."""

    @pytest.fixture(autouse=True)
    def pages(self, production_build):
        timeline_path = PROD_PUBLIC / "history" / "timeline" / "index.html"
        glossary_path = PROD_PUBLIC / "history" / "glossary" / "index.html"
        if not timeline_path.exists() or not glossary_path.exists():
            pytest.skip("built timeline/glossary pages not found — run hugo first")
        self.timeline = timeline_path.read_text(encoding="utf-8", errors="ignore")
        self.glossary = glossary_path.read_text(encoding="utf-8", errors="ignore")
        self.glossary_ids = set(
            re.findall(r'<span id="([^"]+)"[^>]*></span>', self.glossary)
        )

    def _glossary_links(self) -> list[str]:
        return re.findall(
            r'<a\b[^>]*href="/history/glossary/#[^"]+"[^>]*>',
            self.timeline,
        )

    def test_glossary_links_have_tooltips(self) -> None:
        links = self._glossary_links()
        assert links, "No glossary links found in the built timeline"

        missing_toggle: list[str] = []
        missing_title: list[str] = []
        empty_title: list[str] = []

        for tag in links:
            href = re.search(r'href="([^"]+)"', tag).group(1)
            if 'data-bs-toggle="tooltip"' not in tag:
                missing_toggle.append(href)
            title = re.search(r'data-bs-title="([^"]*)"', tag)
            if title is None:
                missing_title.append(href)
            elif not html.unescape(title.group(1)).strip():
                empty_title.append(href)

        assert not missing_toggle, (
            "Glossary links missing data-bs-toggle=\"tooltip\":\n"
            + "\n".join(missing_toggle)
        )
        assert not missing_title, (
            "Glossary links missing data-bs-title:\n" + "\n".join(missing_title)
        )
        assert not empty_title, (
            "Glossary links with empty tooltip text:\n" + "\n".join(empty_title)
        )

    def test_glossary_tooltip_targets_resolve(self) -> None:
        anchors = set(
            re.findall(r'href="/history/glossary/#([^"]+)"', self.timeline)
        )
        missing = sorted(anchors - self.glossary_ids)
        assert not missing, (
            "Glossary tooltip targets not found in the built glossary:\n"
            + "\n".join(missing)
        )

    def test_tooltip_max_chars_config(self) -> None:
        config_path = REPO_ROOT / "config" / "_default" / "params.yaml"
        config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
        max_chars = config.get("glossary", {}).get("tooltip_max_chars")
        assert isinstance(max_chars, int) and max_chars > 0, (
            "params.yaml must define a positive glossary.tooltip_max_chars"
        )

    def test_interlisp_d_uses_custom_tooltip(self) -> None:
        match = re.search(
            r'<a\b[^>]*href="/history/glossary/#interlisp-d"[^>]*>',
            self.timeline,
        )
        assert match is not None, (
            "Timeline does not link to /history/glossary/#interlisp-d"
        )
        title = re.search(r'data-bs-title="([^"]*)"', match.group(0))
        assert title is not None, (
            "Interlisp-D glossary link is missing data-bs-title"
        )
        text = html.unescape(title.group(1))
        assert "D stood for both" in text, (
            "Interlisp-D should use its custom data-tooltip text"
        )
        assert not text.endswith("An implementation of"), (
            "Interlisp-D tooltip still ends with the truncated first <dd>"
        )

    def test_glossary_source_anchors_are_unique(self) -> None:
        source_path = (
            REPO_ROOT / "content" / "en" / "history" / "glossary" / "_index.md"
        )
        source = source_path.read_text(encoding="utf-8")
        spans = re.findall(r'<span id="[^"]+"[^>]*></span>', source)
        ids = [
            re.search(r'id="([^"]+)"', span).group(1)
            for span in spans
        ]
        assert len(ids) == len(set(ids)), "Glossary source anchor IDs are not unique"
        assert set(ids) == self.glossary_ids, (
            "Glossary source anchors do not match the built glossary anchors"
        )
        for span in spans:
            tooltip = re.search(r'data-tooltip="([^"]*)"', span)
            if tooltip is not None:
                assert tooltip.group(1).strip(), (
                    f"Empty data-tooltip in glossary source: {span}"
                )

    def test_all_glossary_anchors_have_tooltips(self, tmp_path: Path) -> None:
        probe_name = f"tooltip-probe-{uuid.uuid4().hex}"
        probe_path = (
            REPO_ROOT / "content" / "en" / "history" / f"{probe_name}.md"
        )
        links = "\n".join(
            f"- [{anchor}](/history/glossary/#{anchor})"
            for anchor in sorted(self.glossary_ids)
        )
        probe_path.write_text(
            "---\n"
            'title: "Glossary tooltip probe"\n'
            "type: docs\n"
            "weight: 9999\n"
            "---\n\n"
            f"{links}\n",
            encoding="utf-8",
        )
        try:
            destination = tmp_path / "public"
            result = subprocess.run(
                ["hugo", "--destination", str(destination), "--logLevel", "warn"],
                cwd=str(REPO_ROOT),
                capture_output=True,
                text=True,
            )
            assert result.returncode == 0, (
                f"Hugo probe build failed (exit {result.returncode}):\n"
                f"--- stdout ---\n{result.stdout}\n"
                f"--- stderr ---\n{result.stderr}"
            )
            probe_html = (
                destination / "history" / probe_name / "index.html"
            ).read_text(encoding="utf-8", errors="ignore")
        finally:
            probe_path.unlink(missing_ok=True)

        links_html = re.findall(
            r'<a\b[^>]*href="/history/glossary/#[^"]+"[^>]*>',
            probe_html,
        )
        assert len(links_html) == len(self.glossary_ids), (
            f"Expected {len(self.glossary_ids)} glossary links in the probe "
            f"page, found {len(links_html)}"
        )

        missing_toggle: list[str] = []
        missing_title: list[str] = []
        empty_title: list[str] = []
        for tag in links_html:
            href = re.search(r'href="([^"]+)"', tag).group(1)
            if 'data-bs-toggle="tooltip"' not in tag:
                missing_toggle.append(href)
            title = re.search(r'data-bs-title="([^"]*)"', tag)
            if title is None:
                missing_title.append(href)
            elif not html.unescape(title.group(1)).strip():
                empty_title.append(href)

        assert not missing_toggle, (
            "Glossary probe links missing data-bs-toggle=\"tooltip\":\n"
            + "\n".join(missing_toggle)
        )
        assert not missing_title, (
            "Glossary probe links missing data-bs-title:\n"
            + "\n".join(missing_title)
        )
        assert not empty_title, (
            "Glossary probe links with empty tooltip text:\n"
            + "\n".join(empty_title)
        )
