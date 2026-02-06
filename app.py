import streamlit as st
import pandas as pd

# 1. Configurazione Pagina
st.set_page_config(page_title="Luna Piena", layout="centered")

# 2. Iniezione CSS "Safe" (una riga alla volta per evitare crash metrics_util)
st.write("<style>.stApp{background-color:#0e1117;color:white;}</style>", unsafe_content_allowed=True)
st.write("<style>.menu-card{padding:15px;border-radius:10px;border-left:5px solid #ffd700;background-color:#1e1e1e;margin-bottom:12px;}</style>", unsafe_content_allowed=True)
st.write("<style>.price{float:right;color:#ffd700;font-weight:bold;font-size:1.2rem;}</style>", unsafe_content_allowed=True)

# 3. Parametri Google Sheets
SHEET_ID = "1sRbYNs_KA7Tm5IvqitJhYxYPVria8qDPdMliOPnFO_k"
URL_MANGIARE = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Mangiare"
URL_BERE = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Bere"

@st.cache_data(ttl=30)
def load_data():
    try:
        f = pd.read_csv(URL_MANGIARE)
        b = pd.read_csv(URL_BERE)
        return f, b
    except:
        return None, None

df_food, df_drinks = load_data()

# 4. Header
st.title("🌕 Luna Piena")

if df_food is not None:
    tab1, tab2 = st.tabs(["🍽️ Cucina", "🍹 Bar"])
    
    with tab1:
        for i, row in df_food.iterrows():
            # Creiamo l'HTML in una variabile stringa singola
            html_item = f"<div class='menu-card'><span class='price'>{row['Prezzo']}</span><b>{row['Nome']}</b><br><small style='color:#bbb'>{row['Descrizione']}</small></div>"
            st.write(html_item, unsafe_content_allowed=True)
            if st.button(f"Ordina {row['Nome']}", key=f"f_{i}"):
                st.toast(f"Aggiunto: {row['Nome']}")

    with tab2:
        for i, row in df_drinks.iterrows():
            html_item = f"<div class='menu-card'><span class='price'>{row['Prezzo']}</span><b>{row['Nome']}</b><br><small style='color:#bbb'>{row['Descrizione']}</small></div>"
            st.write(html_item, unsafe_content_allowed=True)
            if st.button(f"Ordina {row['Nome']}", key=f"d_{i}"):
                st.toast(f"Aggiunto: {row['Nome']}")
else:
    st.error("Connessione al menù non riuscita. Verifica il foglio Google.")
