FROM postgres:16

WORKDIR /scripts

COPY olap_schema.sql .

CMD ["bash", "-c", "\
  until pg_isready -h postgres -U postgres; do \
    echo 'Waiting for postgres...'; \
    sleep 2; \
  done && \
  psql -h postgres -U postgres -d Adventureworks -f olap_schema.sql"]