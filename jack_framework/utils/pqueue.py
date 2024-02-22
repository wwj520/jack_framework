# -*- coding:utf-8 -*-
# Author: Jack
# Date: 2024/2/22
"""
队列类
"""
import asyncio
from asyncio import PriorityQueue


class SpiderPriorityQueue(PriorityQueue):

    def __init__(self, maxsize=0):
        super(PriorityQueue, self).__init__(maxsize=maxsize)

    async def get(self):
        """重写get"""
        f = super().get()
        try:
            # f:协程对象或者任务
            return await asyncio.wait_for(f, timeout=0.1)
        except TimeoutError:
            return None
