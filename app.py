import streamlit as st

# Configuración inicial
st.set_page_config(page_title="Estrategia SP500", layout="wide")
st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)

# --- DATOS INICIALES ---
st.title("Datos Iniciales")

col1, col2 = st.columns(2)

with col1:
    spot_cierre = st.number_input("Spot cierre", value=5956.79, step=0.25, format="%.2f")
with col2:
    spot_apertura = st.number_input("Spot apertura", value=5983.80, step=0.25, format="%.2f")

futuro = st.number_input("Futuro (ES1!)", value=5970.00, step=0.25, format="%.2f")

# Cálculos
gap = spot_apertura - spot_cierre
gap_pct = (gap / spot_cierre) * 100 if spot_cierre != 0 else 0
divergencia = futuro - spot_apertura
divergencia_pct = (divergencia / spot_apertura) * 100 if spot_apertura != 0 else 0

# Visualización de valores
st.write("")
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("**Spot cierre**")
    st.markdown("**Spot apertura**")
    st.markdown("**Gap Spot**")
    st.markdown("**Divergencia**")

with col2:
    st.markdown(f"<div style='text-align: right'>{spot_cierre:,.2f}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: right'>{spot_apertura:,.2f}</div>", unsafe_allow_html=True)

    gap_color = "green" if gap != 0 else "lightgray"
    gap_arrow = "↑" if gap > 0 else "↓" if gap < 0 else ""
    st.markdown(
        f"<div style='text-align: right; color:{gap_color}'>{gap:+.2f} {gap_arrow} / {gap_pct:.2f}%</div>",
        unsafe_allow_html=True
    )

    if (gap > 0 and divergencia < 0) or (gap < 0 and divergencia > 0):
        st.markdown(
            f"<div style='text-align: right; color:red'>⚠️ <b>Gap descontado</b></div>",
            unsafe_allow_html=True
        )
    else:
        diver_color = "green" if divergencia_pct >= 0 else "red"
        st.markdown(
            f"<div style='text-align: right; color:{diver_color}'>{divergencia:+.2f} / {divergencia_pct:.2f}%</div>",
            unsafe_allow_html=True
        )

st.markdown("---")

# --- ENTRADA RECOMENDADA ---
st.header("Entrada recomendada")

# Validación: RSI, Volumen, Cuerpo vela, Divergencia
RSI = 61
volumen = 2100
cuerpo_vela = 1.3
div_val = round(divergencia_pct, 2)

entrada_valida = (
    ((gap > 0 and divergencia > 0) or (gap < 0 and divergencia < 0)) and
    RSI > 55 and volumen > 2000 and cuerpo_vela >= 1.25 and abs(divergencia_pct) >= 0.10
)

if (gap > 0 and divergencia > 0) or (gap < 0 and divergencia < 0):
    if entrada_valida:
        if abs(divergencia_pct) >= 0.24:
            entrada_tipo = "🟢 Largo" if divergencia > 0 else "🔴 Corto"
            tp_sl = "+10 / -3"
        else:
            entrada_tipo = "🟡 Largo" if divergencia > 0 else "🟠 Corto"
            tp_sl = "+4 / -3"
        st.markdown(f"**Entrada**\n\n{entrada_tipo}")
        st.markdown(f"**TP / SL**\n\n{tp_sl}")
    else:
        st.markdown(f"<div style='color:gray'>⚠️ No hay entrada recomendada (divergencia insuficiente)</div>", unsafe_allow_html=True)
else:
    st.markdown(f"<div style='color:gray'>⚠️ No hay entrada recomendada (gap ya descontado)</div>", unsafe_allow_html=True)

# --- VALIDACIÓN EN TENDENCIA ---
with st.expander("Validación entrada en tendencia (1min)", expanded=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("**RSI (>55)**")
        st.markdown("**Volumen (>2000)**")
        st.markdown("**Cuerpo vela (≥1.25)**")
        st.markdown("**Divergencia (≥0.10%)**")
    with col2:
        rsi_color = "green" if RSI > 55 else "red"
        vol_color = "green" if volumen > 2000 else "red"
        vela_color = "green" if cuerpo_vela >= 1.25 else "red"
        div_color = "green" if abs(div_val) >= 0.10 else "red"

        st.markdown(f"<div style='text-align: right; color:{rsi_color}'>{RSI}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: right; color:{vol_color}'>{volumen}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: right; color:{vela_color}'>{cuerpo_vela}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: right; color:{div_color}'>{div_val:.2f}</div>", unsafe_allow_html=True)
