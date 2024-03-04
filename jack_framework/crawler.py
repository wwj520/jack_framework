# -*- coding:utf-8 -*-
# Author: Jack
# Date: 2024/2/16
"""
连接engine和自写的spider；启动爬虫
"""
import asyncio
import inspect

from jack_framework.core.engine import Engine
from jack_framework.settings.settings_manager import SettingManager
from jack_framework.spider import Spider
from typing import Type, Final, Set, Optional
from jack_framework.utils.project import merge_settings


class Crawler:
    """连接engine和自写的spider"""
    def __init__(self, spider: Type[Spider], settings):
        self.spider_cls = spider
        self.spider: Optional[Spider] = None
        self.engine: Optional[Engine] = None
        self.settings: SettingManager = settings.copy()

    async def crawl(self):
        """配置引擎启动"""
        self.spider = self._create_spider()
        self.engine = self._create_engine()
        await self.engine.start_spider(self.spider)

    def _create_spider(self) -> Spider:
        # todo 测试比较与self.spider_cls()的区别
        spider = self.spider_cls.create_instance(self)
        self._set_spider(spider)
        return spider

    def _create_engine(self):
        # 这里将self直接丢进Engine中，是将Crawler中是所有属性方法都传给引擎
        return Engine(self)

    def _set_spider(self, spider):
        merge_settings(spider, self.settings)


class CrawlerProcess(object):
    """爬虫脚本启动类，实现多个脚本并发启动"""

    def __init__(self, settings=None):
        self.settings = settings
        self.crawlers: Final[Set] = set()  # 添加多个启动类并发
        self._active: Final[Set] = set()   #

    async def crawl(self, spider: Type[Spider]):
        crawler: Crawler = self._create_crawler(spider)
        self.crawlers.add(crawler)

        tasks = await self._crawl(crawler)
        self._active.add(tasks)

    @staticmethod
    async def _crawl(crawler):
        """爬虫启动位置"""
        return asyncio.create_task(crawler.crawl())

    def _create_crawler(self, spider_cls) -> Crawler:
        """
        :param spider_cls: 类本身不是实例
        :return: 爬虫类和配置的
        """
        if inspect.isclass(spider_cls):
            crawler = Crawler(spider_cls, self.settings)  # noqa
            return crawler
        raise TypeError('spider_cls is must be Class')

    async def crawl_start(self):
        # asyncio.gather并发执行多个协程
        await asyncio.gather(*self._active)
