import streamlit as st
import pandas as pd

# 1. Inizializzazione Pagina
st.set_page_config(page_title="Luna Piena", layout="centered")

# 2. CSS Semplificato (evitiamo st.markdown multiriga complesso)
st.write("<style>.stApp{background-color:#0e1117;color:white;}.menu-card{padding:10px;border-radius:10px;border-left:5px solid #ffd700;background-color:#1e1e1e;margin-bottom:10px;}.price{float:right;color:#ffd700;font-weight:bold;}</style>", unsafe_content_allowed=True)

# 3. Parametri Google Sheets
SHEET_ID = "1sRbYNs_KA7Tm5IvqitJhYxYPVria8qDPdMliOPnFO_k"
URL_MANGIARE = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Mangiare"
URL_BERE = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Bere"

@st.cache_data(ttl=30)
def load_menu_data():
    try:
        f = pd.read_csv(URL_MANGIARE)
        b = pd.read_csv(URL_BERE)
        return f, b
    except:
        return None, None

df_food, df_drinks = load_menu_data()

# 4. Header
st.title("🌕 Luna Piena")

if df_food is not None:
    tab1, tab2 = st.tabs(["🍽️ Cucina", "🍹 Bar"])
    
    with tab1:
        for i, row in df_food.iterrows():
            # Usiamo stringhe singole per evitare errori di parsing 3.13
            card_html = f"<div class='menu-card'><span class='price'>{row['Prezzo']}</span><b>{row['Nome']}</b><br><small>{row['Descrizione']}</small></div>"
            st.markdown(card_html, unsafe_content_allowed=True)
            if st.button(f"Ordina {row['Nome']}", key=f"f_{i}"):
                st.toast(f"Aggiunto {row['Nome']}")

    with tab2:
        for i, row in df_drinks.iterrows():
            card_html = f"<div class='menu-card'><span class='price'>{row['Prezzo']}</span><b>{row['Nome']}</b><br><small>{row['Descrizione']}</small></div>"
            st.markdown(card_html, unsafe_content_allowed=True)
            if st.button(f"Ordina {row['Nome']}", key=f"d_{i}"):
                st.toast(f"Aggiunto {row['Nome']}")
else:
    st.error("Dati non disponibili. Controlla il link del foglio Google.")
