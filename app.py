import streamlit as st
import yfinance as yf

st.markdown("## Datos Iniciales")

# Intentar obtener datos de SPY
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
    spot_cierre = st.number_input("Spot cierre (manual)", step=1.0)
    spot_apertura = st.number_input("Spot apertura (manual)", step=1.0)
else:
    spot_cierre = spot_cierre_auto
    spot_apertura = spot_apertura_auto

futuro = st.number_input("Futuro (ES1!)", step=1.0)

# Mostrar valores alineados estilo tabla
col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("Spot cierre")
with col2:
    st.markdown(f"<p style='text-align:right'><strong>{spot_cierre:,.2f}</strong></p>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("Spot apertura")
with col2:
    st.markdown(f"<p style='text-align:right'><strong>{spot_apertura:,.2f}</strong></p>", unsafe_allow_html=True)

# Calcular Gap y Divergencia
gap_valor = spot_apertura - spot_cierre
gap_pct = (gap_valor / spot_cierre) * 100
flecha = "↑" if gap_valor > 0 else "↓"
gap_txt = f"{gap_valor:,.2f} {flecha} / {abs(gap_pct):.2f}%"

divergencia_valor = futuro - spot_apertura
divergencia_pct = (divergencia_valor / spot_apertura) * 100
div_color = "green" if (gap_valor > 0 and divergencia_valor < 0) or (gap_valor < 0 and divergencia_valor > 0) else "red"
div_txt = f"<span style='color:{div_color}'>{divergencia_valor:,.2f} / {abs(divergencia_pct):.2f}%</span>"

col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("Gap Spot")
with col2:
    st.markdown(f"<p style='text-align:right'>{gap_txt}</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("Divergencia")
with col2:
    st.markdown(f"<p style='text-align:right'>{div_txt}</p>", unsafe_allow_html=True)

