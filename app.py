# ==============================
# STREAMLIT DASHBOARD (IMPROVED)
# ==============================

import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="PhonePe Dashboard", layout="wide")

# ------------------------------
# Load Data with Error Handling
# ------------------------------
try:
    df = pd.read_csv("data.csv")
except:
    st.error("❌ data.csv not found. Please check file location.")
    st.stop()

# ------------------------------
# Title
# ------------------------------
st.title("📊 PhonePe Transaction Insights Dashboard")

st.markdown("Analyze digital transaction trends across states and quarters")

# ------------------------------
# Sidebar Filters
# ------------------------------
st.sidebar.header("🔍 Filters")

state = st.sidebar.selectbox("Select State", sorted(df['state'].unique()))
quarter = st.sidebar.selectbox("Select Quarter", sorted(df['quarter'].unique()))

# ------------------------------
# Filter Data
# ------------------------------
filtered_df = df[(df['state'] == state) & (df['quarter'] == quarter)]

# ------------------------------
# Handle Empty Data
# ------------------------------
if filtered_df.empty:
    st.warning("⚠️ No data available for selected filters")
    st.stop()

# ------------------------------
# KPI Section
# ------------------------------
st.subheader("📌 Key Metrics")

col1, col2 = st.columns(2)

col1.metric("Total Transactions", int(filtered_df['count'].sum()))
col2.metric("Total Amount", f"₹ {filtered_df['amount'].sum():,.2f}")

# ------------------------------
# Charts Section
# ------------------------------
st.subheader("📈 Transaction Trends")

col3, col4 = st.columns(2)

# Line chart
trend = df[df['state'] == state].groupby('quarter')['amount'].sum()
col3.line_chart(trend)

# Bar chart
count_trend = df[df['state'] == state].groupby('quarter')['count'].sum()
col4.bar_chart(count_trend)

# ------------------------------
# Top States
# ------------------------------
st.subheader("🏆 Top 10 States by Transaction Amount")

top_states = df.groupby('state')['amount'].sum().sort_values(ascending=False).head(10)
st.bar_chart(top_states)

# ------------------------------
# Data Preview
# ------------------------------
st.subheader("📄 Filtered Data Preview")

st.dataframe(filtered_df)