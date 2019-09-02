# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from AQI.items import AqiItem


class AqiSpider(CrawlSpider):
    name = 'aqi_crawl'
    allowed_domains = ['aqistudy.cn']

    start_urls = 'https://www.aqistudy.cn/historydata/'

    # 请求的规则
    rules = (
        Rule(LinkExtractor(allow='monthdata')),
        Rule(LinkExtractor(allow='daydata'), callback='parse_data'),
    )

    # 解析数据
    def parse_data(self, response):

        item = AqiItem()
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
            item['PM10'] = tr.xpath('./td[5]/text()').extractt()
            # SO2
            item['SO2'] = tr.xpath('./td[6]/text()').extract()
            # CO
            item['CO'] = tr.xpath('./td[7]/text()').extract()
            # NO2
            item['NO2'] = tr.xpath('./td[8]/text()').extract()
            # O3 8h
            item['O3'] = tr.xpath('./td[9]/text()').extract()

            yield item
