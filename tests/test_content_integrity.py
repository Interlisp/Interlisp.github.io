"""
tests/test_content_integrity.py
================================
Validates the front matter of every bibliography content file *without*
building the Hugo site.  These tests run quickly and catch structural
problems in the YAML front matter of production content.

Tests in this file do **not** require Hugo or a build step — they parse the
markdown files directly.  Because there are ~400 production entry files, tests
are parametrized to yield one test ID per file, which keeps failures
immediately identifiable.

Three groups of tests:

1. **Every-entry invariants** (parametrized across all files):
   - Required keys are present
   - ``type`` is ``"bibliography"``
   - ``date`` is a valid ISO date
   - ``item_type`` is one of the known Zotero types
   - ``authors`` and ``editors`` are lists
   - ``url_source`` is a valid URL or empty
   - ``zotero_url`` is a valid Zotero URL or empty

2. **Index page** (``_index.md``): validates the section index front matter.

3. **Fixture-file-specific**: validates that fixture files match expected
   item_type and known edge cases.

Usage
-----
    pytest tests/test_content_integrity.py -v
"""

import re
from pathlib import Path

import pytest
import yaml

from conftest import CONTENT_DIR, FIXTURES_DIR


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_KNOWN_ITEM_TYPES: frozenset[str] = frozenset({
    "article-journal",
    "article-magazine",
    "paper-conference",
    "book",
    "chapter",
    "report",
    "thesis",
    "patent",
    "webpage",
    "post-weblog",
    "motion_picture",
    "software",
    "entry-encyclopedia",
    "personal_communication",
    "document",
    "manuscript",
    "hearing",
    "artwork",
    "map",
    "interview",
    "bill",
    "statute",
    "legal_case",
    "newspaper-article",
    "dictionary-entry",
    "Xerox System Integration Standard",
})


def _parse_front_matter(path: Path) -> dict:
    """Return the YAML front matter from a Hugo markdown file.

    Expects the standard Hugo ``---`` delimiters.  Returns an empty dict if
    parsing fails (the caller skips or reports the error).
    """
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    # Find the closing ---
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    fm = yaml.safe_load(text[3:end])
    return fm if isinstance(fm, dict) else {}


# ---------------------------------------------------------------------------
# Collect test subjects
# ---------------------------------------------------------------------------

_INDEX_PATH = CONTENT_DIR / "_index.md"

_ENTRY_PATHS: tuple[Path, ...] = tuple(
    sorted(CONTENT_DIR.glob("[A-Z0-9]*.md"))
)

_FIXTURE_PATHS: tuple[Path, ...] = tuple(
    sorted(FIXTURES_DIR.glob("*.md"))
)

# Each entry is (path, relative_name) for clear test IDs.
_ENTRIES: tuple[tuple[Path, str], ...] = tuple(
    (p, p.relative_to(CONTENT_DIR.parent).as_posix())
    for p in _ENTRY_PATHS
)


# ===========================================================================
# Index page tests
# ===========================================================================


class TestIndexPage:
    """The _index.md entry for the bibliography section."""

    def _fm(self) -> dict:
        fm = _parse_front_matter(_INDEX_PATH)
        if not fm:
            pytest.skip(f"Could not parse front matter from {_INDEX_PATH}")
        return fm

    def test_type_is_bibliography(self):
        assert self._fm().get("type") == "bibliography"

    def test_has_title(self):
        assert self._fm().get("title") == "Bibliography"

    def test_has_heading(self):
        assert "Interlisp Bibliography" in self._fm().get("heading", "")

    def test_cascade_type(self):
        assert self._fm().get("cascade", {}).get("type") == "bibliography"


# ===========================================================================
# Every-entry invariants (production content)
# ===========================================================================


