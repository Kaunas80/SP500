import streamlit as st
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="Entrada SP500", layout="centered")

# --- Funciones ---
def get_spy_prices():
    spy = yf.Ticker("SPY")
    hist = spy.history(period="2d", interval="1d")
    close_spot = round(hist['Close'][-2] * 10, 2)
    open_spot = round(hist['Open'][-1] * 10, 2)
    return close_spot, open_spot

def calcular_gap_divergencia(spot_cierre, spot_apertura, futuro):
    gap = round(spot_apertura - spot_cierre, 2)
    esperado = round(spot_cierre + gap, 2)
    divergencia = round(futuro - esperado, 2)
    return gap, divergencia

# --- Simulamos valores de indicadores (reemplazar por datos reales si se automatiza) ---
rsi = 61
volumen = 2700
cuerpo_vela = 1.85
impulso = +2.2
retroceso = -0.8
puntos_entrada = 540.0
ultimo_precio = 541.75
diff_trailing = round(ultimo_precio - puntos_entrada, 2)

# --- Estilos básicos ---
def mostrar_valor(etiqueta, valor, color=None):
    alineacion = f"<div style='text-align:right; color:{color};'>{valor}</div>" if color else f"<div style='text-align:right;'>{valor}</div>"
    col1, col2 = st.columns([1,1])
    with col1:
        st.markdown(f"**{etiqueta}**")
    with col2:
        st.markdown(alineacion, unsafe_allow_html=True)

# --- DATOS INICIALES ---
st.markdown("## Datos Iniciales")
spot_cierre, spot_apertura = get_spy_prices()
futuro = st.number_input("Futuro (ES1!)", value=spot_apertura, step=0.25, label_visibility="collapsed")

gap, divergencia = calcular_gap_divergencia(spot_cierre, spot_apertura, futuro)

# Colores para Gap y Divergencia
gap_color = "green" if gap > 0 else "red"
div_color = "green" if (gap > 0 and divergencia > 0) or (gap < 0 and divergencia < 0) else "red"

mostrar_valor("Spot cierre", spot_cierre)
mostrar_valor("Spot apertura", spot_apertura)
mostrar_valor("Futuro (ES1!)", futuro)
mostrar_valor("Gap Spot", f"{gap:+.2f}", gap_color)
mostrar_valor("Divergencia", f"{divergencia:+.2f}", div_color)

st.button("Recalcular")

# --- ENTRADA RECOMENDADA ---
st.markdown("## Entrada recomendada")

if divergencia > 0:
    st.markdown("<h3 style='color:green;'>↑ Entrada en largo</h3>", unsafe_allow_html=True)
    mostrar_valor("TP", "+10.00", "red")
    mostrar_valor("SL", "-5.00", "red")
else:
    st.markdown("<h3 style='color:red;'>↓ Entrada en corto</h3>", unsafe_allow_html=True)
    mostrar_valor("TP", "-10.00", "green")
    mostrar_valor("SL", "+5.00", "green")

# --- VALIDACIÓN EN TENDENCIA ---
with st.expander("Validación entrada en tendencia (1min)"):
    mostrar_valor("RSI ≥ 55", f"({rsi})", "green" if rsi >= 55 else "red")
    mostrar_valor("Volumen ≥ 2000", f"({volumen})", "green" if volumen >= 2000 else "red")
    mostrar_valor("Cuerpo vela ≥ 1.25 pt", f"({cuerpo_vela})", "green" if cuerpo_vela >= 1.25 else "red")

# --- TP EXTENDIDO ---
with st.expander("Condiciones TP extendido"):
    mostrar_valor("Impulso ≥ 2 pt", f"({impulso})", "green" if impulso >= 2 else "red")
    mostrar_valor("Retroceso ≤ -0.5 pt", f"({retroceso})", "green" if retroceso <= -0.5 else "red")
    mostrar_valor("Volumen ≥ 2500", f"({volumen})", "green" if volumen >= 2500 else "red")

# --- SL TRAILING ---
with st.expander("Condiciones SL Trailing"):
    mostrar_valor("Diferencia desde entrada", f"{diff_trailing:+.2f}", "green" if diff_trailing > 0 else "red")




