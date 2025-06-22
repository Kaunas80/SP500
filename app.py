import streamlit as st
import yfinance as yf

st.markdown("## Datos Iniciales")

# Obtener datos del SPY desde yfinance
try:
    spy = yf.Ticker("SPY")
    hist = spy.history(period="7d")

    spot_cierre = hist['Close'].dropna().iloc[-1] * 10
    spot_apertura_series = hist['Open'].dropna()
    spot_apertura = spot_apertura_series[spot_apertura_series != (spot_cierre / 10)].iloc[-1] * 10
    error_spy = False
except Exception:
    spot_cierre = None
    spot_apertura = None
    error_spy = True

# Entrada manual si falla la lectura
if error_spy:
    st.error("❌ No se pudo obtener el precio de preapertura del SPY.")
    spot_cierre = st.number_input("Spot cierre (manual)", value=0.0, step=1.0, format="%.2f")
    spot_apertura = st.number_input("Spot apertura (manual)", value=0.0, step=1.0, format="%.2f")

# Entrada manual del Futuro (siempre)
futuro = st.number_input("Futuro (ES1!)", value=0.0, step=1.0, format="%.2f")

# Mostrar datos solo si están disponibles
if spot_cierre and spot_apertura:

    # Calcular Gap
    gap = spot_apertura - spot_cierre
    gap_pct = (gap / spot_cierre) * 100
    gap_color = "green" if gap > 0 else "red"
    flecha = "↑" if gap > 0 else "↓"
    flecha_coloreada = f"<span style='color:{gap_color}'>{flecha}</span>"
    gap_txt = f"{gap:,.2f} {flecha_coloreada} / {abs(gap_pct):.2f}%"

    # Calcular Divergencia
    divergencia = spot_apertura - futuro
    divergencia_pct = (divergencia / spot_apertura) * 100
    div_color = "green" if (gap > 0 and divergencia > 0) or (gap < 0 and divergencia < 0) else "red"
    div_txt = f"<span style='color:{div_color}'>{divergencia:,.2f} / {abs(divergencia_pct):.2f}%</span>"

    # Mostrar en formato tabla
    def fila(nombre, valor_html):
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown(f"<div style='text-align: left;'>{nombre}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div style='text-align: right;'>{valor_html}</div>", unsafe_allow_html=True)

    fila("Spot cierre", f"{spot_cierre:,.2f}")
    fila("Spot apertura", f"{spot_apertura:,.2f}")
    fila("Gap Spot", gap_txt)
    fila("Divergencia", div_txt)

# ----------------------------------------------
# BLOQUE ENTRADA RECOMENDADA (a continuación)
# ----------------------------------------------

# Simulamos valores límite y valores actuales para validaciones
rsi_valor = 61
rsi_limite = 55

volumen_valor = 1.8
volumen_limite = 1.5

impulso_valor = 0.35
impulso_limite = 0.30

trailing_valor = 5960
trailing_limite = 5955

# --- Estilo y Layout ---
st.markdown("### Entrada recomendada")
col1, col2 = st.columns([1, 3])

# Entrada sugerida
with col1:
    st.write("**Entrada**")
with col2:
    entrada_tipo = "Largo"
    entrada_color = "green" if entrada_tipo == "Largo" else "red"
    entrada_icono = "⬆️" if entrada_tipo == "Largo" else "⬇️"
    st.markdown(f"<div style='text-align:right; color:{entrada_color}; font-weight:bold'>{entrada_icono} {entrada_tipo}</div>", unsafe_allow_html=True)

# TP y SL
col1, col2 = st.columns([1, 3])
with col1:
    st.write("TP / SL")
with col2:
    st.markdown(f"<div style='text-align:right'>6000 / 5940</div>", unsafe_allow_html=True)

# Validación en tendencia (desplegable)
with st.expander("Validación entrada en tendencia (1min)"):
    def render_validacion(nombre, limite, actual):
        color = "green" if actual >= limite else "red"
        alineado = f"<div style='display: flex; justify-content: space-between;'><span>{nombre} ({limite})</span><span style='color:{color}'>{actual}</span></div>"
        st.markdown(alineado, unsafe_allow_html=True)

    render_validacion("RSI", rsi_limite, rsi_valor)
    render_validacion("Volumen", volumen_limite, volumen_valor)
    render_validacion("Impulso", impulso_limite, impulso_valor)

# Validación SL Trailing
with st.expander("Condiciones SL Trailing"):
    render_validacion("Valor mínimo admisible", trailing_limite, trailing_valor)

# Validación TP Extendido
with st.expander("Condiciones TP Extendido"):
    render_validacion("Impulso mínimo", impulso_limite, impulso_valor)
    render_validacion("RSI mínimo", rsi_limite, rsi_valor)