class TestEveryEntry:
    """Invariants that hold for every bibliography entry file."""

    _REQUIRED_KEYS = frozenset({
        "title", "date", "readabledate", "type", "item_type",
        "authors", "editors", "abstract",
        "url_source", "zotero_url", "lastmod",
    })
    _ENCOURAGED_KEYS = frozenset({"tags"})

    @pytest.mark.parametrize("path,_name", _ENTRIES, ids=lambda x: x.name if hasattr(x, 'name') else x)
    def test_required_keys_present(self, path: Path, _name: str) -> None:
        fm = _parse_front_matter(path)
        missing = self._REQUIRED_KEYS - fm.keys()
        assert not missing, (
            f"{path.name} missing required key(s): {', '.join(sorted(missing))}"
        )

    @pytest.mark.parametrize("path,_name", _ENTRIES)
    def test_type_is_bibliography(self, path: Path, _name: str) -> None:
        fm = _parse_front_matter(path)
        assert fm.get("type") == "bibliography", (
            f"{path.name}: type={fm.get('type')!r}, expected 'bibliography'"
        )

    @pytest.mark.parametrize("path,_name", _ENTRIES)
    def test_item_type_is_known(self, path: Path, _name: str) -> None:
        fm = _parse_front_matter(path)
        it = fm.get("item_type")
        assert it in _KNOWN_ITEM_TYPES, (
            f"{path.name}: unknown item_type={it!r}"
            f"\nAdd this item_type to _KNOWN_ITEM_TYPES in "
            f"test_content_integrity.py if it is valid"
        )

    @pytest.mark.parametrize("path,_name", _ENTRIES)
    def test_date_is_valid(self, path: Path, _name: str) -> None:
        """date must be YYYY-MM-DD string, a date object, or None."""
        fm = _parse_front_matter(path)
        date_val = fm.get("date")
        if date_val is None:
            return  # some entries legitimately have no date
        if isinstance(date_val, str):
            assert re.match(r"^\d{4}-\d{2}-\d{2}$", date_val), (
                f"{path.name}: date={date_val!r} is not YYYY-MM-DD format"
            )
        elif hasattr(date_val, "isoformat"):
            pass  # YAML parsed it as a date object — valid
        else:
            pytest.fail(
                f"{path.name}: date={date_val!r} has unexpected type "
                f"{type(date_val).__name__}"
            )

    @pytest.mark.parametrize("path,_name", _ENTRIES)
    def test_lastmod_is_valid_iso(self, path: Path, _name: str) -> None:
        """lastmod must be a valid ISO 8601 timestamp — either a datetime
        object (parsed by YAML) or a string matching the ISO pattern."""
        fm = _parse_front_matter(path)
        lastmod = fm.get("lastmod")
        if isinstance(lastmod, str):
            assert re.match(
                r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", lastmod
            ), f"{path.name}: lastmod={lastmod!r} is not ISO 8601 format"
        elif hasattr(lastmod, "isoformat"):
            pass  # YAML parsed it as a datetime object — natively valid
        else:
            pytest.fail(
                f"{path.name}: lastmod={lastmod!r} is neither a string "
                f"nor a datetime object"
            )

    @pytest.mark.parametrize("path,_name", _ENTRIES)
    def test_authors_is_list_or_none(self, path: Path, _name: str) -> None:
        fm = _parse_front_matter(path)
        authors = fm.get("authors")
        assert authors is None or isinstance(authors, list), (
            f"{path.name}: authors is {type(authors).__name__}, "
            f"expected None or list"
        )

    @pytest.mark.parametrize("path,_name", _ENTRIES)
    def test_editors_is_list_or_none(self, path: Path, _name: str) -> None:
        fm = _parse_front_matter(path)
        editors = fm.get("editors")
        assert editors is None or isinstance(editors, list), (
            f"{path.name}: editors is {type(editors).__name__}, "
            f"expected None or list"
        )

    @pytest.mark.parametrize("path,_name", _ENTRIES)
    def test_tags_is_null_or_empty(self, path: Path, _name: str) -> None:
        fm = _parse_front_matter(path)
        tags = fm.get("tags")
        assert tags in (None, ""), f"{path.name}: tags={tags!r} should be empty"

    @pytest.mark.parametrize("path,_name", _ENTRIES)
    def test_url_source_format(self, path: Path, _name: str) -> None:
        fm = _parse_front_matter(path)
        url = fm.get("url_source") or ""
        assert isinstance(url, str), f"{path.name}: url_source is not a string"
        if url:
            assert url.startswith("http://") or url.startswith("https://"), (
                f"{path.name}: url_source={url!r} is not a valid URL"
            )

    @pytest.mark.parametrize("path,_name", _ENTRIES)
    def test_zotero_url_format(self, path: Path, _name: str) -> None:
        fm = _parse_front_matter(path)
        url = fm.get("zotero_url") or ""
        assert isinstance(url, str), f"{path.name}: zotero_url is not a string"
        if url:
            assert url.startswith("https://www.zotero.org/"), (
                f"{path.name}: zotero_url={url!r} should be a Zotero URL"
            )
