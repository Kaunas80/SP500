# ========================
# DATOS INICIALES
# ========================

st.markdown("## Datos Iniciales")

# Descargar datos del SPY
import yfinance as yf
import datetime

hoy = datetime.datetime.now()
ayer = hoy - datetime.timedelta(days=1)
datos_spy = yf.download('SPY', start=ayer, end=hoy, interval='1d')

spot_cierre = round(datos_spy['Close'].iloc[-1] * 10, 2)
spot_apertura = round(datos_spy['Open'].iloc[-1] * 10, 2)

col1, col2 = st.columns([2, 1])
with col1:
    st.write("Spot cierre")
with col2:
    st.write(f"{spot_cierre:,.2f}")

col1, col2 = st.columns([2, 1])
with col1:
    st.write("Spot apertura")
with col2:
    st.write(f"{spot_apertura:,.2f}")

col1, col2 = st.columns([2, 1])
with col1:
    futuro = st.number_input("Futuro (ES1!)", value=5345.0, step=0.25)
with col2:
    st.write("")

# Calcular Gap y Divergencia
gap_abs = round(spot_apertura - spot_cierre, 2)
gap_pct = round((gap_abs / spot_cierre) * 100, 2)
div_abs = round(futuro - spot_apertura, 2)
div_pct = round((div_abs / spot_apertura) * 100, 2)

# Mostrar Gap Spot
col1, col2 = st.columns([2, 1])
with col1:
    st.write("Gap Spot")
with col2:
    gap_color = "green" if gap_abs > 0 else "red"
    st.markdown(f"<div style='text-align:right; color:{gap_color}'>{gap_abs:+.2f} pt ({gap_pct:+.2f}%)</div>", unsafe_allow_html=True)

# Mostrar Divergencia
col1, col2 = st.columns([2, 1])
with col1:
    st.write("Divergencia")
with col2:
    div_color = "green" if (gap_abs > 0 and futuro > spot_apertura) or (gap_abs < 0 and futuro < spot_apertura) else "red"
    st.markdown(f"<div style='text-align:right; color:{div_color}'>{div_abs:+.2f} pt ({div_pct:+.2f}%)</div>", unsafe_allow_html=True)

# Botón al final
st.button("Recalcular")


