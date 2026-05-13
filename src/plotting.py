from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def style(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        template="plotly_white",
        colorway=["#1d4ed8", "#047857", "#b45309", "#b91c1c", "#6d28d9"],
        margin=dict(l=20, r=20, t=55, b=30),
        font=dict(color="#0f172a", size=13),
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,.98)",
        title=dict(font=dict(color="#0f172a", size=18)),
    )
    fig.update_xaxes(gridcolor="#e2e8f0", linecolor="#64748b", zerolinecolor="#94a3b8")
    fig.update_yaxes(gridcolor="#e2e8f0", linecolor="#64748b", zerolinecolor="#94a3b8")
    return fig


def empty_figure(title: str, message: str = "Ainda não há dados suficientes.") -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(size=16, color="#475569"),
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(title=title, height=320)
    return style(fig)


def accuracy_bar(df: pd.DataFrame, title: str) -> go.Figure:
    if df.empty:
        return empty_figure(title)
    df = df.copy()
    df["accuracy"] = df["accuracy"].fillna(0)
    fig = px.bar(df, x="topic", y="accuracy", color="accuracy", color_continuous_scale=["#b91c1c", "#f59e0b", "#047857"], title=title)
    fig.update_yaxes(tickformat=".0%")
    return style(fig)


def mastery_heatmap(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return empty_figure("Mapa de domínio")
    pivot = df.pivot_table(index="topic_type", columns="topic_name", values="mastery_score", aggfunc="mean").fillna(0)
    fig = px.imshow(pivot, color_continuous_scale=["#b91c1c", "#facc15", "#047857"], zmin=0, zmax=100, title="Mapa de domínio")
    return style(fig)


def progress_line(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return empty_figure("Precisão ao longo do tempo")
    fig = px.line(df, x="day", y="accuracy", markers=True, title="Precisão ao longo do tempo")
    fig.update_yaxes(tickformat=".0%")
    return style(fig)
