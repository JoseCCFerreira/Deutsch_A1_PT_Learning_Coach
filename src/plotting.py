from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def style(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        template="plotly_white",
        colorway=["#2563eb", "#16a34a", "#f97316", "#dc2626", "#7c3aed"],
        margin=dict(l=20, r=20, t=55, b=30),
        font=dict(color="#0f172a"),
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,.95)",
    )
    return fig


def accuracy_bar(df: pd.DataFrame, title: str) -> go.Figure:
    if df.empty:
        return go.Figure()
    fig = px.bar(df, x="topic", y="accuracy", color="accuracy", color_continuous_scale=["#dc2626", "#f97316", "#16a34a"], title=title)
    fig.update_yaxes(tickformat=".0%")
    return style(fig)


def mastery_heatmap(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return go.Figure()
    pivot = df.pivot_table(index="topic_type", columns="topic_name", values="mastery_score", aggfunc="mean").fillna(0)
    fig = px.imshow(pivot, color_continuous_scale=["#dc2626", "#facc15", "#16a34a"], zmin=0, zmax=100, title="Mapa de domínio")
    return style(fig)


def progress_line(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return go.Figure()
    fig = px.line(df, x="day", y="accuracy", markers=True, title="Precisão ao longo do tempo")
    fig.update_yaxes(tickformat=".0%")
    return style(fig)
