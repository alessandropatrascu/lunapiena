import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. Configurazione Pagina
st.set_page_config(page_title="Luna Piena - Digital Menu", page_icon="🌕", layout="centered")

# 2. Connessione a Google Sheets
# Nota: Assicurati di aver messo il link nel campo Secrets di Streamlit Cloud
conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=60) # Aggiorna i dati ogni minuto
def load_data():
    food = conn.read(worksheet="Mangiare")
    drinks = conn.read(worksheet="Bere")
    return food, drinks

try:
    df_food, df_drinks = load_data()
except Exception as e:
    st.error("Errore nel caricamento del menu dal Cloud. Verifica i nomi dei fogli.")
    st.stop()

# 3. Custom CSS per il tema scuro "Luna Piena"
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stTabs [data-baseweb="tab"] { color: #ffd700; font-weight: bold; }
    .menu-card {
        padding: 15px; border-radius: 10px; border-left: 5px solid #ffd700;
        background-color: #1e1e1e; margin-bottom: 12px;
    }
    .price { float: right; color: #ffd700; font-weight: bold; font-size: 1.1rem; }
    </style>
    """, unsafe_content_allowed=True)

# 4. Navigazione Sidebar
mode = st.sidebar.radio("Navigazione", ["📱 Ordina al Tavolo", "🤵 Area Cameriere"])

if mode == "📱 Ordina al Tavolo":
    st.title("🌕 Luna Piena")
    tavolo = st.selectbox("Seleziona il numero del tuo tavolo:", [f"{i:02d}" for i in range(1, 21)])
    
    if 'cart' not in st.session_state:
        st.session_state.cart = {}

    tab1, tab2 = st.tabs(["🍽️ MANGIARE", "🍹 BERE"])

    with tab1:
        for cat in df_food['Categoria'].unique():
            st.subheader(cat)
            items = df_food[df_food['Categoria'] == cat]
            for _, row in items.iterrows():
                col_i, col_b = st.columns([4, 1])
                col_i.markdown(f"**{row['Nome']}** ({row['Prezzo']})<br><small>{row['Descrizione']}</small>", unsafe_content_allowed=True)
                if col_b.button("➕", key=f"f_{row['Nome']}"):
                    st.session_state.cart[row['Nome']] = st.session_state.cart.get(row['Nome'], 0) + 1
                    st.toast(f"{row['Nome']} aggiunto!")

    with tab2:
        for cat in df_drinks['Categoria'].unique():
            st.subheader(cat)
            items = df_drinks[df_drinks['Categoria'] == cat]
            for _, row in items.iterrows():
                col_i, col_b = st.columns([4, 1])
                col_i.markdown(f"**{row['Nome']}** ({row['Prezzo']})<br><small>{row['Descrizione']}</small>", unsafe_content_allowed=True)
                if col_b.button("➕", key=f"d_{row['Nome']}"):
                    st.session_state.cart[row['Nome']] = st.session_state.cart.get(row['Nome'], 0) + 1
                    st.toast(f"{row['Nome']} aggiunto!")

    # Gestione Carrello e Invio Ordine
    if st.session_state.cart:
        st.divider()
        st.subheader("🛒 Riepilogo Ordine")
        lista_ordine = []
        for item, qty in st.session_state.cart.items():
            st.write(f"{qty}x {item}")
            lista_ordine.append(f"{qty}x {item}")
        
        if st.button("🚀 INVIA ORDINE AL CAMERIERE"):
            # Creazione riga ordine
            nuovo_ordine = pd.DataFrame([{
                "Tavolo": tavolo,
                "Ordine": ", ".join(lista_ordine),
                "Orario": datetime.now().strftime("%H:%M"),
                "Stato": "In Attesa"
            }])
            # Append sul foglio "Ordini" tramite gsheets connection
            conn.create(worksheet="Ordini", data=nuovo_ordine)
            st.success("Ordine inviato con successo!")
            st.session_state.cart = {}
            st.rerun()

elif mode == "🤵 Area Cameriere":
    st.title("📋 Gestione Ordini")
    password = st.text_input("Inserisci Password Accesso:", type="password")
    
    if password == "luna2026":
        try:
            ordini = conn.read(worksheet="Ordini")
            if ordini.empty:
                st.info("Nessun ordine presente.")
            else:
                for idx, row in ordini.iterrows():
                    if row['Stato'] == "In Attesa":
                        with st.expander(f"🔴 TAVOLO {row['Tavolo']} - {row['Orario']}"):
                            st.write(f"**Dettaglio:** {row['Ordine']}")
                            if st.button(f"Segna come servito", key=f"serve_{idx}"):
                                # Qui andrebbe implementata la logica di update su gsheets
                                st.warning("Funzionalità update Stato richiede configurazione write.")
        except:
            st.info("Inizia a ricevere ordini per visualizzarli qui.")
