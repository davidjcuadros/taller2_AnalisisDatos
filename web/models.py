from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class DimCustomer(Base):
    __tablename__ = "dim_customer"
    __table_args__ = {"schema": "olap"}

    customer_key = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    first_purchase_date = Column(Date)
    cohort_year = Column(Integer)
    cohort_month = Column(Integer)


class DimProduct(Base):
    __tablename__ = "dim_product"
    __table_args__ = {"schema": "olap"}

    product_key = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    product_name = Column(String)
    standard_cost = Column(Numeric)
    list_price = Column(Numeric)


class DimDate(Base):
    __tablename__ = "dim_date"
    __table_args__ = {"schema": "olap"}

    date_key = Column(Integer, primary_key=True)
    full_date = Column(Date)
    year = Column(Integer)
    month = Column(Integer)
    month_name = Column(String)
    quarter = Column(Integer)
    week = Column(Integer)
    is_christmas_season = Column(Boolean)


class FactSales(Base):
    __tablename__ = "fact_sales"
    __table_args__ = {"schema": "olap"}

    sales_key = Column(Integer, primary_key=True)

    order_id = Column(Integer)

    customer_key = Column(Integer, ForeignKey("olap.dim_customer.customer_key"))
    product_key = Column(Integer, ForeignKey("olap.dim_product.product_key"))
    date_key = Column(Integer, ForeignKey("olap.dim_date.date_key"))

    quantity = Column(Integer)
    unit_price = Column(Numeric)
    unit_cost = Column(Numeric)

    revenue = Column(Numeric)
    margin = Column(Numeric)