"""Tests for utils.py"""
from __future__ import annotations

import pandas as pd
import pytest

from utils import (
    add_time_features,
    category_breakdown,
    clean_dataframe,
    compute_revenue,
    monthly_revenue,
    revenue_by_region,
    summary_stats,
    top_products,
)


@pytest.fixture()
def raw_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "order_id": ["ORD-001", "ORD-002", "ORD-003", "ORD-004", "ORD-005"],
            "order_date": ["2024-01-15", "2024-02-20", "bad-date", "2024-01-25", "2024-03-10"],
            "customer_id": ["CUST-01", "", None, "CUST-02", "CUST-03"],
            "product": ["Laptop Pro", " Wireless Mouse ", "USB Hub", "Laptop Pro", "Monitor"],
            "category": ["Electronics", "Electronics", "Electronics", "Electronics", "Electronics"],
            "region": [" north", "SOUTH", "East", "north", "West"],
            "quantity": [1, 2, 3, 1, 2],
            "unit_price": [1299.99, 29.99, 49.99, 1299.99, 349.99],
        }
    )


@pytest.fixture()
def clean_df(raw_df: pd.DataFrame) -> pd.DataFrame:
    return clean_dataframe(raw_df)


@pytest.fixture()
def revenue_df(clean_df: pd.DataFrame) -> pd.DataFrame:
    return compute_revenue(clean_df)


class TestCleanDataframe:
    def test_drops_blank_customer(self, raw_df: pd.DataFrame) -> None:
        result = clean_dataframe(raw_df)
        assert "" not in result["customer_id"].values

    def test_drops_none_customer(self, raw_df: pd.DataFrame) -> None:
        result = clean_dataframe(raw_df)
        assert result["customer_id"].isna().sum() == 0

    def test_drops_bad_date(self, raw_df: pd.DataFrame) -> None:
        result = clean_dataframe(raw_df)
        assert result["order_date"].isna().sum() == 0

    def test_title_cases_region(self, raw_df: pd.DataFrame) -> None:
        result = clean_dataframe(raw_df)
        for region in result["region"]:
            assert region == region.title()

    def test_strips_whitespace_from_product(self) -> None:
        df = pd.DataFrame({
            "order_id": ["ORD-X"],
            "order_date": ["2024-01-01"],
            "customer_id": ["CUST-99"],
            "product": [" Wireless Mouse "],
            "category": ["Electronics"],
            "region": ["North"],
            "quantity": [1],
            "unit_price": [29.99],
        })
        result = clean_dataframe(df)
        assert "Wireless Mouse" in result["product"].values

    def test_order_date_is_datetime(self, raw_df: pd.DataFrame) -> None:
        result = clean_dataframe(raw_df)
        assert pd.api.types.is_datetime64_any_dtype(result["order_date"])

    def test_row_count_after_cleaning(self, raw_df: pd.DataFrame) -> None:
        result = clean_dataframe(raw_df)
        assert len(result) == 3

    def test_does_not_mutate_input(self, raw_df: pd.DataFrame) -> None:
        original_len = len(raw_df)
        clean_dataframe(raw_df)
        assert len(raw_df) == original_len


class TestComputeRevenue:
    def test_revenue_column_added(self, clean_df: pd.DataFrame) -> None:
        result = compute_revenue(clean_df)
        assert "revenue" in result.columns

    def test_revenue_values_correct(self) -> None:
        df = pd.DataFrame({"quantity": [2, 3], "unit_price": [10.0, 5.0]})
        result = compute_revenue(df)
        assert list(result["revenue"]) == [20.0, 15.0]

    def test_does_not_mutate_input(self, clean_df: pd.DataFrame) -> None:
        compute_revenue(clean_df)
        assert "revenue" not in clean_df.columns


