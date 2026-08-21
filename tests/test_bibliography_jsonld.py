"""
tests/test_bibliography_jsonld.py
==================================
Validates the JSON-LD structured data emitted by
``layouts/_partials/bibliography-json-ld.html`` for every Schema.org type
used in the Interlisp bibliography.

Design
------
Each ``ZTEST-*.md`` file in ``tests/fixtures/bibliography/`` is the **mock
input**: controlled Hugo front matter that the template converts to JSON-LD.
The session-scoped ``hugo_build`` fixture (defined in ``conftest.py``) builds
those fixtures into ``tests/public_test/`` via the ``--environment testing``
Hugo configuration, which never touches production content.

Each per-type test class declares an ``ld`` fixture that loads the parsed
JSON-LD dict for that class's fixture slug.  Because ``_load_jsonld`` is
wrapped with ``functools.lru_cache``, each HTML file is read exactly once per
session regardless of how many tests reference it.

Cross-cutting invariants (context, language, date format, key isolation) are
expressed as module-level parametrized functions so that pytest generates one
test ID per slug or (slug, key) combination, making failures immediately
identifiable.

Fixture → Schema.org type map
------------------------------
    ZTEST-JOURNAL.md      article-journal       → ScholarlyArticle
    ZTEST-MAGAZINE.md     article-magazine      → Article
    ZTEST-CONFERENCE.md   paper-conference      → ScholarlyArticle
    ZTEST-BOOK.md         book                  → Book
    ZTEST-CHAPTER.md      chapter               → Chapter
    ZTEST-REPORT.md       report                → Report
    ZTEST-THESIS.md       thesis                → Thesis
    ZTEST-PATENT.md       patent                → CreativeWork (+additionalType)
    ZTEST-WEBPAGE.md      webpage               → WebPage
    ZTEST-BLOG.md         post-weblog           → BlogPosting
    ZTEST-VIDEO.md        motion_picture        → VideoObject
    ZTEST-SOFTWARE.md     software              → SoftwareSourceCode
    ZTEST-ENCYCLOPEDIA.md entry-encyclopedia    → Article
    ZTEST-MESSAGE.md      personal_communication → Message
    ZTEST-NO-URLS.md      report (no URLs)      → edge-case fixture

Usage
-----
    # From the repository root:
    pytest tests/test_bibliography_jsonld.py -v

    # Force a fresh Hugo test build first:
    PYTEST_FORCE_HUGO_BUILD=1 pytest tests/test_bibliography_jsonld.py -v
"""

import functools
import json
from html.parser import HTMLParser
from pathlib import Path

import pytest

from conftest import BIB_PUBLIC, FIXTURE_SLUGS, TEST_PUBLIC

# ---------------------------------------------------------------------------
# HTML extraction
# ---------------------------------------------------------------------------


class _JSONLDExtractor(HTMLParser):
    """Collect the raw text of every ``application/ld+json`` script element."""

    def __init__(self) -> None:
        super().__init__()
        self._in_jsonld: bool = False
        self.blocks: list[str] = []
        self._buf: list[str] = []

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


def _parse_jsonld(path: Path, *, type_filter: str | None = None) -> dict:
    """Return the first Schema.org JSON-LD block from *path*.

    If *type_filter* is given, return the block whose ``@type`` matches it
    (used for the CollectionPage section index).  Otherwise return the first
    block whose ``@context`` is ``https://schema.org``.

    Raises a pytest failure (not an exception) if no matching block is found.
    """
    parser = _JSONLDExtractor()
    parser.feed(path.read_text(encoding="utf-8"))

    for raw in parser.blocks:
        try:
            data = json.loads(raw.strip())
        except json.JSONDecodeError:
            continue
        if not isinstance(data, dict):
            continue
        if type_filter:
            if data.get("@type") == type_filter:
                return data
        elif data.get("@context") == "https://schema.org":
            return data

    pytest.fail(f"No matching JSON-LD block found in {path}")


# ---------------------------------------------------------------------------
# Cached page loaders
# ---------------------------------------------------------------------------


