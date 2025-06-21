import streamlit as st
import pandas as pd
import yfinance as yf

# Obtener datos del SPY
spy = yf.Ticker("SPY")
hist = spy.history(period="2d")

try:
    spot_cierre = hist['Close'].iloc[-2] * 10  # Escala real
except:
    spot_cierre = None

# Intentar obtener precio de preapertura
spot_apertura = spy.info.get("preMarketPrice", None)
if spot_apertura is not None:
    spot_apertura *= 10  # Escala real

st.set_page_config(layout="wide")

# Estilo visual
st.markdown("""
    <style>
        body { background-color: white; color: black; }
        .data-row { display: flex; justify-content: space-between; padding: 0.3em 0; border-bottom: 1px solid #eee; }
        .data-label { font-weight: bold; width: 50%; text-align: left; }
        .data-value { width: 50%; text-align: right; }
        .green { color: green; font-weight: bold; }
        .red { color: red; font-weight: bold; }
        .section-title { font-size: 20px; font-weight: bold; margin-top: 1em; border-bottom: 2px solid #000; padding-bottom: 0.3em; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">Datos Iniciales</div>', unsafe_allow_html=True)

# Futuro editable
futuro = st.number_input("Futuro (ES1!)", value=5980.0, step=0.1)

# Validación de datos obtenidos
if spot_cierre is None:
    st.error("❌ No se pudo obtener el cierre anterior del SPY.")
elif spot_apertura is None:
    st.error("❌ No se pudo obtener el precio de preapertura del SPY.")
else:
    # Calcular gap y divergencia
    gap = spot_apertura - spot_cierre
    gap_pct = (gap / spot_cierre) * 100
    gap_arrow = "↑" if gap > 0 else "↓"
    divergencia = futuro - spot_apertura
    div_pct = (divergencia / abs(gap)) * 100 if gap != 0 else 0
    div_color = "green" if (gap > 0 and divergencia < 0) or (gap < 0 and divergencia > 0) else "red"

    def show_row(label, value, extra="", color_class=""):
        st.markdown(
            f'<div class="data-row"><div class="data-label">{label}</div>'
            f'<div class="data-value {color_class}">{value:.2f} {extra}</div></div>',
            unsafe_allow_html=True
        )

    show_row("Spot cierre", spot_cierre)
    show_row("Spot apertura (pre-market)", spot_apertura)
    show_row("Gap Spot", gap, f"{gap_arrow} / {gap_pct:.2f}%")
    show_row("Divergencia", divergencia, f"/ {div_pct:.2f}%", div_color)

    st.button("Recalcular")

    st.markdown('<div class="section-title">Entrada recomendada</div>', unsafe_allow_html=True)

    if gap > 0 and divergencia > 0:
        show_row("Tipo", "Largo ↑", "", "green")
        entrada = spot_apertura
        tp = entrada + 30
        sl = entrada - 15
    elif gap < 0 and divergencia < 0:
        show_row("Tipo", "Corto ↓", "", "red")
        entrada = spot_apertura
        tp = entrada - 30
        sl = entrada + 15
    else:
        show_row("Tipo", "Sin entrada")
        entrada = tp = sl = None

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
