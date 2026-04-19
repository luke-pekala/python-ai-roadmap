"""Module H — Interactive Data Explorer (Streamlit app)."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from charts import render_bar, render_histogram, render_line, render_scatter

st.set_page_config(page_title="Data Explorer", layout="wide")

st.title("📊 Data Explorer")
st.caption("Module H — Interactive Visualisation · Python AI Roadmap")

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️  Controls")
    uploaded = st.file_uploader("Upload a CSV", type="csv")
    st.markdown("---")
    st.markdown("**Sample datasets**")
    use_sample = st.button("Load sample sales data")

# ── Data loading ─────────────────────────────────────────────────────────────
@st.cache_data
def load_csv(file) -> pd.DataFrame:  # type: ignore[no-untyped-def]
    return pd.read_csv(file)


@st.cache_data
def load_sample() -> pd.DataFrame:
    import numpy as np

    rng = np.random.default_rng(42)
    n = 500
    months = pd.date_range("2023-01-01", periods=18, freq="MS")
    dates = rng.choice(months, size=n)
    categories = rng.choice(["Electronics", "Clothing", "Food"], size=n)
    regions = rng.choice(["North", "South", "East", "West", "Central"], size=n)
    revenue = (rng.normal(loc=250, scale=80, size=n)).clip(min=20).round(2)
    quantity = rng.integers(1, 20, size=n)
    return pd.DataFrame(
        {
            "date": dates,
            "category": categories,
            "region": regions,
            "revenue": revenue,
            "quantity": quantity,
        }
    )


df: pd.DataFrame | None = None

if uploaded:
    df = load_csv(uploaded)
elif use_sample:
    df = load_sample()

# ── Main content ─────────────────────────────────────────────────────────────
if df is None:
    st.info("👈  Upload a CSV or click **Load sample sales data** to get started.")
    st.stop()

st.subheader("Preview")
st.dataframe(df.head(20), use_container_width=True)
st.caption(f"{len(df):,} rows · {len(df.columns)} columns")

st.markdown("---")

# ── Chart builder ─────────────────────────────────────────────────────────────
st.subheader("Chart builder")

col_left, col_right = st.columns(2)

with col_left:
    chart_type = st.selectbox(
        "Chart type", ["Bar", "Line", "Histogram", "Scatter"]
    )

numeric_cols = df.select_dtypes("number").columns.tolist()
all_cols = df.columns.tolist()

with col_right:
    if chart_type in ("Bar", "Histogram"):
        x_col = st.selectbox("Column", all_cols)
        y_col = None
    elif chart_type == "Line":
        x_col = st.selectbox("X axis (date or numeric)", all_cols)
        y_col = st.selectbox("Y axis (numeric)", numeric_cols)
    else:  # Scatter
        x_col = st.selectbox("X axis", numeric_cols)
        y_col = st.selectbox("Y axis", [c for c in numeric_cols if c != x_col] or numeric_cols)

# Optional groupby for bar / line
group_col: str | None = None
if chart_type in ("Bar", "Line") and len(all_cols) > 1:
    with st.expander("Group / colour by (optional)"):
        options = ["None"] + [c for c in all_cols if c != x_col]
        chosen = st.selectbox("Group by", options)
        group_col = None if chosen == "None" else chosen

# Render
try:
    if chart_type == "Bar":
        fig = render_bar(df, x_col, group_col)
    elif chart_type == "Line":
        fig = render_line(df, x_col, y_col, group_col)  # type: ignore[arg-type]
    elif chart_type == "Histogram":
        fig = render_histogram(df, x_col)
    else:
        fig = render_scatter(df, x_col, y_col)  # type: ignore[arg-type]

    st.plotly_chart(fig, use_container_width=True)
except Exception as exc:  # noqa: BLE001
    st.error(f"Could not render chart: {exc}")

# ── Summary stats ─────────────────────────────────────────────────────────────
if numeric_cols:
    st.markdown("---")
    with st.expander("📋 Summary statistics"):
        st.dataframe(df[numeric_cols].describe().T.round(2), use_container_width=True)
