import streamlit as st
import yfinance as yf

st.set_page_config(layout="centered")
st.markdown("<h4>Datos Iniciales</h4>", unsafe_allow_html=True)

# --- Lectura automática SPY desde yfinance ---
spot_cierre_auto = None
spot_apertura_auto = None

try:
    spy = yf.Ticker("SPY")
    hist = spy.history(period="7d")
    spot_cierre_auto = round(hist["Close"][-2] * 10, 2)
    spot_apertura_auto = round(hist["Open"][-1] * 10, 2)
except:
    pass

# --- Entradas manuales (con fallback si falla lectura automática) ---
col1, col2 = st.columns([1.2, 2])
with col1:
    st.write("Spot cierre")
with col2:
    spot_cierre = st.number_input(" ", value=spot_cierre_auto if spot_cierre_auto else 0.00, format="%.2f", key="sc")

col1, col2 = st.columns([1.2, 2])
with col1:
    st.write("Spot apertura")
with col2:
    spot_apertura = st.number_input("  ", value=spot_apertura_auto if spot_apertura_auto else 0.00, format="%.2f", key="sa")

col1, col2 = st.columns([1.2, 2])
with col1:
    st.write("Futuro (ES1!)")
with col2:
    futuro = st.number_input("   ", value=0.00, format="%.2f", key="fut")

# --- Cálculo GAP y DIVERGENCIA ---
gap_valor = round(spot_apertura - spot_cierre, 2)
gap_flecha = "↑" if gap_valor > 0 else ("↓" if gap_valor < 0 else "→")
gap_color = "green" if gap_valor != 0 else "lightgray"

div_valor = spot_apertura - futuro if futuro != 0 else None
div_perc = ((spot_apertura - futuro) / spot_apertura * 100) if futuro != 0 else None

# Gap Spot
col1, col2 = st.columns([1.2, 2])
with col1:
    st.write("Gap Spot")
with col2:
    st.markdown(f"<div style='text-align:right; color:{gap_color}'>{gap_flecha} {gap_valor:.2f}</div>", unsafe_allow_html=True)

# Divergencia
col1, col2 = st.columns([1.2, 2])
with col1:
    st.write("Divergencia")
with col2:
    if futuro == 0:
        st.markdown("<div style='text-align:right; color:gray'>-- / --</div>", unsafe_allow_html=True)
    else:
        gap_direccion = "up" if gap_valor > 0 else "down" if gap_valor < 0 else "neutral"
        div_direccion = "up" if div_valor > 0 else "down" if div_valor < 0 else "neutral"
        div_color = "red" if gap_direccion != div_direccion else "green"
        st.markdown(f"<div style='text-align:right; color:{div_color}'>{div_valor:.2f} / {div_perc:.2f}%</div>", unsafe_allow_html=True)

# --- Entrada recomendada ---
st.markdown("### Entrada recomendada")

# Condiciones para entrada
entrada = None
icono = ""
color = ""
tp = ""
sl = ""

if futuro == 0:
    mensaje = "⚠️ Falta dato del Futuro"
    st.markdown(f"<div style='text-align:center; color:gray'>{mensaje}</div>", unsafe_allow_html=True)
else:
    if gap_direccion == div_direccion and div_perc > 0:
        if div_perc < 0.10:
            st.markdown(f"<div style='text-align:center; color:gray'>⚠️ No hay entrada recomendada (divergencia insuficiente)</div>", unsafe_allow_html=True)
        else:
            entrada = "Largo" if div_direccion == "up" else "Corto"
            color = "orange" if div_perc < 0.24 else "green"
            icono = "⬆️" if entrada == "Largo" else "⬇️"
            if div_perc < 0.24:
                tp, sl = "+4", "-3" if entrada == "Largo" else "-4", "+3"
            else:
                tp, sl = "+10", "-3" if entrada == "Largo" else "-10", "+3"
    else:
        st.markdown(f"<div style='text-align:center; color:red'>🚫 Gap descontado. No hay entrada recomendada.</div>", unsafe_allow_html=True)

# Mostrar entrada si aplica
if entrada:
    col1, col2 = st.columns([1.2, 2])
    with col1:
        st.write("Entrada")
    with col2:
        st.markdown(f"<div style='text-align:right; color:{color}; font-weight:bold; font-size:20px'>{icono} {entrada}</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 2])
    with col1:
        st.write("TP / SL")
    with col2:
        st.markdown(f"<div style='text-align:right'>{tp} / {sl}</div>", unsafe_allow_html=True)

# --- Validación entrada en tendencia (siempre visible) ---
st.markdown("### Validación entrada en tendencia (1min)")
def validar(nombre, actual, limite, operador):
    if operador == ">":
        cumple = actual > limite
    elif operador == "<":
        cumple = actual < limite
    else:
        cumple = False
    color = "green" if cumple else "red"
    st.markdown(f"<div style='display:flex; justify-content:space-between;'><span>{nombre} ({limite})</span><span style='color:{color}'>{actual}</span></div>", unsafe_allow_html=True)

validar("RSI", 61, 55, ">")
validar("Volumen", 2100, 2000, ">")
validar("Cuerpo vela", 1.5, 1.25, ">")
if futuro != 0:
    validar("Divergencia", round(div_perc, 2), 0.10, ">")
