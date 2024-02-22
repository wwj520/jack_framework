# -*- coding:utf-8 -*-
# Author: Jack
# Date: 2024/2/21
from jack_framework.spider import Spider


class BaseSpider(Spider):

    start_urls = ["https://www.baidu.com", "https://www.baidu.com"]

    def start_requests(self):
        print("初始发送")
        return self.start_urls
