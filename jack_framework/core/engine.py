# -*- coding:utf-8 -*-
# Author: Jack
# Date: 2024/2/21
"""
引擎脚本: 负责串联爬虫【框架核心】
"""
from typing import Generator, Optional
from jack_framework.core.download import Downloader
from jack_framework.core.scheduler import Scheduler


class Engine(object):

    def __init__(self):
        self.downloader: Downloader = Downloader()
        self.start_requests: Optional[Generator] = None
        self.scheduler: Optional[Scheduler] = None

    async def start_spider(self, spider):
        self.scheduler = Scheduler()
        if hasattr(self.scheduler, "open"):
            self.scheduler.open()
        self.downloader = Downloader()
        self.start_requests = iter(spider.start_requests())  # 用iter是为了防止继承者重写start_requests，不适用yield，强制转为迭代器
        await self.crawl()

    async def crawl(self):
        """主逻辑"""
        while True:
            if request := await self._get_next_request() is not None:
                await self._crawl(request)
            else:
                try:
                    start_request = next(self.start_requests)  # todo
                    # start_request = next([])  # todo
                except StopIteration:
                    print('结束')
                    self.start_requests = None
                except Exception as e:
                    # 捕获非Generator的错误
                    break
                else:
                    # 入队
                    await self.enqueue_request(start_request)

    async def enqueue_request(self, request):
        await self._scheduler_request(request)

    async def _scheduler_request(self, request):
        # todo 去重
        await self.scheduler.enqueue_request(request)

    async def _get_next_request(self):
        """从队列获取请求"""
        return await self.scheduler.next_request()

    async def _crawl(self, request):
        await self.downloader.download(request)
