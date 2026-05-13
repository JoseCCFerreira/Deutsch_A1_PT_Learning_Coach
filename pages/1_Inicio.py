from __future__ import annotations

import streamlit as st

from src.adaptive_engine import recommend_next
from src.learning_path import recommended_lesson
from src.progress_analytics import progress_summary
from src.ui import card, get_conn, render_metric_row, setup_page


setup_page("Início")
conn = get_conn()
user_id = 1

st.title("Deutsch A1 PT Learning Coach")
st.caption("O teu treinador pessoal para aprender alemão A1 a partir do zero, explicado em português.")

summary = progress_summary(conn, user_id)
recommendation = recommend_next(conn, user_id)
lesson = recommended_lesson(conn)

render_metric_row(
    [
        ("Progresso A1", f"{summary['overall_progress']}%", None),
        ("Vocabulário aprendido", f"{summary['vocabulary_learned']}/{summary['vocabulary_total']}", None),
        ("Revisões hoje", str(summary["due_reviews"]), None),
        ("Precisão", f"{summary['accuracy']:.0%}", None),
        ("Sequência", f"{summary['streak']} dias", None),
    ]
)

left, right = st.columns([1.1, 0.9])
with left:
    card(
        "Plano de hoje",
        f"Começa por <strong>{lesson['title_pt']}</strong>. Depois pratica <strong>{recommendation['exercise_type']}</strong>. "
        f"Motivo: {recommendation['reason']}",
    )
    card(
        "Pontos fracos detectados",
        f"Gramática: <span class='warn'>{summary['weakest_grammar']}</span><br>"
        f"Vocabulário: <span class='warn'>{summary['weakest_vocabulary']}</span>",
    )
    if st.button("Começar treino de hoje", type="primary", use_container_width=True):
        st.switch_page("pages/5_Exercicios.py")
    if st.button("Fazer diagnóstico rápido", use_container_width=True):
        st.switch_page("pages/10_Diagnostico.py")

with right:
    st.subheader("Como usar")
    st.markdown(
        """
        1. Vai a **Aprender A1** para seguir o caminho guiado.
        2. Usa **Vocabulario** para flashcards com artigos.
        3. Faz **Exercicios** para o motor aprender os teus erros.
        4. Revê em **Revisao Espacada**.
        5. Consulta **Diagnostico** para saber o que estudar a seguir.
        """
    )
