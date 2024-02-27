# -*- coding:utf-8 -*-
# Author: Jack
# Date: 2024/2/21
"""
引擎脚本: 负责串联爬虫【框架核心】
"""
import asyncio
from typing import Generator, Optional, Callable
from jack_framework import Request
from jack_framework.core.download import Downloader
from jack_framework.core.scheduler import Scheduler
from jack_framework.exceptions import OutPutError
from jack_framework.spider import Spider
from inspect import iscoroutine
from jack_framework.task_manager import TaskManager
from jack_framework.utils.spider import transform


class Engine(object):

    def __init__(self):
        self.downloader: Downloader = Downloader()
        self.start_requests: Optional[Generator] = None
        self.scheduler: Optional[Scheduler] = None
        self.spider: Optional[Spider] = None
        self.engine_run = False  # engine启动标识--测试
        self.task_manager: Optional[TaskManager] = TaskManager()

    async def start_spider(self, spider):
        self.engine_run = True
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
        print('do something')

    async def crawl(self):
        """主逻辑"""
        while self.engine_run:
            if (request := await self._get_next_request()) is not None:
                await self._crawl(request)
            else:
                try:
                    start_request = next(self.start_requests)  # todo
                    # start_request = next([])  # todo
                except StopIteration:
                    # 协程结束问题的捕获
                    print('结束')
                    self.start_requests = None
                except Exception as e:  # 捕获非Generator的错误
                    # 0. 发送请求的task运行完毕 1. 判断调度器是否空 2.下载器是否空
                    if await self._exit():
                        self.engine_run = False
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
        # 异步处理
        async def crawl_task():
            outputs = await self._fetch(request)
            if outputs:
                await self. _handle_spider_output(outputs)
        # 并发信号量
        await self.task_manager.semaphore.acquire()
        self.task_manager.create_task(crawl_task())

    async def _fetch(self, request):
        """获取结果"""
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

    async def _handle_spider_output(self, outputs):
        async for spider_output in outputs:
            # 判断是数据还是请求
            if isinstance(spider_output, Request):
                await self.enqueue_request(spider_output)
            # todo 判断数据 Item
            # elif 数据
            else:
                raise OutPutError(f'{type(spider_output)} must return Request or Item')

    async def _exit(self):
        """事件循环退出"""
        if self.scheduler.idle() and self.downloader.idle_task() and self.task_manager.all_done():
            return True
        return False
