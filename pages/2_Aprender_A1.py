from __future__ import annotations

import streamlit as st

from src.learning_path import load_lessons
from src.ui import card, get_conn, setup_page

setup_page("Aprender A1")
conn = get_conn()
st.title("Aprender A1 passo a passo")
st.caption("Explicações em português, exemplos alemães simples e foco no nível A1.")

lessons = load_lessons(conn)
for module, group in lessons.groupby("module"):
    with st.expander(module, expanded=module == "Módulo 1"):
        for lesson in group.itertuples(index=False):
            card(
                lesson.title_pt,
                f"<strong>Alemão:</strong> {lesson.title_de}<br>"
                f"<strong>Explicação:</strong> {lesson.description_pt}<br>"
                f"<strong>Gramática:</strong> {lesson.grammar_focus}<br>"
                f"<strong>Vocabulário:</strong> {lesson.vocabulary_topic}<br>"
                f"<strong>Foco:</strong> {lesson.skill_focus}",
            )
            cols = st.columns(3)
            cols[0].button("Mini quiz", key=f"quiz_{lesson.lesson_id}")
            cols[1].button("Praticar", key=f"practice_{lesson.lesson_id}")
            cols[2].button("Marcar completo", key=f"done_{lesson.lesson_id}")

st.info("Dica: não avances demasiado depressa. Se a precisão estiver abaixo de 80%, volta aos exercícios do tópico.")
