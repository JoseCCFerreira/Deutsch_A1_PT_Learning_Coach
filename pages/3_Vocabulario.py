from __future__ import annotations

import streamlit as st

from src.audio import generate_tts
from src.ui import get_conn, setup_page
from src.vocabulary import article_badge, load_vocabulary, mark_word

setup_page("Vocabulário")
conn = get_conn()
st.title("Vocabulario A1")
st.caption("Treina palavras, artigos e exemplos. Para nomes, aprende sempre artigo + palavra.")

topics = ["Todos"] + [r[0] for r in conn.execute("SELECT DISTINCT topic FROM vocabulary ORDER BY topic").fetchall()]
articles = ["Todos", "der", "die", "das", ""]
col1, col2, col3 = st.columns(3)
topic = col1.selectbox("Tema", topics)
article = col2.selectbox("Artigo", articles)
search = col3.text_input("Pesquisar")
vocab = load_vocabulary(conn, topic, article)
if search:
    mask = vocab["german"].str.contains(search, case=False, na=False) | vocab["portuguese"].str.contains(search, case=False, na=False)
    vocab = vocab[mask]

if vocab.empty:
    st.warning("Não há vocabulário para estes filtros.")
    st.stop()

row = vocab.iloc[st.number_input("Cartão", 0, len(vocab) - 1, 0)]
st.markdown(
    f"""
    <div class='coach-card'>
    <h2>{article_badge(row['article'])} {row['german']}</h2>
    <p><strong>Português:</strong> {row['portuguese']}</p>
    <p><strong>Plural:</strong> {row['plural'] or 'n/a'}</p>
    <p><strong>Exemplo:</strong> {row['example_de']}<br>{row['example_pt']}</p>
    <p><strong>Pronúncia:</strong> {row['pronunciation_hint']}</p>
    </div>
    """,
    unsafe_allow_html=True,
)
audio = generate_tts(row["german"])
if audio:
    st.audio(str(audio))
cols = st.columns(3)
if cols[0].button("Adicionar à revisão"):
    conn.execute(
        "INSERT OR IGNORE INTO review_queue(user_id,item_type,item_id,ease_factor,interval_days,repetitions,due_date,last_result) VALUES (1,'vocabulary',?,2.5,0,0,datetime('now'),'new')",
        (int(row["vocab_id"]),),
    )
    conn.commit()
    st.success("Adicionado à revisão.")
if cols[1].button("Já sei"):
    mark_word(conn, 1, int(row["vocab_id"]), "known")
    st.success("Marcado como conhecido.")
if cols[2].button("Difícil"):
    mark_word(conn, 1, int(row["vocab_id"]), "difficult")
    st.warning("Marcado como difícil.")

st.dataframe(vocab, use_container_width=True, hide_index=True)
