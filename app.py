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
        # Pulizia nomi colonne
        f.columns = f.columns.str.strip()
        b.columns = b.columns.str.strip()
        return f, b
    except:
        return None, None

df_food, df_drinks = load_menu_data()

# 3. Header Nativo (Senza HTML per evitare il crash)
st.title("🌕 LUNA PIENA")
st.caption("Sapori autentici sotto il cielo stellato")
st.divider()

if df_food is not None and df_drinks is not None:
    # Sidebar per il Carrello
    if 'cart' not in st.session_state:
        st.session_state.cart = {}
    
    with st.sidebar:
        st.title("🛒 Il tuo Ordine")
        tavolo = st.selectbox("Seleziona Tavolo", [f"Tavolo {i:02d}" for i in range(1, 21)])
        if not st.session_state.cart:
            st.write("Il carrello è vuoto")
        else:
            for item, qty in st.session_state.cart.items():
                st.write(f"**{qty}x** {item}")
            if st.button("🚀 INVIA COMANDA", use_container_width=True):
                st.success(f"Ordine inviato per il {tavolo}!")
                st.session_state.cart = {}
                st.rerun()

    # Visualizzazione Menu con Tab
    tab1, tab2 = st.tabs(["🍽️ CUCINA", "🍷 CANTINA"])
    
    with tab1:
        # Raggruppiamo per categoria
        for cat in df_food['Categoria'].unique():
            st.subheader(cat)
            items = df_food[df_food['Categoria'] == cat]
            for i, row in items.iterrows():
                with st.container(border=True):
                    c1, c2 = st.columns([3, 1])
                    c1.markdown(f"**{row['Nome']}**")
                    c1.caption(row['Descrizione'])
                    # Visualizziamo il prezzo nel bottone stesso per pulizia
                    if c2.button(f"{row['Prezzo']}", key=f"f_{i}", use_container_width=True):
                        st.session_state.cart[row['Nome']] = st.session_state.cart.get(row['Nome'], 0) + 1
                        st.toast(f"Aggiunto: {row['Nome']}")

    with tab2:
        for cat in df_drinks['Categoria'].unique():
            st.subheader(cat)
            items = df_drinks[df_drinks['Categoria'] == cat]
            for i, row in items.iterrows():
                with st.container(border=True):
                    c1, c2 = st.columns([3, 1])
                    c1.markdown(f"**{row['Nome']}**")
                    c1.caption(row['Descrizione'])
                    if c2.button(f"{row['Prezzo']}", key=f"d_{i}", use_container_width=True):
                        st.session_state.cart[row['Nome']] = st.session_state.cart.get(row['Nome'], 0) + 1
                        st.toast(f"Aggiunto: {row['Nome']}")

else:
    st.error("Connessione al database fallita. Controlla il link del foglio Google.")
