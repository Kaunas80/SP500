from datetime import datetime, timedelta
import yfinance as yf
import streamlit as st

st.set_page_config(layout="wide")

# --- BLOQUE 1: DATOS INICIALES ---

st.markdown("## Datos Iniciales")

# Leer datos desde yfinance con respaldo manual
spy = yf.Ticker("SPY")
hist = spy.history(period="7d")

spot_cierre = None
spot_apertura = None
error_lectura = False

try:
    spot_cierre = round(hist["Close"][-2] * 10, 2)
    spot_apertura = round(hist["Open"][-1] * 10, 2)
except:
    error_lectura = True

col1, col2 = st.columns([2, 2])
with col1:
    spot_cierre = st.number_input("Spot cierre", value=spot_cierre if spot_cierre else 0.0, step=0.25)
with col2:
    spot_apertura = st.number_input("Spot apertura", value=spot_apertura if spot_apertura else 0.0, step=0.25)

# Entrada manual del valor del Futuro (ES1!)
futuro = st.number_input("Futuro (ES1!)", value=0.0, step=0.25)

# Cálculo del Gap Spot
gap_spot = spot_apertura - spot_cierre
gap_pct = (gap_spot / spot_cierre) * 100 if spot_cierre != 0 else 0

if gap_spot > 0:
    flecha_gap = "↑"
elif gap_spot < 0:
    flecha_gap = "↓"
else:
    flecha_gap = "–"

gap_color = "green" if gap_spot != 0 else "lightgray"
gap_text = f"{gap_spot:.2f} {flecha_gap} / {gap_pct:.2f}%"
st.markdown(f"<div style='display: flex; justify-content: space-between;'><span>Gap Spot</span><span style='color:{gap_color}'>{gap_text}</span></div>", unsafe_allow_html=True)

# Cálculo de la Divergencia
divergencia = spot_apertura - futuro
divergencia_pct = (divergencia / spot_apertura) * 100 if spot_apertura != 0 else 0

# Mostrar Divergencia
div_color = "green" if (
    (gap_spot > 0 and divergencia < 0) or (gap_spot < 0 and divergencia > 0)
) else "red"

div_text = f"{divergencia:.2f} / {divergencia_pct:.2f}%"
st.markdown(f"<div style='display: flex; justify-content: space-between;'><span>Divergencia</span><span style='color:{div_color}'>{div_text}</span></div>", unsafe_allow_html=True)

# Mostrar mensaje si el gap ya ha sido descontado
gap_descontado = (gap_spot > 0 and divergencia > 0) or (gap_spot < 0 and divergencia < 0)
if gap_descontado:
    st.markdown("<div style='color:red'><b>⚠️ Gap descontado</b></div>", unsafe_allow_html=True)

st.markdown("---")

# --- BLOQUE 2: ENTRADA RECOMENDADA ---

st.markdown("## Entrada recomendada")

# Parámetros simulados para validación
rsi_valor = 61
rsi_limite = 55
volumen_valor = 2300
volumen_limite = 2000
cuerpo_valor = 1.35
cuerpo_limite = 1.25

# Evaluar dirección del gap
tipo_entrada = "Largo" if divergencia < 0 else "Corto"
entrada_icono = "⬆️" if tipo_entrada == "Largo" else "⬇️"
entrada_color = "gray"
entrada_texto = ""
tp_sl = ""
mostrar_validacion = False

if gap_descontado:
    entrada_color = "#D3D3D3"
    entrada_texto = "⚠️ No hay entrada recomendada (gap ya descontado)"
else:
    if abs(divergencia_pct) < 0.10:
        entrada_color = "#D3D3D3"
        entrada_texto = "🚧 No hay entrada recomendada (divergencia insuficiente)"
    elif abs(divergencia_pct) < 0.24:
        entrada_color = "#f5a623"  # Mostaza
        entrada_texto = f"{entrada_icono} {tipo_entrada}"
        tp_sl = "+4 / -3" if tipo_entrada == "Largo" else "-4 / +3"
        mostrar_validacion = True
    else:
        entrada_color = "green" if tipo_entrada == "Largo" else "red"
        entrada_texto = f"{entrada_icono} {tipo_entrada}"
        tp_sl = "+10 / -3" if tipo_entrada == "Largo" else "-10 / +3"
        mostrar_validacion = True

col1, col2 = st.columns([1, 3])
with col1:
    st.write("**Entrada**")
with col2:
    st.markdown(f"<div style='text-align:right; color:{entrada_color}; font-weight:bold'>{entrada_texto}</div>", unsafe_allow_html=True)

# Mostrar TP / SL si corresponde
if tp_sl:
    col1, col2 = st.columns([1, 3])
    with col1:
        st.write("TP / SL")
    with col2:
        st.markdown(f"<div style='text-align:right'>{tp_sl}</div>", unsafe_allow_html=True)

# Validaciones dentro del desplegable
if mostrar_validacion:
    with st.expander("Validación entrada en tendencia (1min)"):
        def render_validacion(nombre, limite, actual):
            color = "green" if actual >= limite else "red"
            alineado = f"<div style='display: flex; justify-content: space-between;'><span>{nombre} ({limite})</span><span style='color:{color}'>{actual}</span></div>"
            st.markdown(alineado, unsafe_allow_html=True)

        render_validacion("RSI", rsi_limite, rsi_valor)
        render_validacion("Volumen", volumen_limite, volumen_valor)
        render_validacion("Cuerpo vela", cuerpo_limite, cuerpo_valor)

st.markdown("---")
