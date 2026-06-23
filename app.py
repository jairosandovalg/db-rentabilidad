import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página (Debe ser la primera línea)
st.set_page_config(page_title="Cuadro de Mando Gerencial", page_icon="📈", layout="wide")

# Estilo CSS personalizado para forzar el Modo Oscuro Premium
st.markdown("""
    <style>
    /* Fondo principal y barra lateral */
    .stApp {background-color: #0E1117; color: #FFFFFF;}
    [data-testid="stSidebar"] {background-color: #161B22; border-right: 1px solid #30363D;}
    
    /* Títulos y textos generales */
    h1, h2, h3, p {color: #FFFFFF !important;}
    
    /* Tarjetas de Métricas (KPIs) en Fondo Oscuro */
    div[data-testid="stMetricValue"] {font-size: 30px; font-weight: bold; color: #58A6FF;}
    div[data-testid="stMetricLabel"] {font-size: 14px; color: #8B949E;}
    div[data-testid="metric-container"] {
        background-color: #161B22; 
        border: 1px solid #30363D; 
        padding: 15px 20px; 
        border-radius: 10px;
    }
    
    /* Líneas divisorias */
    hr {border-top: 1px solid #30363D;}
    </style>
""", unsafe_allow_html=True)

st.title("📊 Cuadro de Mando Gerencial")
st.markdown("### Resumen Ejecutivo de Ventas y Rendimiento Operativo")
st.write("---")

# 2. Base de datos de ejemplo
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
st.sidebar.header("🕹️ Panel de Control Ejecutivo")

# ---- FILTRO 1: CATEGORÍAS ----
categorias_disponibles = df_original["Categoría"].unique()
categorias_seleccionadas = st.sidebar.multiselect(
    "1. Filtrar por Categoría:",
    options=categorias_disponibles,
    default=categorias_disponibles
)

# ---- FILTRO 2: PRODUCTOS (Depende de Categoría) ----
df_filtrado_productos = df_original[df_original["Categoría"].isin(categorias_seleccionadas)]
productos_disponibles = df_filtrado_productos["Producto"].unique()

productos_seleccionados = st.sidebar.multiselect(
    "2. Filtrar por Producto:",
    options=productos_disponibles,
    default=productos_disponibles
)

# ---- FILTRO 3: MES / TIEMPO (Depende de Categoría y Producto) ----
df_filtrado_meses = df_filtrado_productos[df_filtrado_productos["Producto"].isin(productos_seleccionados)]
meses_disponibles = df_filtrado_meses["Mes"].unique()

meses_seleccionados = st.sidebar.multiselect(
    "3. Filtrar por Período (Mes):",
    options=meses_disponibles,
    default=meses_disponibles
)

# ---- APLICACIÓN FINAL DE FILTROS CRUZADOS ----
df_filtrado = df_original[
    (df_original["Categoría"].isin(categorias_seleccionadas)) & 
    (df_original["Producto"].isin(productos_seleccionados)) &
    (df_original["Mes"].isin(meses_seleccionados))
]
# =================================================================

if not df_filtrado.empty:
    
    # =================================================================
    # 🧮 CAPA DE KPIs (Fondo Oscuro estilizado vía CSS superior)
    # =================================================================
    total_ingresos = df_filtrado["Ventas_USD"].sum()
