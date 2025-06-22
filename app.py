import streamlit as st
import yfinance as yf

# --- Obtener datos del SPY desde yfinance ---
try:
    spy = yf.Ticker("SPY")
    hist = spy.history(period="7d")
    spot_cierre = round(hist['Close'][-2] * 10, 2)
    spot_apertura = round(hist['Open'][-1] * 10, 2)
    error_datos = False
except:
    spot_cierre = st.number_input("Spot cierre", value=0.0, format="%.2f")
    spot_apertura = st.number_input("Spot apertura", value=0.0, format="%.2f")
    error_datos = True

# --- Input manual del Futuro ---
futuro = st.number_input("Futuro (ES1!)", value=0.0, format="%.2f")

# --- Calcular GAP y Divergencia ---
gap_spot = spot_apertura - spot_cierre
porcentaje_gap = (gap_spot / spot_cierre) * 100 if spot_cierre else 0

# Divergencia = (Spot apertura - Futuro) / Spot apertura
divergencia = (spot_apertura - futuro)
porcentaje_div = (divergencia / spot_apertura) * 100 if spot_apertura else 0

# --- Determinar colores y flechas ---
direccion_gap = "↑" if gap_spot > 0 else "↓"
color_gap = "green" if gap_spot > 0 else "red"

# Determinar si el gap ya fue descontado o no
if (gap_spot > 0 and divergencia > 0) or (gap_spot < 0 and divergencia < 0):
    color_div = "red"  # Ya fue descontado
else:
    color_div = "green"  # Aún no se ha descontado

# --- Bloque: Datos Iniciales ---
st.markdown("<h2 style='color:white;'>Datos Iniciales</h2>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 3])
with col1:
    st.write("Spot cierre")
with col2:
    st.markdown(f"<div style='text-align:right'>{spot_cierre:,.2f}</div>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 3])
with col1:
    st.write("Spot apertura")
with col2:
    st.markdown(f"<div style='text-align:right'>{spot_apertura:,.2f}</div>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 3])
with col1:
    st.write("Gap Spot")
with col2:
    st.markdown(
        f"<div style='text-align:right; color:{color_gap}'>{gap_spot:+.2f} {direccion_gap} / {abs(porcentaje_gap):.2f}%</div>",
        unsafe_allow_html=True
    )

col1, col2 = st.columns([1, 3])
with col1:
    st.write("Divergencia")
with col2:
    st.markdown(
        f"<div style='text-align:right; color:{color_div}'>{divergencia:+.2f} / {abs(porcentaje_div):.2f}%</div>",
        unsafe_allow_html=True
    )
