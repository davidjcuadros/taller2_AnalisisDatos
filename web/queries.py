from sqlalchemy import select, func, case

from sqlalchemy.orm import aliased
from models import FactSales, DimProduct, DimCustomer, DimDate


# 1️⃣ Porcentaje ingresos clientes recurrentes
def q1_revenue_recurrent_customers():

    # Número de órdenes por cliente
    orders_per_customer = (
        select(
            FactSales.customer_key,
            func.count(func.distinct(FactSales.order_id)).label("orders")
        )
        .group_by(FactSales.customer_key)
        .subquery()
    )

    # Revenue por cliente
    revenue_per_customer = (
        select(
            FactSales.customer_key,
            func.sum(FactSales.revenue).label("revenue")
        )
        .group_by(FactSales.customer_key)
        .subquery()
    )

    # Clasificar cliente
    classified = (
        select(
            revenue_per_customer.c.revenue,
            case(
                (orders_per_customer.c.orders == 1, "single_purchase"),
                else_="recurrent"
            ).label("customer_type")
        )
        .join(
            orders_per_customer,
            revenue_per_customer.c.customer_key == orders_per_customer.c.customer_key
        )
        .subquery()
    )

    # Revenue total
    total_revenue = select(func.sum(classified.c.revenue)).scalar_subquery()

    # Resultado final
    stmt = (
        select(
            classified.c.customer_type,
            func.sum(classified.c.revenue).label("revenue"),
            (
                func.sum(classified.c.revenue) / total_revenue * 100
            ).label("percentage")
        )
        .group_by(classified.c.customer_type)
    )

    return stmt


# 2️⃣ Productos con mayor varianza de margen
def q2_margin_variance_products():

    stmt = (
        select(
            DimProduct.product_name,
            func.variance(FactSales.margin).label("margin_variance")
        )
        .join(FactSales, DimProduct.product_key == FactSales.product_key)
        .group_by(DimProduct.product_name)
        .order_by(func.variance(FactSales.margin).desc())
        .limit(10)
    )

    return stmt


# 3️⃣ Top 10 pares de productos (Market Basket)
def q3_market_basket():

    f1 = aliased(FactSales)
    f2 = aliased(FactSales)

    p1 = aliased(DimProduct)
    p2 = aliased(DimProduct)

    stmt = (
        select(
            p1.product_name.label("product_1"),
            p2.product_name.label("product_2"),
            func.count().label("frequency")
        )
        .select_from(f1)
        .join(f2, (f1.order_id == f2.order_id) & (f1.product_key < f2.product_key))
        .join(p1, f1.product_key == p1.product_key)
        .join(p2, f2.product_key == p2.product_key)
        .group_by(p1.product_name, p2.product_name)
        .order_by(func.count().desc())
        .limit(10)
    )

    return stmt


from sqlalchemy import select, func
from models import FactSales, DimCustomer, DimDate


def q4_cohort_analysis():

    # 1️⃣ margen total por cohorte
    cohort_margin = (
        select(
            DimCustomer.cohort_year,
            DimCustomer.cohort_month,
            func.sum(FactSales.margin).label("total_margin")
        )
        .join(FactSales, DimCustomer.customer_key == FactSales.customer_key)
        .group_by(
            DimCustomer.cohort_year,
            DimCustomer.cohort_month
        )
        .order_by(func.sum(FactSales.margin).desc())
        .limit(3)
        .subquery()
    )

    # 2️⃣ análisis mensual solo para las top 3 cohortes
    stmt = (
        select(
            DimCustomer.cohort_year,
            DimCustomer.cohort_month,
            DimDate.year.label("order_year"),
            DimDate.month.label("order_month"),
            func.count(func.distinct(FactSales.customer_key)).label("customers"),
            func.sum(FactSales.margin).label("margin")
        )
        .join(FactSales, DimCustomer.customer_key == FactSales.customer_key)
        .join(DimDate, FactSales.date_key == DimDate.date_key)
        .join(
            cohort_margin,
            (DimCustomer.cohort_year == cohort_margin.c.cohort_year) &
            (DimCustomer.cohort_month == cohort_margin.c.cohort_month)
        )
        .group_by(
            DimCustomer.cohort_year,
            DimCustomer.cohort_month,
            DimDate.year,
            DimDate.month
        )
        .order_by(
            DimCustomer.cohort_year,
            DimCustomer.cohort_month,
            DimDate.year,
            DimDate.month
        )
    )

    return stmt