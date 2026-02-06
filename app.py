import streamlit as st
import pandas as pd
import re

# 1. Configurazione - Tema pulito
st.set_page_config(page_title="Luna Piena", layout="centered")

# 2. Caricamento Dati
SHEET_ID = "1sRbYNs_KA7Tm5IvqitJhYxYPVria8qDPdMliOPnFO_k"
URL_MANGIARE = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Mangiare"
URL_BERE = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Bere"

@st.cache_data(ttl=30)
def load_data():
    try:
        f = pd.read_csv(URL_MANGIARE).fillna("")
        b = pd.read_csv(URL_BERE).fillna("")
        return f, b
    except:
        return None, None

def get_price(price_str):
    try:
        return float(re.sub(r'[^\d.]', '', str(price_str).replace(',', '.')))
    except:
        return 0.0

# --- LOGICA CARRELLO (Risolve il bug del clic) ---
if 'cart' not in st.session_state:
    st.session_state.cart = []

def add_to_cart(nome, prezzo):
    st.session_state.cart.append({"nome": nome, "prezzo": prezzo})
    st.toast(f"Aggiunto: {nome}")

df_food, df_drinks = load_data()

# --- INTERFACCIA MINIMAL ---
st.title("Luna Piena")
st.write("---")

if df_food is not None:
    # Sidebar minimalista per il conto
    with st.sidebar:
        st.subheader("Il tuo Tavolo")
        tavolo = st.selectbox("Seleziona", [f"Tavolo {i:02d}" for i in range(1, 21)])
        st.divider()
        
        if st.session_state.cart:
            totale = sum(item['prezzo'] for item in st.session_state.cart)
            for item in st.session_state.cart:
                st.caption(f"1x {item['nome']} — {item['prezzo']:.2f}€")
            
            st.write(f"### Totale: {totale:.2f} €")
            if st.button("Invia Ordine", use_container_width=True, type="primary"):
                st.success("Inviato!")
                st.session_state.cart = []
                st.rerun()
            if st.button("Svuota", use_container_width=True):
                st.session_state.cart = []
                st.rerun()
        else:
            st.write("Seleziona i piatti dal menù.")

    # Tabs con stile pulito
    tab_food, tab_drink = st.tabs(["Cucina", "Bevande"])

    with tab_food:
        for cat in df_food['Categoria'].unique():
            st.markdown(f"#### {cat}")
            items = df_food[df_food['Categoria'] == cat]
            for i, row in items.iterrows():
                # Card minimalista senza bordi pesanti
                col_txt, col_btn = st.columns([4, 1.2])
                with col_txt:
                    st.write(f"**{row['Nome']}**")
                    st.caption(row['Descrizione'])
                with col_btn:
                    p_val = get_price(row['Prezzo'])
                    # On_click risolve il bug della sincronizzazione
                    st.button(f"{row['Prezzo']}", 
                              key=f"f_{i}", 
                              on_click=add_to_cart, 
                              args=(row['Nome'], p_val),
                              use_container_width=True)
            st.write("")

    with tab_drink:
        for cat in df_drinks['Categoria'].unique():
            st.markdown(f"#### {cat}")
            items = df_drinks[df_drinks['Categoria'] == cat]
            for i, row in items.iterrows():
                col_txt, col_btn = st.columns([4, 1.2])
                with col_txt:
                    st.write(f"**{row['Nome']}**")
                    st.caption(row['Descrizione'])
                with col_btn:
                    p_val = get_price(row['Prezzo'])
                    st.button(f"{row['Prezzo']}", 
                              key=f"d_{i}", 
                              on_click=add_to_cart, 
                              args=(row['Nome'], p_val),
                              use_container_width=True)
            st.write("")
