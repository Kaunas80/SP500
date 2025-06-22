import streamlit as st
import yfinance as yf

# --- CARGA AUTOMÁTICA DE DATOS DEL SPY ---
try:
    spy = yf.Ticker("SPY")
    hist = spy.history(period="7d")
    spot_cierre_auto = round(hist["Close"][-2] * 10, 2)
    spot_apertura_auto = round(hist["Open"][-1] * 10, 2)
    spy_error = False
except Exception:
    spot_cierre_auto = None
    spot_apertura_auto = None
    spy_error = True

# --- BLOQUE 1: DATOS INICIALES ---
st.markdown("## Datos Iniciales")

if spy_error:
    st.error("❌ No se pudo obtener el precio de preapertura del SPY.")

spot_cierre = st.number_input("Spot cierre (manual)", value=spot_cierre_auto or 0.0, step=1.0, format="%.2f")
spot_apertura = st.number_input("Spot apertura (manual)", value=spot_apertura_auto or 0.0, step=1.0, format="%.2f")
futuro = st.number_input("Futuro (ES1!)", value=0.0, step=1.0, format="%.2f")

# --- CÁLCULOS ---
gap = round(spot_apertura - spot_cierre, 2)
gap_pct = round((gap / spot_cierre) * 100, 2) if spot_cierre != 0 else 0.0

divergencia = round(spot_apertura - futuro, 2)
divergencia_pct = round((divergencia / spot_apertura) * 100, 2) if spot_apertura != 0 else 0.0

# --- VISUALIZACIÓN DEL BLOQUE ---
st.markdown(f"""
<div style='display: flex; justify-content: space-between;'>
  <span>Spot cierre</span><span style='text-align:right'>{spot_cierre:,.2f}</span>
</div>
<div style='display: flex; justify-content: space-between;'>
  <span>Spot apertura</span><span style='text-align:right'>{spot_apertura:,.2f}</span>
</div>
<div style='display: flex; justify-content: space-between;'>
  <span>Gap Spot</span>
  <span style='text-align:right; color:{"green" if gap > 0 else "red"}'>
    {gap:.2f} {"↑" if gap > 0 else "↓"} / {abs(gap_pct):.2f}%
  </span>
</div>
<div style='display: flex; justify-content: space-between;'>
  <span>Divergencia</span>
  <span style='text-align:right; color:{"green" if (gap > 0 and divergencia > 0) or (gap < 0 and divergencia < 0) else "red"}'>
    {divergencia:.2f} / {abs(divergencia_pct):.2f}%
  </span>
</div>
""", unsafe_allow_html=True)

# --- BLOQUE 2: ENTRADA RECOMENDADA ---
st.markdown("## Entrada recomendada")

# Tipo de entrada
entrada_tipo = "Largo" if gap > 0 else "Corto"
entrada_color = "green" if entrada_tipo == "Largo" else "red"
entrada_icono = "⬆️" if entrada_tipo == "Largo" else "⬇️"

# Determinar color mostaza o verde
if (divergencia_pct > 0.24 and entrada_tipo == "Largo") or (divergencia_pct < -0.24 and entrada_tipo == "Corto"):
    entrada_color = "#00cc00"  # verde
    tp_val, sl_val = 10, 3
elif (divergencia_pct > 0.10 and entrada_tipo == "Largo") or (divergencia_pct < -0.10 and entrada_tipo == "Corto"):
    entrada_color = "#e0aa00"  # mostaza
    tp_val, sl_val = 4, 3
else:
    entrada_color = "grey"
    tp_val, sl_val = 0, 0

# Mostrar Entrada
col1, col2 = st.columns([1, 3])
with col1:
    st.write("Entrada")
with col2:
    st.markdown(
        f"<div style='text-align:right; color:{entrada_color}; font-weight:bold'>{entrada_icono} {entrada_tipo}</div>",
        unsafe_allow_html=True,
    )

# Mostrar TP / SL como diferencia en puntos
col1, col2 = st.columns([1, 3])
with col1:
    st.write("TP / SL")
with col2:
    tp_str = f"+{tp_val}" if entrada_tipo == "Largo" else f"-{tp_val}"
    sl_str = f"-{sl_val}" if entrada_tipo == "Largo" else f"+{sl_val}"
    st.markdown(f"<div style='text-align:right'>{tp_str} / {sl_str}</div>", unsafe_allow_html=True)

# --- VALIDACIONES (simuladas por ahora) ---
with st.expander("Validación entrada en tendencia (1min)"):
    def render_validacion(nombre, limite, actual):
        color = "green" if actual >= limite else "red"
        st.markdown(
            f"<div style='display: flex; justify-content: space-between;'>"
            f"<span>{nombre} ({limite})</span><span style='color:{color}'>{actual}</span></div>",
            unsafe_allow_html=True)

    render_validacion("RSI", 55, 61)
    render_validacion("Volumen", 2000, 2800)
    render_validacion("Cuerpo vela", 1.25, 1.35)
    render_validacion("Divergencia", 0.10, abs(divergencia_pct))

# --- TP EXTENDIDO ---
with st.expander("Condiciones TP Extendido"):
    render_validacion("Impulso mínimo", 0.30, 0.38)
    render_validacion("RSI mínimo", 55, 61)

# --- SL TRAILING ---
with st.expander("Condiciones SL Trailing"):
    render_validacion("Valor mínimo admisible", 5955, spot_apertura)
