import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Mini", layout="wide")
st.title("📊 Panel de Control Express")

datos = {
    "Producto": ["Laptops", "Teclados", "Monitores", "Mouses"],
    "Ventas_USD": [15000, 2500, 8000, 1200],
    "Unidades": [15, 80, 30, 65]
}
df = pd.DataFrame(datos)

col1, col2 = st.columns(2)
col1.metric(label="💰 Ingresos Totales", value=f"${df['Ventas_USD'].sum():,}")
col2.metric(label="📦 Total Unidades", value=f"{df['Unidades'].sum():,}")

fig = px.bar(df, x="Producto", y="Ventas_USD", text_auto=True)
st.plotly_chart(fig, use_container_width=True)
