# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AqiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass

    city_name = scrapy.Field()
    # 日期
    date = scrapy.Field()
    # AQI
    aqi = scrapy.Field()
    # 质量等级
    level = scrapy.Field()
    # PM2.5
    PM2_5 = scrapy.Field()
    # PM10
    PM10 = scrapy.Field()
    # SO2
    SO2 = scrapy.Field()
    # CO
    CO = scrapy.Field()
    # NO2
    NO2 = scrapy.Field()
    # O3 8h
    O3 = scrapy.Field()

    # 抓取时间
    crawl_time = scrapy.Field()
    # 爬虫名称
    spider = scrapy.Field()