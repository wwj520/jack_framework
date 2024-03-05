# -*- coding:utf-8 -*-
# Author: Jack
# Date: 2024/2/21
from jack_framework import Request
from jack_framework.spider import Spider
from items import BaiduSpiderItem  # type: ignore


class BaseSpider(Spider):

    start_urls = ["https://www.baidu.com", "https://www.baidu.com"]

    def parse(self, response):
        for i in range(10):
            url = "https://www.baidu"
            request = Request(url=url, callback=self.parse_page)
            yield request

    def parse_page(self, response):
        print("parse_page", response)
        for i in range(10):
            url = "https://www.baidu"
            request = Request(url=url, callback=self.parse_detail_page)
            yield request

    def parse_detail_page(self, response):
        print("parse_detail", response)
        item = BaiduSpiderItem()
        item["url"] = response.url
        item["title"] = response