@functools.lru_cache(maxsize=None)
def _load_jsonld(slug: str) -> dict:
    """Return the Schema.org JSON-LD dict for the bibliography page *slug*.

    Results are cached (lru_cache) so each HTML file is read exactly once per
    test session regardless of how many test methods reference the same slug.

    Skips (does not fail) when the built page is absent so that collection
    errors clearly identify the missing file rather than producing confusing
    assertion failures.
    """
    path = BIB_PUBLIC / slug / "index.html"
    if not path.exists():
        pytest.skip(
            f"Built page not found: {path}\n"
            "Run 'hugo --environment testing --destination tests/public_test' "
            "from the repo root, then re-run the tests."
        )
    return _parse_jsonld(path)


@functools.lru_cache(maxsize=1)
def _load_jsonld_section() -> dict:
    """Return the CollectionPage JSON-LD dict from the bibliography index page."""
    path = TEST_PUBLIC / "history" / "bibliography" / "index.html"
    if not path.exists():
        pytest.skip(f"Section index page not found: {path}")
    return _parse_jsonld(path, type_filter="CollectionPage")


# ---------------------------------------------------------------------------
# Shared assertion helpers
# ---------------------------------------------------------------------------


def _assert_base(ld: dict, expected_type: str, expected_name: str) -> None:
    """Assert the fields that must appear on every single bibliography page."""
    assert ld.get("@context") == "https://schema.org", (
        f"@context must be 'https://schema.org', got {ld.get('@context')!r}"
    )
    assert ld.get("@type") == expected_type, (
        f"@type must be {expected_type!r}, got {ld.get('@type')!r}"
    )
    assert ld.get("name") == expected_name, (
        f"name must be {expected_name!r}, got {ld.get('name')!r}"
    )
    assert ld.get("inLanguage") == "en-US", (
        f"inLanguage must be 'en-US', got {ld.get('inLanguage')!r}"
    )
    assert ld.get("url", "").endswith("/"), (
        f"url must end with '/', got {ld.get('url')!r}"
    )


def _assert_person(
    person: dict,
    expected_name: str,
    family: str | None = None,
    given: str | None = None,
) -> None:
    """Assert a Schema.org Person object."""
    assert person.get("@type") == "Person", (
        f"@type must be 'Person', got {person.get('@type')!r}"
    )
    assert person.get("name") == expected_name, (
        f"name must be {expected_name!r}, got {person.get('name')!r}"
    )
    if family is not None:
        assert person.get("familyName") == family, (
            f"familyName must be {family!r}, got {person.get('familyName')!r}"
        )
    if given is not None:
        assert person.get("givenName") == given, (
            f"givenName must be {given!r}, got {person.get('givenName')!r}"
        )


def _assert_org(obj: dict, expected_name: str) -> None:
    """Assert a Schema.org Organization object."""
    assert obj.get("@type") == "Organization", (
        f"@type must be 'Organization', got {obj.get('@type')!r}"
    )
    assert obj.get("name") == expected_name, (
        f"name must be {expected_name!r}, got {obj.get('name')!r}"
    )


# ===========================================================================
# Per-type test classes
#
# Each class declares an ``ld`` fixture (autouse=True) that loads the JSON-LD
# for that class's fixture page into ``self.ld``.  All test methods access the
# data via ``self.ld`` rather than calling ``_load_jsonld`` independently,
# making the data dependency explicit.  ``_load_jsonld`` is cached so the
# fixture is effectively free after the first call.
# ===========================================================================


