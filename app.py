import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta

st.set_page_config(page_title="Estrategia SP500", layout="centered")

st.markdown("## Datos Iniciales")

# === Obtener datos SPY ===
try:
    spy = yf.Ticker("SPY")
    hist = spy.history(period="5d")
    spot_cierre_auto = hist["Close"].iloc[-2] * 10 if len(hist) >= 2 else None
    pre_market = spy.history(period="1d", interval="1m")
    spot_apertura_auto = pre_market["Open"].iloc[0] * 10 if not pre_market.empty else None
    datos_ok = spot_cierre_auto and spot_apertura_auto
except:
    datos_ok = False

if not datos_ok:
    st.error("❌ No se pudo obtener el precio de preapertura del SPY.")
    spot_cierre = st.number_input("Spot cierre (manual)", step=1.0, format="%.2f")
    spot_apertura = st.number_input("Spot apertura (manual)", step=1.0, format="%.2f")
else:
    spot_cierre = spot_cierre_auto
    spot_apertura = spot_apertura_auto

futuro = st.number_input("Futuro (ES1!)", step=1.0, format="%.2f")

# === Cálculos ===
gap_valor = spot_apertura - spot_cierre
gap_pct = (gap_valor / spot_cierre) * 100 if spot_cierre else 0
flecha = "↑" if gap_valor > 0 else "↓"
flecha_color = "green" if gap_valor > 0 else "red"
flecha_coloreada = f"<span style='color:{flecha_color}'>{flecha}</span>"
gap_txt = f"{gap_valor:,.2f} {flecha_coloreada} / {abs(gap_pct):.2f}%"

divergencia_valor = futuro - spot_apertura
divergencia_pct = (divergencia_valor / spot_apertura) * 100 if spot_apertura else 0
div_color = "green" if (gap_valor > 0 and divergencia_valor < 0) or (gap_valor < 0 and divergencia_valor > 0) else "red"
div_txt = f"<span style='color:{div_color}'>{divergencia_valor:,.2f} / {abs(divergencia_pct):.2f}%</span>"

# === Visualización alineada ===
def fila(nombre, valor_html):
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"{nombre}")
    with col2:
        st.markdown(f"<p style='text-align:right'>{valor_html}</p>", unsafe_allow_html=True)

fila("Spot cierre", f"{spot_cierre:,.2f}")
fila("Spot apertura", f"{spot_apertura:,.2f}")
fila("Gap Spot", gap_txt)
fila("Divergencia", div_txt)

