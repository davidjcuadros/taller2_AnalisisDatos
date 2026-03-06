import pandas as pd


def extract_sales(engine):

    query = """
    SELECT
        soh.salesorderid AS order_id,
        soh.customerid,
        soh.orderdate,
        sod.productid,
        sod.orderqty AS quantity,
        sod.unitprice,
        p.standardcost
    FROM sales.salesorderheader soh
    JOIN sales.salesorderdetail sod
        ON soh.salesorderid = sod.salesorderid
    JOIN production.product p
        ON sod.productid = p.productid
    """

    df = pd.read_sql(query, engine)

    return df


def extract_customers(engine):

    query = """
    SELECT
        customerid
    FROM sales.customer
    """

    return pd.read_sql(query, engine)


def extract_products(engine):

    query = """
    SELECT
        productid,
        name,
        standardcost,
        listprice
    FROM production.product
    """

    return pd.read_sql(query, engine)