# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class Sreality5Pipeline:
    def process_item(self, item, spider):
        return item


class DuplicatesPipeline(object):

    def __init__(self):
        self.names_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter['name'] in self.names_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.names_seen.add(adapter['name'])
            return item

class SavingToPostgresqlPipeline(object):

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.connection = psycopg2.connect(
            host = 'database',
            user = 'postgres',
            password = 'postgres',
            database = 'postgres',
            port = '5432'
        )
        self.curr = self.connection.cursor()

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        try: 
            self.curr.execute(""" INSERT INTO flat (name, location, img_url) VALUES (%s, %s, %s) """,(
                item["name"],
                item["location"],
                item["img_url"]
            ))
        except BaseException as e:
            print(e)

        self.connection.commit()
