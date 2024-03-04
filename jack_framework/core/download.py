# -*- coding:utf-8 -*-
# Author: Jack
# Date: 2024/2/21
"""下载器"""
import asyncio

import requests


class Downloader(object):

    def __init__(self):
        self._active = set()

    async def fetch(self, request):
        self._active.add(request)
        response = await self.download(request)
        self._active.remove(request)
        return response

    async def download(self, request):
        """发送请求下载"""
        # response = requests.get(request.url)
        await asyncio.sleep(0.5)
        return "get result successfully"
        # return response.url

    def idle_task(self) -> bool:
        return len(self) == 0

    def __len__(self):
        return len(self._active)

