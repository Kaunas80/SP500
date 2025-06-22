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

# Entrada sugerida (se determina en función del gap)
entrada_tipo = "Largo" if gap > 0 else "Corto"
entrada_color = "green" if entrada_tipo == "Largo" else "red"
entrada_icono = "⬆️" if entrada_tipo == "Largo" else "⬇️"

col1, col2 = st.columns([1, 3])
with col1:
    st.write("**Entrada**")
with col2:
    st.markdown(
        f"<div style='text-align:right; color:{entrada_color}; font-weight:bold'>{entrada_icono} {entrada_tipo}</div>",
        unsafe_allow_html=True)

# TP y SL mostrados solo como puntos, con signo
tp_puntos = 20
sl_puntos = 20
if entrada_tipo == "Largo":
    tp_valor = f"+{tp_puntos}"
    sl_valor = f"-{sl_puntos}"
else:
    tp_valor = f"-{tp_puntos}"
    sl_valor = f"+{sl_puntos}"

col1, col2 = st.columns([1, 3])
with col1:
    st.write("TP / SL")
with col2:
    st.markdown(f"<div style='text-align:right'>{tp_valor} / {sl_valor}</div>", unsafe_allow_html=True)

# -------- Validaciones --------

# Valores simulados
rsi_valor = 61
rsi_limite = 55

volumen_valor = 1.8
volumen_limite = 1.5

impulso_valor = 0.35
impulso_limite = 0.30

trailing_valor = 5960
trailing_limite = 5955

# Función para validación
def render_validacion(nombre, limite, actual):
    color = "green" if actual >= limite else "red"
    alineado = f"<div style='display: flex; justify-content: space-between;'><span>{nombre} ({limite})</span><span style='color:{color}'>{actual}</span></div>"
    st.markdown(alineado, unsafe_allow_html=True)

# Bloque desplegable: Validación en tendencia
with st.expander("Validación entrada en tendencia (1min)"):
    render_validacion("RSI", rsi_limite, rsi_valor)
    render_validacion("Volumen", volumen_limite, volumen_valor)
    render_validacion("Impulso", impulso_limite, impulso_valor)

# Bloque desplegable: SL Trailing
with st.expander("Condiciones SL Trailing"):
    render_validacion("Valor mínimo admisible", trailing_limite, trailing_valor)

# Bloque desplegable: TP Extendido
with st.expander("Condiciones TP Extendido"):
    render_validacion("Impulso mínimo", impulso_limite, impulso_valor)
    render_validacion("RSI mínimo", rsi_limite, rsi_valor)
