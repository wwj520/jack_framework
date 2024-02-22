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

    async def download(self, url):
        # response = requests.get(url)
        # print(response)
        await asyncio.sleep(0.1)
        print("get  ")


