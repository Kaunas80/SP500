import streamlit as st
import yfinance as yf

st.markdown("## Datos Iniciales")

# Obtener datos del SPY desde yfinance
try:
    spy = yf.Ticker("SPY")
    hist = spy.history(period="7d")

    spot_cierre = hist['Close'].dropna().iloc[-1] * 10
    spot_apertura_series = hist['Open'].dropna()
    spot_apertura = spot_apertura_series[spot_apertura_series != (spot_cierre / 10)].iloc[-1] * 10
    error_spy = False
except Exception:
    spot_cierre = None
    spot_apertura = None
    error_spy = True

# Entrada manual si falla la lectura
if error_spy:
    st.error("❌ No se pudo obtener el precio de preapertura del SPY.")
    spot_cierre = st.number_input("Spot cierre (manual)", value=0.0, step=1.0, format="%.2f")
    spot_apertura = st.number_input("Spot apertura (manual)", value=0.0, step=1.0, format="%.2f")

# Entrada manual del Futuro (siempre)
futuro = st.number_input("Futuro (ES1!)", value=0.0, step=1.0, format="%.2f")

# Mostrar datos solo si están disponibles
if spot_cierre and spot_apertura:

    # Calcular Gap
    gap = spot_apertura - spot_cierre
    gap_pct = (gap / spot_cierre) * 100
    gap_color = "green" if gap > 0 else "red"
    flecha = "↑" if gap > 0 else "↓"
    flecha_coloreada = f"<span style='color:{gap_color}'>{flecha}</span>"
    gap_txt = f"{gap:,.2f} {flecha_coloreada} / {abs(gap_pct):.2f}%"

    # Calcular Divergencia
    divergencia = spot_apertura - futuro
    divergencia_pct = (divergencia / spot_apertura) * 100
    div_color = "green" if (gap > 0 and divergencia > 0) or (gap < 0 and divergencia < 0) else "red"
    div_txt = f"<span style='color:{div_color}'>{divergencia:,.2f} / {abs(divergencia_pct):.2f}%</span>"

    # Mostrar en formato tabla
    def fila(nombre, valor_html):
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown(f"<div style='text-align: left;'>{nombre}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div style='text-align: right;'>{valor_html}</div>", unsafe_allow_html=True)

    fila("Spot cierre", f"{spot_cierre:,.2f}")
    fila("Spot apertura", f"{spot_apertura:,.2f}")
    fila("Gap Spot", gap_txt)
    fila("Divergencia", div_txt)
