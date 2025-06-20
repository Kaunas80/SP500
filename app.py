import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Estrategia SP500", layout="centered")

st.markdown("""
    <style>
        body {
            background-color: white;
            color: black;
        }
        .stButton>button {
            background-color: white;
            color: black;
            border: 1px solid #999;
            margin-top: 10px;
        }
        .valor-derecha {
            float: right;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# ========================
# DATOS INICIALES
# ========================
st.markdown("## Datos Iniciales")

# Descargar datos
hoy = datetime.now()
ayer = hoy - timedelta(days=1)
datos_spy = yf.download('SPY', start=ayer, end=hoy, interval='1d')

spot_cierre = round(datos_spy['Close'].iloc[-1] * 10, 2)
spot_apertura = round(datos_spy['Open'].iloc[-1] * 10, 2)

# Input editable
futuro = st.number_input("Futuro (ES1!)", value=round(spot_apertura, 1), step=0.25)

# Gap y Divergencia
gap = round(spot_apertura - spot_cierre, 2)
gap_pct = round((gap / spot_cierre) * 100, 2)

div = round(futuro - spot_apertura, 2)
div_pct = round((div / spot_apertura) * 100, 2)

# Mostrar tabla alineada
st.markdown(f"""
<div>
    <div>Spot cierre<span class="valor-derecha">{spot_cierre}</span></div>
    <div>Spot apertura<span class="valor-derecha">{spot_apertura}</span></div>
    <div>Futuro (ES1!)<span class="valor-derecha">{futuro}</span></div>
    <div>Gap Spot<span class="valor-derecha" style="color:{'green' if gap > 0 else 'red'};">{gap:+.2f} pt ({gap_pct:+.2f}%)</span></div>
    <div>Divergencia<span class="valor-derecha" style="color:{'green' if (gap > 0 and div > 0) or (gap < 0 and div < 0) else 'red'};">{div:+.2f} pt ({div_pct:+.2f}%)</span></div>
</div>
""", unsafe_allow_html=True)

# Botón recalcular
st.button("Recalcular")

# ========================
# ENTRADA RECOMENDADA
# ========================
st.markdown("## Entrada recomendada")

# Tipo de entrada
entrada = "compra" if div < 0 else "venta"
color = "green" if entrada == "compra" else "red"
flecha = "⬆️" if entrada == "compra" else "⬇️"

st.markdown(f"<h3 style='color:{color};'>{flecha} Entrada en {'largo' if entrada == 'compra' else 'corto'}</h3>", unsafe_allow_html=True)

# TP y SL
tp = futuro + 5 if entrada == "compra" else futuro - 10
sl = futuro - 5 if entrada == "compra" else futuro + 5

st.markdown(f"<div>TP<span class='valor-derecha'>{tp:.2f}</span></div>", unsafe_allow_html=True)
st.markdown(f"<div>SL<span class='valor-derecha'>{sl:.2f}</span></div>", unsafe_allow_html=True)

# ========================
# VALIDACIÓN EN TENDENCIA
# ========================
with st.expander("Validación entrada en tendencia (1min)"):
    data_validacion = {
        "Condición": ["RSI ≥ 55", "Volumen ≥ 2000", "Cuerpo vela ≥ 1.25 pt"],
        "Valor actual": [61, 2700, 1.85],
    }
    df_val = pd.DataFrame(data_validacion)
    st.dataframe(df_val, use_container_width=True)

# ========================
# TP EXTENDIDO
# ========================
with st.expander("Condiciones TP extendido"):
    df_tp_ext = pd.DataFrame({
        "Condición": ["Impulso ≥ 2 pt", "Retroceso ≤ -0.5 pt", "Volumen ≥ 2500"],
        "Valor actual": [2.2, -0.8, 2700],
    })
    st.dataframe(df_tp_ext, use_container_width=True)

# ========================
# SL TRAILING
# ========================
with st.expander("Condiciones SL Trailing"):
    df_trail = pd.DataFrame({
        "Condición": ["Diferencia desde entrada"],
        "Valor actual": [f"{abs(futuro - spot_apertura):+.2f} pt"],
    })
    st.dataframe(df_trail, use_container_width=True)

