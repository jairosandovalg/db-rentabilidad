import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Mini", layout="wide")
st.title("📊 Panel de Control Express")

# 1. Base de datos original
datos = {
    "Producto": ["Laptops", "Teclados", "Monitores", "Mouses"],
    "Ventas_USD": [15000, 2500, 8000, 1200],
    "Unidades": [15, 80, 30, 65]
}
df_original = pd.DataFrame(datos)

# =================================================================
# 🔥 NUEVA SECCIÓN: FILTROS EN LA BARRA LATERAL (SIDEBAR)
# =================================================================
st.sidebar.header("🎯 Filtros del Dashboard")

# Selector múltiple que toma los productos únicos de nuestra base de datos
productos_seleccionados = st.sidebar.multiselect(
    "Selecciona los productos a mostrar:",
    options=df_original["Producto"].unique(),
    default=df_original["Producto"].unique() # Por defecto, todos seleccionados
)

# Aplicamos el filtro al DataFrame original para crear un DataFrame filtrado
df_filtrado = df_original[df_original["Producto"].isin(productos_seleccionados)]
# =================================================================

st.write("---")

# Validación: Si hay al menos un producto seleccionado, muestra el dashboard
if not df_filtrado.empty:
    
    # 2. Métricas basadas en los datos filtrados
    col1, col2 = st.columns(2)
    col1.metric(label="💰 Ingresos Totales", value=f"${df_filtrado['Ventas_USD'].sum():,}")
    col2.metric(label="📦 Total Unidades", value=f"{df_filtrado['Unidades'].sum():,}")
    
    st.write("---")

    # 3. Gráfico basado en los datos filtrados
    fig = px.bar(df_filtrado, x="Producto", y="Ventas_USD", text_auto=True, title="Ventas por Producto Seleccionado")
    st.plotly_chart(fig, use_container_width=True)
    
    # 4. Tabla de datos (Opcional, pero útil para verificar el filtro)
    st.dataframe(df_filtrado, use_container_width=True, hide_index=True)

else:
    # Mensaje de advertencia si el usuario desmarca absolutamente todo
    st.warning("⚠️ Por favor, selecciona al menos un producto en la barra lateral para visualizar el dashboard.")
