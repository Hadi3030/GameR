import streamlit as st

st.set_page_config(page_title="Snake Level Game", layout="centered")

st.title("🐍 Snake Level Game (Pygame)")
st.write("Klik tombol di bawah untuk menjalankan game.")

if st.button("▶️ Run Game"):
    st.info("Game sedang dijalankan... Tutup tab ini untuk menghentikan game.")
    import run_game
    run_game.main()
