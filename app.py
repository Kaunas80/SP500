import streamlit as st
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="Estrategia SP500", layout="centered")

st.markdown("""
    <style>
        .data-row {
            display: flex;
            justify-content: space-between;
            border-bottom: 1px solid #eee;
            padding: 6px 0;
        }
        .data-label {
            flex: 1;
            text-align: right;
            font-weight: bold;
            padding-right: 10px;
        }
        .data-value {
            flex: 1;
            text-align: right;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("## Datos Iniciales")

# Obtener datos de SPY
def obtener_datos_spy():
    try:
        spy = yf.Ticker("SPY")
        df = spy.history(period="2d")
        cierre = df["Close"].iloc[-2] * 10
        preapertura = spy.info.get("preMarketPrice", None)
        if preapertura is not None:
            preapertura *= 10
        return round(cierre, 2), round(preapertura, 2) if preapertura else None
    except:
        return None, None

spot_cierre, spot_apertura = obtener_datos_spy()

# Entrada manual si falla lectura automática
if spot_cierre is None:
    spot_cierre = st.number_input("Spot cierre", value=0.0, step=1.0, format="%.2f")
if spot_apertura is None:
    spot_apertura = st.number_input("Spot apertura", value=0.0, step=1.0, format="%.2f")

# Futuro siempre manual
futuro = st.number_input("Futuro (ES1!)", value=5980.00, step=1.0, format="%.2f")

# Cálculos
if spot_cierre and spot_apertura:
    gap = round(spot_apertura - spot_cierre, 2)
    gap_pct = round((gap / spot_cierre) * 100, 2)
    gap_flecha = "↑" if gap > 0 else "↓"
    gap_texto = f"{gap:,.2f} {gap_flecha} / {abs(gap_pct):.2f}%"

    divergencia = round(futuro - spot_apertura, 2)
    divergencia_pct = round((divergencia / abs(gap)) * 100, 2) if gap != 0 else 0
    diver_color = "green" if (gap > 0 and divergencia < 0) or (gap < 0 and divergencia < 0) else "red"
    diver_texto = f"<span style='color:{diver_color}; font-weight:bold'>{divergencia:,.2f} / {abs(divergencia_pct):.2f}%</span>"

    # Mostrar bloque alineado como tabla
    st.markdown(f"""
        <div class="data-row"><div class="data-label">Spot cierre</div><div class="data-value">{spot_cierre:,.2f}</div></div>
        <div class="data-row"><div class="data-label">Spot apertura</div><div class="data-value">{spot_apertura:,.2f}</div></div>
        <div class="data-row"><div class="data-label">Futuro (ES1!)</div><div class="data-value">{futuro:,.2f}</div></div>
        <div class="data-row"><div class="data-label">Gap Spot</div><div class="data-value">{gap_texto}</div></div>
        <div class="data-row"><div class="data-label">Divergencia</div><div class="data-value">{diver_texto}</div></div>
    """, unsafe_allow_html=True)