class TestScholarlyArticle:
    """article-journal → ScholarlyArticle.  Fixture: ZTEST-JOURNAL.md

    Also exercises author name splitting, sameAs ordering, periodical
    isPartOf, and pagination fields.
    """

    @pytest.fixture(autouse=True)
    def ld(self):
        self.ld = _load_jsonld("ztest-journal")

    def test_base_fields(self):
        _assert_base(self.ld, "ScholarlyArticle", "Test Scholarly Article")

    def test_date_published(self):
        assert self.ld["datePublished"] == "2020-03-15"

    def test_date_modified(self):
        assert self.ld["dateModified"] == "2023-01-10T00:00:00Z"

    def test_description_from_abstract(self):
        assert "journal article" in self.ld.get("description", "").lower()

    def test_authors_count_and_order(self):
        authors = self.ld["author"]
        assert len(authors) == 2, f"Expected 2 authors, got {len(authors)}"
        # "Smith, Alice J." → familyName=Smith, givenName=Alice J.
        _assert_person(authors[0], "Alice J. Smith", family="Smith", given="Alice J.")
        # "Jones, Bob" → familyName=Jones, givenName=Bob
        _assert_person(authors[1], "Bob Jones", family="Jones", given="Bob")

    def test_same_as_contains_both_urls(self):
        same_as = self.ld["sameAs"]
        assert "https://example.com/journal-article" in same_as
        assert "https://www.zotero.org/groups/test/items/ZTESTJNL" in same_as

    def test_same_as_url_source_precedes_zotero(self):
        """url_source must appear before zotero_url in the sameAs array."""
        same_as = self.ld["sameAs"]
        assert same_as.index("https://example.com/journal-article") < same_as.index(
            "https://www.zotero.org/groups/test/items/ZTESTJNL"
        )

    def test_periodical_is_part_of(self):
        is_part_of = self.ld["isPartOf"]
        assert is_part_of["@type"] == "Periodical"
        assert is_part_of["name"] == "Journal of Test Science"

    def test_volume_number(self):
        assert self.ld["volumeNumber"] == "5"

    def test_issue_number(self):
        assert self.ld["issueNumber"] == "2"

    def test_pagination(self):
        assert self.ld["pagination"] == "45-67"

class TestMagazineArticle:
    """article-magazine → Article.  Fixture: ZTEST-MAGAZINE.md

    Shares the periodical field block with article-journal but maps to
    Schema.org Article rather than ScholarlyArticle.
    """

    @pytest.fixture(autouse=True)
    def ld(self):
        self.ld = _load_jsonld("ztest-magazine")

    def test_base_fields(self):
        _assert_base(self.ld, "Article", "Test Magazine Article")

    def test_author(self):
        authors = self.ld["author"]
        assert len(authors) == 1
        _assert_person(authors[0], "Jane Doe", family="Doe", given="Jane")

    def test_periodical_is_part_of(self):
        is_part_of = self.ld["isPartOf"]
        assert is_part_of["@type"] == "Periodical"
        assert is_part_of["name"] == "Computing Monthly"

    def test_volume_issue_pagination(self):
        assert self.ld["volumeNumber"] == "10"
        assert self.ld["issueNumber"] == "6"
        assert self.ld["pagination"] == "12-14"


class TestConferencePaper:
    """paper-conference → ScholarlyArticle.  Fixture: ZTEST-CONFERENCE.md

    Exercises proceedings isPartOf (Book), publisher, and locationCreated
    (place field → Schema.org Place).
    """

    @pytest.fixture(autouse=True)
    def ld(self):
        self.ld = _load_jsonld("ztest-conference")

    def test_base_fields(self):
        _assert_base(self.ld, "ScholarlyArticle", "Test Conference Paper")

    def test_proceedings_is_part_of(self):
        is_part_of = self.ld["isPartOf"]
        assert is_part_of["@type"] == "Book"
        assert is_part_of["name"] == "Proceedings of the Test Conference 2019"

    def test_publisher(self):
        _assert_org(self.ld["publisher"], "ACM")

    def test_location_created(self):
        """place front-matter maps to a Schema.org Place via locationCreated."""
        location = self.ld["locationCreated"]
        assert location["@type"] == "Place"
        assert location["name"] == "San Francisco, CA"

    def test_authors_with_compound_given_name(self):
        """'Brown, Carol K.' splits to givenName='Carol K.', familyName='Brown'."""
        authors = self.ld["author"]
        assert len(authors) == 2
        _assert_person(authors[0], "Carol K. Brown", family="Brown", given="Carol K.")
        _assert_person(authors[1], "David White", family="White", given="David")


class TestBook:
    """book → Book.  Fixture: ZTEST-BOOK.md"""

    @pytest.fixture(autouse=True)
    def ld(self):
        self.ld = _load_jsonld("ztest-book")

    def test_base_fields(self):
        _assert_base(self.ld, "Book", "Test Book Title")

    def test_publisher(self):
        _assert_org(self.ld["publisher"], "Test Publisher")

    def test_author(self):
        authors = self.ld["author"]
        assert len(authors) == 1
        _assert_person(authors[0], "Test Author", family="Author", given="Test")

    def test_same_as_order(self):
        """url_source must be the first element; zotero_url the second."""
        same_as = self.ld["sameAs"]
        assert same_as[0] == "https://example.com/book"
        assert same_as[1] == "https://www.zotero.org/groups/test/items/ZTESTBOOK"


