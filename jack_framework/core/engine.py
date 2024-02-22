# -*- coding:utf-8 -*-
# Author: Jack
# Date: 2024/2/21
"""
引擎脚本: 负责串联爬虫【框架核心】
"""
import asyncio
from typing import Generator, Optional, Callable
from jack_framework.core.download import Downloader
from jack_framework.core.scheduler import Scheduler
from jack_framework.spider import Spider
from inspect import iscoroutine
from jack_framework.utils.spider import transform


class Engine(object):

    def __init__(self):
        self.downloader: Downloader = Downloader()
        self.start_requests: Optional[Generator] = None
        self.scheduler: Optional[Scheduler] = None
        self.spider: Optional[Spider] = None

    async def start_spider(self, spider):
        self.spider = spider
        self.scheduler = Scheduler()
        if hasattr(self.scheduler, "open"):
            self.scheduler.open()
        self.downloader = Downloader()
        self.start_requests = iter(spider.start_requests())  # 用iter是为了防止继承者重写start_requests，不适用yield，强制转为迭代器
        await self._open_spider()

    async def _open_spider(self):
        """做爬取额外的事情"""
        await asyncio.create_task(self.crawl())

    async def crawl(self):
        """主逻辑"""
        while True:
            if (request := await self._get_next_request()) is not None:
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
        # todo 实现并发
        outputs = await self._fetch(request)
        # 处理outputs
        if outputs:
            async for output in outputs:
                print(output)

    async def _fetch(self, request):
        async def _success(_response):
            callback: Callable = request.callback or self.spider.parse
            if _outputs := callback(_response):
                # 判断是否是协程对象
                if iscoroutine(_outputs):
                    await _outputs
                else:
                    return transform(_outputs)

        _response = await self.downloader.fetch(request)
        outputs = await _success(_response)
        return outputs
