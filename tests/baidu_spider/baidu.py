# -*- coding:utf-8 -*-
# Author: Jack
# Date: 2024/2/21
from jack_framework import Request
from jack_framework.spider import Spider


class BaseSpider(Spider):

    start_urls = ["https://www.baidu.com", "https://www.baidu.com"]

    def parse(self, response):
        print("1111")
        for i in range(10):
            url = "https://www.baidu"
            request = Request(url=url)
            yield request
