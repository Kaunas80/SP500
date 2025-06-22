import streamlit as st

# --- BLOQUE 1: DATOS INICIALES (VERSIÓN APROBADA) ---
st.markdown("## Datos Iniciales")

col1, col2 = st.columns([1, 1])
with col1:
    spot_cierre = st.number_input("Spot cierre", value=0.0, format="%.2f")
with col2:
    spot_apertura = st.number_input("Spot apertura", value=0.0, format="%.2f")

futuro = st.number_input("Futuro (ES1!)", value=0.0, format="%.2f")

# Cálculo del GAP
gap = spot_apertura - spot_cierre
gap_pct = (gap / spot_cierre) * 100 if spot_cierre else 0
gap_color = "green" if gap > 0 else "red"
gap_flecha = "↑" if gap > 0 else "↓"

# Cálculo de Divergencia
divergencia = spot_apertura - futuro
divergencia_pct = (divergencia / spot_apertura) * 100 if spot_apertura else 0
divergencia_color = "green" if (gap > 0 and divergencia > 0) or (gap < 0 and divergencia < 0) else "red"

# Visualización tipo tabla
st.markdown(f"""
<div style="display: grid; grid-template-columns: 1fr 1fr; font-size: 18px;">
  <div style="text-align: left;">Spot cierre</div><div style="text-align: right;">{spot_cierre:,.2f}</div>
  <div style="text-align: left;">Spot apertura</div><div style="text-align: right;">{spot_apertura:,.2f}</div>
  <div style="text-align: left;">Gap Spot</div><div style="text-align: right; color:{gap_color};">{gap:,.2f} {gap_flecha} / {abs(gap_pct):.2f}%</div>
  <div style="text-align: left;">Divergencia</div><div style="text-align: right; color:{divergencia_color};">{divergencia:,.2f} / {abs(divergencia_pct):.2f}%</div>
</div>
""", unsafe_allow_html=True)


# --- BLOQUE 2: ENTRADA RECOMENDADA ---
st.markdown("## Entrada recomendada")

# Simulación de valores técnicos (serán automáticos más adelante)
rsi_valor = 61
volumen_valor = 2100
cuerpo_vela_valor = 1.30

# Reglas de validación de tendencia
valida_rsi = rsi_valor > 55
valida_volumen = volumen_valor > 2000
valida_cuerpo = cuerpo_vela_valor >= 1.25
valida_div = abs(divergencia_pct) >= 0.10

entrada_valida = valida_rsi and valida_volumen and valida_cuerpo and valida_div

# Reglas de TP / SL
div_extendida = abs(divergencia_pct) >= 0.24
tp = 10 if div_extendida else 4
sl = 3

# Tipo de entrada
entrada_tipo = "Largo" if divergencia > 0 else "Corto"
entrada_color = "green" if entrada_valida and div_extendida else ("orange" if entrada_valida else "gray")
entrada_icono = "⬆️" if entrada_tipo == "Largo" else "⬇️"

# Entrada visual
col1, col2 = st.columns([1, 3])
with col1:
    st.write("**Entrada**")
with col2:
    st.markdown(f"<div style='text-align:right; color:{entrada_color}; font-weight:bold'>{entrada_icono} {entrada_tipo}</div>", unsafe_allow_html=True)

# TP / SL
col1, col2 = st.columns([1, 3])
with col1:
    st.write("TP / SL")
with col2:
    st.markdown(f"<div style='text-align:right'>+{tp} / -{sl}</div>", unsafe_allow_html=True)

# Validación entrada en tendencia
with st.expander("Validación entrada en tendencia (1min)"):
    def validar(nombre, limite, actual, condicion):
        color = "green" if condicion else "red"
        st.markdown(
            f"<div style='display: flex; justify-content: space-between;'><span>{nombre}</span><span style='color:{color}'>{actual}</span></div>",
            unsafe_allow_html=True)

    validar("RSI (>55)", 55, rsi_valor, valida_rsi)
    validar("Volumen (>2000)", 2000, volumen_valor, valida_volumen)
    validar("Cuerpo vela (≥1.25)", 1.25, cuerpo_vela_valor, valida_cuerpo)
    validar("Divergencia (≥0.10%)", 0.10, abs(divergencia_pct), valida_div)

# SL Trailing
with st.expander("Condiciones SL Trailing"):
    validar("Valor mínimo admisible", 5955, 5960, True)  # Simulado

# TP Extendido
with st.expander("Condiciones TP Extendido"):
    validar("Impulso mínimo", 0.30, 0.35, True)
    validar("RSI mínimo", 55, rsi_valor, True)