class TestAddTimeFeatures:
    def test_columns_added(self, revenue_df: pd.DataFrame) -> None:
        result = add_time_features(revenue_df)
        for col in ["year", "month", "quarter", "day_of_week"]:
            assert col in result.columns

    def test_month_range(self, revenue_df: pd.DataFrame) -> None:
        result = add_time_features(revenue_df)
        assert result["month"].between(1, 12).all()

    def test_quarter_range(self, revenue_df: pd.DataFrame) -> None:
        result = add_time_features(revenue_df)
        assert result["quarter"].between(1, 4).all()


class TestSummaryStats:
    def test_returns_all_keys(self, revenue_df: pd.DataFrame) -> None:
        stats = summary_stats(revenue_df)
        expected = {
            "total_revenue", "mean_order_value", "median_order_value",
            "std_order_value", "p25", "p75", "min", "max",
        }
        assert expected == set(stats.keys())

    def test_total_revenue_positive(self, revenue_df: pd.DataFrame) -> None:
        assert summary_stats(revenue_df)["total_revenue"] > 0

    def test_min_lte_median_lte_max(self, revenue_df: pd.DataFrame) -> None:
        stats = summary_stats(revenue_df)
        assert stats["min"] <= stats["median_order_value"] <= stats["max"]

    def test_p25_lte_p75(self, revenue_df: pd.DataFrame) -> None:
        stats = summary_stats(revenue_df)
        assert stats["p25"] <= stats["p75"]

    def test_all_values_are_floats(self, revenue_df: pd.DataFrame) -> None:
        for v in summary_stats(revenue_df).values():
            assert isinstance(v, float)

    def test_known_values(self) -> None:
        df = pd.DataFrame({"revenue": [10.0, 20.0, 30.0]})
        stats = summary_stats(df)
        assert stats["total_revenue"] == pytest.approx(60.0)
        assert stats["mean_order_value"] == pytest.approx(20.0)


class TestTopProducts:
    def test_returns_series(self, revenue_df: pd.DataFrame) -> None:
        assert isinstance(top_products(revenue_df), pd.Series)

    def test_default_top_10(self, revenue_df: pd.DataFrame) -> None:
        assert len(top_products(revenue_df)) <= 10

    def test_custom_n(self, revenue_df: pd.DataFrame) -> None:
        assert len(top_products(revenue_df, n=2)) <= 2

    def test_descending_order(self, revenue_df: pd.DataFrame) -> None:
        result = top_products(revenue_df)
        assert list(result) == sorted(result, reverse=True)


class TestRevenueByRegion:
    def test_returns_series(self, revenue_df: pd.DataFrame) -> None:
        assert isinstance(revenue_by_region(revenue_df), pd.Series)

    def test_descending_order(self, revenue_df: pd.DataFrame) -> None:
        result = revenue_by_region(revenue_df)
        assert list(result) == sorted(result, reverse=True)

    def test_no_null_index(self, revenue_df: pd.DataFrame) -> None:
        assert revenue_by_region(revenue_df).index.isna().sum() == 0


class TestMonthlyRevenue:
    def test_returns_series(self, revenue_df: pd.DataFrame) -> None:
        assert isinstance(monthly_revenue(revenue_df), pd.Series)

    def test_index_is_string(self, revenue_df: pd.DataFrame) -> None:
        assert all(isinstance(i, str) for i in monthly_revenue(revenue_df).index)

    def test_all_positive(self, revenue_df: pd.DataFrame) -> None:
        assert (monthly_revenue(revenue_df) > 0).all()


class TestCategoryBreakdown:
    def test_returns_dataframe(self, revenue_df: pd.DataFrame) -> None:
        assert isinstance(category_breakdown(revenue_df), pd.DataFrame)

    def test_expected_columns(self, revenue_df: pd.DataFrame) -> None:
        result = category_breakdown(revenue_df)
        assert "total_revenue" in result.columns
        assert "order_count" in result.columns
        assert "avg_order_value" in result.columns

    def test_no_negative_revenue(self, revenue_df: pd.DataFrame) -> None:
        assert (category_breakdown(revenue_df)["total_revenue"] >= 0).all()
