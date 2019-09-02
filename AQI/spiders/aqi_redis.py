# -*- coding: utf-8 -*-
import scrapy
from AQI.items import AqiItem
from scrapy_redis.spiders import RedisSpider


# 修改继承关系
class AqiSpider(RedisSpider):
    name = 'aqi_redis'
    allowed_domains = ['aqistudy.cn']
    base_url = 'https://www.aqistudy.cn/historydata/'

    # redis_key
    redis_key = 'aqi'

    # 解析城市名称
    def parse(self, response):
        city_name_list = response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/ul/div[2]/li/a/text()').extract()[
                         2:3]
        city_link_list = response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/ul/div[2]/li/a/@href').extract()[
                         2:3]

        for city_name, city_link in zip(city_name_list, city_link_list):
            item = AqiItem()
            item['city_name'] = city_name

            # 拼接url
            city_url = self.base_url + city_link

            # 发送城市月份天气请求
            yield scrapy.Request(city_url, callback=self.parse_month, meta={'aqi': item})

    # 解析月份
    def parse_month(self, response):
        # 接受从城市列表传过来的item
        item = response.meta['aqi']

        month_link_list = response.xpath('/html/body/div[3]/div[1]/div[1]/table/tbody/tr/td[1]/a/@href').extract()

        # 拼接月份请求的url
        for month_link in month_link_list[:1]:
            month_link = self.base_url + month_link

            # 发送城市每月下每天的天气请求
            yield scrapy.Request(month_link, callback=self.parse_day, meta={'aqi': item})

    # 解析每天天气
    def parse_day(self, response):
        # 接受从月份列表传过来的item
        item = response.meta['aqi']

        # 取出所有行数的tr标签
        tr_list = response.xpath('//tr')
        # 删除第一行，表头
        tr_list.pop(0)

        # 遍历tr,取出数据
        for tr in tr_list:
            # 日期
            item['date'] = tr.xpath('./td[1]/text()').extract()
            # AQI
            item['aqi'] = tr.xpath('./td[2]/text()').extract()
            # 质量等级
            item['level'] = tr.xpath('./td[3]/span/text()').extract()
            # PM2.5
            item['PM2_5'] = tr.xpath('./td[4]/text()').extract()
            # PM10
            item['PM10'] = tr.xpath('./td[5]/text()').extract()
            # SO2
            item['SO2'] = tr.xpath('./td[6]/text()').extract()
            # CO
            item['CO'] = tr.xpath('./td[7]/text()').extract()
            # NO2
            item['NO2'] = tr.xpath('./td[8]/text()').extract()
            # O3 8h
            item['O3'] = tr.xpath('./td[9]/text()').extract()

            yield item
