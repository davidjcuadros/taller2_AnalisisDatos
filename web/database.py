from sqlalchemy import create_engine

def get_engine():

    user = "postgres"
    password = "postgres"
    host = "localhost"
    port = "5432"
    db = "Adventureworks"

    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"

    engine = create_engine(url)

    return engine