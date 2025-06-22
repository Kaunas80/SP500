import streamlit as st
import yfinance as yf

# Configuración de estilo
st.set_page_config(page_title="Estrategia SP500", layout="wide")

st.markdown(
    """
    <style>
    .valor-derecha {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.25rem;
    }
    .valor-derecha span:first-child {
        font-weight: bold;
    }
    .valor-derecha span:last-child {
        text-align: right;
        min-width: 100px;
    }
    .verde {color: green;}
    .rojo {color: red;}
    .gris {color: lightgray;}
    .mostaza {color: #e6ac00;}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Datos Iniciales")

col1, col2 = st.columns(2)
with col1:
    spot_cierre = st.number_input("Spot cierre", value=5956.79, step=0.25, format="%.2f")
with col2:
    spot_apertura = st.number_input("Spot apertura", value=5983.80, step=0.25, format="%.2f")

futuro = st.number_input("Futuro (ES1!)", value=0.0, step=0.25, format="%.2f")

# Cálculos
gap = spot_apertura - spot_cierre
gap_pct = (gap / spot_cierre) * 100 if spot_cierre else 0
divergencia = (futuro - spot_apertura) / spot_apertura if spot_apertura else 0
divergencia_pct = divergencia * 100

# Lógica visual
flecha = "↑" if gap > 0 else "↓" if gap < 0 else ""
color_gap = "verde" if gap != 0 else "gris"
color_div = "verde" if (gap > 0 and divergencia < 0) or (gap < 0 and divergencia > 0) else "rojo"

# Mostrar valores
st.markdown(f"""
<div class="valor-derecha"><span>Spot cierre</span><span>{spot_cierre:,.2f}</span></div>
<div class="valor-derecha"><span>Spot apertura</span><span>{spot_apertura:,.2f}</span></div>
<div class="valor-derecha"><span>Gap Spot</span><span class="{color_gap}">{gap:+.2f} {flecha} / {gap_pct:.2f}%</span></div>
""", unsafe_allow_html=True)

# Divergencia visual o mensaje si ya se descontó
if (gap > 0 and divergencia > 0) or (gap < 0 and divergencia < 0):
    st.markdown(f"""
    <div class="valor-derecha"><span>Divergencia</span><span class="rojo">⚠️ Gap descontado</span></div>
    """, unsafe_allow_html=True)
    entrada_valida = False
else:
    st.markdown(f"""
    <div class="valor-derecha"><span>Divergencia</span><span class="{color_div}">{spot_apertura:,.2f} / {divergencia_pct:.2f}%</span></div>
    """, unsafe_allow_html=True)
    entrada_valida = True

st.markdown("---")
st.header("Entrada recomendada")

# Determinar tipo de entrada
if entrada_valida and abs(divergencia_pct) >= 0.10:
    tipo_entrada = "Largo" if divergencia < 0 else "Corto"
    color_tipo = "verde" if tipo_entrada == "Largo" else "rojo"
    flecha = "⬆" if tipo_entrada == "Largo" else "⬇"
    
    if abs(divergencia_pct) >= 0.24:
        tp, sl = "+10", "-3"
        color_entrada = "verde"
    else:
        tp, sl = "+4", "-3"
        color_entrada = "mostaza"

    st.markdown(f'<p class="{color_entrada}">{flecha} <b>{tipo_entrada}</b></p>', unsafe_allow_html=True)
    st.markdown(f"**TP / SL**: {tp} / {sl}")
else:
    mensaje = "⚠️ No hay entrada recomendada (gap ya descontado)" if not entrada_valida else "⚠️ No hay entrada recomendada (divergencia insuficiente)"
    st.markdown(f'<p class="gris">{mensaje}</p>', unsafe_allow_html=True)

# Validación (siempre visible)
st.markdown("---")
with st.expander("Validación entrada en tendencia (1min)", expanded=True):
    rsi = 61
    volumen = 2100
    cuerpo_vela = 1.3

    st.markdown(f"""
    <div class="valor-derecha"><span>RSI (&gt;55)</span><span class="verde">{rsi}</span></div>
    <div class="valor-derecha"><span>Volumen (&gt;2000)</span><span class="verde">{volumen}</span></div>
    <div class="valor-derecha"><span>Cuerpo vela (≥1.25)</span><span class="verde">{cuerpo_vela}</span></div>
    <div class="valor-derecha"><span>Divergencia (≥0.10%)</span><span class="{ 'verde' if abs(divergencia_pct) >= 0.10 else 'rojo' }">{divergencia_pct:.2f}%</span></div>
    """, unsafe_allow_html=True)
