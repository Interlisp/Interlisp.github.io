"""
tests/test_site_jsonld.py
=========================
Validates the site-wide JSON-LD structured data added in Phase 1.2 of
``docs/SEO_IMPROVEMENT_PLAN.md``:

    Organization  → home page            (layouts/_partials/schema-organization.html)
    Article       → regular content pages (layouts/_partials/schema-article.html)
    FAQPage       → pages with `schema: faq` front matter
                                          (layouts/_partials/schema-faq.html)
    BreadcrumbList→ every non-home page   (layouts/_partials/schema-breadcrumb.html)

These complement ``test_bibliography_jsonld.py``, which covers the
type-specific schema emitted for bibliography pages.  In particular, this
module asserts that regular pages do **not** collide with the bibliography
schema (no generic ``Article`` on bibliography entries).

Design
------
The session-scoped, autouse ``hugo_build`` fixture (conftest.py) builds the
*testing* environment into ``tests/public_test/``.  That environment mounts the
real ``content/en`` tree alongside the ``tests/fixtures/bibliography`` fixtures,
so a single build exercises both real content pages and bibliography fixtures.
(It is the CI-reliable build: the generated ``content/en/history/bibliography/**``
entries are gitignored and absent in CI, but the ZTEST fixtures are always
present.)

Usage
-----
    pytest tests/test_site_jsonld.py -v
    PYTEST_FORCE_HUGO_BUILD=1 pytest tests/test_site_jsonld.py -v
"""

import html as html_mod
import json
import re
from html.parser import HTMLParser
from pathlib import Path

import pytest
import yaml

from conftest import REPO_ROOT, TEST_PUBLIC

# ---------------------------------------------------------------------------
# HTML extraction helpers
# ---------------------------------------------------------------------------


class _JSONLDExtractor(HTMLParser):
    """Collect the raw text of every ``application/ld+json`` script element."""

    def __init__(self) -> None:
        super().__init__()
        self._in_jsonld = False
        self._buf: list[str] = []
        self.blocks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag == "script" and dict(attrs).get("type") == "application/ld+json":
            self._in_jsonld = True
            self._buf = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._in_jsonld:
            self._in_jsonld = False
            self.blocks.append("".join(self._buf))

    def handle_data(self, data: str) -> None:
        if self._in_jsonld:
            self._buf.append(data)


def _jsonld_blocks(path: Path) -> list[dict]:
    """Return every parseable JSON-LD object in *path*.

    Skips (does not fail) when the built page is absent so collection errors
    clearly point at the missing file.
    """
    if not path.exists():
        pytest.skip(
            f"Built page not found: {path}\n"
            "Run 'hugo --environment testing --destination tests/public_test' "
            "from the repo root, then re-run the tests."
        )
    parser = _JSONLDExtractor()
    parser.feed(path.read_text(encoding="utf-8"))
    out: list[dict] = []
    for raw in parser.blocks:
        try:
            data = json.loads(raw.strip())
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict):
            out.append(data)
    return out


def _find(path: Path, type_filter: str) -> dict:
    """Return the first JSON-LD object with ``@type == type_filter``."""
    for data in _jsonld_blocks(path):
        if data.get("@type") == type_filter:
            return data
    pytest.fail(f"No {type_filter!r} JSON-LD block found in {path}")


def _all_pages() -> list[Path]:
    """Every built ``index.html`` in the testing output (plus 404.html)."""
    pages = sorted(TEST_PUBLIC.rglob("index.html"))
    not_found = TEST_PUBLIC / "404.html"
    if not_found.exists():
        pages.append(not_found)
    return pages


def _site_config() -> dict:
    cfg = REPO_ROOT / "config" / "_default" / "hugo.yaml"
    return yaml.safe_load(cfg.read_text(encoding="utf-8")) or {}


def _base_url() -> str:
    cfg = REPO_ROOT / "config" / "testing" / "hugo.yaml"
    return (yaml.safe_load(cfg.read_text(encoding="utf-8")) or {}).get("baseURL", "")


HOME = TEST_PUBLIC / "index.html"
FAQS = TEST_PUBLIC / "project" / "faqs" / "index.html"
PRIVACY = TEST_PUBLIC / "privacy" / "index.html"
NESTED = (
    TEST_PUBLIC / "software" / "install-and-run" / "linux"
    / "linux-standard-from-github" / "index.html"
)
BIB_ENTRY = TEST_PUBLIC / "history" / "bibliography" / "ztest-journal" / "index.html"


