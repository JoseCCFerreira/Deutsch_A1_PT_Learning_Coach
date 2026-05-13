from __future__ import annotations

import streamlit as st

from src.plotting import mastery_heatmap, progress_line
from src.progress_analytics import mastery_table, progress_over_time, progress_summary
from src.ui import get_conn, render_metric_row, setup_page

setup_page("Progresso")
conn = get_conn()
st.title("Progresso A1")
summary = progress_summary(conn)
render_metric_row(
    [
        ("Progresso A1", f"{summary['overall_progress']}%", None),
        ("Vocabulário", f"{summary['vocabulary_learned']}/{summary['vocabulary_total']}", None),
        ("Exercícios", str(summary["attempts"]), None),
        ("Precisão", f"{summary['accuracy']:.0%}", None),
    ]
)
st.progress(summary["overall_progress"], text="Progresso geral estimado")
st.plotly_chart(mastery_heatmap(mastery_table(conn)), use_container_width=True)
st.plotly_chart(progress_line(progress_over_time(conn)), use_container_width=True)

st.subheader("Checklist A1")
items = [
    "Consigo apresentar-me",
    "Consigo dizer de onde sou",
    "Consigo fazer perguntas simples",
    "Consigo compreender frases simples",
    "Consigo escrever uma apresentação curta",
    "Consigo entender números e preços",
    "Consigo pedir comida e bebida",
    "Consigo pedir direções",
]
for item in items:
    st.checkbox(item, value=False)