class TestChapter:
    """chapter → Chapter.  Fixture: ZTEST-CHAPTER.md

    isPartOf is a Book that also carries a nested publisher Organization.
    """

    @pytest.fixture(autouse=True)
    def ld(self):
        self.ld = _load_jsonld("ztest-chapter")

    def test_base_fields(self):
        _assert_base(self.ld, "Chapter", "Test Chapter Title")

    def test_is_part_of_book(self):
        parent = self.ld["isPartOf"]
        assert parent["@type"] == "Book"
        assert parent["name"] == "Test Book of Chapters"

    def test_parent_book_publisher(self):
        """publisher is nested inside the isPartOf Book, not at the top level."""
        _assert_org(self.ld["isPartOf"]["publisher"], "Chapter Publisher")

    def test_pagination(self):
        assert self.ld["pagination"] == "100-120"

    def test_editor(self):
        editors = self.ld["editor"]
        assert len(editors) == 1
        _assert_person(editors[0], "Test Editor", family="Editor", given="Test")

    def test_author(self):
        authors = self.ld["author"]
        assert len(authors) == 1
        _assert_person(authors[0], "Test Writer", family="Writer", given="Test")


class TestReport:
    """report → Report.  Fixture: ZTEST-REPORT.md"""

    @pytest.fixture(autouse=True)
    def ld(self):
        self.ld = _load_jsonld("ztest-report")

    def test_base_fields(self):
        _assert_base(self.ld, "Report", "Test Technical Report")

    def test_publisher(self):
        _assert_org(self.ld["publisher"], "Test Research Lab")

    def test_author(self):
        authors = self.ld["author"]
        assert len(authors) == 1
        _assert_person(authors[0], "Test Researcher", family="Researcher", given="Test")


class TestThesis:
    """thesis → Thesis.  Fixture: ZTEST-THESIS.md"""

    @pytest.fixture(autouse=True)
    def ld(self):
        self.ld = _load_jsonld("ztest-thesis")

    def test_base_fields(self):
        _assert_base(self.ld, "Thesis", "Test Doctoral Thesis")

    def test_source_organization(self):
        org = self.ld["sourceOrganization"]
        assert org["@type"] == "CollegeOrUniversity"
        assert org["name"] == "Test University"

    def test_author(self):
        authors = self.ld["author"]
        assert len(authors) == 1
        _assert_person(authors[0], "Test Student", family="Student", given="Test")

    def test_no_publisher_key(self):
        """Theses must use sourceOrganization, not publisher."""
        assert "publisher" not in self.ld


class TestPatent:
    """patent → CreativeWork + additionalType "Patent".  Fixture: ZTEST-PATENT.md

    Verifies identifier PropertyValue objects, copyrightHolder (assignee),
    and validIn DefinedRegion (issuing authority).
    """

    @pytest.fixture(autouse=True)
    def ld(self):
        self.ld = _load_jsonld("ztest-patent")

    def test_base_fields(self):
        """Patent @type is CreativeWork; Patent identity comes from additionalType."""
        _assert_base(self.ld, "CreativeWork", "Test Patent for Widget")

    def test_additional_type_is_patent(self):
        assert self.ld["additionalType"] == "Patent"

    def test_patent_number_identifier(self):
        match = next(
            (i for i in self.ld["identifier"] if i.get("propertyID") == "patent-number"),
            None,
        )
        assert match is not None, "No 'patent-number' identifier found"
        assert match["@type"] == "PropertyValue"
        assert match["value"] == "US9876543B2"

    def test_application_number_identifier(self):
        match = next(
            (i for i in self.ld["identifier"] if i.get("propertyID") == "application-number"),
            None,
        )
        assert match is not None, "No 'application-number' identifier found"
        assert match["@type"] == "PropertyValue"
        assert match["value"] == "US12345678"

    def test_assignee_maps_to_copyright_holder(self):
        """Assignee (rights owner) maps to copyrightHolder, not funder."""
        _assert_org(self.ld["copyrightHolder"], "Test Corporation")

    def test_issuing_authority_maps_to_valid_in(self):
        """Issuing authority (jurisdiction) maps to validIn DefinedRegion."""
        region = self.ld["validIn"]
        assert region["@type"] == "DefinedRegion"
        assert region["name"] == "United States"

    def test_author(self):
        authors = self.ld["author"]
        assert len(authors) == 1
        _assert_person(authors[0], "Test Inventor", family="Inventor", given="Test")


