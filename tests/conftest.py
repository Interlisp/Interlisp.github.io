"""
tests/conftest.py
=================
Shared test infrastructure for the Interlisp bibliography test suite.

Contains:
  - Path constants consumed by all test modules
  - FIXTURE_SLUGS: canonical list of every test fixture slug
  - ``hugo_build``: session-scoped fixture — builds the *test* environment
    (``tests/public_test/``) used by test_bibliography_jsonld.py
  - ``production_build``: session-scoped fixture — builds the *production*
    site (``public/``) used by test_hugo_build.py and test_html_validation.py

Non-fixture utilities (JSON-LD extraction, assertion helpers) live in the
test module that uses them.  Only things needed by *multiple* test files, or
the pytest fixture infrastructure itself, belong here.
"""

import os
import subprocess
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT: Path = Path(__file__).parent.parent
PROD_PUBLIC: Path = REPO_ROOT / "public"
TEST_PUBLIC: Path = REPO_ROOT / "tests" / "public_test"
BIB_PUBLIC: Path = TEST_PUBLIC / "history" / "bibliography"
FIXTURES_DIR: Path = REPO_ROOT / "tests" / "fixtures" / "bibliography"
CONTENT_DIR: Path = REPO_ROOT / "content" / "en" / "history" / "bibliography"

# Hugo lowercases filenames when generating URL slugs.
FIXTURE_SLUGS: tuple[str, ...] = (
    "ztest-journal",
    "ztest-magazine",
    "ztest-conference",
    "ztest-book",
    "ztest-chapter",
    "ztest-report",
    "ztest-thesis",
    "ztest-patent",
    "ztest-webpage",
    "ztest-blog",
    "ztest-video",
    "ztest-software",
    "ztest-encyclopedia",
    "ztest-message",
    "ztest-no-urls",
)


# ---------------------------------------------------------------------------
# Shared staleness helper
# ---------------------------------------------------------------------------


def _is_stale(output_dir: Path, *source_dirs: Path) -> bool:
    """Return True when *output_dir* is absent, empty, or older than any file
    in *source_dirs*.  Always returns True when ``PYTEST_FORCE_HUGO_BUILD=1``
    is set.
    """
    if os.environ.get("PYTEST_FORCE_HUGO_BUILD"):
        return True

    html_files = list(output_dir.rglob("index.html"))
    if not html_files:
        return True

    oldest_output = min(f.stat().st_mtime for f in html_files)

    for source in source_dirs:
        for path in source.rglob("*"):
            if path.is_file() and path.stat().st_mtime > oldest_output:
                return True

    return False


def _run_hugo(*extra_args: str) -> subprocess.CompletedProcess:
    """Run Hugo with *extra_args* and return the CompletedProcess.  Raises a
    pytest failure immediately if Hugo exits with a non-zero return code.
    """
    result = subprocess.run(
        ["hugo", *extra_args],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        pytest.fail(
            f"Hugo build failed (exit {result.returncode}):\n"
            f"--- stdout ---\n{result.stdout}\n"
            f"--- stderr ---\n{result.stderr}"
        )
    return result


# ---------------------------------------------------------------------------
# Session-scoped fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session", autouse=True)
def hugo_build() -> None:
    """Build the Hugo *test* site (``tests/public_test/``) when stale.

    Uses ``--environment testing`` so that ``config/testing/hugo.yaml`` mounts
    the fixture content without touching production content.

    Set ``PYTEST_FORCE_HUGO_BUILD=1`` to force a rebuild unconditionally.
    """
    if not _is_stale(
        BIB_PUBLIC,
        REPO_ROOT / "layouts",
        REPO_ROOT / "config" / "testing",
        FIXTURES_DIR,
    ):
        return

    result = _run_hugo("--environment", "testing", "--destination", "tests/public_test")
    if result.stderr:
        print(f"\n[hugo test-build warnings]\n{result.stderr}", flush=True)


@pytest.fixture(scope="session")
def production_build() -> subprocess.CompletedProcess:
    """Build the *production* Hugo site (``public/``) when stale and return
    the ``CompletedProcess`` so callers can inspect stdout/stderr.

    Tests that need the production build should declare this fixture as a
    parameter.  It is *not* autouse — only tests that explicitly request it
    will trigger a production build.
    """
    if not _is_stale(
        PROD_PUBLIC,
        REPO_ROOT / "layouts",
        REPO_ROOT / "content",
        REPO_ROOT / "data",
        REPO_ROOT / "config" / "_default",
    ):
        # Site is up-to-date; run a no-op build to capture stderr for tests.
        return subprocess.run(
            ["hugo", "--logLevel", "warn"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
        )

    return _run_hugo("--cleanDestinationDir", "--logLevel", "warn")
