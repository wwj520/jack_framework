# -*- coding:utf-8 -*-
# Author: Jack
# Date: 2024/2/27
"""
task管理
"""
import asyncio
from typing import Set, Final
from asyncio import Task, Future, Semaphore


class TaskManager:

    def __init__(self, total_concurrency=10):
        """
        :param total_concurrency: 默认并发数
        """
        self.current_task: Final[Set] = set()
        self.semaphore: Semaphore = Semaphore(total_concurrency)

    def create_task(self, coroutine) -> Task:
        """
        :param coroutine: 传入请求的协程对象
        :return:
        """
        task = asyncio.create_task(coroutine)
        self.current_task.add(task)

        def done_task(_future: Future):
            self.current_task.remove(task)
            self.semaphore.release()

        # Future对象完成时被调用
        task.add_done_callback(done_task)

    def all_done(self) -> bool:
        """判断当前所有tasks任务是否为空"""
        return len(self.current_task) == 0
