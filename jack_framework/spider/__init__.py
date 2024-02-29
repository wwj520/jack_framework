# -*- coding:utf-8 -*-
# Author: Jack
# Date: 2024/2/21
from jack_framework import Request


class Spider(object):
    def __init__(self):
        if not hasattr(self, "start_urls"):
            self.start_urls = []
        self.crawler = None  # 在crawler.py中需要

    @classmethod
    def create_instance(cls, crawler, *args, **kwargs):
        """动态创建实例"""
        o = cls()
        o.crawler = crawler
        return o

    def start_requests(self):
        """起始方法"""
        if self.start_urls:
            for url in self.start_urls:
                yield Request(url=url)
        else:
            if hasattr(self, "start_url") and isinstance(getattr(self, "start_url"), str):
                yield Request(url=getattr(self, "start_url"))

    def parse(self, response):
        raise NotImplementedError("parse method not implemented")
