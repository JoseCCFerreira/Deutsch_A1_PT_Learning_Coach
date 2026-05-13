from __future__ import annotations

import streamlit as st

from src.audio import generate_tts
from src.speaking_feedback import evaluate_speaking
from src.ui import get_conn, setup_page

setup_page("Ouvir e Falar")
get_conn()
st.title("Ouvir e Falar")
sentences = ["Ich komme aus Portugal.", "Ich wohne in Braga.", "Guten Morgen.", "Ich möchte Wasser.", "Wie heißen Sie?"]
sentence = st.selectbox("Frase alemã", sentences)
audio = generate_tts(sentence)
if audio:
    st.audio(str(audio))
else:
    st.warning("Não consegui gerar áudio agora. Podes praticar lendo a frase.")
st.write("Repete em voz alta. Depois escreve o que disseste ou o que ouviste.")
typed = st.text_input("O que disseste/ouviste")
if st.button("Avaliar tentativa"):
    result = evaluate_speaking(sentence, typed)
    st.metric("Pontuação aproximada", f"{result['score']:.0f}/100")
    st.info(result["feedback_pt"])
