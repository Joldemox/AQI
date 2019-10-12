# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html


from scrapy import signals
from selenium import webdriver
import time
import scrapy


# 自定义下载器
# 因为原本的下载器无法对js动态数据进行下载
class AqiDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        # return None

        '''
        至此，自定义发送请求，
        对得到对内容构建成响应对象进行返回
        '''
        url = request.url
        # selenium下载数据
        # 为了节约时间，因为selenium运行速度较慢，所以尽量少用
        if url != 'https://www.aqistudy.cn/historydata/':
            '''只有请求动态界面时才使用'''
            # 创建浏览器对象
            # 创建对为无头浏览器
            driver = webdriver.Chrome()
            # 发送get请求
            driver.get(url)
            # 设置延迟，处于网络考虑
            time.sleep(2)
            # 获取数据
            data = driver.page_source
            # 关闭浏览器
            driver.quit()
            # print(data)

            # 构建响应对象，用于返回给引擎
            return scrapy.http.HtmlResponse(
                url=request.url,
                status=200,
                body=data.encode('utf-8'),
                request=request,
                encoding='utf-8',
            )
