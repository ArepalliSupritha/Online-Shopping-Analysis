import streamlit as st
import pandas as pd
import plotly.express as px

from database import load_data
from analysis import (
    get_total_revenue,
    get_total_orders,
    get_total_customers,
    get_category_sales,
    get_monthly_sales,
    get_top_products
)

st.set_page_config(
    page_title="Online Shopping Analytics",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Online Shopping Data Analysis")
st.write(
    "Analyze sales, customers, products, and shopping trends."
)

# Load data from SQLite
df = load_data()

# Sidebar filters
st.sidebar.header("Filter Data")

categories = sorted(df["category"].dropna().unique())

selected_categories = st.sidebar.multiselect(
    "Select Categories",
    categories,
    default=categories
)

payment_methods = sorted(
    df["payment_method"].dropna().unique()
)

selected_payments = st.sidebar.multiselect(
    "Select Payment Methods",
    payment_methods,
    default=payment_methods
)

df["order_date"] = pd.to_datetime(df["order_date"])

min_date = df["order_date"].min().date()
max_date = df["order_date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

filtered_df = df[
    df["category"].isin(selected_categories)
    & df["payment_method"].isin(selected_payments)
].copy()

if isinstance(date_range, (tuple, list)):
    if len(date_range) == 2:
        start_date, end_date = date_range

        filtered_df = filtered_df[
            (filtered_df["order_date"].dt.date >= start_date)
            & (filtered_df["order_date"].dt.date <= end_date)
        ]
    elif len(date_range) == 1:
        selected_date = date_range[0]

        filtered_df = filtered_df[
            filtered_df["order_date"].dt.date == selected_date
        ]

elif date_range:
    filtered_df = filtered_df[
        filtered_df["order_date"].dt.date == date_range
    ]

if filtered_df.empty:
    st.warning("No orders match the selected filters.")

else:
    # KPI metrics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Revenue",
        f"₹{get_total_revenue(filtered_df):,.2f}"
    )

    col2.metric(
        "Total Orders",
        f"{get_total_orders(filtered_df):,}"
    )

    col3.metric(
        "Unique Customers",
        f"{get_total_customers(filtered_df):,}"
    )

    col4.metric(
        "Units Sold",
        f"{filtered_df['quantity'].sum():,}"
    )

    st.divider()

    # Monthly sales chart
    st.subheader("Monthly Sales Analysis")

    monthly_sales = get_monthly_sales(filtered_df)

    fig_monthly = px.line(
        monthly_sales,
        x="month",
        y="revenue",
        markers=True,
        title="Revenue by Month",
        labels={
            "month": "Month",
            "revenue": "Revenue (₹)"
        }
    )

    st.plotly_chart(fig_monthly, use_container_width=True)

    # Category and payment analysis
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Sales by Category")

        category_sales = get_category_sales(filtered_df)

        fig_category = px.bar(
            category_sales,
            x="category",
            y="revenue",
            title="Revenue by Product Category",
            labels={
                "category": "Category",
                "revenue": "Revenue (₹)"
            }
        )

        st.plotly_chart(
            fig_category,
            use_container_width=True
        )

    with col2:
        st.subheader("Payment Methods")

        payment_sales = (
            filtered_df.groupby("payment_method")
            .size()
            .reset_index(name="orders")
        )

        fig_payment = px.pie(
            payment_sales,
            names="payment_method",
            values="orders",
            title="Orders by Payment Method"
        )

        st.plotly_chart(
            fig_payment,
            use_container_width=True
        )

    # Popular products
    st.subheader("Popular Products")

    top_products = get_top_products(filtered_df)

    fig_products = px.bar(
        top_products,
        x="product",
        y="total_quantity",
        title="Top Products by Units Sold",
        labels={
            "product": "Product",
            "total_quantity": "Units Sold"
        }
    )

    st.plotly_chart(
        fig_products,
        use_container_width=True
    )

    # Dataset
    st.subheader("Shopping Order Details")

    display_df = filtered_df.copy()
    display_df["order_date"] = (
        display_df["order_date"].dt.strftime("%Y-%m-%d")
    )

    st.dataframe(display_df, use_container_width=True)

    # Download report
    csv_data = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv_data,
        file_name="shopping_analysis.csv",
        mime="text/csv"
    )