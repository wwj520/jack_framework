# -*- coding:utf-8 -*-
# Author: Jack
# Date: 2024/2/21
"""下载器"""
import asyncio
import requests
import time


class Downloader(object):

    def __init__(self):
        pass

    async def fetch(self, request):
        return await self.download(request)

    async def download(self, request):
        # response = requests.get(request.url)
        # (response)
        await asyncio.sleep(0.1)
        return "get result successfully"


