import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta

# Configuración general
st.set_page_config(layout="wide")
st.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)

st.markdown("""
    <style>
    .valor {
        text-align: right;
        float: right;
    }
    .verde {
        color: green;
    }
    .rojo {
        color: red;
    }
    .mostaza {
        color: #e6b800;
    }
    .gris {
        color: lightgrey;
    }
    .bold {
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# FUNCIONES

def calcular_gap(spot_apertura, spot_cierre):
    puntos = round(spot_apertura - spot_cierre, 2)
    porcentaje = round((puntos / spot_cierre) * 100, 2)
    return puntos, porcentaje

def calcular_divergencia(futuro, spot_apertura):
    puntos = round(futuro - spot_apertura, 2)
    porcentaje = round((puntos / spot_apertura) * 100, 4)
    return puntos, porcentaje

# TITULO
st.markdown("# Datos Iniciales")

# INPUTS MANUALES
col1, col2 = st.columns(2)
with col1:
    spot_cierre = st.number_input("Spot cierre", value=5956.79, step=0.25, format="%.2f")
with col2:
    spot_apertura = st.number_input("Spot apertura", value=5983.80, step=0.25, format="%.2f")

futuro = st.number_input("Futuro (ES1!)", value=0.00, step=0.25, format="%.2f")

# CALCULOS
p_gap, gap_pct = calcular_gap(spot_apertura, spot_cierre)
p_div, div_pct = calcular_divergencia(futuro, spot_apertura)

# MOSTRAR DATOS CALCULADOS
st.markdown(f"""
**Spot cierre** <span class='valor'>{spot_cierre:,.2f}</span>  
**Spot apertura** <span class='valor'>{spot_apertura:,.2f}</span>  
**Gap Spot** <span class='valor verde'>{p_gap:+.2f} {'↑' if p_gap > 0 else '↓' if p_gap < 0 else ''} / {gap_pct:.2f}%</span>  
**Divergencia** <span class='valor {'rojo' if (p_gap > 0 and p_div > 0) or (p_gap < 0 and p_div < 0) else 'verde'}'>{f"{p_div:+.2f} / {div_pct:.2f}%" if (futuro != 0.00) else "<span class='rojo'>⚠ Gap descontado</span>"}</span>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("# Entrada recomendada")

# RECOMENDACION
entrada = ""
color = ""
ipc = ""
tp = sl = None

if (p_gap > 0 and p_div < 0):
    entrada = "Largo"
    ipc = "⬆"
    if div_pct >= 0.24:
        tp, sl = 10, 3
        color = "verde"
    elif div_pct >= 0.10:
        tp, sl = 4, 3
        color = "mostaza"
elif (p_gap < 0 and p_div > 0):
    entrada = "Corto"
    ipc = "⬇"
    if div_pct >= 0.24:
        tp, sl = 10, 3
        color = "rojo"
    elif div_pct >= 0.10:
        tp, sl = 4, 3
        color = "mostaza"
else:
    entrada = "No hay entrada recomendada (gap ya descontado)"
    ipc = "⚠"
    color = "gris"

# MOSTRAR ENTRADA
if "No hay entrada" in entrada:
    st.markdown(f"<span class='{color}'><b>{ipc} {entrada}</b></span>", unsafe_allow_html=True)
else:
    st.markdown(f"<span class='{color}'><b>{ipc} {entrada}</b></span>", unsafe_allow_html=True)
    st.markdown(f"**TP / SL** <span class='valor'>+{tp} / -{sl}</span>", unsafe_allow_html=True)

# BLOQUE VALIDACION - SIEMPRE VISIBLE
with st.expander("Validación entrada en tendencia (1min)", expanded=True):
    rsi = 61
    volumen = 2100
    cuerpo_vela = 1.3
    divergencia_actual = round(abs(div_pct), 2)
    
    st.markdown(f"**RSI (>55)** <span class='valor verde'>{rsi}</span>", unsafe_allow_html=True)
    st.markdown(f"**Volumen (>2000)** <span class='valor verde'>{volumen}</span>", unsafe_allow_html=True)
    st.markdown(f"**Cuerpo vela (≥1.25)** <span class='valor verde'>{cuerpo_vela}</span>", unsafe_allow_html=True)
    st.markdown(f"**Divergencia (≥0.10%)** <span class='valor {'verde' if div_pct >= 0.10 else 'rojo'}'>{divergencia_actual:.2f}</span>", unsafe_allow_html=True)
