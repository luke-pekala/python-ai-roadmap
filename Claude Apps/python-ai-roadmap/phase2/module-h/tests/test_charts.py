"""Tests for charts.py — Module H."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import pytest

from charts import render_bar, render_histogram, render_line, render_scatter


@pytest.fixture()
def sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "category": ["A", "B", "A", "C", "B", "A"],
            "region": ["North", "South", "North", "East", "South", "West"],
            "revenue": [100.0, 200.0, 150.0, 300.0, 250.0, 120.0],
            "quantity": [1, 2, 3, 4, 5, 6],
            "date": pd.date_range("2023-01-01", periods=6, freq="MS"),
        }
    )


# ── render_bar ────────────────────────────────────────────────────────────────

class TestRenderBar:
    def test_returns_figure(self, sample_df: pd.DataFrame) -> None:
        fig = render_bar(sample_df, "category")
        assert isinstance(fig, go.Figure)

    def test_has_data(self, sample_df: pd.DataFrame) -> None:
        fig = render_bar(sample_df, "category")
        assert len(fig.data) > 0

    def test_with_group(self, sample_df: pd.DataFrame) -> None:
        fig = render_bar(sample_df, "category", group_col="region")
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0

    def test_title_contains_col(self, sample_df: pd.DataFrame) -> None:
        fig = render_bar(sample_df, "category")
        assert "category" in fig.layout.title.text.lower()

    def test_numeric_col(self, sample_df: pd.DataFrame) -> None:
        fig = render_bar(sample_df, "revenue")
        assert isinstance(fig, go.Figure)

    def test_does_not_mutate(self, sample_df: pd.DataFrame) -> None:
        original_cols = list(sample_df.columns)
        render_bar(sample_df, "category")
        assert list(sample_df.columns) == original_cols


# ── render_line ───────────────────────────────────────────────────────────────

class TestRenderLine:
    def test_returns_figure(self, sample_df: pd.DataFrame) -> None:
        fig = render_line(sample_df, "date", "revenue")
        assert isinstance(fig, go.Figure)

    def test_has_data(self, sample_df: pd.DataFrame) -> None:
        fig = render_line(sample_df, "date", "revenue")
        assert len(fig.data) > 0

    def test_with_group(self, sample_df: pd.DataFrame) -> None:
        fig = render_line(sample_df, "date", "revenue", group_col="category")
        assert isinstance(fig, go.Figure)

    def test_string_x_axis(self, sample_df: pd.DataFrame) -> None:
        fig = render_line(sample_df, "category", "revenue")
        assert isinstance(fig, go.Figure)

    def test_does_not_mutate(self, sample_df: pd.DataFrame) -> None:
        before = sample_df["revenue"].sum()
        render_line(sample_df, "date", "revenue")
        assert sample_df["revenue"].sum() == before


# ── render_histogram ──────────────────────────────────────────────────────────

class TestRenderHistogram:
    def test_returns_figure(self, sample_df: pd.DataFrame) -> None:
        fig = render_histogram(sample_df, "revenue")
        assert isinstance(fig, go.Figure)

    def test_has_data(self, sample_df: pd.DataFrame) -> None:
        fig = render_histogram(sample_df, "revenue")
        assert len(fig.data) > 0

    def test_title_contains_col(self, sample_df: pd.DataFrame) -> None:
        fig = render_histogram(sample_df, "revenue")
        assert "revenue" in fig.layout.title.text.lower()

    def test_integer_col(self, sample_df: pd.DataFrame) -> None:
        fig = render_histogram(sample_df, "quantity")
        assert isinstance(fig, go.Figure)

    def test_does_not_mutate(self, sample_df: pd.DataFrame) -> None:
        original_len = len(sample_df)
        render_histogram(sample_df, "revenue")
        assert len(sample_df) == original_len


# ── render_scatter ────────────────────────────────────────────────────────────

class TestRenderScatter:
    def test_returns_figure(self, sample_df: pd.DataFrame) -> None:
        fig = render_scatter(sample_df, "revenue", "quantity")
        assert isinstance(fig, go.Figure)

    def test_has_data(self, sample_df: pd.DataFrame) -> None:
        fig = render_scatter(sample_df, "revenue", "quantity")
        assert len(fig.data) > 0

    def test_title_contains_cols(self, sample_df: pd.DataFrame) -> None:
        fig = render_scatter(sample_df, "revenue", "quantity")
        title = fig.layout.title.text.lower()
        assert "revenue" in title or "quantity" in title

    def test_with_color(self, sample_df: pd.DataFrame) -> None:
        fig = render_scatter(sample_df, "revenue", "quantity", color_col="category")
        assert isinstance(fig, go.Figure)

    def test_does_not_mutate(self, sample_df: pd.DataFrame) -> None:
        before = sample_df["revenue"].tolist()
        render_scatter(sample_df, "revenue", "quantity")
        assert sample_df["revenue"].tolist() == before
