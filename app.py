import streamlit as st
import pandas as pd

# Precios de preapertura (temporales)
precios_preapertura = {
    'AAPL': 210.5,
    'MSFT': 445.8,
    'AMZN': 132.4,
    'NVDA': 122.3,
    'GOOGL': 165.1,
    'META': 123.7,
    'TSLA': 190.2,
    'BRK.B': 361.3,
    'UNH': 518.4,
    'JPM': 198.5,
    'JNJ': 156.4,
    'V': 270.3,
    'XOM': 112.9,
    'PG': 166.8,
    'MA': 437.2
}

pesos = {
    'AAPL': 0.072,
    'MSFT': 0.069,
    'AMZN': 0.052,
    'NVDA': 0.045,
    'GOOGL': 0.035,
    'META': 0.031,
    'TSLA': 0.030,
    'BRK.B': 0.025,
    'UNH': 0.022,
    'JPM': 0.021,
    'JNJ': 0.020,
    'V': 0.019,
    'XOM': 0.018,
    'PG': 0.018,
    'MA': 0.017
}

st.set_page_config(layout="wide")

st.markdown("""
    <style>
        body { background-color: white; color: black; }
        .data-row { display: flex; justify-content: space-between; padding: 0.3em 0; border-bottom: 1px solid #eee; }
        .data-label { font-weight: bold; width: 50%; text-align: left; }
        .data-value { width: 50%; text-align: right; }
        .green { color: green; font-weight: bold; }
        .red { color: red; font-weight: bold; }
        .section-title { font-size: 20px; font-weight: bold; margin-top: 1em; border-bottom: 2px solid #000; padding-bottom: 0.3em; }
        input[type=number] {
            text-align: right;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">Datos Iniciales</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    spot_cierre = st.number_input("Spot cierre", value=547.0, step=0.1)
with col2:
    futuro = st.number_input("Futuro (ES1!)", value=546.5, step=0.1)

# Cálculo automático del Spot apertura
spot_apertura = sum(precios_preapertura[ticker] * pesos[ticker] for ticker in precios_preapertura)

# Asegurar escalares y multiplicar ×10
if isinstance(spot_cierre, pd.Series):
    spot_cierre = spot_cierre.item()
if isinstance(spot_apertura, pd.Series):
    spot_apertura = spot_apertura.item()
if isinstance(futuro, pd.Series):
    futuro = futuro.item()

spot_cierre = float(spot_cierre) * 10
spot_apertura = float(spot_apertura) * 10
futuro = float(futuro) * 10

# Cálculos
gap = spot_apertura - spot_cierre
divergencia = futuro - spot_apertura
gap_pct = (gap / spot_apertura) * 100
div_pct = (divergencia / spot_apertura) * 100

# Dirección del gap (↑ o ↓)
gap_arrow = "↑" if gap > 0 else "↓"

# Color corregido para divergencia
if (gap > 0 and divergencia < 0) or (gap < 0 and divergencia > 0):
    div_color = "green"
else:
    div_color = "red"

# Visualización
def show_row(label, value, extra="", color_class=""):
    st.markdown(
        f'<div class="data-row"><div class="data-label">{label}</div>'
        f'<div class="data-value {color_class}">{value:.2f} {extra}</div></div>',
        unsafe_allow_html=True
    )

show_row("Spot apertura (calculado)", spot_apertura)
show_row("Gap Spot", gap, f"{gap_arrow} / {gap_pct:.2f}%")
show_row("Divergencia", divergencia, f"/ {div_pct:.2f}%", div_color)

st.button("Recalcular")

# Entrada recomendada
st.markdown('<div class="section-title">Entrada recomendada</div>', unsafe_allow_html=True)

if gap > 0 and divergencia > 0:
    st.markdown('<div class="data-row"><div class="data-label">Tipo</div>'
                '<div class="data-value green">Largo ↑</div></div>', unsafe_allow_html=True)
    entrada = spot_apertura
    tp = entrada + 30
    sl = entrada - 15

elif gap < 0 and divergencia < 0:
    st.markdown('<div class="data-row"><div class="data-label">Tipo</div>'
                '<div class="data-value red">Corto ↓</div></div>', unsafe_allow_html=True)
    entrada = spot_apertura
    tp = entrada - 30
    sl = entrada + 15

else:
    entrada = tp = sl = None
    st.markdown('<div class="data-row"><div class="data-label">Tipo</div>'
                '<div class="data-value">Sin entrada</div></div>', unsafe_allow_html=True)

if entrada:
    show_row("Entrada", entrada)
    show_row("TP", tp)
    show_row("SL", sl)

    with st.expander("Validación entrada en tendencia (1min)"):
        show_row("RSI > 55", 60)
        show_row("Impulso > 0", 1.3)
        show_row("Volumen > 100%", 122)

        with st.expander("Condiciones TP Extendido"):
            show_row("Retroceso < 40%", 32)
            show_row("Volatilidad > 1.0", 1.18)

        with st.expander("Condiciones SL Trailing"):
            show_row("Velocidad > 0.5", 0.76)
            show_row("RSI se mantiene > 55", 61)
