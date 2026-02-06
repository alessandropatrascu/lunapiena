import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. Configurazione Pagina (DEVE essere la prima istruzione Streamlit)
st.set_page_config(page_title="Luna Piena Live", layout="centered")

# 2. CSS in una variabile per pulizia
custom_css = """
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .menu-card {
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #ffd700;
        background-color: #1e1e1e;
        margin-bottom: 12px;
    }
    .price { float: right; color: #ffd700; font-weight: bold; }
    </style>
"""
st.markdown(custom_css, unsafe_content_allowed=True)

# 3. Connessione a Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Carichiamo i dati dai fogli (assicurati che i nomi siano corretti nel Google Sheet)
    df_food = conn.read(worksheet="Mangiare")
    df_drinks = conn.read(worksheet="Bere")
except Exception as e:
    st.error("⚠️ Errore di connessione al database. Controlla i Secrets su Streamlit Cloud.")
    st.stop()

# --- INTERFACCIA ---
st.title("🌕 Luna Piena")

mode = st.sidebar.radio("Navigazione", ["📱 Ordina", "🤵 Area Cameriere"])

if mode == "📱 Ordina":
    tavolo = st.selectbox("Seleziona Tavolo:", [f"{i:02d}" for i in range(1, 21)])
    
    tab1, tab2 = st.tabs(["🍽️ Mangiare", "🍹 Bere"])
    
    with tab1:
        for _, row in df_food.iterrows():
            with st.container():
                st.markdown(f"""<div class="menu-card">
                    <span class="price">{row['Prezzo']}</span>
                    <b>{row['Nome']}</b><br><small>{row['Descrizione']}</small>
                </div>""", unsafe_content_allowed=True)
                if st.button(f"Aggiungi {row['Nome']}", key=f"btn_{row['Nome']}"):
                    st.toast(f"{row['Nome']} aggiunto!")
                    # Qui aggiungeremo la logica per salvare l'ordine

elif mode == "🤵 Area Cameriere":
    pwd = st.text_input("Password di servizio:", type="password")
    if pwd == "luna2026":
        st.success("Accesso autorizzato. Visualizzazione ordini...")
        # Qui leggeremo il foglio "Ordini"
