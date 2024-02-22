# -*- coding:utf-8 -*-
# Author: Jack
# Date: 2024/2/21
import asyncio

from jack_framework.core.engine import Engine
from tests.baidu_spider.baidu import BaseSpider


async def run():
    baidu_spider = BaseSpider()
    await Engine().start_spider(baidu_spider)


if __name__ == '__main__':
    asyncio.run(run())