import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta

st.set_page_config(page_title="Estrategia SP500", layout="centered")
st.markdown("## Datos Iniciales")

# --- Obtener datos de SPY ---
def obtener_datos_spy():
    try:
        hoy = datetime.today()
        spy = yf.Ticker("SPY")
        df = spy.history(period="2d")
        cierre = df["Close"].iloc[-2] * 10  # Día anterior
        preapertura = df["Close"].iloc[-1] * 10  # Último valor disponible
        return round(cierre, 2), round(preapertura, 2)
    except:
        return None, None

spot_cierre, spot_apertura = obtener_datos_spy()

# --- Mostrar entradas manuales si falla la lectura automática ---
if spot_cierre is None or spot_apertura is None:
    st.error("❌ No se pudo obtener automáticamente el precio de preapertura del SPY.")
    spot_cierre = st.number_input("Spot cierre", value=0.0, step=1.0, format="%.2f")
    spot_apertura = st.number_input("Spot apertura (manual)", value=0.0, step=1.0, format="%.2f")
else:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div style='text-align: right;'>Spot cierre</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: right; font-weight: bold;'>{spot_cierre:,.2f}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div style='text-align: right;'>Spot apertura</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: right; font-weight: bold;'>{spot_apertura:,.2f}</div>", unsafe_allow_html=True)

# --- Entrada manual del Futuro ---
futuro = st.number_input("Futuro (ES1!)", value=5980.00, step=1.0, format="%.2f")

# --- Cálculo GAP y Divergencia ---
if spot_cierre and spot_apertura:
    gap = round(spot_apertura - spot_cierre, 2)
    gap_pct = round((gap / spot_cierre) * 100, 2)
    gap_signo = "↑" if gap > 0 else "↓"
    gap_texto = f"{gap:,.2f} {gap_signo} / {abs(gap_pct):.2f}%"

    divergencia = round(futuro - spot_apertura, 2)
    divergencia_pct = round((divergencia / abs(gap)) * 100, 2) if gap != 0 else 0
    divergencia_color = "green" if (gap > 0 and divergencia < 0) or (gap < 0 and divergencia > 0) else "red"
    divergencia_texto = f"<span style='color:{divergencia_color}; font-weight:bold'>{divergencia:,.2f} / {abs(divergencia_pct):.2f}%</span>"

    st.markdown("---")
    st.markdown(f"<div style='text-align: right;'>Gap Spot</div><div style='text-align: right; font-weight: bold;'>{gap_texto}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: right;'>Divergencia</div><div style='text-align: right;'>{divergencia_texto}</div>", unsafe_allow_html=True)
