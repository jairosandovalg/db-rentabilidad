import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración básica inicial
st.set_page_config(page_title="Dashboard Mini", layout="wide")
st.title("📊 Panel de Control Express")
st.write("Carga ultra rápida sin procesos pesados en segundo plano.")
st.write("---")

# 2. Datos mínimos fijos (Evita que Python trabaje de más)
datos = {
    "Producto": ["Laptops", "Teclados", "Monitores", "Mouses"],
    "Ventas_USD": [15000, 2500, 8000, 1200],
    "Unidades": [15, 80, 30, 65]
}
df = pd.DataFrame(datos)

# 3. Mostrar Métricas en columnas inmediatas
col1, col2 = st.columns(2)
with col1:
    st.metric(label="💰 Ingresos Totales", value=f"${df['Ventas_USD'].sum():,}")
with col2:
    st.metric(label="📦 Total Unidades", value=f"{df['Unidades'].sum():,}")

st.write("---")

# 4. Un solo gráfico rápido de barras
st.subheader("📈 Ventas por Categoría")
fig = px.bar(df, x="Producto", y="Ventas_USD", text_auto=True)
st.plotly_chart(fig, use_container_width=True)

# 5. Tabla de datos simple
st.subheader("📋 Datos Base")
st.dataframe(df, use_container_width=True, hide_index=True)
