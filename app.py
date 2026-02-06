import streamlit as st
import pandas as pd

# 1. Configurazione Pagina
st.set_page_config(page_title="Luna Piena", page_icon="🌕", layout="centered")

# 2. Parametri Google Sheets (Metodo CSV stabile)
SHEET_ID = "1sRbYNs_KA7Tm5IvqitJhYxYPVria8qDPdMliOPnFO_k"
URL_MANGIARE = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Mangiare"
URL_BERE = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Bere"

@st.cache_data(ttl=30)
def load_menu_data():
    try:
        # Carichiamo i dati ignorando errori di parsing
        f = pd.read_csv(URL_MANGIARE)
        b = pd.read_csv(URL_BERE)
        return f, b
    except:
        return None, None

df_food, df_drinks = load_menu_data()

# 3. Interfaccia Utente (Nativa Streamlit)
st.title("🌕 Luna Piena")
st.caption("Esperienza gastronomica sotto la luce della luna")

if df_food is not None:
    # Navigazione semplice
    scelta = st.radio("Cosa desideri consultare?", ["🍽️ Cucina", "🍹 Bar"], horizontal=True)
    
    # Mostriamo il menù usando st.container(border=True) che crea l'effetto "card"
    if scelta == "🍽️ Cucina":
        for i, row in df_food.iterrows():
            with st.container(border=True):
                c1, c2 = st.columns([3, 1])
                c1.subheader(row['Nome'])
                c1.write(f"_{row['Descrizione']}_")
                c2.button(f"**{row['Prezzo']}**", key=f"f_{i}", help="Clicca per aggiungere")
                
    else:
        for i, row in df_drinks.iterrows():
            with st.container(border=True):
                c1, c2 = st.columns([3, 1])
                c1.subheader(row['Nome'])
                c1.write(f"_{row['Descrizione']}_")
                c2.button(f"**{row['Prezzo']}**", key=f"d_{i}", help="Clicca per aggiungere")

else:
    st.error("Il menù è temporaneamente non disponibile. Riprova tra pochi istanti.")

# 4. Footer
st.divider()
st.info("📍 Via delle Stelle, 12 | 🤵 Area Cameriere accessibile dalla Sidebar")
