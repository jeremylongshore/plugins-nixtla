"""Pytest tests for the AICurator.

Important: this curator is a stub by design — when the plugin runs inside
Claude Code, Claude itself does the LLM-grade curation in the conversation.
The AICurator class only provides keyword-based relevance scoring,
truncation, and key-point extraction. Tests below verify that real surface.

(The earlier version of this file mocked openai/anthropic SDK module
attributes; the implementation never imported either, so those tests
collected but failed at patch time. Replaced wholesale per bead nixtla-8nk.)
"""

from __future__ import annotations

import pytest
from nixtla_search_to_slack.ai_curator import AICurator, CuratedContent
from nixtla_search_to_slack.content_aggregator import Content


def _make_content(title: str = "TimeGPT v2.1 multivariate", description: str = "") -> Content:
    """Helper for creating Content fixtures."""
    return Content(
        title=title,
        url="https://example.com/article",
        description=description,
        source="web",
        timestamp="2026-05-04T00:00:00Z",
        metadata={},
    )


@pytest.fixture
def curator():
    return AICurator()


# ---------------------------------------------------------------------------
# Initialization
# ---------------------------------------------------------------------------


class TestAICuratorInit:
    def test_init_without_env_config(self):
        c = AICurator()
        assert c.env_config == {}

    def test_init_with_env_config(self):
        cfg = {"FOO": "bar"}
        c = AICurator(env_config=cfg)
        assert c.env_config == cfg


# ---------------------------------------------------------------------------
# curate() — top-level contract
# ---------------------------------------------------------------------------


class TestCurate:
    def test_returns_curated_content_list(self, curator):
        items = [_make_content("TimeGPT release notes", "Nixtla released new model.")]
        result = curator.curate(items)
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], CuratedContent)

    def test_preserves_input_count(self, curator):
        items = [_make_content("a"), _make_content("b"), _make_content("c")]
        assert len(curator.curate(items)) == 3

    def test_empty_input(self, curator):
        assert curator.curate([]) == []


# ---------------------------------------------------------------------------
# _calculate_relevance — keyword-based scoring with asymmetric inputs
# ---------------------------------------------------------------------------


class TestRelevanceScoring:
    def test_no_keywords_returns_base_score(self, curator):
        c = _make_content("Cooking recipes", "How to bake bread.")
        assert curator._calculate_relevance(c) == 30

    def test_nixtla_keyword_boosts_score(self, curator):
        # 'nixtla' is a keyword (+10) AND triggers the +20 boost.
        c = _make_content("Nixtla update", "")
        # base 30 + 10 (1 keyword: nixtla) + 20 (nixtla boost) = 60
        assert curator._calculate_relevance(c) == 60

    def test_timegpt_boost_separate_from_nixtla(self, curator):
        c = _make_content("TimeGPT release", "")
        # base 30 + 10 (timegpt keyword) + 15 (timegpt boost) = 55
        assert curator._calculate_relevance(c) == 55

    def test_score_capped_at_100(self, curator):
        desc = "TimeGPT statsforecast mlforecast neuralforecast nixtla time-series forecasting prediction arima lstm prophet autoets autotheta seasonal"
        c = _make_content("Nixtla TimeGPT", desc)
        assert curator._calculate_relevance(c) == 100

    def test_text_match_is_case_insensitive(self, curator):
        c = _make_content("NIXTLA NEWS", "TIMEGPT v2 RELEASED")
        # base 30 + 10 (nixtla) + 10 (timegpt) + 20 + 15 = 85
        assert curator._calculate_relevance(c) == 85


# ---------------------------------------------------------------------------
# _extract_key_points
# ---------------------------------------------------------------------------


class TestExtractKeyPoints:
    def test_empty_description_returns_placeholder(self, curator):
        assert curator._extract_key_points("") == ["See source for details"]

    def test_none_description_returns_placeholder(self, curator):
        assert curator._extract_key_points(None) == ["See source for details"]

    def test_very_short_sentences_filtered_out(self, curator):
        desc = "Short. Tiny. Hi."
        assert curator._extract_key_points(desc) == ["See source for details"]

    def test_extracts_up_to_three_points(self, curator):
        desc = (
            "TimeGPT introduces multivariate forecasting in v2.1. "
            "It outperforms baselines on the M5 benchmark by 15%. "
            "The Python SDK now supports async/await for batch calls. "
            "A fourth sentence here will be skipped because the cap is three."
        )
        points = curator._extract_key_points(desc)
        assert len(points) == 3
        assert all(len(p) > 20 for p in points)


# ---------------------------------------------------------------------------
# _generate_why_it_matters — score-banded output
# ---------------------------------------------------------------------------


class TestWhyItMatters:
    @pytest.mark.parametrize(
        "score, expected_phrase",
        [
            (95, "Directly relevant to Nixtla"),
            (80, "Directly relevant to Nixtla"),
            (75, "Relevant to time-series forecasting practitioners"),
            (60, "Relevant to time-series forecasting practitioners"),
            (50, "May be of interest to data scientists"),
            (40, "May be of interest to data scientists"),
            (35, "General interest for the forecasting community"),
            (0, "General interest for the forecasting community"),
        ],
    )
    def test_band_boundaries(self, curator, score, expected_phrase):
        c = _make_content()
        assert expected_phrase in curator._generate_why_it_matters(c, score)


# ---------------------------------------------------------------------------
# _process_content — the integrating method
# ---------------------------------------------------------------------------


class TestProcessContent:
    def test_summary_truncates_long_descriptions(self, curator):
        desc = "x" * 500
        c = _make_content(description=desc)
        result = curator._process_content(c)
        # Summary capped at 300 chars per impl.
        assert len(result.summary) == 300

    def test_summary_falls_back_to_title_when_no_description(self, curator):
        c = _make_content(title="Just a title", description="")
        result = curator._process_content(c)
        assert result.summary == "Just a title"

    def test_relevance_score_is_int_in_range(self, curator):
        c = _make_content("Nixtla TimeGPT", "Forecasting with statsforecast")
        result = curator._process_content(c)
        assert isinstance(result.relevance_score, int)
        assert 0 <= result.relevance_score <= 100
