import streamlit as st

# Simulación de valores de entrada
spot_cierre = 5956.79
spot_apertura = 5983.80
futuro = 5970.00
gap = spot_apertura - spot_cierre
gap_pct = (gap / spot_cierre) * 100
divergencia = futuro - spot_apertura
div_pct = (divergencia / spot_apertura) * 100

# Simulación de condiciones
rsi = 61
volumen = 2100
cuerpo_vela = 1.3

# Evaluación
entrada = None
tipo_entrada = None
tp = None
sl = None
mensaje_rechazo = ""

# Determinar dirección del gap y divergencia
gap_positivo = gap > 0
div_positiva = divergencia > 0
gap_no_descontado = (gap_positivo and not div_positiva) or (not gap_positivo and div_positiva)

# Determinar entrada
if gap != 0:
    if gap_no_descontado:
        if abs(div_pct) >= 0.10:
            tipo_entrada = "Largo" if div_positiva else "Corto"
            entrada = True
            tp = 10 if abs(div_pct) >= 0.24 else 4
            sl = 3
        else:
            mensaje_rechazo = "No hay entrada recomendada (divergencia insuficiente)"
    else:
        mensaje_rechazo = "No hay entrada recomendada (gap ya descontado)"
else:
    mensaje_rechazo = "No hay entrada recomendada (gap nulo)"

# Estilo
st.markdown("""
<style>
.valor-derecha {
    display: flex;
    justify-content: space-between;
    padding: 6px 0;
    font-size: 18px;
}
.valor-derecha span:first-child {
    font-weight: bold;
}
.verde {
    color: green;
    font-size: 20px;
}
.rojo {
    color: red;
    font-size: 20px;
}
.gris {
    color: lightgray;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# Bloque: Datos Iniciales
st.markdown("## Datos Iniciales")

st.markdown(f"""
<div class="valor-derecha"><span>Spot cierre</span><span>{spot_cierre:,.2f}</span></div>
<div class="valor-derecha"><span>Spot apertura</span><span>{spot_apertura:,.2f}</span></div>
<div class="valor-derecha">
    <span>Gap Spot</span>
    <span style="color:{'green' if gap != 0 else 'lightgray'}">
        {gap:+.2f} {'↑' if gap > 0 else '↓' if gap < 0 else ''} / {abs(gap_pct):.2f}%
    </span>
</div>
<div class="valor-derecha">
    <span>Divergencia</span>
    <span style="color:{'green' if gap_no_descontado else 'red'}">
        {divergencia:+.2f} / {abs(div_pct):.2f}%
    </span>
</div>
""", unsafe_allow_html=True)

# Mostrar mensaje si el gap está descontado
if not gap_no_descontado:
    st.markdown('<span class="rojo">⚠️ <b>Gap descontado</b></span>', unsafe_allow_html=True)

st.markdown("---")

# Bloque: Entrada recomendada
st.markdown("## Entrada recomendada")

if entrada:
    color = "verde" if tipo_entrada == "Largo" else "rojo"
    flecha = "⬆️" if tipo_entrada == "Largo" else "⬇️"
    st.markdown(f"""
    <div class="valor-derecha"><span>Entrada</span><span class="{color}">{flecha} <b>{tipo_entrada}</b></span></div>
    <div class="valor-derecha"><span>TP / SL:</span><span class="{color}">+{tp} / -{sl}</span></div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="valor-derecha">
        <span>Entrada</span>
        <span class="gris">⚠️ <b>{mensaje_rechazo}</b></span>
    </div>
    """, unsafe_allow_html=True)

# Validación entrada en tendencia (1min)
st.markdown("---")
with st.expander("Validación entrada en tendencia (1min)", expanded=True):
    st.markdown(f"""
    <div class="valor-derecha"><span>RSI (&gt;55)</span><span style="color: {'green' if rsi > 55 else 'red'}">{rsi}</span></div>
    <div class="valor-derecha"><span>Volumen (&gt;2000)</span><span style="color: {'green' if volumen > 2000 else 'red'}">{volumen}</span></div>
    <div class="valor-derecha"><span>Cuerpo vela (≥1.25)</span><span style="color: {'green' if cuerpo_vela >= 1.25 else 'red'}">{cuerpo_vela}</span></div>
    <div class="valor-derecha"><span>Divergencia (≥0.10%)</span><span style="color: {'green' if abs(div_pct) >= 0.10 else 'red'}">{abs(div_pct):.2f}%</span></div>
    """, unsafe_allow_html=True)