class TestWebPage:
    """webpage → WebPage.  Fixture: ZTEST-WEBPAGE.md"""

    @pytest.fixture(autouse=True)
    def ld(self):
        self.ld = _load_jsonld("ztest-webpage")

    def test_base_fields(self):
        _assert_base(self.ld, "WebPage", "Test Web Page")

    def test_is_part_of_website(self):
        parent = self.ld["isPartOf"]
        assert parent["@type"] == "WebSite"
        assert parent["name"] == "Test Website"


class TestBlogPosting:
    """post-weblog → BlogPosting.  Fixture: ZTEST-BLOG.md"""

    @pytest.fixture(autouse=True)
    def ld(self):
        self.ld = _load_jsonld("ztest-blog")

    def test_base_fields(self):
        _assert_base(self.ld, "BlogPosting", "Test Blog Post")

    def test_is_part_of_blog(self):
        parent = self.ld["isPartOf"]
        assert parent["@type"] == "Blog"
        assert parent["name"] == "Test Tech Blog"


class TestVideoObject:
    """motion_picture → VideoObject.  Fixture: ZTEST-VIDEO.md"""

    @pytest.fixture(autouse=True)
    def ld(self):
        self.ld = _load_jsonld("ztest-video")

    def test_base_fields(self):
        _assert_base(self.ld, "VideoObject", "Test Motion Picture")

    def test_production_company(self):
        _assert_org(self.ld["productionCompany"], "Test Film Studio")

    def test_encoding_format(self):
        assert self.ld["encodingFormat"] == "MP4"

    def test_part_of_series(self):
        series = self.ld["partOfSeries"]
        assert series["@type"] == "CreativeWorkSeries"
        assert series["name"] == "Test Film Series"


class TestSoftwareSourceCode:
    """software → SoftwareSourceCode.  Fixture: ZTEST-SOFTWARE.md

    Also exercises the single-name (no comma) author edge case via the
    "Singularity" entry, which must produce only a ``name`` key.
    """

    @pytest.fixture(autouse=True)
    def ld(self):
        self.ld = _load_jsonld("ztest-software")

    def test_base_fields(self):
        _assert_base(self.ld, "SoftwareSourceCode", "Test Software")

    def test_author_count(self):
        assert len(self.ld["author"]) == 2

    def test_author_with_comma_split(self):
        """'Developer, Test' → familyName='Developer', givenName='Test'."""
        _assert_person(self.ld["author"][0], "Test Developer", family="Developer", given="Test")

    def test_author_without_comma_has_only_name(self):
        """'Singularity' (no comma) → only 'name'; no familyName or givenName."""
        single = next((a for a in self.ld["author"] if a["name"] == "Singularity"), None)
        assert single is not None, "'Singularity' author not found in author array"
        assert single["@type"] == "Person"
        assert "familyName" not in single, "Single-name author must not have familyName"
        assert "givenName" not in single, "Single-name author must not have givenName"


class TestEncyclopediaEntry:
    """entry-encyclopedia → Article + isPartOf Book.  Fixture: ZTEST-ENCYCLOPEDIA.md"""

    @pytest.fixture(autouse=True)
    def ld(self):
        self.ld = _load_jsonld("ztest-encyclopedia")

    def test_base_fields(self):
        _assert_base(self.ld, "Article", "Test Encyclopedia Entry")

    def test_is_part_of_book(self):
        """encyclopedia_title maps to isPartOf with @type Book."""
        parent = self.ld["isPartOf"]
        assert parent["@type"] == "Book"
        assert parent["name"] == "Encyclopedia of Test Computing"


class TestPersonalCommunication:
    """personal_communication → Message.  Fixture: ZTEST-MESSAGE.md"""

    @pytest.fixture(autouse=True)
    def ld(self):
        self.ld = _load_jsonld("ztest-message")

    def test_base_fields(self):
        _assert_base(self.ld, "Message", "Test Personal Communication")

    def test_author(self):
        authors = self.ld["author"]
        assert len(authors) == 1
        _assert_person(authors[0], "Test Sender", family="Sender", given="Test")


