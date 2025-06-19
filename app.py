import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Estrategia SP500", layout="wide")

# ====================
# FUNCIONES AUXILIARES
# ====================
def get_spy_prices():
    now = datetime.now()
    end = now
    start = now - timedelta(days=5)
    data = yf.download("SPY", start=start, end=end, interval="1d")
    if len(data) >= 2:
        cierre = round(data['Close'].iloc[-2] * 10, 2)
        apertura = round(data['Open'].iloc[-1] * 10, 2)
        return cierre, apertura
    return None, None

# ====================
# DATOS INICIALES
# ====================
st.title("📈 Estrategia SP500 - Versión Web")

spot_cierre, spot_apertura = get_spy_prices()

col1, col2, col3 = st.columns(3)

with col1:
    st.write(f"**📉 Spot cierre:** {'{:.2f}'.format(spot_cierre) if spot_cierre else 'N/D'}")
with col2:
    st.write(f"**📈 Spot apertura:** {'{:.2f}'.format(spot_apertura) if spot_apertura else 'N/D'}")
with col3:
    futuro = st.number_input("📊 Futuro (ES1!)", value=5345.0, step=0.25)

# Gap y Divergencia
gap = round((spot_apertura - spot_cierre) / spot_cierre * 100, 2) if spot_cierre and spot_apertura else 0
divergencia = round((futuro - spot_apertura) / spot_apertura * 100, 2) if spot_apertura else 0

st.markdown("---")
st.subheader("📊 Datos Iniciales")

col4, col5, col6 = st.columns(3)
with col4:
    st.write(f"**📏 Gap:** {gap:.2f}%")
with col5:
    st.write(f"**📐 Divergencia:** {divergencia:.2f}%")
with col6:
    st.write("")

# ====================
# ENTRADA RECOMENDADA
# ====================
st.markdown("---")
st.subheader("📌 Entrada recomendada")

entrada = spot_apertura
tp = round(entrada + 5.5, 2)
sl = round(entrada - 3.5, 2)

tipo = "LARGO" if divergencia >= 0 else "CORTO"
color = "green" if tipo == "LARGO" else "red"

st.markdown(f"**🔵 Tipo de entrada:** <span style='color:{color}'>{tipo}</span>", unsafe_allow_html=True)
st.markdown(f"**🎯 Entrada:** <span style='color:{color}'>{entrada:.2f}</span>", unsafe_allow_html=True)
st.markdown(f"**✅ TP:** <span style='color:{'red' if tipo == 'LARGO' else 'green'}'>{tp:.2f}</span>", unsafe_allow_html=True)
st.markdown(f"**🛑 SL:** <span style='color:{'red' if tipo == 'LARGO' else 'green'}'>{sl:.2f}</span>", unsafe_allow_html=True)

# ====================
# VALIDACIÓN TENDENCIA (1min)
# ====================
with st.expander("🔎 Validación entrada en tendencia (1min)"):
    data_validacion = {
        "Condición": ["RSI > 55", "Volumen ≥ 2000", "Cuerpo vela ≥ 1.25 pt", "Impulso ≥ 2.00 pt", "Retroceso ≤ -1.00 pt"],
        "Valor límite": [55, 2000, 1.25, 2.00, -1.00],
        "Valor actual": [61, 2700, 1.85, 2.10, -0.70]
    }
    df_val = pd.DataFrame(data_validacion)
    st.dataframe(df_val, use_container_width=True)

# ====================
# TP EXTENDIDO
# ====================
with st.expander("🎯 Condiciones TP Extendido"):
    df_tp_ext = pd.DataFrame({
        "Condición": ["RSI > 60", "Volumen > 2500", "Cuerpo vela ≥ 1.25 pt", "Gap Spot ≥ 0.24%", "Divergencia ≥ 0.10%", "Impulso ≥ 2.00 pt", "Retroceso ≤ -1.00 pt"],
        "Valor límite": [60, 2500, 1.25, 0.24, 0.10, 2.00, -1.00],
        "Valor actual": [61, 2700, 1.85, gap, divergencia, 2.10, -0.70]
    })
    st.dataframe(df_tp_ext, use_container_width=True)

# ====================
# SL TRAILING
# ====================
with st.expander("🛡 Condiciones SL Trailing"):
    df_trail = pd.DataFrame({
        "Condición": ["Avance ≥ 2.0 pt", "RSI > 55", "Volumen > 2000"],
        "Valor límite": [2.0, 55, 2000],
        "Valor actual": [2.20, 58, 2600]
    })
    st.dataframe(df_trail, use_container_width=True)

# ====================
# BOTÓN RECALCULAR
# ====================
st.markdown("---")
st.button("🔄 Forzar actualización de datos")

