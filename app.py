import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Estrategia SP500", layout="centered")

# === ESTILO PERSONALIZADO ===
st.markdown("""
<style>
    .datos-grid {
        display: grid;
        grid-template-columns: 1fr auto;
        row-gap: 0.5rem;
        column-gap: 1rem;
        align-items: center;
        font-family: sans-serif;
    }
    .label {
        text-align: right;
        font-weight: 500;
    }
    .valor {
        text-align: right;
    }
    .valor-destacado {
        text-align: right;
        font-weight: bold;
    }
    .positivo {
        color: green;
        font-weight: bold;
    }
    .negativo {
        color: red;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("## Datos Iniciales")

# === DATOS AUTOMÁTICOS DEL SPY ===
try:
    spy = yf.Ticker("SPY")
    hist = spy.history(period="2d")
    spot_cierre = hist["Close"].iloc[-2] * 10
    spot_apertura = hist["Open"].iloc[-1] * 10
    spot_error = False
except:
    spot_cierre = None
    spot_apertura = None
    spot_error = True

# === ENTRADA MANUAL EN CASO DE ERROR ===
manual_spot_apertura = False
if spot_error:
    st.warning("⚠️ No se pudo obtener automáticamente el precio del SPY. Introduce los datos manualmente.")
    spot_cierre = st.number_input("Spot cierre (manual)", value=0.0, step=0.1, format="%.2f")
    spot_apertura = st.number_input("Spot apertura (manual)", value=0.0, step=0.1, format="%.2f")
    manual_spot_apertura = True

# === FUTURO ES1! ===
futuro = st.number_input("Futuro (ES1!)", value=5980.0, step=0.5, format="%.2f")

# === CÁLCULOS ===
gap = spot_apertura - spot_cierre
gap_pct = (gap / spot_cierre * 100) if spot_cierre else 0
divergencia = futuro - spot_apertura
divergencia_pct = (divergencia / abs(gap) * 100) if gap else 0

# === ESTILO GAP Y DIVERGENCIA ===
gap_flecha = "↑" if gap > 0 else "↓"
gap_color = "negativo" if gap < 0 else "positivo"
div_color = "positivo" if (
    (gap > 0 and futuro < spot_apertura) or (gap < 0 and futuro > spot_apertura)
) else "negativo"

# === PRESENTACIÓN DE DATOS ===
st.markdown("<div class='datos-grid'>", unsafe_allow_html=True)

st.markdown("<div class='label'>Spot cierre</div>", unsafe_allow_html=True)
st.markdown(f"<div class='valor-destacado'>{spot_cierre:,.2f}</div>", unsafe_allow_html=True)

st.markdown("<div class='label'>Spot apertura</div>", unsafe_allow_html=True)
st.markdown(f"<div class='valor-destacado'>{spot_apertura:,.2f}</div>", unsafe_allow_html=True)

st.markdown("<div class='label'>Gap Spot</div>", unsafe_allow_html=True)
st.markdown(
    f"<div class='{gap_color}'>{gap:,.2f} {gap_flecha} / {abs(gap_pct):.2f}%</div>",
    unsafe_allow_html=True
)

st.markdown("<div class='label'>Divergencia</div>", unsafe_allow_html=True)
st.markdown(
    f"<div class='{div_color}'>{divergencia:,.2f} / {abs(divergencia_pct):.2f}%</div>",
    unsafe_allow_html=True
)

st.markdown("</div>", unsafe_allow_html=True)
