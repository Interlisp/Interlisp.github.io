"""
tests/test_bibliography_page.py
===============================
Validates the ``div.bibliography-meta`` block rendered by
``layouts/bibliography/single.html`` for the entry types added by the
bibliography-types implementation (``document``, ``standard``, ``software``)
and for the ``report`` key fix.

``test_bibliography_jsonld.py`` covers the structured-data contract; this
module checks that the same frontmatter values are visible on the page.  The
session-scoped ``hugo_build`` fixture in ``conftest.py`` builds the
``--environment testing`` site, so all assertions run against the ``ZTEST-*``
fixtures and never touch production content.
"""

from __future__ import annotations

import re

import pytest

from conftest import BIB_PUBLIC

pytestmark = pytest.mark.usefixtures("hugo_build")


def _meta_text(slug: str) -> str:
    """Return the entry's metadata block as whitespace-normalised plain text."""
    path = BIB_PUBLIC / slug / "index.html"
    assert path.is_file(), f"missing built page: {path}"
    html = path.read_text(encoding="utf-8")
    match = re.search(r'<div class="bibliography-meta">(.*?)</div>', html, re.S)
    assert match, f"no bibliography-meta block in {path}"
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", match.group(1))).strip()


@pytest.mark.parametrize(
    ("slug", "expected"),
    [
        # Document with no Zotero Type: publisher only, no genre line.
        ("ztest-document", ("Publisher: Test Documentation Office",)),
        # Transcript: the genre is surfaced as the document type.
        (
            "ztest-transcript",
            (
                "Document Type: Transcript",
                "Publisher: Test Oral History Institute",
            ),
        ),
        # Standard: series, number, version, publisher and place all render.
        (
            "ztest-standard",
            (
                "Series: Test System Integration Standard",
                "Standard Number: TSTD 059003",
                "Version: 2.0",
                "Publisher: Test Standards Institute",
                "Place: Testville, CA, USA",
            ),
        ),
        # Software: Zotero Type becomes the programming language.
        ("ztest-software", ("Programming Language: TestLang",)),
        # Report: regression guard for the snake_case key fix.
        (
            "ztest-report",
            (
                "Report Type: Test Report Type",
                "Report Number: TR-2005-001",
            ),
        ),
    ],
)
def test_metadata_block(slug: str, expected: tuple[str, ...]) -> None:
    text = _meta_text(slug)
    for fragment in expected:
        assert fragment in text, f"{slug}: expected {fragment!r} in {text!r}"


def test_document_without_genre_omits_type_line() -> None:
    """An empty ``genre`` must not render an empty 'Document Type' line."""
    assert "Document Type:" not in _meta_text("ztest-document")
