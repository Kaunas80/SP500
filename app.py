import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(layout="wide")

# =====================
# Función para obtener valores
# =====================
def obtener_valores_spy():
    spy = yf.Ticker("SPY")
    try:
        cierre = spy.history(period="2d")['Close'].iloc[-2] * 10
    except:
        cierre = None
    try:
        apertura = spy.info.get("preMarketPrice", None)
        if apertura:
            apertura *= 10
    except:
        apertura = None
    return cierre, apertura

# =====================
# Obtener valores
# =====================
spot_cierre, spot_apertura = obtener_valores_spy()

# =====================
# Interfaz visual
# =====================
st.markdown("""
    <style>
        body { background-color: white; color: black; }
        .data-row { display: flex; justify-content: space-between; padding: 0.3em 0; border-bottom: 1px solid #eee; }
        .data-label { font-weight: bold; width: 50%; text-align: left; }
        .data-value { width: 50%; text-align: right; }
        .green { color: green; font-weight: bold; }
        .red { color: red; font-weight: bold; }
        .section-title { font-size: 20px; font-weight: bold; margin-top: 1em; border-bottom: 2px solid #000; padding-bottom: 0.3em; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">Datos Iniciales</div>', unsafe_allow_html=True)

# =====================
# Entradas manuales en caso de error
# =====================
if spot_cierre is None:
    spot_cierre = st.number_input("Spot cierre (manual)", value=0.0, step=0.1)
else:
    st.markdown(f'<div class="data-row"><div class="data-label">Spot cierre</div><div class="data-value">{spot_cierre:.2f}</div></div>', unsafe_allow_html=True)

if spot_apertura is None:
    spot_apertura = st.number_input("Spot apertura (manual)", value=0.0, step=0.1)
else:
    st.markdown(f'<div class="data-row"><div class="data-label">Spot apertura</div><div class="data-value">{spot_apertura:.2f}</div></div>', unsafe_allow_html=True)

# =====================
# Entrada manual: Futuro
# =====================
futuro = st.number_input("Futuro (ES1!)", value=5980.0, step=0.1)

# =====================
# Cálculos si todo está disponible
# =====================
if spot_cierre and spot_apertura:
    gap = spot_apertura - spot_cierre
    gap_pct = (gap / spot_apertura) * 100
    gap_arrow = "↑" if gap > 0 else "↓"

    divergencia = futuro - spot_apertura
    div_pct = (divergencia / abs(gap)) * 100 if gap != 0 else 0
    div_color = "green" if (gap > 0 and divergencia < 0) or (gap < 0 and divergencia > 0) else "red"

    # Mostrar valores
    st.markdown(f'<div class="data-row"><div class="data-label">Spot apertura (calculado)</div><div class="data-value">{spot_apertura:.2f}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="data-row"><div class="data-label">Gap Spot</div><div class="data-value">{gap:.2f} {gap_arrow} / {gap_pct:.2f}%</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="data-row"><div class="data-label">Divergencia</div><div class="data-value {div_color}">{divergencia:.2f} / {div_pct:.2f}%</div></div>', unsafe_allow_html=True)

    st.button("Recalcular")

    # =====================
    # Entrada recomendada
    # =====================
    st.markdown('<div class="section-title">Entrada recomendada</div>', unsafe_allow_html=True)

    if gap > 0 and divergencia > 0:
        st.markdown('<div class="data-row"><div class="data-label">Tipo</div><div class="data-value green">Largo ↑</div></div>', unsafe_allow_html=True)
        entrada = spot_apertura
        tp = entrada + 30
        sl = entrada - 15
    elif gap < 0 and divergencia < 0:
        st.markdown('<div class="data-row"><div class="data-label">Tipo</div><div class="data-value red">Corto ↓</div></div>', unsafe_allow_html=True)
        entrada = spot_apertura
        tp = entrada - 30
        sl = entrada + 15
    else:
        st.markdown('<div class="data-row"><div class="data-label">Tipo</div><div class="data-value">Sin entrada</div></div>', unsafe_allow_html=True)
        entrada = tp = sl = None

    if entrada:
        st.markdown(f'<div class="data-row"><div class="data-label">Entrada</div><div class="data-value">{entrada:.2f}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="data-row"><div class="data-label">TP</div><div class="data-value">{tp:.2f}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="data-row"><div class="data-label">SL</div><div class="data-value">{sl:.2f}</div></div>', unsafe_allow_html=True)

        with st.expander("Validación entrada en tendencia (1min)"):
            st.markdown('<div class="data-row"><div class="data-label">RSI > 55</div><div class="data-value">60</div></div>', unsafe_allow_html=True)
            st.markdown('<div class="data-row"><div class="data-label">Impulso > 0</div><div class="data-value">1.3</div></div>', unsafe_allow_html=True)
            st.markdown('<div class="data-row"><div class="data-label">Volumen > 100%</div><div class="data-value">122</div></div>', unsafe_allow_html=True)

        with st.expander("Condiciones TP Extendido"):
            st.markdown('<div class="data-row"><div class="data-label">Retroceso < 40%</div><div class="data-value">32</div></div>', unsafe_allow_html=True)
            st.markdown('<div class="data-row"><div class="data-label">Volatilidad > 1.0</div><div class="data-value">1.18</div></div>', unsafe_allow_html=True)

        with st.expander("Condiciones SL Trailing"):
            st.markdown('<div class="data-row"><div class="data-label">Velocidad > 0.5</div><div class="data-value">0.76</div></div>', unsafe_allow_html=True)
            st.markdown('<div class="data-row"><div class="data-label">RSI se mantiene > 55</div><div class="data-value">61</div></div>', unsafe_allow_html=True)
