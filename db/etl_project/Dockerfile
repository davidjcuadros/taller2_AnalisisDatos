FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar pg_isready
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["bash", "-c", "\
  until pg_isready -h postgres -U postgres; do \
    echo 'Waiting for postgres...'; \
    sleep 2; \
  done && \
  python main.py"]