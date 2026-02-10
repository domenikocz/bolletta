import streamlit as st

# Configurazione pagina
st.set_page_config(page_title="Simulatore Bolletta Luce", page_icon="⚡")

def calcola_bolletta(consumo_annuo, potenza, residente):
    # --- PARAMETRI ARERA (Esempio valori aggiornabili) ---
    prezzo_energia_kwh = 0.125      # Quota energia (PE + PD + PPE)
    quota_fissa_anno = 58.40        # Commercializzazione (PCV)
    quota_potenza_kw_anno = 21.48   # Trasporto - Quota potenza
    quota_fissa_trasp_anno = 20.12  # Trasporto - Quota fissa
    quota_energia_trasp_kwh = 0.0102 # Trasporto - Quota energia
    oneri_sistema_kwh = 0.0321      # Oneri di sistema (ASOS + ARIM)
    accisa_kwh = 0.0227             # Imposta erariale
    
    # Parametri calcolo mensile
    consumo_mensile = consumo_annuo / 12
    
    # 1. Spesa Materia Energia
    spesa_materia = (consumo_mensile * prezzo_energia_kwh) + (quota_fissa_anno / 12)
    
    # 2. Trasporto e Gestione Contatore
    spesa_trasporto = (quota_fissa_trasp_anno / 12) + \
                      (potenza * quota_potenza_kw_anno / 12) + \
                      (consumo_mensile * quota_energia_trasp_kwh)
    
    # 3. Oneri di Sistema
    spesa_oneri = consumo_mensile * oneri_sistema_kwh
    
    # 4. Imposte (Accise e IVA)
    # Semplificazione accise per residenti (esenzione primi 150kWh/mese non applicata qui)
    totale_accise = consumo_mensile * accisa_kwh
    imponibile = spesa_materia + spesa_trasporto + spesa_oneri + totale_accise
    iva = imponibile * 0.10
    
    totale_mensile = imponibile + iva
    
    return {
        "Materia Energia": spesa_materia,
        "Trasporto e Contatore": spesa_trasporto,
        "Oneri di Sistema": spesa_oneri,
        "Accise": totale_accise,
        "IVA (10%)": iva,
        "Totale Mensile": totale_mensile,
        "Totale Annuo": totale_mensile * 12
    }

# --- INTERFACCIA STREAMLIT ---
st.title("⚡ Simulatore Bolletta Luce Online")
st.markdown("Calcola una stima della tua bolletta basata sui parametri standard ARERA.")

with st.sidebar:
    st.header("Parametri Utenza")
    consumo = st.number_input("Consumo Annuo (kWh)", min_value=0, value=2700, step=100)
    potenza = st.slider("Potenza Impegnata (kW)", 1.5, 6.0, 3.0, 0.5)
    residente = st.checkbox("Utenza Residente", value=True)
    st.info("I prezzi utilizzati sono stime medie basate sulle componenti ARERA.")

# Calcolo
risultati = calcola_bolletta(consumo, potenza, residente)

# Visualizzazione Risultati
col1, col2 = st.columns(2)
with col1:
    st.metric("Totale Mensile Stimato", f"€ {risultati['Totale Mensile']:.2f}")
with col2:
    st.metric("Totale Annuo Stimato", f"€ {risultati['Totale Annuo']:.2f}")

st.subheader("Dettaglio Voci in Bolletta (Mensile)")

# Creazione tabella per dettaglio
dettaglio_data = {
    "Voce di Spesa": ["Materia Energia", "Trasporto e Contatore", "Oneri di Sistema", "Accise", "IVA"],
    "Importo (€)": [
        f"{risultati['Materia Energia']:.2f}",
        f"{risultati['Trasporto e Contatore']:.2f}",
        f"{risultati['Oneri di Sistema']:.2f}",
        f"{risultati['Accise']:.2f}",
        f"{risultati['IVA (10%)']:.2f}"
    ]
}
st.table(dettaglio_data)

# Grafico a torta
import pandas as pd
df_grafico = pd.DataFrame({
    "Voce": ["Materia", "Trasporto", "Oneri", "Imposte"],
    "Valore": [risultati['Materia Energia'], risultati['Trasporto e Contatore'], 
               risultati['Oneri di Sistema'], risultati['Accise'] + risultati['IVA (10%)']]
})
st.bar_chart(df_grafico.set_index("Voce"))
