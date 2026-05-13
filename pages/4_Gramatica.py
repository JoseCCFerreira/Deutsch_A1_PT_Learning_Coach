from __future__ import annotations

import streamlit as st

from src.grammar import load_grammar_topics
from src.progress_analytics import mastery_table
from src.ui import card, get_conn, setup_page

setup_page("Gramática")
conn = get_conn()
st.title("Gramática A1 explicada em português")
topics = load_grammar_topics(conn)
mastery = mastery_table(conn)

selected = st.selectbox("Tópico", topics["topic_name"].tolist())
topic = topics[topics["topic_name"] == selected].iloc[0]
score = 0
if not mastery.empty:
    rows = mastery[(mastery["topic_type"] == "grammar") & (mastery["topic_name"] == selected)]
    if not rows.empty:
        score = rows.iloc[0]["mastery_score"]
st.progress(int(score), text=f"Domínio estimado: {score:.0f}/100")
card(
    selected,
    f"{topic['explanation_pt']}<br><br><strong>Exemplos:</strong><br>{topic['examples_de']}<br>{topic['examples_pt']}"
    "<br><br><strong>Erro comum:</strong> portugueses tendem a traduzir palavra por palavra; em alemão, artigo, verbo e posição importam.",
)
if st.button("Praticar este tópico", type="primary"):
    st.switch_page("pages/5_Exercicios.py")
