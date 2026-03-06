import pandas as pd

def transform_products(df_products):

    df = df_products.copy()

    df = df.rename(columns={
        "productid": "product_id",
        "name": "product_name",
        "standardcost": "standard_cost",
        "listprice": "list_price"
    })

    return df


def transform_customers(df_customers, df_sales):

    df = df_customers.copy()

    first_purchase = (
        df_sales.groupby("customerid")["orderdate"]
        .min()
        .reset_index()
    )

    first_purchase["cohort_year"] = first_purchase["orderdate"].dt.year
    first_purchase["cohort_month"] = first_purchase["orderdate"].dt.month

    df = df.merge(first_purchase, on="customerid", how="left")

    df = df.rename(columns={
        "customerid": "customer_id",
        "orderdate": "first_purchase_date"
    })

    return df


def transform_date(df_sales):

    df_dates = pd.DataFrame()

    df_dates["full_date"] = pd.to_datetime(df_sales["orderdate"].unique())

    df_dates["date_key"] = df_dates["full_date"].dt.strftime("%Y%m%d").astype(int)

    df_dates["year"] = df_dates["full_date"].dt.year
    df_dates["month"] = df_dates["full_date"].dt.month
    df_dates["month_name"] = df_dates["full_date"].dt.month_name()
    df_dates["quarter"] = df_dates["full_date"].dt.quarter
    df_dates["week"] = df_dates["full_date"].dt.isocalendar().week

    df_dates["is_christmas_season"] = df_dates["month"].isin([11,12])

    return df_dates


def transform_fact_sales(df_sales, dim_customer, dim_product, dim_date):

    df = df_sales.copy()

    df["revenue"] = df["quantity"] * df["unitprice"]
    df["margin"] = (df["unitprice"] - df["standardcost"]) * df["quantity"]

    df["date_key"] = pd.to_datetime(df["orderdate"]).dt.strftime("%Y%m%d").astype(int)

    df = df.merge(
        dim_customer[["customer_key", "customer_id"]],
        left_on="customerid",
        right_on="customer_id"
    )

    df = df.merge(
        dim_product[["product_key", "product_id"]],
        left_on="productid",
        right_on="product_id"
    )

    df_fact = df[[
        "order_id",
        "customer_key",
        "product_key",
        "date_key",
        "quantity",
        "unitprice",
        "standardcost",
        "revenue",
        "margin"
    ]]

    df_fact = df_fact.rename(columns={
        "unitprice":"unit_price",
        "standardcost":"unit_cost"
    })

    return df_fact