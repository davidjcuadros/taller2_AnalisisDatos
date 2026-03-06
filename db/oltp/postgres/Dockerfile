FROM postgres:16

RUN apt-get update && apt-get -y install dos2unix

# Crear carpeta de trabajo
RUN mkdir /data

# Copiar TODOS los archivos ya convertidos
COPY data/ /data/

# Script de inicialización
COPY install.sh /docker-entrypoint-initdb.d/

WORKDIR /data/

RUN dos2unix /docker-entrypoint-initdb.d/*.sh