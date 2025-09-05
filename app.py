import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="E-Commerce Sales Analysis", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("E-Commerce-Sales-Analysis/data/ecommerce_sales.csv", parse_dates=["Order Date", "Ship Date"])

df = load_data()

st.title("📊 E-Commerce Sales Analysis Dashboard")

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    segment = st.multiselect("Segment", sorted(df["Segment"].unique()), default=sorted(df["Segment"].unique()))
    category = st.multiselect("Category", sorted(df["Category"].unique()), default=sorted(df["Category"].unique()))
    region = st.multiselect("Region", sorted(df["Region"].unique()), default=sorted(df["Region"].unique()))
    date_range = st.date_input("Order Date Range",
                               value=(df["Order Date"].min(), df["Order Date"].max()))

mask = (
    df["Segment"].isin(segment) &
    df["Category"].isin(category) &
    df["Region"].isin(region) &
    (df["Order Date"] >= pd.to_datetime(date_range[0])) &
    (df["Order Date"] <= pd.to_datetime(date_range[1]))
)
dff = df.loc[mask].copy()

# KPIs
total_sales = dff["Sales"].sum()
total_profit = dff["Profit"].sum()
total_orders = dff["Order ID"].nunique()

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total Sales", f"${total_sales:,.0f}")
kpi2.metric("Total Profit", f"${total_profit:,.0f}")
kpi3.metric("Unique Orders", f"{total_orders:,}")

st.markdown("---")

# Charts
col1, col2 = st.columns(2)
with col1:
    sales_over_time = dff.groupby(pd.Grouper(key="Order Date", freq="M"))["Sales"].sum().reset_index()
    fig1 = px.line(sales_over_time, x="Order Date", y="Sales", title="Sales Over Time (Monthly)")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    category_sales = dff.groupby("Category")["Sales"].sum().reset_index().sort_values("Sales", ascending=False)
    fig2 = px.bar(category_sales, x="Category", y="Sales", title="Sales by Category")
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    region_profit = dff.groupby("Region")["Profit"].sum().reset_index().sort_values("Profit", ascending=False)
    fig3 = px.bar(region_profit, x="Region", y="Profit", title="Profit by Region")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    subcat_sales = dff.groupby("Sub-Category")["Sales"].sum().reset_index().sort_values("Sales", ascending=False).head(10)
    fig4 = px.bar(subcat_sales, x="Sub-Category", y="Sales", title="Top 10 Sub-Categories by Sales")
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.subheader("Raw Data")
st.dataframe(dff.sort_values("Order Date", ascending=False))
