from __future__ import annotations

import streamlit as st

from src.ui import get_conn, setup_page
from src.utils import now_iso
from src.writing_feedback import evaluate_writing

setup_page("Escrita")
conn = get_conn()
st.title("Treino de escrita")
prompts = [
    "Escreve 4 frases em alemão para te apresentares.",
    "Escreve onde vives e de onde vens.",
    "Escreve uma mensagem curta para marcar um café.",
    "Escreve um diálogo simples num restaurante.",
]
prompt = st.selectbox("Tarefa", prompts)
text = st.text_area("Escreve em alemão", height=180, value="Hallo, ich heiße Carlos.\nIch komme aus Portugal.\nIch wohne in Braga.")
if st.button("Corrigir", type="primary"):
    result = evaluate_writing(prompt, text)
    st.metric("Pontuação", f"{result['score']}/100")
    st.success(result["corrected_text_de"])
    st.info(result["feedback_pt"])
    conn.execute(
        """
        INSERT INTO writing_attempts(user_id,prompt_pt,user_text_de,corrected_text_de,feedback_pt,grammar_errors,vocabulary_errors,score,created_at)
        VALUES (1,?,?,?,?,?,?,?,?)
        """,
        (prompt, text, result["corrected_text_de"], result["feedback_pt"], result["grammar_errors"], result["vocabulary_errors"], result["score"], now_iso()),
    )
    conn.commit()
