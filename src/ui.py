from __future__ import annotations

import streamlit as st

from .db import connect, create_schema, ensure_default_user
from .seed_data import seed_database


def setup_page(title: str = "Deutsch A1 PT Learning Coach") -> None:
    st.set_page_config(page_title=title, layout="wide", page_icon="DE")
    st.markdown(
        """
        <style>
        .stApp { background: linear-gradient(135deg,#dbeafe 0%,#f8fafc 42%,#dcfce7 100%); color:#0f172a; }
        section[data-testid="stSidebar"] { background:#0f172a; border-right:1px solid rgba(255,255,255,.16); }
        section[data-testid="stSidebar"] * { color:#f9fafb !important; }
        h1,h2,h3,h4 { color:#0f172a; letter-spacing:0; font-weight:800; }
        p, li, label, span, div { letter-spacing:0; }
        div[data-testid="stMetric"] {
            background:#ffffff;
            border:1px solid #94a3b8;
            border-left:6px solid #1d4ed8;
            border-radius:10px;
            padding:16px;
            box-shadow:0 10px 24px rgba(15,23,42,.12);
        }
        div[data-testid="stMetric"] label,
        div[data-testid="stMetric"] [data-testid="stMetricValue"] { color:#0f172a !important; }
        .coach-card {
            background:#ffffff;
            border:1px solid #94a3b8;
            border-radius:10px;
            padding:16px;
            margin-bottom:12px;
            box-shadow:0 10px 24px rgba(15,23,42,.11);
            color:#0f172a;
        }
        .coach-card p, .coach-card li { color:#334155; }
        .stAlert { border-radius:10px; }
        div[data-testid="stDataFrame"] {
            border:1px solid #94a3b8;
            border-radius:10px;
            overflow:hidden;
        }
        code {
            background:#e2e8f0 !important;
            color:#0f172a !important;
            border:1px solid #94a3b8;
            border-radius:6px;
            padding:2px 6px;
        }
        .ok { color:#16a34a; font-weight:800; }
        .bad { color:#dc2626; font-weight:800; }
        .warn { color:#b45309; font-weight:800; }
        .article { display:inline-block; min-width:46px; text-align:center; color:white; border-radius:6px; padding:4px 8px; font-weight:900; }
        .der { background:#2563eb; } .die { background:#db2777; } .das { background:#16a34a; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def get_conn():
    conn = connect()
    create_schema(conn)
    ensure_default_user(conn)
    seed_database(conn)
    return conn


def card(title: str, body: str) -> None:
    st.markdown(f"<div class='coach-card'><strong>{title}</strong><br>{body}</div>", unsafe_allow_html=True)


def render_metric_row(items: list[tuple[str, str, str | None]]) -> None:
    cols = st.columns(len(items))
    for col, (label, value, delta) in zip(cols, items):
        col.metric(label, value, delta)