# ===========================================================================
# Organization
# ===========================================================================


class TestOrganization:
    """The home page carries a single Organization block."""

    @pytest.fixture(autouse=True)
    def ld(self):
        self.ld = _find(HOME, "Organization")

    def test_context_and_type(self):
        assert self.ld["@context"] == "https://schema.org"
        assert self.ld["@type"] == "Organization"

    def test_name_matches_site_title(self):
        assert self.ld["name"] == _site_config().get("title")

    def test_url_is_home(self):
        assert self.ld["url"].endswith("/")

    def test_logo_is_absolute_image(self):
        logo = self.ld["logo"]
        assert logo.startswith("http")
        assert logo.lower().endswith(".png")

    def test_same_as_includes_social_profiles(self):
        same_as = set(self.ld.get("sameAs", []))
        for expected in (
            "https://fosstodon.org/@interlisp",
            "https://bsky.app/profile/interlisp.org",
            "https://www.youtube.com/@Interlisp",
            "https://github.com/interlisp",
        ):
            assert expected in same_as, f"sameAs missing {expected!r}"

    def test_same_as_excludes_non_http(self):
        for url in self.ld.get("sameAs", []):
            assert url.startswith("http"), f"non-http profile in sameAs: {url!r}"

    def test_home_has_no_article(self):
        assert not any(
            d.get("@type") == "Article" for d in _jsonld_blocks(HOME)
        ), "Home page must not emit an Article block"


# ===========================================================================
# Article
# ===========================================================================


class TestArticle:
    """Regular content pages emit an Article block."""

    @pytest.fixture(autouse=True)
    def ld(self):
        self.ld = _find(PRIVACY, "Article")

    def test_context_and_type(self):
        assert self.ld["@context"] == "https://schema.org"
        assert self.ld["@type"] == "Article"

    def test_headline_present(self):
        assert self.ld.get("headline", "").strip()

    def test_url_matches_page(self):
        assert self.ld["url"].endswith("/privacy/")

    def test_author_is_organization(self):
        assert self.ld["author"]["@type"] == "Organization"
        assert self.ld["author"]["name"] == "Interlisp.org"

    def test_publisher_is_organization_with_logo(self):
        pub = self.ld["publisher"]
        assert pub["@type"] == "Organization"
        assert pub["logo"]["@type"] == "ImageObject"
        assert pub["logo"]["url"].startswith("http")

    def test_main_entity_points_at_page(self):
        meop = self.ld["mainEntityOfPage"]
        assert meop["@type"] == "WebPage"
        assert meop["@id"] == self.ld["url"]

    def test_dates_are_iso(self):
        for key in ("datePublished", "dateModified"):
            assert key in self.ld, f"Article missing {key}"
            assert re.match(r"\d{4}-\d{2}-\d{2}T", self.ld[key]), self.ld[key]

    def test_image_is_absolute(self):
        assert self.ld["image"].startswith("http")

    def test_section_pages_have_no_article(self):
        """Section/list pages (e.g. /software/) are not articles."""
        section = TEST_PUBLIC / "software" / "index.html"
        assert not any(
            d.get("@type") == "Article" for d in _jsonld_blocks(section)
        ), "Section page must not emit an Article block"


# ===========================================================================
# FAQPage
# ===========================================================================


class TestFaqPage:
    """Pages opted in with `schema: faq` emit a FAQPage block."""

    @pytest.fixture(autouse=True)
    def ld(self):
        self.ld = _find(FAQS, "FAQPage")

    def test_context_and_type(self):
        assert self.ld["@context"] == "https://schema.org"
        assert self.ld["@type"] == "FAQPage"

    def test_has_questions(self):
        assert len(self.ld["mainEntity"]) >= 1

    def test_each_entry_is_question_with_answer(self):
        for q in self.ld["mainEntity"]:
            assert q["@type"] == "Question"
            assert q["name"].strip()
            ans = q["acceptedAnswer"]
            assert ans["@type"] == "Answer"
            assert ans["text"].strip()

    def test_questions_match_h2_headings(self):
        """Each H2 on the page becomes one question, in document order."""
        html = FAQS.read_text(encoding="utf-8")
        headings = [
            re.sub(r"\s+", " ", html_mod.unescape(re.sub(r"<[^>]+>", "", h))).strip()
            for h in re.findall(r"<h2[^>]*>(.*?)</h2>", html, re.S)
        ]
        names = [q["name"] for q in self.ld["mainEntity"]]
        assert names == headings

    def test_no_html_entities_in_text(self):
        """plainify + htmlUnescape must leave no raw entities behind."""
        blob = json.dumps(self.ld)
        assert not re.search(r"&[a-zA-Z]+;", blob), (
            "HTML entity leaked into FAQPage text"
        )


