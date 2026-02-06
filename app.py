import streamlit as st
import pandas as pd

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
        return f, b
    except:
        return None, None

df_food, df_drinks = load_menu_data()

# 3. Logo e Titolo con Stile
st.markdown("<h1 style='text-align: center; color: #FFD700;'>🌕 LUNA PIENA</h1>", unsafe_content_allowed=True)
st.markdown("<p style='text-align: center; font-style: italic; color: #999;'>Sapori autentici sotto il cielo stellato</p>", unsafe_content_allowed=True)
st.divider()

if df_food is not None:
    # Sidebar per il Carrello (rende tutto più ordinato)
    if 'cart' not in st.session_state:
        st.session_state.cart = {}
    
    with st.sidebar:
        st.title("🛒 Il tuo Ordine")
        tavolo = st.selectbox("Tavolo", [f"Tavolo {i:02d}" for i in range(1, 21)])
        if not st.session_state.cart:
            st.write("Il carrello è vuoto")
        else:
            for item, qty in st.session_state.cart.items():
                st.write(f"**{qty}x** {item}")
            if st.button("🚀 INVIA COMANDA"):
                st.success(f"Ordine inviato per il {tavolo}!")
                st.session_state.cart = {}
                st.rerun()

    # Visualizzazione Menu
    tab1, tab2 = st.tabs(["✨ CUCINA", "🍷 CANTINA"])
    
    with tab1:
        for cat in df_food['Categoria'].unique():
            st.markdown(f"### {cat}")
            items = df_food[df_food['Categoria'] == cat]
            for i, row in items.iterrows():
                with st.container(border=True):
                    col_txt, col_price = st.columns([4, 1])
                    col_txt.markdown(f"**{row['Nome']}**")
                    col_txt.caption(row['Descrizione'])
                    col_price.markdown(f"<span style='color: #FFD700; font-weight: bold;'>{row['Prezzo']}</span>", unsafe_content_allowed=True)
                    if st.button(f"Ordina {row['Nome']}", key=f"f_{i}", use_container_width=True):
                        st.session_state.cart[row['Nome']] = st.session_state.cart.get(row['Nome'], 0) + 1
                        st.toast(f"Aggiunto: {row['Nome']}")

    with tab2:
        for cat in df_drinks['Categoria'].unique():
            st.markdown(f"### {cat}")
            items = df_drinks[df_drinks['Categoria'] == cat]
            for i, row in items.iterrows():
                with st.container(border=True):
                    col_txt, col_price = st.columns([4, 1])
                    col_txt.markdown(f"**{row['Nome']}**")
                    col_txt.caption(row['Descrizione'])
                    col_price.markdown(f"<span style='color: #FFD700; font-weight: bold;'>{row['Prezzo']}</span>", unsafe_content_allowed=True)
                    if st.button(f"Ordina {row['Nome']}", key=f"d_{i}", use_container_width=True):
                        st.session_state.cart[row['Nome']] = st.session_state.cart.get(row['Nome'], 0) + 1
                        st.toast(f"Aggiunto: {row['Nome']}")

else:
    st.error("Errore nel caricamento. Verifica il file Google Sheets.")
