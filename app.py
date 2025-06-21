import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta

st.set_page_config(page_title="Estrategia SP500", layout="centered")

st.markdown("<h2 style='margin-bottom: 1rem;'>Datos Iniciales</h2>", unsafe_allow_html=True)

# --- Obtener datos SPY automáticamente ---
def obtener_datos_spy():
    try:
        hoy = datetime.today()
        ayer = hoy - timedelta(days=1)
        datos = yf.download("SPY", start=ayer.strftime('%Y-%m-%d'), end=hoy.strftime('%Y-%m-%d'), progress=False)

        cierre = datos["Close"][-1] * 10
        premarket = yf.Ticker("SPY").info["preMarketPrice"] * 10
        return round(cierre, 2), round(premarket, 2)
    except:
        return None, None

spot_cierre, spot_apertura = obtener_datos_spy()

# --- Entrada manual si falla conexión ---
if spot_cierre is None or spot_apertura is None:
    st.error("❌ No se pudo obtener el precio de preapertura del SPY.")
    spot_cierre = st.number_input("Spot cierre (manual)", value=0.0, format="%.2f", key="cierre_manual")
    spot_apertura = st.number_input("Spot apertura (manual)", value=0.0, format="%.2f", key="apertura_manual")

# --- Entrada de Futuro ---
futuro = st.number_input("Futuro (ES1!)", value=5980.00, format="%.2f")

# --- Cálculo de GAP y Divergencia ---
gap_valor = spot_apertura - spot_cierre
gap_pct = (gap_valor / spot_cierre) * 100 if spot_cierre else 0
flecha = "↑" if gap_valor > 0 else "↓"

div_valor = futuro - spot_apertura
div_pct = (abs(div_valor) / abs(gap_valor)) * 100 if gap_valor != 0 else 0
div_color = "green" if (gap_valor > 0 and div_valor < 0) or (gap_valor < 0 and div_valor > 0) else "red"

# --- Mostrar datos alineados ---
def fila(nombre, valor):
    st.markdown(f"<div style='display: flex; justify-content: space-between;'>"
                f"<span>{nombre}</span><span><b>{valor}</b></span></div>", unsafe_allow_html=True)

fila("Spot cierre", f"{spot_cierre:,.2f}")
fila("Spot apertura", f"{spot_apertura:,.2f}")
fila("Gap Spot", f"{gap_valor:,.2f} {flecha} / {abs(gap_pct):.2f}%")
st.markdown(
    f"<div style='display: flex; justify-content: space-between;'>"
    f"<span>Divergencia</span><span style='color:{div_color}; font-weight:bold;'>{div_valor:,.2f} / {abs(div_pct):.2f}%</span>"
    f"</div>", unsafe_allow_html=True
)

