# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from functools import reduce
import psycopg2

class ZufangfenxiPipeline(object):

    def process_item(self, item, spider):
        if item['price'] and item['price'].find('-') > 0:
            lists = item['price'].split('-')
            price = reduce(lambda x,y:int(x) + int(y), lists)
            item['price'] = str(round(price / len(lists)))
        return item

    def item_completed(self, results, item, info):
        return item


class PostgresPipeline(object):

    def __init__(self):
        self.connection = psycopg2.connect(database='scrapy', host='47.93.220.203', port='5432', user='postgres', password='postgres')
        # self.connection.commit = True

    def open_spider(self, spider):
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        self.cursor.execute('insert into 租房(area,price,position,rooms, url, origin) values(%s,%s, %s,%s,%s,%s)', (item['area'], item['price'], item['position'], item['rooms'], item['url'], '链家网'))
        self.connection.commit()
        return item