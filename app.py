import streamlit as st
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="Entrada SP500", layout="centered")

# --- Funciones ---
def get_spy_prices():
    spy = yf.Ticker("SPY")
    hist = spy.history(period="2d", interval="1d")
    close_spot = round(hist['Close'][-2] * 10, 2)
    open_spot = round(hist['Open'][-1] * 10, 2)
    return close_spot, open_spot

def calcular_gap_divergencia(spot_cierre, spot_apertura, futuro):
    gap_abs = spot_apertura - spot_cierre
    gap_pct = round((gap_abs / spot_cierre) * 100, 2)
    esperado = spot_cierre + gap_abs
    divergencia_abs = futuro - esperado
    divergencia_pct = round((divergencia_abs / spot_cierre) * 100, 2)
    return round(gap_abs,2), gap_pct, round(divergencia_abs,2), divergencia_pct

# --- Simulaciones de valores ---
rsi = 61
volumen = 2700
cuerpo_vela = 1.85
impulso = 2.2
retroceso = -0.8
punto_entrada = 540.00
precio_actual = 541.75
diferencia_trailing = round(precio_actual - punto_entrada, 2)

# --- Presentación de valores ---
def mostrar_fila(etiqueta, valor, color=None):
    col1, col2 = st.columns([1,1])
    with col1:
        st.markdown(f"<div style='text-align:left;'>{etiqueta}</div>", unsafe_allow_html=True)
    with col2:
        texto = f"<div style='text-align:right; color:{color};'>{valor}</div>" if color else f"<div style='text-align:right;'>{valor}</div>"
        st.markdown(texto, unsafe_allow_html=True)

# --- BLOQUE: DATOS INICIALES ---
st.markdown("## Datos Iniciales")

spot_cierre, spot_apertura = get_spy_prices()
futuro = st.number_input("Futuro (ES1!)", value=spot_apertura, step=0.25, label_visibility="collapsed")

gap_valor, gap_pct, div_valor, div_pct = calcular_gap_divergencia(spot_cierre, spot_apertura, futuro)

gap_color = "green" if gap_valor > 0 else "red"
div_color = "green" if (gap_valor > 0 and div_valor > 0) or (gap_valor < 0 and div_valor < 0) else "red"

mostrar_fila("Spot cierre", spot_cierre)
mostrar_fila("Spot apertura", spot_apertura)
mostrar_fila("Futuro (ES1!)", futuro)
mostrar_fila("Gap Spot", f"{gap_valor:+.2f} pt ({gap_pct:+.2f}%)", gap_color)
mostrar_fila("Divergencia", f"{div_valor:+.2f} pt ({div_pct:+.2f}%)", div_color)

st.button("Recalcular")

# --- BLOQUE: ENTRADA RECOMENDADA ---
st.markdown("## Entrada recomendada")

if div_valor > 0:
    st.markdown("<h3 style='color:green;'>↑ Entrada en largo</h3>", unsafe_allow_html=True)
    mostrar_fila("TP", "+10.00", "red")
    mostrar_fila("SL", "-5.00", "red")
else:
    st.markdown("<h3 style='color:red;'>↓ Entrada en corto</h3>", unsafe_allow_html=True)
    mostrar_fila("TP", "-10.00", "green")
    mostrar_fila("SL", "+5.00", "green")

# --- BLOQUE: VALIDACIÓN EN TENDENCIA (1min) ---
with st.expander("Validación entrada en tendencia (1min)"):
    mostrar_fila("RSI ≥ 55", f"({rsi})", "green" if rsi >= 55 else "red")
    mostrar_fila("Volumen ≥ 2000", f"({volumen})", "green" if volumen >= 2000 else "red")
    mostrar_fila("Cuerpo vela ≥ 1.25 pt", f"({cuerpo_vela})", "green" if cuerpo_vela >= 1.25 else "red")

# --- BLOQUE: TP EXTENDIDO ---
with st.expander("Condiciones TP extendido"):
    mostrar_fila("Impulso ≥ 2 pt", f"({impulso})", "green" if impulso >= 2 else "red")
    mostrar_fila("Retroceso ≤ -0.5 pt", f"({retroceso})", "green" if retroceso <= -0.5 else "red")
    mostrar_fila("Volumen ≥ 2500", f"({volumen})", "green" if volumen >= 2500 else "red")

# --- BLOQUE: SL TRAILING ---
with st.expander("Condiciones SL Trailing"):
    mostrar_fila("Diferencia desde entrada", f"{diferencia_trailing:+.2f} pt", "green" if diferencia_trailing > 0 else "red")


