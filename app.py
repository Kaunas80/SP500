import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

st.set_page_config(page_title="Estrategia SP500", layout="centered", page_icon="📈")

st.markdown(
    """
    <style>
        body {
            background-color: white;
            color: black;
        }
        .stButton > button {
            background-color: #0066ff;
            color: white;
            border: none;
            padding: 8px 16px;
            font-weight: bold;
            margin-top: 10px;
        }
        .stButton > button:hover {
            background-color: #0051cc;
        }
        .metric-container {
            font-weight: bold;
        }
        .verde {
            color: green;
        }
        .rojo {
            color: red;
        }
        .alineado-derecha {
            text-align: right !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("## Datos Iniciales")

# =====================
# DATOS INICIALES
# =====================
hoy = datetime.now()
ayer = hoy - timedelta(days=1)
datos_spy = yf.download('SPY', start=ayer, end=hoy, interval='1d')

spot_cierre = round(datos_spy['Close'].iloc[-1] * 10, 2)
spot_apertura = round(datos_spy['Open'].iloc[-1] * 10, 2)
valor_defecto_futuro = float(spot_apertura)

col1, col2, col3 = st.columns(3)
with col1:
    st.write("Spot cierre")
    st.write(f"<p class='alineado-derecha'>{spot_cierre}</p>", unsafe_allow_html=True)
with col2:
    st.write("Spot apertura")
    st.write(f"<p class='alineado-derecha'>{spot_apertura}</p>", unsafe_allow_html=True)
with col3:
    futuro = st.number_input("Futuro (ES1!)", value=valor_defecto_futuro, step=0.25)

# Cálculo GAP y DIVERGENCIA
gap = round((spot_apertura - spot_cierre), 2)
gap_pct = round((gap / spot_cierre) * 100, 2)

divergencia = round((futuro - spot_apertura), 2)
div_pct = round((divergencia / spot_apertura) * 100, 2)

gap_color = "verde" if gap > 0 else "rojo"
div_color = "verde" if (gap > 0 and futuro > spot_apertura) or (gap < 0 and futuro < spot_apertura) else "rojo"

st.markdown(f"**Gap Spot:** <span class='{gap_color}'>+{gap} pt ({gap_pct}%)</span>" if gap > 0 else f"**Gap Spot:** <span class='{gap_color}'>{gap} pt ({gap_pct}%)</span>", unsafe_allow_html=True)
st.markdown(f"**Divergencia:** <span class='{div_color}'>+{divergencia} pt ({div_pct}%)</span>" if divergencia > 0 else f"**Divergencia:** <span class='{div_color}'>{divergencia} pt ({div_pct}%)</span>", unsafe_allow_html=True)

st.button("Recalcular", type="primary")

# =====================
# ENTRADA RECOMENDADA
# =====================
st.markdown("## Entrada recomendada")

entrada = round((spot_apertura + futuro) / 2, 2)
tp = round(entrada + 5, 2)
sl = round(entrada - 5, 2)

tipo_entrada = "largo" if futuro > spot_apertura else "corto"
color_entrada = "verde" if tipo_entrada == "largo" else "rojo"
flecha = "⬆️" if tipo_entrada == "largo" else "⬇️"
texto = "Entrada en largo" if tipo_entrada == "largo" else "Entrada en corto"

st.markdown(f"<h4 class='{color_entrada}'>{flecha} {texto}</h4>", unsafe_allow_html=True)
st.write(f"TP: {tp}")
st.write(f"SL: {sl}")

# =====================
# VALIDACIÓN EN TENDENCIA
# =====================
with st.expander("Validación entrada en tendencia (1min)"):
    rsi = 61
    volumen = 2700
    cuerpo_vela = 1.85
    impulso = 2.2
    retroceso = -0.8

    data = {
        "Condición": ["RSI ≥ 55", "Volumen ≥ 2000", "Cuerpo vela ≥ 1.25 pt", "Impulso ≥ 2.0 pt", "Retroceso ≤ -1.0 pt"],
        "Valor actual": [rsi, volumen, cuerpo_vela, impulso, retroceso]
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

# =====================
# TP EXTENDIDO
# =====================
with st.expander("Condiciones TP extendido"):
    st.write("Impulso ≥ 2 pt")
    st.write("Retroceso ≤ -0.5 pt")
    st.write("Volumen ≥ 2500")
    st.write(f"<p class='alineado-derecha'>({impulso})</p>", unsafe_allow_html=True)
    st.write(f"<p class='alineado-derecha'>({retroceso})</p>", unsafe_allow_html=True)
    st.write(f"<p class='alineado-derecha'>({volumen})</p>", unsafe_allow_html=True)

# =====================
# SL TRAILING
# =====================
with st.expander("Condiciones SL Trailing"):
    st.write("Diferencia desde entrada")
    avance = round(abs(futuro - entrada), 2)
    st.write(f"<p class='alineado-derecha'>{avance}</p>", unsafe_allow_html=True)

