# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime
from scrapy.exporters import JsonItemExporter, CsvItemExporter
import redis
import pymongo


# 数据流管道
# 无论是什么数据，都经过此管道标明具体爬虫、抓取的时间
class AqiDataPipeline(object):
    def process_item(self, item, spider):
        # 抓取时间
        item['crawl_time'] = datetime.utcnow()
        # 爬虫名称
        # item['spider'] = spider.name()

        return item


# json管道
# 写入文件，设计文件都打开与关闭
class AqiJsonPipeline(object):
    def open_spider(self, spider):
        self.file = open('aqi.json', 'wb')
        self.writer = JsonItemExporter(self.file)

    def close_spider(self, spider):
        self.writer.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.writer.export_item(item)
        return item


# csv管道
# 可以用excl打开的表格形式
class AqiCsvPipeline(object):
    def open_spider(self, spider):
        self.file = open('aqi.csv', 'wb')
        self.writer = CsvItemExporter(self.file)

    def close_spider(self, spider):
        self.writer.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.writer.export_item(item)
        return item


# redis管道
# 可以用excl打开的表格形式
class AqiReidsPipeline(object):
    # redis中没有close去关闭数据库，所以只需要连接打开就可以了
    def open_spider(self, spider):
        # 链接数据库
        self.client = redis.StrictRedis(host='127.0.0.1', port=6379)
        # 储存的key
        self.save_key = 'aqi_redis'

    def process_item(self, item, spider):
        self.client.lpush(self.save_key, dict(item))
        return item


# mongodb管道
class AqiMongodbPipeline(object):
    def open_spider(self, spider):
        # 链接数据库
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        # 数据库名字和集合名字
        self.collection = self.client.AQI.aqi

    # mongodb是可以关闭数据库的，但是不关闭也不影响
    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item
