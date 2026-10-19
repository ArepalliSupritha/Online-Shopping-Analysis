import pandas as pd


def get_total_revenue(df):
    return df["revenue"].sum()


def get_total_orders(df):
    return df["order_id"].nunique()


def get_total_customers(df):
    return df["customer_id"].nunique()


def get_category_sales(df):
    return (
        df.groupby("category", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )


def get_monthly_sales(df):
    result = df.copy()

    result["order_date"] = pd.to_datetime(
        result["order_date"]
    )

    result["month"] = (
        result["order_date"].dt.to_period("M").astype(str)
    )

    return (
        result.groupby("month", as_index=False)["revenue"]
        .sum()
        .sort_values("month")
    )


def get_top_products(df, limit=10):
    return (
        df.groupby("product", as_index=False)
        .agg(
            total_quantity=("quantity", "sum"),
            total_revenue=("revenue", "sum")
        )
        .sort_values("total_quantity", ascending=False)
        .head(limit)
    )
    