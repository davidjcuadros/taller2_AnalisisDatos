CREATE SCHEMA IF NOT EXISTS olap;

CREATE TABLE olap.dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    customer_name TEXT,
    city TEXT,
    country TEXT,
    first_purchase_date DATE,
    cohort_year INT,
    cohort_month INT,
    UNIQUE(customer_id)
);

CREATE TABLE olap.dim_product (
    product_key SERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    product_name TEXT,
    subcategory TEXT,
    category TEXT,
    standard_cost NUMERIC(12,2),
    list_price NUMERIC(12,2),
    UNIQUE(product_id)
);

CREATE TABLE olap.dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL,
    year INT,
    month INT,
    month_name TEXT,
    quarter INT,
    week INT,
    is_christmas_season BOOLEAN
);

CREATE TABLE olap.fact_sales (
    sales_key SERIAL PRIMARY KEY,

    order_id INT NOT NULL,

    customer_key INT REFERENCES olap.dim_customer(customer_key),
    product_key INT REFERENCES olap.dim_product(product_key),
    date_key INT REFERENCES olap.dim_date(date_key),

    quantity INT NOT NULL,
    unit_price NUMERIC(12,2),
    unit_cost NUMERIC(12,2),

    revenue NUMERIC(14,2),
    margin NUMERIC(14,2)
);

CREATE INDEX idx_fact_sales_customer ON olap.fact_sales(customer_key);
CREATE INDEX idx_fact_sales_product ON olap.fact_sales(product_key);
CREATE INDEX idx_fact_sales_date ON olap.fact_sales(date_key);
CREATE INDEX idx_fact_sales_order ON olap.fact_sales(order_id);