"""
utils.py -- Reusable data cleaning and analysis helpers for the sales EDA.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy of the raw sales DataFrame."""
    df = df.copy()
    df = df[df["customer_id"].notna() & (df["customer_id"].str.strip() != "")]
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df = df.dropna(subset=["order_date"])
    df["region"] = df["region"].str.strip().str.title()
    df["product"] = df["product"].str.strip()
    df["category"] = df["category"].str.strip()
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df = df.dropna(subset=["quantity", "unit_price"])
    return df.reset_index(drop=True)


def compute_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Add a revenue column (quantity x unit_price) and return the DataFrame."""
    df = df.copy()
    df["revenue"] = df["quantity"] * df["unit_price"]
    return df


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add year, month, quarter, and day_of_week from order_date."""
    df = df.copy()
    df["year"] = df["order_date"].dt.year
    df["month"] = df["order_date"].dt.month
    df["quarter"] = df["order_date"].dt.quarter
    df["day_of_week"] = df["order_date"].dt.day_name()
    return df


def top_products(df: pd.DataFrame, n: int = 10) -> pd.Series:
    """Return the top-n products by total revenue (descending)."""
    return (
        df.groupby("product")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
    )


def revenue_by_region(df: pd.DataFrame) -> pd.Series:
    """Return total revenue per region (descending)."""
    return df.groupby("region")["revenue"].sum().sort_values(ascending=False)


def monthly_revenue(df: pd.DataFrame) -> pd.Series:
    """Return total revenue per calendar month (YYYY-MM label, sorted)."""
    monthly = (
        df.groupby(df["order_date"].dt.to_period("M"))["revenue"]
        .sum()
        .sort_index()
    )
    monthly.index = monthly.index.astype(str)
    return monthly


def summary_stats(df: pd.DataFrame) -> dict[str, float]:
    """Return a dict of key revenue statistics using NumPy directly."""
    revenues: np.ndarray = df["revenue"].to_numpy()
    return {
        "total_revenue": float(np.sum(revenues)),
        "mean_order_value": float(np.mean(revenues)),
        "median_order_value": float(np.median(revenues)),
        "std_order_value": float(np.std(revenues)),
        "p25": float(np.percentile(revenues, 25)),
        "p75": float(np.percentile(revenues, 75)),
        "min": float(np.min(revenues)),
        "max": float(np.max(revenues)),
    }


def category_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Return per-category aggregation: total revenue, order count, avg order value."""
    return (
        df.groupby("category")
        .agg(
            total_revenue=("revenue", "sum"),
            order_count=("revenue", "count"),
            avg_order_value=("revenue", "mean"),
        )
        .sort_values("total_revenue", ascending=False)
        .round(2)
    )
