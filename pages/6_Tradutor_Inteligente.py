from __future__ import annotations

import streamlit as st

from src.translator import translate_offline
from src.ui import get_conn, setup_page

setup_page("Tradutor Inteligente")
conn = get_conn()
st.title("Tradutor inteligente A1")
st.caption("Tradução aproximada com explicação. Não é só dicionário: mostra estrutura, palavras e treino.")

direction = st.radio("Direção", ["Alemão -> Português", "Português -> Alemão"], horizontal=True)
text = st.text_area("Texto", value="Ich komme aus Portugal.")
if st.button("Traduzir e explicar", type="primary"):
    result = translate_offline(conn, text, "de" if direction.startswith("Alemão") else "pt", "pt" if direction.startswith("Alemão") else "de")
    st.subheader("Tradução")
    st.success(result["translated_text"])
    if result["approximate"]:
        st.warning("Tradução aproximada usando o dicionário local A1.")
    st.subheader("Palavra por palavra")
    st.table(result["breakdown"])
    st.subheader("Gramática")
    st.info(result["explanation_pt"])
    st.subheader("Prática")
    for item in result["practice"]:
        st.write("- " + item)
