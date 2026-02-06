import streamlit as st
import pandas as pd
import re

# 1. Configurazione Pagina
st.set_page_config(page_title="Luna Piena - Menu", page_icon="🌕", layout="centered")

# 2. Parametri Google Sheets
SHEET_ID = "1sRbYNs_KA7Tm5IvqitJhYxYPVria8qDPdMliOPnFO_k"
URL_MANGIARE = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Mangiare"
URL_BERE = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Bere"

@st.cache_data(ttl=30)
def load_menu_data():
    try:
        f = pd.read_csv(URL_MANGIARE)
        b = pd.read_csv(URL_BERE)
        return f.fillna(""), b.fillna("")
    except:
        return None, None

def get_price_float(price_str):
    """Estrae il numero da una stringa tipo '15.50€'"""
    try:
        return float(re.sub(r'[^\d.]', '', price_str.replace(',', '.')))
    except:
        return 0.0

df_food, df_drinks = load_menu_data()

# --- HEADER ---
st.title("🌕 LUNA PIENA")
st.write("---")

if df_food is not None:
    # Inizializzazione Carrello
    if 'cart' not in st.session_state:
        st.session_state.cart = [] # Lista di dizionari con {nome, prezzo}

    # --- SIDEBAR: IL CONTO ---
    with st.sidebar:
        st.header("🛒 Il tuo Tavolo")
        tavolo = st.selectbox("Numero:", [f"{i:02d}" for i in range(1, 21)])
        st.write("---")
        
        if not st.session_state.cart:
            st.info("Aggiungi piatti per vedere il totale.")
        else:
            totale = 0.0
            for item in st.session_state.cart:
                st.write(f"1x **{item['nome']}**")
                totale += item['prezzo']
            
            st.write("---")
            st.subheader(f"Totale: {totale:.2f} €")
            
            if st.button("🚀 INVIA ORDINE", use_container_width=True):
                st.success("Comanda inviata in cucina!")
                st.session_state.cart = []
                st.balloons()
            
            if st.button("🗑️ Svuota Carrello", type="secondary"):
                st.session_state.cart = []
                st.rerun()

    # --- MENU PRINCIPALE ---
    tab1, tab2 = st.tabs(["✨ PIATTI SCELTI", "🍷 LA CANTINA"])

    with tab1:
        for cat in df_food['Categoria'].unique():
            st.subheader(f"🔹 {cat.upper()}")
            items = df_food[df_food['Categoria'] == cat]
            for i, row in items.iterrows():
                with st.container(border=True):
                    c1, c2 = st.columns([3, 1])
                    c1.markdown(f"### {row['Nome']}")
                    c1.write(f"{row['Descrizione']}")
                    # Bottone col prezzo
                    if c2.button(f"➕ {row['Prezzo']}", key=f"f_{i}", use_container_width=True):
                        st.session_state.cart.append({
                            "nome": row['Nome'], 
                            "prezzo": get_price_float(row['Prezzo'])
                        })
                        st.toast(f"Aggiunto: {row['Nome']}")

    with tab2:
        for cat in df_drinks['Categoria'].unique():
            st.subheader(f"🔸 {cat.upper()}")
            items = df_drinks[df_drinks['Categoria'] == cat]
            for i, row in items.iterrows():
                with st.container(border=True):
                    c1, c2 = st.columns([3, 1])
                    c1.markdown(f"### {row['Nome']}")
                    c1.write(f"{row['Descrizione']}")
                    if c2.button(f"➕ {row['Prezzo']}", key=f"d_{i}", use_container_width=True):
                        st.session_state.cart.append({
                            "nome": row['Nome'], 
                            "prezzo": get_price_float(row['Prezzo'])
                        })
                        st.toast(f"Aggiunto: {row['Nome']}")
else:
    st.error("Dati non disponibili.")
