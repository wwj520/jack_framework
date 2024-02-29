# -*- coding:utf-8 -*-
# Author: Jack
# Date: 2024/2/21
import asyncio

from jack_framework.core.engine import Engine
from tests.baidu_spider.spiders.baidu import BaseSpider
from tests.baidu_spider.spiders.baidu2 import BaseSpider2
from jack_framework.utils.project import get_project_settings
from jack_framework.crawler import CrawlerProcess


async def run():
    settings = get_project_settings("settings")
    process = CrawlerProcess(settings)
    # 同时创建两个测试
    await process.crawl(BaseSpider)
    await process.crawl(BaseSpider2)
    await process.crawl_start()


if __name__ == '__main__':
    import time
    a = time.time()
    asyncio.run(run())
    print("耗时:", time.time()-a)
