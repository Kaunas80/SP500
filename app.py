import streamlit as st
import yfinance as yf

st.set_page_config(layout="wide")

# ---------- BLOQUE 1: DATOS INICIALES ----------

st.markdown("## Datos Iniciales")

# Intentamos obtener datos automáticamente desde yfinance
try:
    spy = yf.Ticker("SPY")
    hist = spy.history(period="7d")

    spot_cierre_real = round(hist["Close"][-2] * 10, 2)
    spot_apertura_real = round(hist["Open"][-1] * 10, 2)

    spot_cierre = spot_cierre_real
    spot_apertura = spot_apertura_real
    error_yf = False
except:
    spot_cierre = st.number_input("Spot cierre (manual)", step=1.0, format="%.2f")
    spot_apertura = st.number_input("Spot apertura (manual)", step=1.0, format="%.2f")
    error_yf = True

futuro = st.number_input("Futuro (ES1!)", step=1.0, format="%.2f")

# Cálculo de GAP Spot y Divergencia
gap = spot_apertura - spot_cierre
gap_pct = (gap / spot_cierre) * 100 if spot_cierre else 0

divergencia = spot_apertura - futuro
divergencia_pct = (divergencia / spot_apertura) * 100 if spot_apertura else 0

# Colores y flechas
gap_color = "green" if gap > 0 else "red"
gap_flecha = "↑" if gap > 0 else "↓"

div_color = "green" if (gap > 0 and divergencia < 0) or (gap < 0 and divergencia > 0) else "red"

# Diseño tipo tabla
st.markdown("""
<style>
.valor-dato {float:right; font-weight:bold;}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style='display:flex; justify-content:space-between;'><span>Spot cierre</span><span class='valor-dato'>{spot_cierre:,.2f}</span></div>
<div style='display:flex; justify-content:space-between;'><span>Spot apertura</span><span class='valor-dato'>{spot_apertura:,.2f}</span></div>
<div style='display:flex; justify-content:space-between;'><span>Gap Spot</span>
<span class='valor-dato' style='color:{gap_color}'>{gap:,.2f} {gap_flecha} / {abs(gap_pct):.2f}%</span></div>
<div style='display:flex; justify-content:space-between;'><span>Divergencia</span>
<span class='valor-dato' style='color:{div_color}'>{divergencia:,.2f} / {abs(divergencia_pct):.2f}%</span></div>
""", unsafe_allow_html=True)

# ---------- BLOQUE 2: ENTRADA RECOMENDADA ----------

st.markdown("## Entrada recomendada")

# Valores simulados
rsi_valor = 61
volumen_valor = 2100
cuerpo_vela_valor = 1.35
divergencia_pct_abs = abs(divergencia_pct)

entrada_tipo = "Largo" if gap > 0 else "Corto"

# Validación condiciones
valida_rsi = (entrada_tipo == "Largo" and rsi_valor > 55) or (entrada_tipo == "Corto" and rsi_valor < 45)
valida_volumen = volumen_valor > 2000
valida_cuerpo = cuerpo_vela_valor >= 1.25
valida_divergencia = (divergencia_pct > 10 and entrada_tipo == "Largo") or (divergencia_pct < -10 and entrada_tipo == "Corto")

condiciones_base_ok = valida_rsi and valida_volumen and valida_cuerpo and valida_divergencia

# Color y TP/SL
if condiciones_base_ok:
    if (divergencia_pct > 24 and entrada_tipo == "Largo") or (divergencia_pct < -24 and entrada_tipo == "Corto"):
        color_recomendacion = "#2ecc71"  # Verde
        tp = 10
        sl = 3
    else:
        color_recomendacion = "#f1c40f"  # Mostaza
        tp = 4
        sl = 3
else:
    color_recomendacion = "grey"
    tp = None
    sl = None

# Mostrar entrada
col1, col2 = st.columns([1, 3])
with col1:
    st.write("**Entrada**")
with col2:
    if condiciones_base_ok:
        icono = "⬆️" if entrada_tipo == "Largo" else "⬇️"
        st.markdown(f"<div style='text-align:right; color:{color_recomendacion}; font-weight:bold'>{icono} {entrada_tipo}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='text-align:right; color:grey;'>Condiciones no cumplidas</div>", unsafe_allow_html=True)

# TP/SL
col1, col2 = st.columns([1, 3])
with col1:
    st.write("TP / SL")
with col2:
    if tp and sl:
        tp_str = f"+{tp}" if entrada_tipo == "Largo" else f"-{tp}"
        sl_str = f"-{sl}" if entrada_tipo == "Largo" else f"+{sl}"
        st.markdown(f"<div style='text-align:right'>{tp_str} / {sl_str}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='text-align:right'>–</div>", unsafe_allow_html=True)

# Validaciones
with st.expander("Validación entrada en tendencia (1min)"):
    def render_validacion(nombre, limite, actual, operador=">="):
        if operador == ">=":
            ok = actual >= limite
        elif operador == "<":
            ok = actual < limite
        else:
            ok = False
        color = "green" if ok else "red"
        st.markdown(f"<div style='display:flex; justify-content:space-between;'><span>{nombre} ({limite})</span><span style='color:{color}'>{actual}</span></div>", unsafe_allow_html=True)

    render_validacion("RSI", 55 if entrada_tipo == "Largo" else 45, rsi_valor, ">" if entrada_tipo == "Largo" else "<")
    render_validacion("Volumen", 2000, volumen_valor)
    render_validacion("Cuerpo vela", 1.25, cuerpo_vela_valor)
    render_validacion("Divergencia %", "10%", abs(divergencia_pct), ">")

with st.expander("Condiciones SL Trailing"):
    render_validacion("--", 0, 0)

with st.expander("Condiciones TP Extendido"):
    render_validacion("--", 0, 0)
