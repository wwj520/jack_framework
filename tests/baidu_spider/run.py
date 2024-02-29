# -*- coding:utf-8 -*-
# Author: Jack
# Date: 2024/2/21
import asyncio

from jack_framework.core.engine import Engine
from tests.baidu_spider.baidu import BaseSpider
from jack_framework.utils.project import get_project_settings


async def run():
    settings = get_project_settings("settings")
    baidu_spider = BaseSpider()
    await Engine(settings).start_spider(baidu_spider)


if __name__ == '__main__':
    import time
    a = time.time()
    asyncio.run(run())
    print(time.time()-a)
