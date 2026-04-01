import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(
    page_title="La Paradoja del Falso Positivo - ITBA Future Day", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Estilo CSS (Branding ITBA + Estilo de Libro)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    .highlight {
        background-color: #eef4ff;
        padding: 15px;
        border-left: 5px solid #003366;
        border-radius: 5px;
        margin: 10px 0;
    }
    .book-quote {
        font-style: italic;
        color: #444;
        background-color: #f1f1f1;
        border-left: 5px solid #ccc;
        padding: 15px;
        margin: 15px 0;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar con Logo y Controles
try:
    st.sidebar.image("logo_itba.png", use_container_width=True)
except:
    st.sidebar.warning("⚠️ Recordá colocar 'logo_itba.png' en la carpeta.")

st.sidebar.title("Panel de Control")
st.sidebar.markdown("---")

st.sidebar.subheader("📊 Datos de Población")
pop_total = st.sidebar.number_input("Población Total", value=45000000, step=1000000)
pop_buscados = st.sidebar.number_input("Personas con pedido de captura (D)", value=45000, step=1000)

st.sidebar.subheader("🛡️ Calidad del Sistema")
sensibilidad = st.sidebar.number_input("Sensibilidad P(+|D)", value=0.999, min_value=0.0, max_value=1.0, step=0.001, format="%.3f")
especificidad = st.sidebar.number_input("Especificidad P(-|ND)", value=0.999, min_value=0.0, max_value=1.0, step=0.001, format="%.3f")

# 4. Cálculos
prevalencia = pop_buscados / pop_total
tp = pop_buscados * sensibilidad
fp = (pop_total - pop_buscados) * (1 - especificidad)
vpp = tp / (tp + fp) if (tp + fp) > 0 else 0

# 5. Cuerpo Principal: LA NARRATIVA INICIAL (TU CASO BASE)
st.title("🕵️‍♂️ El Dilema del Reconocimiento Facial")
st.markdown("**Un experimento interactivo sobre la Falacia del Fiscal**")

st.markdown(f"""
### El Escenario
En Argentina hay aproximadamente **{pop_total:,}** habitantes. De ellos, la justicia busca a **{pop_buscados:,}** personas. 
Se instala un sistema de cámaras con una precisión asombrosa del **{sensibilidad*100}%**.

* **Si pasa un delincuente:** El sistema da un "HIT" (+) con probabilidad del **{sensibilidad*100}%**.
* **Si pasa un inocente:** El sistema NO da hit (-) con probabilidad del **{especificidad*100}%**.
""")

st.markdown(f"""
<div class="highlight">
<strong>La Paradoja:</strong> El operador del sistema nota que, de cada dos veces que suena la alarma y detiene a alguien, 
<strong>¡uno resulta ser un transeúnte inocente!</strong> ¿Está fallando el software? 
El probabilista responde: "No, es exactamente el resultado esperado".
</div>
""", unsafe_allow_html=True)

st.divider()

# 6. Desglose del Resultado
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("🧮 La cuenta que no miente")
    st.markdown(f"""
    **1. Aciertos Reales:**
    {pop_buscados:,} buscados × {sensibilidad} = **{int(tp):,} detenidos correctamente.**

    **2. Errores (Falsos Positivos):**
    {pop_total - pop_buscados:,} inocentes × {round(1-especificidad, 4)} = **{int(fp):,} inocentes detenidos.**
    
    *Como hay tantos inocentes, ese 0.1% de error genera un volumen de gente igual al de los delincuentes buscados.*
    """)

with col_right:
    st.subheader("📊 Composición de las Alarmas")
    chart_data = pd.DataFrame({
        'Resultado de la Alarma': ['Delincuente (Real)', 'Inocente (Error)'],
        'Cantidad': [tp, fp]
    }).set_index('Resultado de la Alarma')
    st.bar_chart(chart_data, color="#003366")

st.divider()

# 7. TABS ADICIONALES (CONTENIDO DEL LIBRO)
st.subheader("📚 Profundizando: Condenas, Absoluciones y Cisnes Negros Probabilísticos")
tab1, tab2, tab3 = st.tabs(["⚖️ Condenas y Absoluciones", "📈 Cisnes Negros Financieros", "🔬 Teoría de Bayes"])

with tab1:
    st.markdown("#### La Falacia del Fiscal en el estrado")
    st.write("Imaginemos un crimen en una ciudad de un millón de habitantes. Un identikit reduce los sospechosos a 10 personas.")
    
    col_f, col_a = st.columns(2)
    with col_f:
        st.error("**El Fiscal dice:**")
        st.write("'La probabilidad de que un inocente coincida con el identikit es de 9 entre 1.000.000 (0.0009%). ¡Es casi imposible que sea inocente!'")
    with col_a:
        st.success("**El Defensor dice:**")
        st.write("'De los 10 que coinciden, 9 son inocentes. La probabilidad de que mi cliente sea inocente es del 90%. Debe ser absuelto.'")
    
    st.markdown("""
    <div class="book-quote">
    <strong>Caso Lucía de Berk:</strong> Esta confusión costó la libertad de la enfermera holandesa. 
    Se argumentó que era "muy poco probable" que tantas muertes ocurrieran en sus turnos, ignorando que la 
    probabilidad de muertes naturales en ese contexto era, en realidad, mucho más alta.
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("#### Los Profetas del Desastre")
    st.markdown("""
    En finanzas, el "Cisne Negro" es un crack económico impredecible. Muchos gurúes lanzan alertas constantemente.
    """)
    
    st.markdown(f"""
    <div class="book-quote">
    "Si hay mil indicadores económicos confiables al 99%, pero la catástrofe tiene una probabilidad mucho menor al 1%, 
    tendremos muchísimos casos de anuncios de desastres que no ocurrirán. El test no falla; simplemente el evento es tan raro 
    que el 1% de error del indicador genera una cantidad de falsos positivos inmanejable."
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **Lección:** Un indicador que falla 9 de cada 10 veces predeciento una crisis no es 'malo'; simplemente está operando sobre un evento de bajísima prevalencia.")

with tab3:
    st.markdown("#### El Teorema de Bayes")
    st.write("La fórmula que explica por qué el operador de Constitución encontraba un 50% de error:")
    st.latex(r"P(D|+) = \frac{P(+|D) \cdot P(D)}{P(+|D) \cdot P(D) + P(+|ND) \cdot P(ND)}")
    
    st.markdown(f"""
    * **Sensibilidad $P(+|D)$:** {sensibilidad}
    * **Tasa Base $P(D)$:** {prevalencia:.5f}
    * **Probabilidad Posterior:** {vpp:.4f}
    """)
    st.write("Si el resultado es 0.5, significa que ante un 'Hit', las chances de acierto y error están empatadas.")

st.sidebar.markdown("---")
st.sidebar.caption("Contenido adaptado de: Metodología de la Investigación Científica (Maipue, 2020)")