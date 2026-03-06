from src.db import get_engine
from src.extract import extract_sales, extract_products, extract_customers
from src.transform import (
    transform_products,
    transform_customers,
    transform_date,
    transform_fact_sales
)
from src.load import load_table

import pandas as pd

def run_etl():

    engine = get_engine()

    print("Extracting data...")

    df_sales = extract_sales(engine)
    df_products = extract_products(engine)
    df_customers = extract_customers(engine)

    print("Transforming dimensions...")

    dim_product = transform_products(df_products)
    dim_customer = transform_customers(df_customers, df_sales)
    dim_date = transform_date(df_sales)

    print("Loading dimensions...")

    load_table(dim_product, "dim_product", engine)
    load_table(dim_customer, "dim_customer", engine)
    load_table(dim_date, "dim_date", engine)

    dim_product_db = pd.read_sql("SELECT * FROM olap.dim_product", engine)
    dim_customer_db = pd.read_sql("SELECT * FROM olap.dim_customer", engine)
    dim_date_db = pd.read_sql("SELECT * FROM olap.dim_date", engine)

    print("Transforming fact table...")

    fact_sales = transform_fact_sales(
        df_sales,
        dim_customer_db,
        dim_product_db,
        dim_date_db
    )

    print("Loading fact table...")

    load_table(fact_sales, "fact_sales", engine)

    print("ETL completed!")

if __name__ == "__main__":
    run_etl()