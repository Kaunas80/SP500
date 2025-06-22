import streamlit as st
import yfinance as yf
import datetime

st.set_page_config(layout="centered")
st.markdown("""<style>div.block-container{padding-top:2rem;}</style>""", unsafe_allow_html=True)

# --- BLOQUE 1: DATOS INICIALES ---
st.markdown("## Datos Iniciales")

# Lectura automática desde yfinance
hoy = datetime.datetime.now().date()
spy = yf.Ticker("SPY")
hist = spy.history(period="7d")

spot_cierre = None
spot_apertura = None

try:
    spot_cierre = round(hist['Close'][-2] * 10, 2)
    spot_apertura = round(hist['Open'][-1] * 10, 2)
except:
    st.warning("No se pudieron obtener los datos automáticamente. Introduce los valores manualmente.")

col1, col2 = st.columns([1, 1])
with col1:
    spot_cierre_input = st.number_input("Spot cierre", value=spot_cierre if spot_cierre else 0.00, step=0.25, format="%.2f")
with col2:
    futuro = st.number_input("Futuro (ES1!)", value=0.00, step=0.25, format="%.2f")

if spot_apertura is None:
    spot_apertura = st.number_input("Spot apertura", value=0.00, step=0.25, format="%.2f")
else:
    st.markdown(f"<div style='display: flex; justify-content: space-between;'><span><b>Spot apertura</b></span><span>{spot_apertura:.2f}</span></div>", unsafe_allow_html=True)

# Gap y Divergencia
if spot_cierre_input != 0:
    gap = round(spot_apertura - spot_cierre_input, 2)
else:
    gap = 0.00

if spot_apertura != 0:
    divergencia = round((futuro - spot_apertura) / spot_apertura * 100, 2)
else:
    divergencia = 0.00

flecha_gap = "↑" if gap > 0 else ("↓" if gap < 0 else "→")
color_gap = "green" if gap != 0 else "lightgrey"

color_div = "green" if (gap > 0 and divergencia < 0) or (gap < 0 and divergencia > 0) else "red"

# Mostrar valores
st.markdown(f"<div style='display: flex; justify-content: space-between;'><span><b>Gap Spot</b></span><span style='color:{color_gap}'>{flecha_gap} {gap:.2f}</span></div>", unsafe_allow_html=True)
st.markdown(f"<div style='display: flex; justify-content: space-between;'><span><b>Divergencia</b></span><span style='color:{color_div}'>{divergencia:.2f}%</span></div>", unsafe_allow_html=True)

if (gap > 0 and divergencia > 0) or (gap < 0 and divergencia < 0):
    st.markdown("<span style='color:red'><b>Gap descontado</b></span>", unsafe_allow_html=True)

# --- BLOQUE 2: ENTRADA RECOMENDADA ---
st.markdown("""
<style>
.recomendacion {
    text-align: right;
    font-size: 1.6em;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown("## Entrada recomendada")

entrada = None
color_entrada = "gray"
icono_entrada = "⚠️"
mensaje = "No hay entrada recomendada"

if ((gap > 0 and divergencia < 0) or (gap < 0 and divergencia > 0)) and futuro != 0:
    if gap > 0 and divergencia < 0:
        entrada = "Largo"
        color_entrada = "green"
        icono_entrada = "⬆️"
    elif gap < 0 and divergencia > 0:
        entrada = "Corto"
        color_entrada = "red"
        icono_entrada = "⬇️"

    if abs(divergencia) < 0.10:
        color_entrada = "gray"
        icono_entrada = "⚠️"
        mensaje = "No hay entrada recomendada (divergencia insuficiente)"
    else:
        mensaje = f"{icono_entrada} {entrada}"
else:
    mensaje = "❌ Gap descontado"

st.markdown(f"<div class='recomendacion' style='color:{color_entrada}'>{mensaje}</div>", unsafe_allow_html=True)

# TP / SL
if entrada:
    if abs(divergencia) < 0.24:
        tp, sl = "+4", "-3" if entrada == "Largo" else "-4", "+3"
    else:
        tp, sl = "+10", "-3" if entrada == "Largo" else "-10", "+3"
    st.markdown(f"<div style='display: flex; justify-content: space-between;'><span><b>TP / SL</b></span><span style='text-align:right'>{tp} / {sl}</span></div>", unsafe_allow_html=True)

# VALIDACIÓN TENDENCIA
with st.expander("Validación entrada en tendencia (1min)", expanded=True):
    def mostrar_validacion(nombre, valor_limite, valor_real):
        color = "green" if valor_real >= valor_limite else "red"
        st.markdown(f"<div style='display: flex; justify-content: space-between;'><span>{nombre} ({valor_limite})</span><span style='color:{color}'>{valor_real}</span></div>", unsafe_allow_html=True)

    mostrar_validacion("RSI", 55, 57)
    mostrar_validacion("Volumen", 2000, 2100)
    mostrar_validacion("Cuerpo de vela", 1.25, 1.35)
    mostrar_validacion("Divergencia", "0.10%", f"{divergencia:.2f}%")

# SL TRAILING
with st.expander("Condiciones SL Trailing"):
    mostrar_validacion("Valor mínimo", 5925, 5932)

# TP EXTENDIDO
with st.expander("Condiciones TP Extendido"):
    mostrar_validacion("Divergencia mínima", "0.24%", f"{divergencia:.2f}%")
    mostrar_validacion("RSI mínimo", 55, 57)
