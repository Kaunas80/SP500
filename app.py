import streamlit as st

# --- BLOQUE 1: DATOS INICIALES ---
st.markdown("## Datos Iniciales")

col1, col2 = st.columns([1, 1])
with col1:
    spot_cierre = st.number_input("Spot cierre", value=0.0, format="%.2f", step=0.25)
with col2:
    spot_apertura = st.number_input("Spot apertura", value=0.0, format="%.2f", step=0.25)

futuro = st.number_input("Futuro (ES1!)", value=0.0, format="%.2f", step=0.25)

# Gap Spot
gap = spot_apertura - spot_cierre
gap_pct = (gap / spot_cierre) * 100 if spot_cierre else 0
gap_icon = "↑" if gap > 0 else "↓" if gap < 0 else "-"
gap_color = "green" if gap != 0 else "lightgray"

# Divergencia
div_valor = spot_apertura - futuro
div_pct = (div_valor / spot_apertura) * 100 if spot_apertura else 0

# Color de divergencia: verde si el gap no se ha descontado, rojo si ya lo fue
if spot_apertura > spot_cierre:
    div_color = "green" if futuro < spot_apertura else "red"
elif spot_apertura < spot_cierre:
    div_color = "green" if futuro > spot_apertura else "red"
else:
    div_color = "gray"

# Mensaje adicional si el gap ya fue descontado
gap_descontado = (
    (spot_apertura > spot_cierre and futuro >= spot_apertura) or
    (spot_apertura < spot_cierre and futuro <= spot_apertura)
)

# Visualización tipo tabla
st.markdown(f"""
<div style="display: grid; grid-template-columns: 1fr 1fr; font-size: 18px;">
  <div style="text-align: left;">Spot cierre</div><div style="text-align: right;">{spot_cierre:,.2f}</div>
  <div style="text-align: left;">Spot apertura</div><div style="text-align: right;">{spot_apertura:,.2f}</div>
  <div style="text-align: left;">Gap Spot</div><div style="text-align: right; color:{gap_color};">{gap:,.2f} {gap_icon} / {abs(gap_pct):.2f}%</div>
  <div style="text-align: left;">Divergencia</div><div style="text-align: right; color:{div_color};">{div_valor:,.2f} / {abs(div_pct):.2f}%</div>
</div>
""", unsafe_allow_html=True)

if gap_descontado:
    st.markdown("<div style='text-align:right; color:red; font-weight:bold'>Gap descontado</div>", unsafe_allow_html=True)


# --- BLOQUE 2: ENTRADA RECOMENDADA ---
st.markdown("## Entrada recomendada")

# Simulaciones técnicas (pueden automatizarse luego)
rsi_valor = 61
volumen_valor = 2100
cuerpo_valor = 1.30

valida_rsi = rsi_valor > 55
valida_volumen = volumen_valor > 2000
valida_cuerpo = cuerpo_valor >= 1.25
valida_div = abs(div_pct) >= 0.10
gap_no_descontado = not gap_descontado

entrada_valida = all([valida_rsi, valida_volumen, valida_cuerpo, valida_div]) and gap_no_descontado

if gap_no_descontado:
    entrada_tipo = "Largo" if div_valor > 0 else "Corto"
    icono = "⬆️" if entrada_tipo == "Largo" else "⬇️"

    if abs(div_pct) >= 0.24:
        entrada_color = "green" if entrada_tipo == "Largo" else "red"
        tp = 10
        sl = 3
    else:
        entrada_color = "orange"
        tp = 4
        sl = 3
else:
    entrada_tipo = "No hay entrada recomendada (gap ya descontado)"
    icono = "⚠️"
    entrada_color = "lightgray"
    tp = None
    sl = None

# Mostrar entrada
col1, col2 = st.columns([1, 3])
with col1:
    st.write("**Entrada**")
with col2:
    st.markdown(f"<div style='text-align:right; color:{entrada_color}; font-weight:bold'>{icono} {entrada_tipo}</div>", unsafe_allow_html=True)

# TP/SL solo si hay entrada válida
if entrada_valida:
    col1, col2 = st.columns([1, 3])
    with col1:
        st.write("TP / SL")
    with col2:
        st.markdown(f"<div style='text-align:right'>+{tp} / -{sl}</div>", unsafe_allow_html=True)

# Validaciones
with st.expander("Validación entrada en tendencia (1min)"):
    def validar(nombre, limite, actual, cumple):
        color = "green" if cumple else "red"
        st.markdown(f"<div style='display:flex; justify-content:space-between;'><span>{nombre}</span><span style='color:{color}'>{actual}</span></div>", unsafe_allow_html=True)

    validar("RSI (>55)", 55, rsi_valor, valida_rsi)
    validar("Volumen (>2000)", 2000, volumen_valor, valida_volumen)
    validar("Cuerpo vela (≥1.25)", 1.25, cuerpo_valor, valida_cuerpo)
    validar("Divergencia (≥0.10%)", 0.10, round(abs(div_pct), 2), valida_div)

with st.expander("Condiciones SL Trailing"):
    validar("Valor mínimo admisible", 5955, 5960, True)

with st.expander("Condiciones TP Extendido"):
    validar("Impulso mínimo", 0.30, 0.35, True)
    validar("RSI mínimo", 55, rsi_valor, True)
