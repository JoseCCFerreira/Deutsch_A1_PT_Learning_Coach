from __future__ import annotations

import streamlit as st

from src.spaced_repetition import due_reviews, update_review
from src.ui import get_conn, setup_page

setup_page("Revisão Espaçada")
conn = get_conn()
st.title("Revisao Espacada")
due = due_reviews(conn)
st.metric("Itens para rever hoje", len(due))
if due.empty:
    st.success("Sem revisões em atraso. Excelente.")
    st.stop()
item = due.iloc[0]
st.subheader(f"{item['article'] or ''} {item['german']}")
with st.expander("Mostrar resposta"):
    st.write(item["portuguese"])
    st.write(item["example_de"])
    st.write(item["example_pt"])
cols = st.columns(4)
for label, col in zip(["Não sabia", "Difícil", "Médio", "Fácil"], cols):
    if col.button(label, use_container_width=True):
        update_review(conn, int(item["review_id"]), label)
        st.rerun()
st.dataframe(due, use_container_width=True, hide_index=True)
