"""Identifier and value validators for safe BigQuery query construction.

BigQuery does not support parameterized identifiers (table names, column
names, dataset names). The only way to safely interpolate them into a
query string is to validate against a strict allow-list first. This
module is the canonical validator for that.

Values inside WHERE clauses *can* be parameterized via
``bigquery.QueryJobConfig(query_parameters=[...])`` and callers should
prefer that path. ``safe_where_value`` is a narrow fallback for callers
that pre-construct simple date or numeric filters.

Reference: https://cloud.google.com/bigquery/docs/schemas#column_names
"""

from __future__ import annotations

import re

# BigQuery identifiers: letters, digits, underscores. Must start with a
# letter or underscore. Length 1–1024 chars.
_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]{0,1023}$")

# Project IDs: 6–30 chars, lowercase letters/digits/hyphens, must start with
# a letter, must not end with a hyphen.
_PROJECT_ID_RE = re.compile(r"^[a-z][a-z0-9-]{4,28}[a-z0-9]$")

# Safe WHERE-clause values: YYYY-MM-DD dates or integer/decimal literals.
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_NUMERIC_RE = re.compile(r"^-?\d+(?:\.\d+)?$")


class InvalidIdentifierError(ValueError):
    """Raised when an identifier or value fails validation."""


def validate_identifier(name: str, kind: str = "identifier") -> str:
    """Return ``name`` if it is a safe BigQuery identifier.

    Raises:
        InvalidIdentifierError: if ``name`` is not a string, or fails the
            BigQuery identifier regex.
    """
    if not isinstance(name, str):
        raise InvalidIdentifierError(f"{kind} must be a string, got {type(name).__name__}")
    if not _IDENTIFIER_RE.match(name):
        raise InvalidIdentifierError(
            f"Invalid {kind} {name!r}: must match BigQuery identifier rules "
            f"(start with letter or underscore, only [A-Za-z0-9_], length 1-1024)"
        )
    return name


def validate_project_id(project_id: str) -> str:
    """Return ``project_id`` if it is a valid GCP project ID.

    Raises:
        InvalidIdentifierError: if ``project_id`` is not a string or
            fails the project-ID regex.
    """
    if not isinstance(project_id, str):
        raise InvalidIdentifierError(
            f"project_id must be a string, got {type(project_id).__name__}"
        )
    if not _PROJECT_ID_RE.match(project_id):
        raise InvalidIdentifierError(
            f"Invalid project_id {project_id!r}: must be 6-30 chars, "
            f"lowercase letters/digits/hyphens, start with a letter, "
            f"not end with a hyphen"
        )
    return project_id


def safe_where_value(value) -> str:
    """Return ``value`` formatted for safe WHERE-clause interpolation.

    Accepts only:
      - int / float / numeric strings → unquoted numeric literal
      - YYYY-MM-DD date strings → single-quoted SQL date literal

    Anything else raises ``InvalidIdentifierError`` — callers with
    arbitrary user-supplied values must use BigQuery parameterized queries
    via ``QueryJobConfig(query_parameters=[ScalarQueryParameter(...)])``.
    """
    if isinstance(value, bool):
        # bool is a subclass of int — reject explicitly to avoid surprises.
        raise InvalidIdentifierError(
            "WHERE value must not be a bool; cast to int explicitly if intended"
        )
    if isinstance(value, (int, float)):
        return str(value)
    if not isinstance(value, str):
        raise InvalidIdentifierError(
            f"WHERE value must be str or numeric, got {type(value).__name__}"
        )
    if _DATE_RE.match(value):
        return f"'{value}'"
    if _NUMERIC_RE.match(value):
        return value
    raise InvalidIdentifierError(
        f"WHERE value {value!r} not in safe form; use parameterized queries "
        f"(QueryJobConfig(query_parameters=...)) for arbitrary user values"
    )
