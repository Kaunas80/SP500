import streamlit as st
import yfinance as yf

st.set_page_config(layout="centered", page_title="Estrategia SP500")

st.markdown(
    """
    <style>
        body { background-color: white; color: black; }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        div[data-testid="stNumberInput"] input {
            text-align: right;
        }
        div[data-testid="metric-container"] {
            text-align: right;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Datos Iniciales")

# Función para obtener el valor de cierre anterior del SPY
def obtener_cierre_spy():
    try:
        spy = yf.Ticker("SPY")
        hist = spy.history(period="2d")
        return round(hist["Close"].iloc[-1] * 10, 2)
    except Exception:
        return None

# Función para obtener el valor de preapertura del SPY
def obtener_preapertura_spy():
    try:
        spy = yf.Ticker("SPY")
        premarket = spy.info.get("preMarketPrice")
        if premarket:
            return round(premarket * 10, 2)
    except Exception:
        return None

# Obtener valores automáticos
spot_cierre = obtener_cierre_spy()
spot_apertura = obtener_preapertura_spy()

# Mostrar valores o entrada manual si falla la lectura
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if spot_cierre:
        st.markdown("**Spot cierre**")
        st.write(f"{spot_cierre:,.2f}")
    else:
        spot_cierre = st.number_input("Spot cierre", format="%.2f")

with col2:
    if spot_apertura:
        st.markdown("**Spot apertura**")
        st.write(f"{spot_apertura:,.2f}")
    else:
        spot_apertura = st.number_input("Spot apertura (manual)", format="%.2f")

with col3:
    futuro = st.number_input("Futuro (ES1!)", format="%.2f", value=5980.00)

# Si los valores están disponibles, hacer cálculos
if spot_cierre and spot_apertura:
    spot_cierre = float(spot_cierre)
    spot_apertura = float(spot_apertura)
    gap = spot_apertura - spot_cierre
    gap_pct = (gap / spot_apertura) * 100 if spot_apertura else 0

    divergencia = futuro - spot_apertura
    divergencia_pct = (divergencia / abs(gap)) * 100 if gap != 0 else 0

    # Dirección del gap
    flecha = "↑" if gap > 0 else "↓"
    gap_str = f"{gap:,.2f} {flecha} / {gap_pct:.2f}%"

    # Color para divergencia
    gap_alcista = gap > 0
    diver_verde = (gap_alcista and divergencia < 0) or (not gap_alcista and divergencia > 0)
    color_div = "green" if diver_verde else "red"
    diver_str = f"<span style='color:{color_div}'>{divergencia:,.2f} / {divergencia_pct:.2f}%</span>"

    # Mostrar resultados
    st.markdown("---")
    st.markdown("**Spot apertura (calculado)**")
    st.write(f"{spot_apertura:,.2f}")

    st.markdown("**Gap Spot**")
    st.write(gap_str)

    st.markdown("**Divergencia**", unsafe_allow_html=True)
    st.markdown(diver_str, unsafe_allow_html=True)

    st.button("Recalcular")
