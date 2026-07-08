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
    ``https://stumbo.github.io/InterlispDraft.github.io/``), Hugo prepends
    that path (``/InterlispDraft.github.io``) to every site-root-relative
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
                # If baseURL has a path component (e.g., /InterlispDraft.github.io),
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
