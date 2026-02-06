import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configurazione Pagina (Deve essere la primissima riga)
st.set_page_config(page_title="Luna Piena", page_icon="🌕", layout="centered")

# 2. Definizione del CSS (evitiamo indentazioni strane nel markdown)
style = """
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .menu-card {
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #ffd700;
        background-color: #1e1e1e;
        margin-bottom: 12px;
    }
    .price { float: right; color: #ffd700; font-weight: bold; }
    .desc { font-size: 0.85rem; color: #bbbbbb; }
</style>
"""
st.markdown(style, unsafe_content_allowed=True)

# 3. Caricamento Dati (Metodo CSV diretto, più stabile)
SHEET_ID = "1sRbYNs_KA7Tm5IvqitJhYxYPVria8qDPdMliOPnFO_k"
URL_MANGIARE = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Mangiare"
URL_BERE = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Bere"

@st.cache_data(ttl=60)
def get_menu():
    try:
        f = pd.read_csv(URL_MANGIARE)
        b = pd.read_csv(URL_BERE)
        return f, b
    except Exception as e:
        st.error(f"Errore di connessione al foglio Google. Verifica la condivisione.")
        return None, None

df_food, df_drinks = get_menu()

# 4. Interfaccia
st.title("🌕 Luna Piena")

if df_food is not None:
    mode = st.sidebar.selectbox("Menu", ["📱 Ordina", "🤵 Cameriere"])

    if mode == "📱 Ordina":
        tavolo = st.selectbox("Tavolo", [f"Tavolo {i:02d}" for i in range(1, 21)])
        
        t1, t2 = st.tabs(["🍽️ Cucina", "🍹 Bar"])
        
        with t1:
            for _, row in df_food.iterrows():
                st.markdown(f"""<div class="menu-card">
                    <span class="price">{row['Prezzo']}</span>
                    <b>{row['Nome']}</b><br>
                    <span class="desc">{row['Descrizione']}</span>
                </div>""", unsafe_content_allowed=True)
                if st.button(f"Aggiungi {row['Nome']}", key=f"f_{row['Nome']}"):
                    st.toast(f"{row['Nome']} aggiunto!")

        with t2:
            for _, row in df_drinks.iterrows():
                st.markdown(f"""<div class="menu-card">
                    <span class="price">{row['Prezzo']}</span>
                    <b>{row['Nome']}</b><br>
                    <span class="desc">{row['Descrizione']}</span>
                </div>""", unsafe_content_allowed=True)
                if st.button(f"Aggiungi {row['Nome']}", key=f"d_{row['Nome']}"):
                    st.toast(f"{row['Nome']} aggiunto!")
    
    else:
        pwd = st.text_input("Password", type="password")
        if pwd == "luna2026":
            st.success("Area Personale")
