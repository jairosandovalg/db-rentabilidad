import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Configuración de la página (Debe ser la primera línea de Streamlit)
st.set_page_config(
    page_title="Dashboard Comercial de Pruebas",
    page_icon="📊",
    layout="wide" # Configura la app en pantalla ancha
)

# 2. Título principal de la aplicación
st.title("📊 Dashboard de Rendimiento Comercial")
st.markdown("Bienvenido al panel de control simplificado. Los datos se actualizan dinámicamente según los filtros.")
st.write("---")

# 3. Simulación de datos (Simulamos un histórico de ventas)
@st.cache_data
def generar_datos_simulados():
    np.random.seed(42)
    fechas = pd.date_range(start="2026-01-01", end="2026-06-20", freq="D")
    regiones = ["Norte", "Sur", "Centro", "Este"]
    productos = ["Laptops", "Teclados", "Monitores", "Mouses"]
    
    datos = []
    for fecha in fechas:
        for _ in range(np.random.randint(1, 5)): # Entre 1 y 4 ventas por día
            datos.append({
                "Fecha": fecha,
                "Región": np.random.choice(regiones),
                "Producto": np.random.choice(productos),
                "Monto": round(np.random.uniform(50, 1200), 2),
                "Cantidad": np.random.randint(1, 5)
            })
    return pd.DataFrame(datos)

df_original = generar_datos_simulados()

# 4. Barra Lateral (Sidebar) para los Filtros
st.sidebar.header("🎯 Filtros Disponibles")

# Filtro de Región
lista_regiones = df_original["Región"].unique()
regiones_seleccionadas = st.sidebar.multiselect(
    "Selecciona la(s) Región(es):",
    options=lista_regiones,
    default=lista_regiones # Por defecto seleccionamos todas
)

# Filtro de Producto
lista_productos = df_original["Producto"].unique()
productos_seleccionados = st.sidebar.multiselect(
    "Selecciona el o los Productos:",
    options=lista_productos,
    default=lista_productos
)

# Aplicar los filtros al DataFrame original
df_filtrado = df_original[
    (df_original["Región"].isin(regiones_seleccionadas)) & 
    (df_original["Producto"].isin(productos_seleccionados))
]

# 5. Sección de Métricas Clave (KPIs) en columnas
if not df_filtrado.empty:
    col1, col2, col3, col4 = st.columns(4)
    
    # Cálculos dinámicos
    total_ventas = df_filtrado["Monto"].sum()
    total_un
