FROM postgres:alpine

# ENV PGUSER=user_47

ENV POSTGRES_PASSWORD=postgres
# ENV POSTGRES_USER=user_47
# ENV POSTGRES_DB=flats_db

COPY create_fixtures.sql /docker-entrypoint-initdb.d/create_fixtures.sql

EXPOSE 5432