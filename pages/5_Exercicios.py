from __future__ import annotations

import streamlit as st

from src.adaptive_engine import recommend_next
from src.exercise_checker import save_attempt
from src.exercise_generator import generate_dynamic_exercise, options_for
from src.ui import card, get_conn, setup_page

setup_page("Exercícios")
conn = get_conn()
st.title("Exercicios dinâmicos")
rec = recommend_next(conn)
card("Recomendação", f"{rec['reason']}<br>Tipo sugerido: <strong>{rec['exercise_type']}</strong>")

if "current_exercise" not in st.session_state:
    st.session_state.current_exercise = generate_dynamic_exercise(conn, rec.get("vocabulary_topic"))
ex = st.session_state.current_exercise
st.subheader(ex["prompt_pt"])
if ex.get("prompt_de"):
    st.code(ex["prompt_de"])
options = options_for(ex)
if ex["exercise_type"] in {"multiple_choice", "article_choice", "verb_conjugation"}:
    answer = st.radio("Escolhe:", options, horizontal=True)
else:
    answer = st.text_input("A tua resposta")

if st.button("Verificar", type="primary"):
    result = save_attempt(conn, 1, ex, answer)
    if result["is_correct"]:
        st.success("Certo. Muito bem.")
    else:
        st.error("Ainda não. Vamos corrigir com calma.")
    st.write("Resposta correta:", ex["correct_answer"])
    st.info(ex["explanation_pt"])
    st.write("Tipo de erro:", result["error_type"] or "sem erro")

if st.button("Próximo exercício"):
    st.session_state.current_exercise = generate_dynamic_exercise(conn, rec.get("vocabulary_topic"))
    st.rerun()
