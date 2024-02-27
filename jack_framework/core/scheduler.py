# -*- coding:utf-8 -*-
# Author: Jack
# Date: 2024/2/22
"""
调度器：负责队列
"""
from typing import Optional
from jack_framework.utils.pqueue import SpiderPriorityQueue


class Scheduler(object):
    def __init__(self):
        self.request_queue: Optional[SpiderPriorityQueue] = None

    def open(self):
        self.request_queue = SpiderPriorityQueue()

    async def next_request(self):
        """获取请求"""
        request = await self.request_queue.get()
        return request

    async def enqueue_request(self, request):
        """存入请求"""
        await self.request_queue.put(request)

    def idle(self):
        return len(self) == 0

    def __len__(self):
        return self.request_queue.qsize()
