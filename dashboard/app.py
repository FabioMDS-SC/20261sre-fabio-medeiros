import streamlit as st
import pandas as pd
import clickhouse_connect
import plotly.express as px
import os

st.set_page_config(page_title="Olist Dashboard - AWS", layout="wide")

@st.cache_resource
def get_client():
    return clickhouse_connect.get_client(
        host='10.0.1.96',
        port=8123,
        username='admin',
        password='password123',
        database='olist'
    )

st.title("📦 Olist Data Pipeline Dashboard")
st.write("Visualização de dados processados via AWS (S3 -> ClickHouse)")

try:
    client = get_client()
    
    # Query de exemplo: Contagem de registros por tag (arquivo)
    query = "SELECT tag, count() as total FROM olist.ingestion GROUP BY tag ORDER BY total DESC"
    df = client.query_df(query)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Registros por Arquivo")
        st.dataframe(df, use_container_width=True)
        
    with col2:
        st.subheader("Distribuição de Cargas")
        fig = px.pie(df, values='total', names='tag')
        st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao conectar ao ClickHouse: {e}")
