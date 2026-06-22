import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página con estilo gerencial (Debe ser la primera línea)
st.set_page_config(page_title="Cuadro de Mando Gerencial", page_icon="📈", layout="wide")

# Estilo personalizado para mejorar la estética ejecutiva
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    div[data-testid="stMetricValue"] {font-size: 28px; font-weight: bold; color: #1e3d59;}
    div[data-testid="stMetricLabel"] {font-size: 14px; color: #6c757d;}
    </style>
""", unsafe_allow_html=True)

st.title("📊 Cuadro de Mando Gerencial")
st.markdown("### Resumen Ejecutivo de Ventas y Rendimiento Operativo")
st.write("---")

# 2. Base de datos de ejemplo (Con Categorías y Meses para las nuevas dimensiones)
datos = {
    "Producto": ["Laptops", "Teclados", "Monitores", "Mouses", "Laptops", "Teclados", "Monitores", "Mouses"],
    "Categoría": ["Hardware", "Periféricos", "Hardware", "Periféricos", "Hardware", "Periféricos", "Hardware", "Periféricos"],
    "Mes": ["Enero", "Enero", "Enero", "Enero", "Febrero", "Febrero", "Febrero", "Febrero"],
    "Ventas_USD": [15000, 2500, 8000, 1200, 18500, 2900, 9200, 1100],
    "Unidades": [15, 80, 30, 65, 18, 92, 35, 60]
}
df_original = pd.DataFrame(datos)

# =================================================================
# 🎯 SECCIÓN: FILTROS MULTIDIMENSIONALES EN CASCADA (BARRA LATERAL)
# =================================================================
st.sidebar.header("🕹️ Panel de Control Ejecutivos")

# ---- FILTRO 1: CATEGORÍAS ----
categorias_disponibles = df_original["Categoría"].unique()
categorias_seleccionadas = st.sidebar.multiselect(
    "1. Filtrar por Categoría:",
    options=categorias_disponibles,
    default=categorias_disponibles
)

# ---- FILTRO 2: PRODUCTOS (Depende de Categoría) ----
# Usamos el DataFrame original filtrado por las categorías seleccionadas
df_filtrado_productos = df_original[df_original["Categoría"].isin(categorias_seleccionadas)]
productos_disponibles = df_filtrado_productos["Producto"].unique()

productos_seleccionados = st.sidebar.multiselect(
    "2. Filtrar por Producto:",
    options=productos_disponibles,
    default=productos_disponibles
)

# ---- FILTRO 3: MES / TIEMPO (Depende de Categoría y Producto) ----
# CORREGIDO: Usamos el DataFrame del paso anterior filtrado por los productos seleccionados
df_filtrado_meses = df_filtrado_productos[df_filtrado_productos["Producto"].isin(productos_seleccionados)]
meses_disponibles = df_filtrado_meses["Mes"].unique()

meses_seleccionados = st.sidebar.multiselect(
    "3. Filtrar por Período (Mes):",
    options=meses_disponibles,
    default=meses_disponibles
)

# ---- APLICACIÓN FINAL DE FILTROS CRUZADOS ----
# Este es el DataFrame definitivo que usarán tus gráficos y KPIs
df_filtrado = df_original[
    (df_original["Categoría"].isin(categorias_seleccionadas)) & 
    (df_original["Producto"].isin(productos_seleccionados)) &
    (df_original["Mes"].isin(meses_seleccionados))
]
# =================================================================

# Validación de seguridad de datos: Si el usuario desmarca todo, no se rompe la app
if not df_filtrado.empty:
    
    # =================================================================
    # 🧮 CAPA DE KPIs (Métricas Principales de Alto Nivel)
    # =================================================================
    total_ingresos = df_filtrado["Ventas_USD"].sum()
    total_unidades = df_filtrado["Unidades"].sum()
    ticket_promedio = df_filtrado["Ventas_USD"].sum() / df_filtrado["Unidades"].sum() if total_unidades > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="💰 INGRESOS TOTALES (USD)", value=f"${total_ingresos:,.2f}")
    with col2:
        st.metric(label="📦 VOLUMEN DE VENTAS (UNIDADES)", value=f"{total_unidades:,} und")
    with col3:
        st.metric(label="🎫 TICKET PROMEDIO POR UNIDAD", value=f"${ticket_promedio:,.2f}")
    
    st.write("---")

    # =================================================================
    # 📊 SECCIÓN ANALÍTICA (Distribución, Comparativa y Tendencia)
    # =================================================================
    fila_graficos1, fila_graficos2 = st.columns(2)
    
    with fila_graficos1:
        st.subheader("🍰 Participación Comercial por Categoría")
        fig_circular = px.pie(
            df_filtrado, 
            values="Ventas_USD", 
            names="Categoría", 
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_circular.update_traces(textinfo="percent+label")
        st.plotly_chart(fig_circular, use_container_width=True)
        
    with fila_graficos2:
        st.subheader("📈 Tendencia Temporal de Ventas")
        # Agrupación por mes para la línea de tendencia dinámicamente ordenada
        df_tendencia = df_filtrado.groupby("Mes")["Ventas_USD"].sum().reset_index()
        
        # Estabiliza el orden cronológico básico si ambos meses están presentes
        orden_meses = ["Enero", "Febrero"]
        df_tendencia['Mes'] = pd.Categorical(df_tendencia['Mes'], categories=orden_meses, ordered=True)
        df_tendencia = df_tendencia.sort_values('Mes')

        fig_linea = px.line(
            df_tendencia, 
            x="Mes", 
            y="Ventas_USD", 
            markers=True,
            labels={"Ventas_USD": "Ingresos (USD)", "Mes": "Período"},
            color_discrete_sequence=["#1e3d59"]
        )
        st.plotly_chart(fig_linea, use_container_width=True)

    st.write("---")
    
    # Gráfico de barras comparativo por producto y mes
    st.subheader("📊 Rendimiento Individual por Línea de Producto")
    fig_barras = px.bar(
        df_filtrado, 
        x="Producto", 
        y="Ventas_USD", 
        color="Mes",
        barmode="group",
        text_auto=True,
        color_discrete_sequence=["#17b978", "#a6f6f1"]
    )
    st.plotly_chart(fig_barras, use_container_width=True)

    # =================================================================
    # 📋 DETALLE OPERATIVO (Tabla de Datos Auditable Oculta)
    # =================================================================
    st.write("---")
    with st.expander("🔍 Ver Registro de Datos Operativos Completo"):
        st.dataframe(
            df_filtrado.sort_values(by="Ventas_USD", ascending=False), 
            use_container_width=True, 
            hide_index=True
        )

else:
    st.warning("⚠️ Sin datos consolidados. Modifica la combinación de filtros en la barra lateral para recalcular el modelo gerencial.")
