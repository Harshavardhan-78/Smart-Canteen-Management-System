import streamlit as st
from utils.db_handler import fetch_sales_data
from utils.processor import generate_historical_insights

st.title("📊 Smart Dashboard")

if "owner_id" not in st.session_state:
    st.error("Please login")
    st.stop()

df = fetch_sales_data(st.session_state["owner_id"])

if df.empty:
    st.warning("No historical sales data")
    st.stop()

st.subheader("🔍 Insights from Past Data")
for insight in generate_historical_insights(df):
    st.success(insight)

st.subheader("📦 Item-wise Sales")
st.bar_chart(df.groupby("item")["quantity"].sum())