class TestCollectionPage:
    """The bibliography section index emits CollectionPage + ItemList JSON-LD."""

    @pytest.fixture(autouse=True)
    def ld(self):
        self.ld = _load_jsonld_section()

    def test_base_structure(self):
        assert self.ld["@context"] == "https://schema.org"
        assert self.ld["@type"] == "CollectionPage"
        assert self.ld["inLanguage"] == "en-US"

    def test_main_entity_is_item_list(self):
        assert self.ld["mainEntity"]["@type"] == "ItemList"

    def test_item_list_contains_all_fixtures(self):
        """Every fixture slug must appear in the ItemList URLs."""
        urls = {item["url"] for item in self.ld["mainEntity"]["itemListElement"]}
        for slug in FIXTURE_SLUGS:
            assert any(slug in u for u in urls), (
                f"ItemList missing entry for fixture slug '{slug}'"
            )

    def test_item_list_positions_are_sequential(self):
        positions = [i["position"] for i in self.ld["mainEntity"]["itemListElement"]]
        assert positions == list(range(1, len(positions) + 1))

    def test_number_of_items_matches_list_length(self):
        main = self.ld["mainEntity"]
        assert main["numberOfItems"] == len(main["itemListElement"])


# ===========================================================================
# Cross-cutting parametrized tests
#
# These tests validate invariants that must hold for every fixture or for
# multiple (slug, key) combinations.  Using @pytest.mark.parametrize instead
# of loops means pytest generates one test ID per case, so a failure
# immediately identifies *which* slug or key combination broke — e.g.:
#
#   FAILED test_bibliography_jsonld.py::test_in_language_is_en_us[ztest-blog]
#   FAILED test_bibliography_jsonld.py::test_journal_key_absent[ztest-book-volumeNumber]
# ===========================================================================


@pytest.mark.parametrize("slug,expected_date", [
    ("ztest-journal", "2020-03-15"),
    ("ztest-book",    "1995-01-01"),
    ("ztest-thesis",  "2010-05-01"),
])
def test_date_published_is_iso_format(slug: str, expected_date: str) -> None:
    """datePublished is always YYYY-MM-DD regardless of front-matter input."""
    assert _load_jsonld(slug)["datePublished"] == expected_date


@pytest.mark.parametrize("slug", FIXTURE_SLUGS)
def test_in_language_is_en_us(slug: str) -> None:
    """Every bibliography page must carry inLanguage='en-US'."""
    assert _load_jsonld(slug).get("inLanguage") == "en-US"


@pytest.mark.parametrize("slug", FIXTURE_SLUGS)
def test_context_is_schema_org(slug: str) -> None:
    """Every bibliography page must declare @context='https://schema.org'."""
    assert _load_jsonld(slug).get("@context") == "https://schema.org"


@pytest.mark.parametrize("slug,key", [
    (slug, key)
    for slug in ("ztest-book", "ztest-thesis", "ztest-report")
    for key in ("volumeNumber", "issueNumber", "pagination")
])
def test_journal_key_absent(slug: str, key: str) -> None:
    """Journal pagination fields must not bleed into non-journal item types."""
    assert key not in _load_jsonld(slug), (
        f"{slug} must not have journal-specific key '{key}'"
    )


def test_same_as_absent_when_no_urls() -> None:
    """sameAs is omitted when neither url_source nor zotero_url is set."""
    assert "sameAs" not in _load_jsonld("ztest-no-urls")


def test_date_modified_is_raw_lastmod() -> None:
    """dateModified is stored verbatim as the lastmod front-matter value."""
    assert _load_jsonld("ztest-report")["dateModified"] == "2023-04-01T00:00:00Z"


def test_description_from_abstract() -> None:
    """The abstract front-matter field becomes the JSON-LD description."""
    assert "test abstract for a book" in _load_jsonld("ztest-book")["description"].lower()


def test_conference_location_absent_from_journal() -> None:
    """locationCreated is conference-specific and must not appear on journal pages."""
    assert "locationCreated" not in _load_jsonld("ztest-journal")
