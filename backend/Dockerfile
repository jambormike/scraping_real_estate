FROM ubuntu:latest
# using latest tag is allegedly bad practice
# playwright install-deps fails on Debian

RUN apt update

RUN apt install -y libpq-dev

RUN apt install -y pip
RUN pip install scrapy-playwright
RUN pip install psycopg2

RUN playwright install firefox chromium
RUN playwright install-deps

WORKDIR /app
COPY . .

EXPOSE 3000

CMD ["scrapy", "crawl", "flat_spider"]