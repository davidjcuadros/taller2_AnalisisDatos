def load_table(df, table_name, engine):

    df.to_sql(
        table_name,
        engine,
        schema="olap",
        if_exists="append",
        index=False
    )