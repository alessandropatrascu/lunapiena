import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configurazione Pagina
st.set_page_config(page_title="Luna Piena - Sistema Ordini", layout="centered")

# --- DATABASE LOCALE ---
ORDERS_FILE = "ordini.csv"
MENU_FILE = "menu.xlsx"

if not os.path.exists(ORDERS_FILE):
    pd.DataFrame(columns=["Tavolo", "Ordine", "Orario", "Stato"]).to_csv(ORDERS_FILE, index=False)

@st.cache_data(ttl=60) # Ricarica il menu ogni minuto se ci sono modifiche al file Excel
def load_menu():
    food = pd.read_excel(MENU_FILE, sheet_name="Mangiare")
    drinks = pd.read_excel(MENU_FILE, sheet_name="Bere")
    return food, drinks

# --- STILE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 8px; }
    .order-box {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #ffd700;
        margin-bottom: 10px;
    }
    .price-tag { color: #ffd700; font-weight: bold; }
    </style>
    """, unsafe_content_allowed=True)

# --- LOGICA NAVIGAZIONE ---
st.sidebar.title("🌑 Luna Piena")
mode = st.sidebar.radio("Vai a:", ["📱 Menu Cliente", "🤵 Area Cameriere"])

df_food, df_drinks = load_menu()

# --- 📱 MENU CLIENTE ---
if mode == "📱 Menu Cliente":
    col1, col2 = st.columns([1, 3])
    with col1:
        try: st.image("logo.png", width=80)
        except: st.write("🌕")
    with col2:
        st.title("Luna Piena")

    tavolo = st.selectbox("Seleziona Tavolo:", [f"{i:02d}" for i in range(1, 15)])
    
    # Inizializza Carrello
    if 'cart' not in st.session_state:
        st.session_state.cart = {}

    tabs = st.tabs(["🍕 Cibo", "🍻 Bevande"])

    def add_to_cart(item):
        if item in st.session_state.cart:
            st.session_state.cart[item] += 1
        else:
            st.session_state.cart[item] = 1

    with tabs[0]: # Sezione Cibo
        for cat in df_food['Categoria'].unique():
            st.subheader(cat)
            items = df_food[df_food['Categoria'] == cat]
            for _, row in items.iterrows():
                c1, c2 = st.columns([3, 1])
                c1.markdown(f"**{row['Nome']}** <span class='price-tag'>{row['Prezzo']}</span><br><small>{row['Descrizione']}</small>", unsafe_content_allowed=True)
                if c2.button("Aggiungi", key=f"f_{row['Nome']}"):
                    add_to_cart(row['Nome'])

    with tabs[1]: # Sezione Bere
        for cat in df_drinks['Categoria'].unique():
            st.subheader(cat)
            items = df_drinks[df_drinks['Categoria'] == cat]
            for _, row in items.iterrows():
                c1, c2 = st.columns([3, 1])
                c1.markdown(f"**{row['Nome']}** <span class='price-tag'>{row['Prezzo']}</span><br><small>{row['Descrizione']}</small>", unsafe_content_allowed=True)
                if c2.button("Aggiungi", key=f"b_{row['Nome']}"):
                    add_to_cart(row['Nome'])

    # --- CARRELLO FLUTTUANTE ---
    if st.session_state.cart:
        st.divider()
        st.subheader("🛒 Il tuo carrello")
        riepilogo_testo = ""
        for item, qty in st.session_state.cart.items():
            st.write(f"**{qty}x** {item}")
            riepilogo_testo += f"{qty}x {item}; "
        
        col_clear, col_send = st.columns(2)
        if col_clear.button("Svuota Carrello"):
            st.session_state.cart = {}
            st.rerun()
            
        if col_send.button("🚀 INVIA ORDINE"):
            nuovo = pd.DataFrame([[tavolo, riepilogo_testo, datetime.now().strftime("%H:%M"), "In Attesa"]], 
                                 columns=["Tavolo", "Ordine", "Orario", "Stato"])
            nuovo.to_csv(ORDERS_FILE, mode='a', header=False, index=False)
            st.session_state.cart = {}
            st.success("Ordine inviato con successo!")
            st.balloons()

# --- 🤵 AREA CAMERIERE ---
else:
    st.title("📋 Ordini in Arrivo")
    pwd = st.text_input("Password di servizio:", type="password")
    
    if pwd == "luna2026":
        ordini = pd.read_csv(ORDERS_FILE)
        attesa = ordini[ordini['Stato'] == "In Attesa"]
        
        if attesa.empty:
            st.info("Nessun ordine da servire al momento.")
        else:
            for idx, row in attesa.iterrows():
                with st.container():
                    st.markdown(f"""
                    <div class="order-box">
                        <span style="font-size:1.5rem;">🪑 <b>TAVOLO {row['Tavolo']}</b></span> 
                        <span style="float:right;">🕒 {row['Orario']}</span><br>
                        <p style="font-size:1.2rem; margin-top:10px;">{row['Ordine']}</p>
                    </div>
                    """, unsafe_content_allowed=True)
                    if st.button(f"Segna Servito - Tavolo {row['Tavolo']}", key=f"done_{idx}"):
                        ordini.at[idx, 'Stato'] = "Completato"
                        ordini.to_csv(ORDERS_FILE, index=False)
                        st.rerun()
        
        st.divider()
        if st.checkbox("Mostra Storico (Serviti)"):
            st.dataframe(ordini[ordini['Stato'] == "Completato"])