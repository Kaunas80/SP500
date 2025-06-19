import streamlit as st
import pandas as pd

st.set_page_config(page_title="Estrategia SP500", layout="wide")

# ==================
# ENTRADA DE DATOS
# ==================
st.title("📈 App de Estrategia SP500")

st.subheader("Datos Iniciales")
col1, col2, col3 = st.columns(3)

with col1:
    cierre_spot = st.number_input("📉 Spot cierre anterior", value=533.10)
with col2:
    apertura_spot = st.number_input("📈 Spot apertura", value=534.40)
with col3:
    futuro = st.number_input("📊 Cotización del futuro (ES1!)", value=535.00)

# ==================
# CÁLCULO GAP Y DIVERGENCIA
# ==================
gap = (apertura_spot - cierre_spot) / cierre_spot * 100
divergencia = (futuro - apertura_spot) / apertura_spot * 100

st.markdown("---")
st.subheader("📊 Cálculo GAP & Divergencia")
st.write(f"**Gap Spot**: {gap:.2f}%")
st.write(f"**Divergencia**: {divergencia:.2f}%")

# ==================
# BLOQUE VALIDACIÓN ENTRADA
# ==================
st.markdown("---")
st.subheader("✅ Validación entrada en tendencia (1min)")

rsi_valor = 57.0
volumen_valor = 2700
vela_valor = 1.85
impulso_valor = 2.10
retroceso_valor = -0.70

data_validacion = {
    "Condición": ["RSI > 55", "Volumen ≥ 2000", "Cuerpo vela ≥ 1.25 pt", "Impulso ≥ 2.00 pt", "Retroceso ≤ -1.00 pt"],
    "Valor": [rsi_valor, volumen_valor, vela_valor, impulso_valor, retroceso_valor]
}
df_validacion = pd.DataFrame(data_validacion)
st.dataframe(df_validacion, use_container_width=True)

# ==================
# ENTRADA RECOMENDADA + TP/SL
# ==================
st.markdown("---")
st.subheader("📌 Entrada recomendada")
entrada = apertura_spot
tp = entrada + 5.5
sl = entrada - 3.5
st.write(f"**Entrada**: {entrada:.2f}")
st.write(f"**TP**: {tp:.2f}")
st.write(f"**SL**: {sl:.2f}")

# ==================
# TP EXTENDIDO
# ==================
st.markdown("---")
with st.expander("🎯 Condiciones TP Extendido"):
    tp_ext_data = {
        "Condición": ["RSI > 60", "Volumen > 2500", "Cuerpo vela ≥ 1.25 pt", "Gap Spot ≥ 0.24%", "Divergencia ≥ 0.10%", "Impulso ≥ 2.00 pt", "Retroceso ≤ -1.00 pt"],
        "Valor": [61, 2700, 1.85, gap, divergencia, impulso_valor, retroceso_valor]
    }
    df_tp_ext = pd.DataFrame(tp_ext_data)
    st.dataframe(df_tp_ext, use_container_width=True)

# ==================
# SL TRAILING
# ==================
st.markdown("---")
with st.expander("🛡 Condiciones SL Trailing"):
    avance = 2.20
    rsi_trail = 58
    volumen_trail = 2600
    sl_trail_data = {
        "Condición": ["Avance ≥ 2.0 pt", "RSI > 55", "Volumen > 2000"],
        "Valor": [avance, rsi_trail, volumen_trail]
    }
    df_trail = pd.DataFrame(sl_trail_data)
    st.dataframe(df_trail, use_container_width=True)

# ==================
# RECALCULAR MANUAL
# ==================
st.markdown("---")
st.button("🔄 Recalcular ahora")
