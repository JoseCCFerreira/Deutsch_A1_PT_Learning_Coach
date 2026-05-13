from __future__ import annotations

import streamlit as st

from src.adaptive_engine import recommend_next
from src.plotting import accuracy_bar, mastery_heatmap, progress_line
from src.progress_analytics import accuracy_by, mastery_table, progress_over_time
from src.ui import card, get_conn, setup_page

setup_page("Diagnóstico")
conn = get_conn()
st.title("Diagnóstico")
rec = recommend_next(conn)
card("Plano recomendado", f"{rec['reason']}<br>Pratica: <strong>{rec['exercise_type']}</strong> · Dificuldade {rec['difficulty']}")

grammar = accuracy_by(conn, "grammar_topic")
vocab = accuracy_by(conn, "vocabulary_topic")
errors = accuracy_by(conn, "error_type")
mastery = mastery_table(conn)
timeline = progress_over_time(conn)

st.plotly_chart(accuracy_bar(grammar, "Precisão por gramática"), use_container_width=True)
st.plotly_chart(accuracy_bar(vocab, "Precisão por vocabulário"), use_container_width=True)
st.plotly_chart(accuracy_bar(errors, "Erros por tipo"), use_container_width=True)
st.plotly_chart(mastery_heatmap(mastery), use_container_width=True)
st.plotly_chart(progress_line(timeline), use_container_width=True)
st.subheader("Tópicos mais fracos")
st.dataframe(mastery.head(10), use_container_width=True, hide_index=True)
