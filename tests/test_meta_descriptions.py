"""
tests/test_meta_descriptions.py
===============================
Validates the site-wide ``<meta name="description">`` output added in Phase 1.3
of ``docs/SEO_IMPROVEMENT_PLAN.md``.

The description for every page is produced by
``layouts/_partials/page-description.html`` and injected by Docsy's ``head.html``.

What is checked
---------------
* Every rendered page (except alias/redirect pages) has a non-empty description.
* No description exceeds the hard cap of 200 characters.
* Content pages (the ones a person actually navigates to) are within the
  150-160 character sweet spot.
* Bibliography descriptions are capped at 160 characters.
* Content-page descriptions are unique.

Redirect/alias pages (Hugo emits ``<meta http-equiv="refresh">`` for these) are
skipped: their canonical points at another page and they are ``noindex``.

Usage
-----
    pytest tests/test_meta_descriptions.py -v
    PYTEST_FORCE_HUGO_BUILD=1 pytest tests/test_meta_descriptions.py -v
"""

import html as html_mod
import re
from pathlib import Path

import pytest

from conftest import TEST_PUBLIC

# `<meta name="description" content="...">`, tolerating either attribute order.
_META_DESC_PATTERNS = (
    re.compile(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', re.I | re.S),
    re.compile(r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']', re.I | re.S),
)
_REFRESH_RE = re.compile(r'http-equiv=["\']refresh["\']', re.I)

# A content page is one a person navigates to. Excluded: alias pages, the 404
# page, auto-generated taxonomy pages, and bibliography pages.
_TAXONOMY_LISTS = {"authors", "categories", "tags", "item_type", "author"}
_EXCLUDED_PREFIXES = ("author/", "item_type/")

# Bibliography pages are identified from the rendered HTML, not the URL: an
# entry page (``layouts/bibliography/single.html``) contains the marker below,
# and the section index is the listing page. Hand-written ``type: docs`` pages
# that merely live under the bibliography tree (``intake/``,
# ``zotero-resources/``) lack the marker and are ordinary content pages.
_BIBLIOGRAPHY_SECTION = "history/bibliography"
_BIBLIOGRAPHY_ENTRY_MARKER = 'class="bibliography-entry"'


def _built_pages() -> list[Path]:
    if not TEST_PUBLIC.exists():
        pytest.skip(
            f"Testing build not found at {TEST_PUBLIC}. Run "
            "'hugo --environment testing --destination tests/public_test'."
        )
    pages = sorted(TEST_PUBLIC.rglob("index.html"))
    not_found = TEST_PUBLIC / "404.html"
    if not_found.exists():
        pages.append(not_found)
    return pages


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _is_redirect(html: str) -> bool:
    return bool(_REFRESH_RE.search(html))


def _description(html: str) -> str | None:
    for pattern in _META_DESC_PATTERNS:
        m = pattern.search(html)
        if m:
            # Descriptions are HTML-escaped inside the attribute (e.g. &#39; for
            # an apostrophe). Measure the visible text, as a search engine would.
            return html_mod.unescape(m.group(1))
    return None


def _slug(path: Path) -> str:
    """URL-style slug of a built page, e.g. 'software/index.html' -> 'software'."""
    if path.name == "404.html":
        return "404"
    rel = path.parent.relative_to(TEST_PUBLIC)
    return "" if str(rel) == "." else str(rel).replace("\\", "/")


def _is_bibliography_entry(html: str) -> bool:
    return _BIBLIOGRAPHY_ENTRY_MARKER in html


def _is_bibliography(slug: str, html: str) -> bool:
    """Auto-generated bibliography entries, plus the section index page."""
    return _is_bibliography_entry(html) or slug == _BIBLIOGRAPHY_SECTION


def _is_content_page(slug: str, html: str) -> bool:
    if slug == "404" or slug in _TAXONOMY_LISTS:
        return False
    if any(slug == p.rstrip("/") or slug.startswith(p) for p in _EXCLUDED_PREFIXES):
        return False
    if _is_bibliography(slug, html):
        return False
    return True


@pytest.fixture(scope="module")
def pages() -> dict[str, str]:
    """Map slug -> rendered HTML for every non-redirect built page."""
    out: dict[str, str] = {}
    for path in _built_pages():
        html = _read(path)
        if _is_redirect(html):
            continue
        out[_slug(path)] = html
    assert out, "No non-redirect pages were found in the testing build"
    return out


# ===========================================================================
# Presence
# ===========================================================================


def test_every_page_has_a_description(pages: dict[str, str]) -> None:
    missing = [
        slug for slug, html in pages.items() if not (_description(html) or "").strip()
    ]
    assert not missing, "Pages missing a meta description:\n" + "\n".join(sorted(missing))


# ===========================================================================
# Length
# ===========================================================================


def test_no_description_exceeds_hard_cap(pages: dict[str, str]) -> None:
    over = [
        (slug, len(desc))
        for slug, html in pages.items()
        if (desc := _description(html)) is not None and len(desc) > 200
    ]
    assert not over, "Descriptions over 200 characters:\n" + "\n".join(
        f"{slug}: {n}" for slug, n in sorted(over)
    )


def test_content_pages_in_target_range(pages: dict[str, str]) -> None:
    bad = []
    for slug, html in pages.items():
        if not _is_content_page(slug, html):
            continue
        desc = _description(html)
        assert desc is not None
        if not 150 <= len(desc) <= 160:
            bad.append((slug, len(desc)))
    assert not bad, "Content pages outside 150-160 characters:\n" + "\n".join(
        f"{slug}: {n}" for slug, n in sorted(bad)
    )


def test_bibliography_descriptions_capped(pages: dict[str, str]) -> None:
    bad = []
    for slug, html in pages.items():
        if not _is_bibliography(slug, html):
            continue
        desc = _description(html) or ""
        if len(desc) > 160:
            bad.append((slug, len(desc)))
    assert not bad, "Bibliography descriptions over 160 characters:\n" + "\n".join(
        f"{slug}: {n}" for slug, n in sorted(bad)
    )


# ===========================================================================
# Uniqueness
# ===========================================================================


def test_content_descriptions_are_unique(pages: dict[str, str]) -> None:
    seen: dict[str, list[str]] = {}
    for slug, html in pages.items():
        if not _is_content_page(slug, html):
            continue
        desc = _description(html)
        if desc:
            seen.setdefault(desc, []).append(slug)
    dupes = {d: slugs for d, slugs in seen.items() if len(slugs) > 1}
    assert not dupes, "Duplicate content-page descriptions:\n" + "\n".join(
        f"{d!r} -> {sorted(slugs)}" for d, slugs in sorted(dupes.items())
    )
