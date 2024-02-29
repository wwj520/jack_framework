# -*- coding:utf-8 -*-
# Author: Jack
# Date: 2024/2/22
"""
请求相关
"""

from typing import Optional, Dict, Callable


class Request(object):

    def __init__(
            self, url: str, *,
            method: str = "get",
            headers: Optional[Dict] = None,
            callback: Optional[Callable] = None,
            priority: int = 0,  # 优先级
            cookies: Optional[Dict] = None,
            proxy: Optional[Dict] = None,
            body=''
    ):
        self.url = url
        self.method = method
        self.priority = priority
        self.headers = headers
        self.cookies = cookies
        self.proxy = proxy
        self.body = body
        self.callback = callback

    def __lt__(self, other):
        return self.priority < other.priority

