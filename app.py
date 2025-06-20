import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Estrategia SP500", layout="centered")

# ==========================
# DATOS INICIALES
# ==========================

st.markdown("## Datos Iniciales")

# Obtener datos del SPY
hoy = datetime.now()
ayer = hoy - timedelta(days=1)

datos_spy = yf.download('SPY', start=ayer, end=hoy, interval='1d')

spot_cierre = round(datos_spy['Close'].iloc[-1] * 10, 2) if not datos_spy['Close'].empty else 0.0
spot_apertura = round(datos_spy['Open'].iloc[-1] * 10, 2) if not datos_spy['Open'].empty else 0.0
valor_defecto_futuro = spot_apertura if spot_apertura != 0 else 5340.0

futuro = st.number_input("Futuro (ES1!)", value=valor_defecto_futuro, step=0.25)

# Calcular GAP y Divergencia
gap_abs = futuro - spot_cierre
gap_pct = round(((futuro - spot_cierre) / spot_cierre) * 100, 2) if spot_cierre else 0.0
gap_color = "green" if gap_abs > 0 else "red"

descontado = (futuro - spot_apertura) if gap_abs > 0 else (spot_apertura - futuro)
queda_por_recorrer = abs(gap_abs) > abs(descontado)
divergencia_color = "green" if queda_por_recorrer else "red"
divergencia_abs = round(futuro - spot_apertura, 2)
divergencia_pct = round(((futuro - spot_apertura) / spot_apertura) * 100, 2) if spot_apertura else 0.0

# Mostrar bloque alineado
st.markdown(f"""
<style>
    div[data-testid="stVerticalBlock"] > div {{
        background-color: white;
        color: black;
        padding: 1rem;
        border-radius: 10px;
    }}
    .stNumberInput > div {{
        display: flex;
        justify-content: flex-end;
    }}
    .valor {{
        float: right;
        font-weight: bold;
    }}
</style>
""", unsafe_allow_html=True)

st.write(f"<div><b>Spot cierre:</b> <span class='valor'>{spot_cierre}</span></div>", unsafe_allow_html=True)
st.write(f"<div><b>Spot apertura:</b> <span class='valor'>{spot_apertura}</span></div>", unsafe_allow_html=True)
st.write(f"<div><b>Futuro (ES1!):</b> <span class='valor'>{futuro}</span></div>", unsafe_allow_html=True)

gap_html = f"<span style='color:{gap_color}'>{gap_abs:+.2f} pt ({gap_pct:+.2f}%)</span>"
st.write(f"<div><b>Gap Spot:</b> <span class='valor'>{gap_html}</span></div>", unsafe_allow_html=True)

div_html = f"<span style='color:{divergencia_color}'>{divergencia_abs:+.2f} pt ({divergencia_pct:+.2f}%)</span>"
st.write(f"<div><b>Divergencia:</b> <span class='valor'>{div_html}</span></div>", unsafe_allow_html=True)

st.button("Recalcular")

# ==========================
# ENTRADA RECOMENDADA
# ==========================

st.markdown("## Entrada recomendada")

# Simulación de condiciones
es_largo = spot_apertura > spot_cierre
entrada = round((spot_apertura + spot_cierre) / 2, 2)
tp = entrada + 5 if es_largo else entrada - 5
sl = entrada - 3 if es_largo else entrada + 3
flecha = "↑" if es_largo else "↓"
color = "green" if es_largo else "red"
texto = "Entrada en largo" if es_largo else "Entrada en corto"

st.markdown(f"<h3 style='color:{color}'>{flecha} {texto}</h3>", unsafe_allow_html=True)
st.write(f"<b>TP:</b> {tp:.2f}")
st.write(f"<b>SL:</b> {sl:.2f}")

# ==========================
# VALIDACIÓN EN TENDENCIA
# ==========================

with st.expander("Validación entrada en tendencia (1min)"):
    condiciones = {
        "Condición": ["RSI ≥ 55", "Volumen ≥ 2000", "Cuerpo vela ≥ 1.25 pt"],
        "Valor actual": [61, 2700, 1.85]
    }
    st.dataframe(pd.DataFrame(condiciones), use_container_width=True)

# ==========================
# TP EXTENDIDO
# ==========================

with st.expander("Condiciones TP extendido"):
    condiciones_tp = {
        "Condición": ["Impulso ≥ 2 pt", "Retroceso ≤ -0.5 pt", "Volumen ≥ 2500"],
        "Valor actual": [2.2, -0.8, 2700]
    }
    st.dataframe(pd.DataFrame(condiciones_tp), use_container_width=True)

# ==========================
# SL TRAILING
# ==========================

with st.expander("Condiciones SL Trailing"):
    condiciones_sl = {
        "Condición": ["Diferencia desde entrada"],
        "Valor actual": [1.75]
    }
    st.dataframe(pd.DataFrame(condiciones_sl), use_container_width=True)
