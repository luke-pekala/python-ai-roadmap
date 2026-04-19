"""Chart generation functions for Module H.

All functions accept a DataFrame and return a plotly Figure.
Nothing mutates the input DataFrame.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def render_bar(
    df: pd.DataFrame,
    col: str,
    group_col: str | None = None,
) -> go.Figure:
    """Bar chart: value counts of *col*, optionally split by *group_col*."""
    if group_col:
        counts = (
            df.groupby([col, group_col])
            .size()
            .reset_index(name="count")
        )
        fig = px.bar(
            counts,
            x=col,
            y="count",
            color=group_col,
            barmode="group",
            title=f"Count of {col} by {group_col}",
        )
    else:
        counts = df[col].value_counts().head(15).reset_index()
        counts.columns = [col, "count"]
        fig = px.bar(counts, x=col, y="count", title=f"Top values — {col}")

    fig.update_layout(xaxis_tickangle=-35)
    return fig


def render_line(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    group_col: str | None = None,
) -> go.Figure:
    """Line chart of *y_col* over *x_col*, optionally grouped."""
    plot_df = df.copy()

    # Try to parse dates so plotly sorts the axis properly
    try:
        plot_df[x_col] = pd.to_datetime(plot_df[x_col])
        plot_df = plot_df.sort_values(x_col)
    except (ValueError, TypeError):
        pass

    if group_col:
        agg = plot_df.groupby([x_col, group_col])[y_col].mean().reset_index()
        fig = px.line(
            agg,
            x=x_col,
            y=y_col,
            color=group_col,
            markers=True,
            title=f"{y_col} over {x_col} by {group_col}",
        )
    else:
        agg = plot_df.groupby(x_col)[y_col].mean().reset_index()
        fig = px.line(
            agg,
            x=x_col,
            y=y_col,
            markers=True,
            title=f"Average {y_col} over {x_col}",
        )

    return fig


def render_histogram(df: pd.DataFrame, col: str) -> go.Figure:
    """Histogram with KDE overlay for *col*."""
    fig = px.histogram(
        df,
        x=col,
        marginal="box",
        nbins=30,
        title=f"Distribution — {col}",
    )
    fig.update_traces(opacity=0.75)
    return fig


def render_scatter(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    color_col: str | None = None,
) -> go.Figure:
    """Scatter plot of *x_col* vs *y_col*, optionally coloured by *color_col*."""
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        opacity=0.7,
        trendline="ols",
        title=f"{y_col} vs {x_col}",
    )
    return fig
