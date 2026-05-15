import streamlit as st
import clickhouse_connect
import pandas as pd
import os
from dotenv import load_dotenv
import plotly.express as px

load_dotenv()

st.set_page_config(page_title="Olist Business Dashboard", layout="wide")

st.title("📊 Olist Business Dashboard")

# ClickHouse connection details
CH_HOST = os.getenv("CLICKHOUSE_HOST", "localhost")
CH_USER = os.getenv("CLICKHOUSE_USER", "default")
CH_PASS = os.getenv("CLICKHOUSE_PASSWORD", "")
CH_DB = os.getenv("CLICKHOUSE_DB", "olist")

@st.cache_resource
def get_client():
    return clickhouse_connect.get_client(host=CH_HOST, username=CH_USER, password=CH_PASS, database=CH_DB)

client = get_client()

st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Business Metrics", "Ingestion Status"])

if page == "Business Metrics":
    st.header("📈 Key Performance Indicators")
    
    try:
        # High-level metrics
        metrics_query = f"""
        SELECT 
            count(*) as total_orders,
            sum(total_order_value) as total_gmv,
            avg(total_order_value) as avg_order_value,
            count(DISTINCT customer_id) as unique_customers
        FROM {CH_DB}.fct_orders
        WHERE order_status = 'delivered'
        """
        metrics = client.query_df(metrics_query)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Delivered Orders", f"{metrics['total_orders'][0]:,.0f}")
        col2.metric("Total GMV", f"R$ {metrics['total_gmv'][0]:,.2f}")
        col3.metric("Avg Order Value", f"R$ {metrics['avg_order_value'][0]:,.2f}")
        col4.metric("Unique Customers", f"{metrics['unique_customers'][0]:,.0f}")

        # Sales Trend
        st.subheader("📅 Sales Trend")
        trend_query = f"""
        SELECT 
            order_date,
            sum(total_order_value) as daily_revenue,
            count(*) as daily_orders
        FROM {CH_DB}.fct_orders
        WHERE order_status = 'delivered'
        GROUP BY order_date
        ORDER BY order_date
        """
        df_trend = client.query_df(trend_query)
        df_trend['order_date'] = pd.to_datetime(df_trend['order_date'])
        
        fig_revenue = px.line(df_trend, x='order_date', y='daily_revenue', title='Daily Revenue (Delivered Orders)')
        st.plotly_chart(fig_revenue, use_container_width=True)

        # Order Status Distribution
        st.subheader("📦 Order Status Distribution")
        status_query = f"SELECT order_status, count(*) as count FROM {CH_DB}.fct_orders GROUP BY order_status"
        df_status = client.query_df(status_query)
        fig_status = px.pie(df_status, values='count', names='order_status', title='Orders by Status')
        st.plotly_chart(fig_status, use_container_width=True)

    except Exception as e:
        st.error(f"Error loading business metrics: {e}")
        st.info("Make sure dbt models have been run: `docker exec dbt-runner dbt run --profiles-dir .`")

else:
    st.header("⚙️ Ingestion Status")
    try:
        query = f"SELECT tag, count() as rows, max(unixtime) as last_ingest FROM {CH_DB}.ingestion GROUP BY tag ORDER BY rows DESC"
        df = client.query_df(query)
        st.dataframe(df, use_container_width=True)
        
        st.write("### Recent Raw Data (Sample)")
        sample_df = client.query_df(f"SELECT * FROM {CH_DB}.ingestion LIMIT 10")
        st.dataframe(sample_df, use_container_width=True)

    except Exception as e:
        st.warning("⚠️ Could not load ingestion data.")
        st.error(e)

st.sidebar.markdown("---")
st.sidebar.write("Built with ❤️ using Streamlit, dbt & ClickHouse")
