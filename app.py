import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Luna Piena - Menù Digitale", page_icon="🌕", layout="centered")

# --- PARAMETRI GOOGLE SHEETS ---
# Usiamo l'export CSV per massima compatibilità
SHEET_ID = "1sRbYNs_KA7Tm5IvqitJhYxYPVria8qDPdMliOPnFO_k"
URL_MANGIARE = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Mangiare"
URL_BERE = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Bere"

# --- FUNZIONE CARICAMENTO DATI ---
@st.cache_data(ttl=60)
def load_data():
    try:
        df_f = pd.read_csv(URL_MANGIARE)
        df_b = pd.read_csv(URL_BERE)
        # Pulizia nomi colonne da eventuali spazi
        df_f.columns = df_f.columns.str.strip()
        df_b.columns = df_b.columns.str.strip()
        return df_f, df_b
    except Exception as e:
        st.error(f"Errore nel collegamento al foglio Google: {e}")
        return None, None

df_food, df_drinks = load_data()

# --- CUSTOM CSS (TEMA SCURO & ORO) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #1e1e1e;
        border-radius: 5px;
        color: #ffd700;
        padding: 10px;
    }
    .menu-card {
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #ffd700;
        background-color: #1e1e1e;
        margin-bottom: 12px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }
    .price { float: right; color: #ffd700; font-weight: bold; font-size: 1.1rem; }
    .desc { font-size: 0.9rem; color: #bbbbbb; font-style: italic; }
    .stButton>button {
        background-color: #ffd700;
        color: #0e1117;
        font-weight: bold;
        border-radius: 20px;
        width: 100%;
    }
    </style>
    """, unsafe_content_allowed=True)

# --- HEADER & LOGO ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.markdown("<h1 style='text-align: center;'>🌕 LUNA PIENA</h1>", unsafe_content_allowed=True)
st.markdown("<p style='text-align: center; color: #ffd700;'><i>Esperienza Gastronomica Notturna</i></p>", unsafe_content_allowed=True)

# --- LOGICA NAVIGAZIONE ---
mode = st.sidebar.radio("Scegli modalità:", ["📱 Ordina al Tavolo", "🤵 Area Cameriere"])

if df_food is not None and df_drinks is not None:
    
    if mode == "📱 Ordina al Tavolo":
        # Scelta Tavolo
        tavolo = st.selectbox("Indica il tuo tavolo:", [f"Tavolo {i:02d}" for i in range(1, 21)])
        
        # Carrello locale (session state)
        if 'cart' not in st.session_state:
            st.session_state.cart = {}

        tabs = st.tabs(["🍽️ Cucina", "🍹 Bar"])

        with tabs[0]:
            for cat in df_food['Categoria'].unique():
                st.subheader(f"✨ {cat}")
                items = df_food[df_food['Categoria'] == cat]
                for _, row in items.iterrows():
                    with st.container():
                        st.markdown(f"""
                        <div class="menu-card">
                            <span class="price">{row['Prezzo']}</span>
                            <b>{row['Nome']}</b><br>
                            <span class="desc">{row['Descrizione']}</span>
                        </div>
                        """, unsafe_content_allowed=True)
                        if st.button(f"Aggiungi {row['Nome']}", key=f"f_{row['Nome']}"):
                            st.session_state.cart[row['Nome']] = st.session_state.cart.get(row['Nome'], 0) + 1
                            st.toast(f"Aggiunto: {row['Nome']}")

        with tabs[1]:
            for cat in df_drinks['Categoria'].unique():
                st.subheader(f"🥂 {cat}")
                items = df_drinks[df_drinks['Categoria'] == cat]
                for _, row in items.iterrows():
                    with st.container():
                        st.markdown(f"""
                        <div class="menu-card">
                            <span class="price">{row['Prezzo']}</span>
                            <b>{row['Nome']}</b><br>
                            <span class="desc">{row['Descrizione']}</span>
                        </div>
                        """, unsafe_content_allowed=True)
                        if st.button(f"Aggiungi {row['Nome']}", key=f"d_{row['Nome']}"):
                            st.session_state.cart[row['Nome']] = st.session_state.cart.get(row['Nome'], 0) + 1
                            st.toast(f"Aggiunto: {row['Nome']}")

        # --- VISUALIZZAZIONE CARRELLO ---
        if st.session_state.cart:
            st.sidebar.divider()
            st.sidebar.subheader("🛒 Il tuo Ordine")
            total_items = 0
            for item, qty in st.session_state.cart.items():
                st.sidebar.write(f"**{qty}x** {item}")
                total_items += qty
            
            if st.sidebar.button("🗑️ Svuota tutto"):
                st.session_state.cart = {}
                st.rerun()
                
            if st.sidebar.button("🚀 INVIA COMANDA"):
                # Nota: In modalità "Solo Codice", simuliamo l'invio. 
                # Per scrivere su Google Sheets serve l'API Service Account.
                st.sidebar.success(f"Ordine inviato per il {tavolo}!")
                st.session_state.cart = {}
                st.balloons()

    elif mode == "🤵 Area Cameriere":
        st.title("📋 Pannello Gestione")
        pwd = st.text_input("Inserisci Codice Staff:", type="password")
        if pwd == "luna2026":
            st.info("In questa sezione appariranno gli ordini in tempo reale una volta collegata l'API di scrittura.")
            st.write("Dati attuali caricati dal Cloud:")
            st.dataframe(df_food)
        elif pwd != "":
            st.error("Codice errato")

else:
    st.warning("Caricamento dati in corso... Assicurati che il link nel codice sia corretto.")

# --- FOOTER ---
st.divider()
st.markdown("<p style='text-align: center; font-size: 0.8rem;'>Luna Piena © 2026 - Digital Menù Experience</p>", unsafe_content_allowed=True)
