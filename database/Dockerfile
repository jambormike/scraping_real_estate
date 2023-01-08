FROM postgres:alpine

ENV POSTGRES_PASSWORD=postgres
COPY create_fixtures.sql /docker-entrypoint-initdb.d/create_fixtures.sql

EXPOSE 5432