# ===========================================================================
# BreadcrumbList
# ===========================================================================


class TestBreadcrumb:
    """Every non-home page emits a BreadcrumbList rooted at the home page."""

    @pytest.fixture(autouse=True)
    def ld(self):
        self.ld = _find(NESTED, "BreadcrumbList")

    def test_context_and_type(self):
        assert self.ld["@context"] == "https://schema.org"
        assert self.ld["@type"] == "BreadcrumbList"

    def test_positions_are_sequential(self):
        items = self.ld["itemListElement"]
        assert [i["position"] for i in items] == list(range(1, len(items) + 1))

    def test_first_item_is_home(self):
        items = self.ld["itemListElement"]
        assert items[0]["item"] == _base_url()
        assert items[0]["name"]

    def test_last_item_is_current_page(self):
        items = self.ld["itemListElement"]
        assert items[-1]["item"].endswith("/linux-standard-from-github/")

    def test_home_page_has_no_breadcrumb(self):
        assert not any(
            d.get("@type") == "BreadcrumbList" for d in _jsonld_blocks(HOME)
        ), "Home page must not emit a BreadcrumbList"


# ===========================================================================
# Cross-cutting invariants
# ===========================================================================


def test_organization_only_on_home() -> None:
    """Organization appears on the home page and nowhere else."""
    for page in _all_pages():
        has_org = any(d.get("@type") == "Organization" for d in _jsonld_blocks(page))
        if page == HOME:
            assert has_org, "Home page is missing its Organization block"
        else:
            assert not has_org, f"Organization block unexpectedly on {page}"


def test_faqpage_only_where_opted_in() -> None:
    """FAQPage appears only on pages carrying `schema: faq` front matter."""
    content_root = REPO_ROOT / "content" / "en"
    opted_in: set[str] = set()
    for md in content_root.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        front = text.split("---", 2)
        if len(front) >= 3 and re.search(r"^schema:\s*(faq|\['?faq)", front[1], re.M):
            rel = md.relative_to(content_root)
            slug = rel.parent / rel.stem if rel.name == "_index.md" else rel.with_suffix("")
            opted_in.add(str(slug).replace("\\", "/"))

    for page in _all_pages():
        has_faq = any(d.get("@type") == "FAQPage" for d in _jsonld_blocks(page))
        if has_faq:
            rel = str(page.parent.relative_to(TEST_PUBLIC)).replace("\\", "/")
            rel = "" if rel == "." else rel
            assert rel in opted_in, (
                f"FAQPage emitted on {page} but its source has no `schema: faq`"
            )


def test_no_duplicate_structured_data_blocks() -> None:
    """No page emits more than one of the singleton schema types."""
    singletons = ("Organization", "FAQPage", "BreadcrumbList")
    problems: list[str] = []
    for page in _all_pages():
        blocks = _jsonld_blocks(page)
        for stype in singletons:
            count = sum(1 for d in blocks if d.get("@type") == stype)
            if count > 1:
                problems.append(f"{page}: {count}× {stype}")
    assert not problems, "Duplicate JSON-LD blocks:\n" + "\n".join(problems)


def test_bibliography_pages_have_no_generic_article() -> None:
    """Bibliography pages must use their own schema, not the generic Article."""
    blocks = _jsonld_blocks(BIB_ENTRY)
    generic = [d for d in blocks if d.get("@type") == "Article" and "headline" in d]
    assert not generic, (
        "Bibliography entry emitted a generic Article block (headline present) "
        "in addition to its type-specific schema"
    )
    # The bibliography type-specific schema should still be present.
    assert any(
        d.get("@type") == "ScholarlyArticle" for d in blocks
    ), "Bibliography entry is missing its ScholarlyArticle schema"
    # Breadcrumbs apply to bibliography pages too.
    assert any(d.get("@type") == "BreadcrumbList" for d in blocks)
