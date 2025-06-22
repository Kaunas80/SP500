import streamlit as st

st.set_page_config(layout="wide")

st.markdown("<h1 style='font-size: 36px;'>Datos Iniciales</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    spot_cierre = st.number_input("Spot cierre", value=5956.79, step=0.1, format="%.2f")
with col2:
    spot_apertura = st.number_input("Spot apertura", value=5983.80, step=0.1, format="%.2f")

futuro = st.number_input("Futuro (ES1!)", value=0.00, step=0.1, format="%.2f")

gap = round(spot_apertura - spot_cierre, 2)
gap_pct = round((gap / spot_cierre) * 100, 2)

divergencia = round(spot_apertura - futuro, 2)
divergencia_pct = round((abs(divergencia) / spot_apertura) * 100, 2) if futuro != 0 else None

# Mostrar tabla estilo validado
st.markdown(
    f"""
    <div style="display: grid; grid-template-columns: 1fr auto; gap: 0.25rem 1rem; font-size: 18px;">
        <div><b>Spot apertura</b></div><div style="text-align: right;">{spot_apertura:,.2f}</div>
        <div><b>Gap Spot</b></div>
        <div style="text-align: right; color: {'green' if gap != 0 else 'white'};">
            {gap:+.2f} ↑ / {gap_pct:+.2f}%
        </div>
        <div><b>Divergencia</b></div>
        <div style="text-align: right; color: {'green' if (gap > 0 and divergencia < 0) or (gap < 0 and divergencia > 0) else 'red'};">
            {f"{divergencia:,.2f} / {divergencia_pct:.2f}%" if futuro != 0 else '-- / --'}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")
st.markdown("<h1 style='font-size: 36px;'>Entrada recomendada</h1>", unsafe_allow_html=True)

# Determinar entrada recomendada
entrada = ""
if futuro == 0:
    entrada = "⚠️ Falta dato del Futuro"
else:
    if (gap > 0 and divergencia < 0) or (gap < 0 and divergencia > 0):
        entrada = "⚠️ Gap descontado"
    elif abs(divergencia_pct) < 0.10:
        entrada = "⚠️ No hay entrada recomendada (divergencia insuficiente)"
    else:
        if gap > 0:
            entrada = "<span style='color: green;'>⬆️ <b style=\"font-size: 24px;\">Largo</b></span>"
        else:
            entrada = "<span style='color: red;'>⬇️ <b style=\"font-size: 24px;\">Corto</b></span>"

# Mostrar entrada
st.markdown(f"<div style='text-align: right; font-size: 20px;'>{entrada}</div>", unsafe_allow_html=True)

# Calcular TP y SL
if "Largo" in entrada or "Corto" in entrada:
    tp, sl = ("+4", "-3") if entrada == "<span style='color: green;'>⬆️ <b style=\"font-size: 24px;\">Largo</b></span>" else ("-4", "+3")
    if abs(divergencia_pct) >= 0.24:
        tp = "+10" if "Largo" in entrada else "-10"
    st.markdown(
        f"<div style='text-align: right; font-size: 18px;'>TP / SL: <b>{tp}</b> / <b>{sl}</b></div>",
        unsafe_allow_html=True,
    )
