"""Tests for sql_validation — the SQL injection mitigation layer."""

from __future__ import annotations

import pytest
from src.sql_validation import (
    InvalidIdentifierError,
    safe_where_value,
    validate_identifier,
    validate_project_id,
)

# ---------------------------------------------------------------------------
# validate_identifier
# ---------------------------------------------------------------------------


class TestValidateIdentifier:
    @pytest.mark.parametrize(
        "name",
        [
            "a",
            "_underscore_start",
            "table_name",
            "Mixed_Case_Name",
            "col123",
            "a_" + "x" * 100,  # long but valid
        ],
    )
    def test_valid_identifiers_pass_through(self, name):
        assert validate_identifier(name) == name

    @pytest.mark.parametrize(
        "name",
        [
            "",  # empty
            "1starts_with_digit",
            "has-hyphen",
            "has space",
            "has.dot",
            "has;semicolon",
            "has'quote",
            'has"quote',
            "has`backtick",
            "DROP TABLE users; --",  # the canonical injection
            "table; SELECT * FROM secrets",
            "name OR 1=1",
            "x" * 1025,  # too long
        ],
    )
    def test_invalid_identifiers_raise(self, name):
        with pytest.raises(InvalidIdentifierError):
            validate_identifier(name)

    @pytest.mark.parametrize("non_string", [None, 42, 3.14, [], {}, b"bytes"])
    def test_non_string_input_raises(self, non_string):
        with pytest.raises(InvalidIdentifierError):
            validate_identifier(non_string)

    def test_kind_label_appears_in_error(self):
        with pytest.raises(InvalidIdentifierError, match="dataset"):
            validate_identifier("bad-name", kind="dataset")


# ---------------------------------------------------------------------------
# validate_project_id
# ---------------------------------------------------------------------------


class TestValidateProjectId:
    @pytest.mark.parametrize(
        "project_id",
        [
            "my-project",
            "project1",
            "p" + "x" * 28 + "9",  # 30 chars, ends in digit
            "abcdef",  # 6 chars, all lowercase
            "lab-123-prod",
        ],
    )
    def test_valid_project_ids(self, project_id):
        assert validate_project_id(project_id) == project_id

    @pytest.mark.parametrize(
        "project_id",
        [
            "",
            "abc",  # too short (<6)
            "x" * 31,  # too long (>30)
            "1starts-with-digit",
            "ends-with-hyphen-",
            "Has-Uppercase",
            "has_underscore",
            "has space",
            "drop-table; --",
        ],
    )
    def test_invalid_project_ids(self, project_id):
        with pytest.raises(InvalidIdentifierError):
            validate_project_id(project_id)

    def test_non_string_input_raises(self):
        with pytest.raises(InvalidIdentifierError):
            validate_project_id(None)


# ---------------------------------------------------------------------------
# safe_where_value
# ---------------------------------------------------------------------------


class TestSafeWhereValue:
    def test_int_unquoted(self):
        assert safe_where_value(42) == "42"
        assert safe_where_value(0) == "0"
        assert safe_where_value(-5) == "-5"

    def test_float_unquoted(self):
        assert safe_where_value(3.14) == "3.14"

    def test_numeric_string_unquoted(self):
        assert safe_where_value("100") == "100"
        assert safe_where_value("-42") == "-42"
        assert safe_where_value("3.14") == "3.14"

    def test_date_string_quoted(self):
        assert safe_where_value("2024-01-15") == "'2024-01-15'"

    def test_bool_rejected(self):
        # bool is a subclass of int; we explicitly reject it.
        with pytest.raises(InvalidIdentifierError, match="bool"):
            safe_where_value(True)
        with pytest.raises(InvalidIdentifierError, match="bool"):
            safe_where_value(False)

    @pytest.mark.parametrize(
        "value",
        [
            "arbitrary string",
            "2024-1-1",  # wrong date format
            "01-15-2024",  # wrong date format
            "'; DROP TABLE x; --",  # injection attempt
            "1 OR 1=1",
            "abc",
            "",
            None,
            [],
            {},
        ],
    )
    def test_unsafe_values_rejected(self, value):
        with pytest.raises(InvalidIdentifierError):
            safe_where_value(value)

    def test_bare_year_treated_as_numeric(self):
        # "2024" matches the numeric regex — emitted unquoted as an integer
        # literal. This is intentional: callers passing a year-as-string
        # for filtering get safe numeric interpolation.
        assert safe_where_value("2024") == "2024"

    def test_error_message_suggests_parameterized_queries(self):
        with pytest.raises(InvalidIdentifierError, match="parameterized"):
            safe_where_value("arbitrary user input")
