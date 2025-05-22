
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns


# Configuración de la página en el navegador
st.set_page_config(page_title="Dashboard Interactivo de Ventas", layout="wide")
sns.set(style="whitegrid")


# Título principal dentro del dashboard
st.title("Dashboard de Ventas - Tienda de Conveniencia")


# Carga y Preparación de Datos
df = pd.read_csv('data.csv')
df['Date'] = pd.to_datetime(df['Date'])

# ---------------------------------------------------------------------------------------
# Hipotesis: Evaluar como es el comportamiento de cada sucursal en la ciudades indicada
# en función del método de pago y el tipo de cliente.
# ---------------------------------------------------------------------------------------

# Creación de filtro principales
st.sidebar.header("Filtros")
# El dasboarda filtrará por el tipo de sucursal que está asociada a la ciudad A-Yangon,C-Naypyitaw,B-Mandalay
sucursales = st.sidebar.multiselect("Sucursal", df['City'].unique(), df['City'].unique())
tipos_cliente = st.sidebar.multiselect("Tipo de cliente", df['Customer type'].unique(), df['Customer type'].unique())
metodos_pago = st.sidebar.multiselect("Método de pago", df['Payment'].unique(), df['Payment'].unique())

df_filtrado = df[(df['City'].isin(sucursales)) &
(df['Customer type'].isin(tipos_cliente)) &
(df['Payment'].isin(metodos_pago))]

# ---------------------------------------------------------------------------------------

# Análisis Requerido N°1: Evolución de las Ventas Totales
# Objetivo: Mostrar cómo han variado las ventas totales (Total) a lo largo del tiempo (Date).

st.subheader("1. Evolución de las Ventas Totales")
ventas_por_fecha = df_filtrado.groupby('Date')['Total'].sum().reset_index()
fig1 = px.line(
ventas_por_fecha,
x='Date',
y='Total',
title="Ventas Totales por Fecha"
)
st.plotly_chart(fig1, use_container_width=True)

# ---------------------------------------------------------------------------------------

# Análisis Requerido N°2: Ingresos por Línea de Producto
# Objetivo: Objetivo: Comparar los ingresos (Total) generados por cada Product line.

st.subheader("2. Ingresos por Línea de Producto")
ingresos_por_producto = df_filtrado.groupby('Product line')['Total'].sum().sort_values().reset_index()
fig2 = px.bar(
ingresos_por_producto,
x='Total',
y='Product line',
orientation='h',
title="Ingresos por Línea de Producto"
)
st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------------------------------------------

# Análisis Requerido N°3: Distribución de la Calificación de Clientes
# Objetivo: Analizar la distribución de las calificaciones (Rating) de los clientes.

st.subheader("3. Distribución de la Calificación de Clientes")
fig3 = px.histogram(
df_filtrado,
x='Rating',
nbins=20,
title="Distribución de Calificaciones de Clientes"
)
st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------------------------------------------

# Análisis Requerido N°4: Comparación del Gasto por Tipo de Cliente
# Objetivo: Comparar la distribución del gasto total (Total) entre clientes Member y Normal.

st.subheader("4. Promedio de Gasto por Tipo de Cliente")
gasto_promedio = df_filtrado.groupby('Customer type')['Total'].mean().reset_index()
fig_barras = px.bar(
    gasto_promedio,
    x='Customer type',
    y='Total',
    title="Promedio de Gasto por Tipo de Cliente"
)
st.plotly_chart(fig_barras, use_container_width=True)


# ---------------------------------------------------------------------------------------

# Análisis Requerido N°5: Relación entre Costo y Ganancia Bruta
# Objetivo: Visualizar la relación entre el costo de bienes vendidos (cogs) y el ingreso bruto (gross income).


st.subheader("5. Relación entre Costo y Ganancia Bruta")
fig5 = px.scatter(
df_filtrado,
x='cogs',
y='gross income',
title="Costo vs Ganancia Bruta"
)
st.plotly_chart(fig5, use_container_width=True)

# ---------------------------------------------------------------------------------------

# Análisis Requerido N°6: Métodos de Pago Preferidos
# Objetivo: Identificar los métodos de pago (Payment) más frecuentes.


st.subheader("6. Métodos de Pago Preferidos")
pagos = df_filtrado['Payment'].value_counts().reset_index()
pagos.columns = ['Método de Pago', 'Cantidad']
fig6 = px.pie(
pagos,
names='Método de Pago',
values='Cantidad',
title="Distribución de Métodos de Pago"
)
st.plotly_chart(fig6, use_container_width=True)

# ---------------------------------------------------------------------------------------

# Análisis Requerido N°7: Análisis de Correlación Numérica
# Objetivo: Explorar relaciones lineales entre variables numéricas (Unit price, Quantity, Tax 5%, Total, cogs, gross income, Rating).


st.subheader("7. Análisis de Correlación Numérica")
variables_numericas = ['Unit price', 'Quantity', 'Tax 5%', 'Total', 'cogs', 'gross income', 'Rating']
corr = df_filtrado[variables_numericas].corr()
fig7 = px.imshow(
corr,
text_auto=True,
title="Matriz de Correlación Numérica"
)
st.plotly_chart(fig7, use_container_width=True)

# ---------------------------------------------------------------------------------------

# Análisis Requerido N°8: Composición del Ingreso Bruto por Sucursal y Línea de Producto

# ---------------------------------------------------------------------------------------

st.subheader("8. Composición del Ingreso Bruto por Sucursal y Línea de Producto")
ingreso_sucursal_producto = df_filtrado.groupby(['Branch', 'Product line'])['gross income'].sum().reset_index()
fig8 = px.sunburst(
ingreso_sucursal_producto,
path=['Branch', 'Product line'],
values='gross income',
title="Ingreso Bruto por Sucursal y Línea de Producto"
)
st.plotly_chart(fig8, use_container_width=True)

# ---------------------------------------------------------------------------------------



