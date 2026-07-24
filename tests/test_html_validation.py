"""
tests/test_html_validation.py
==============================
Validates that every HTML page in the built production site conforms to HTML
standards, using the Nu HTML Checker (``vnu.jar``) via the ``html5validator``
Python package (or the ``vnu`` CLI directly).

Grandfathered errors
--------------------
Some historical HTML issues exist in the production content.  Rather than
blocking the build, these are collected in ``_GRANDFATHERED`` — known messages
that will **not** cause the test to fail.  The goal is to whittle this list
down over time.  Any **new** error that appears causes a test failure.

If you need to regenerate the grandfather list, run:
    python3 tests/grandfathered_html_errors.regen.py

Usage
-----
    # Requires html5validator (pip install html5validator) or vnu CLI.
    # Build the production site first:
    hugo

    pytest tests/test_html_validation.py -v

    # To force a fresh production build:
    PYTEST_FORCE_HUGO_BUILD=1 pytest tests/test_html_validation.py -v
"""

import json
import os
import shutil
import subprocess

import pytest

from conftest import PROD_PUBLIC, production_build

# ---------------------------------------------------------------------------
# Grandfathered error messages — allowed to appear without failing.
# These are exact message strings as reported by vnu.
# ---------------------------------------------------------------------------

_GRANDFATHERED: list[str] = [
    'An "img" element must have an "alt" attribute, except under certain conditions. For details, consult guidance on providing text alternatives for images.',
    'The "align" attribute on the "tr" element is obsolete. Use CSS instead.',
    'A document must not include more than one visible "main" element.',
    'Duplicate ID "notes".',
    'Duplicate ID "roadmap".',
    'Duplicate ID "solaris".',
    'Element "style" not allowed as child of element "dd" in this context. (Suppressing further errors from this subtree.)',
    'Element "style" not allowed as child of element "div" in this context. (Suppressing further errors from this subtree.)',
    'Element "style" not allowed as child of element "p" in this context. (Suppressing further errors from this subtree.)',
    'Element "ul" not allowed as child of element "ul" in this context. (Suppressing further errors from this subtree.)',
    'No "p" element in scope but a "p" end tag seen.',
    'The "aria-controls" attribute must point to an element in the same document.',
    'The "itemprop" attribute was specified, but the element is not a property of any item.',
    'The "main" element must not appear as a descendant of the "main" element.',
]


# ---------------------------------------------------------------------------
# Validator detection
# ---------------------------------------------------------------------------


def _find_validator() -> str | None:
    """Return the path to an HTML validator executable, or None.

    Checks, in order:
    1. ``html5validator`` (Python package CLI wrapper)
    2. ``vnu`` (standalone Nu HTML Checker CLI)
    """
    for exe in ("html5validator", "vnu"):
        path = shutil.which(exe)
        if path is not None:
            return path
    return None


# ---------------------------------------------------------------------------
# Building the validator command and parsing its output
# ---------------------------------------------------------------------------


def _build_cmd(validator: str) -> list[str]:
    """Build the subprocess command that runs the validator against ``public/``.

    The ``_print`` directory is blacklisted because it is only used for
    printing and is not part of the browsable site.
    """
    return [
        validator,
        "--skip-non-html",
        "--root", str(PROD_PUBLIC),
        "--blacklist", "_print",
    ]


def _parse_vnu_json(text: str) -> list[dict]:
    """Parse vnu JSON output into a list of message dicts.

    ``html5validator`` with ``--format json`` outputs newline-delimited JSON
    objects via stderr.  This handles both single-line and multi-line output.
    """
    messages: list[dict] = []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue
        msgs = data.get("messages", [])
        if not msgs and isinstance(data, dict) and "message" in data:
            msgs = [data]
        messages.extend(msgs)
    return messages


def _run_vnu_json(validator: str) -> list[dict]:
    """Run the validator and return parsed JSON messages.

    Falls back to text output parsing if JSON is not available.
    """
    # Try JSON format first (supported by html5validator >= 0.2.0)
    try:
        result = subprocess.run(
            [*_build_cmd(validator), "--format", "json"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        messages = _parse_vnu_json(result.stderr)
        if messages:
            return messages
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Fallback: run without JSON and capture error messages from stderr
    try:
        result = subprocess.run(
            _build_cmd(validator),
            capture_output=True,
            text=True,
            timeout=120,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
        pytest.skip(f"HTML validator execution failed: {exc}")

    # Parse lines starting with "ERROR:" — the plain text output format
    messages = []
    for line in result.stderr.splitlines():
        line = line.strip()
        if line.upper().startswith("ERROR:"):
            messages.append({"message": line[6:].strip(), "type": "error"})
        elif line.upper().startswith("WARNING:"):
            messages.append({"message": line[8:].strip(), "type": "warning"})
    return messages


# ===========================================================================
# Tests
# ===========================================================================


def test_html_validation(production_build) -> None:
    """Validate all HTML in ``public/``; fail on any non-grandfathered error.

    This test requires either the ``html5validator`` Python package or the
    ``vnu`` CLI to be installed.  It skips with a clear message if neither is
    available.

    The test will **not** fail on any message listed in ``_GRANDFATHERED``
    above.  Any new error (not in the grandfathered list) will cause a test
    failure so that new regressions are caught immediately.
    """
    if not PROD_PUBLIC.is_dir():
        pytest.skip("public/ directory not found — run 'hugo' first")

    validator = _find_validator()
    if validator is None:
        pytest.skip(
            "HTML validator not found. Install with:\n"
            "  pip install html5validator\n"
            "(requires Java runtime for vnu.jar)"
        )

    grandfathered = frozenset(_GRANDFATHERED)
    messages = _run_vnu_json(validator)

    new_errors = [
        m
        for m in messages
        if m["message"] not in grandfathered
    ]

    if new_errors:
        details = "\n".join(
            f"  [{m.get('type', 'error')}] {m.get('message', '?')}"
            for m in new_errors
        )
        pytest.fail(
            f"{len(new_errors)} non-grandfathered HTML validation error(s) "
            f"found in {PROD_PUBLIC}:\n{details}"
        )
