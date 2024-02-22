# -*- coding:utf-8 -*-
# Author: Jack
# Date: 2024/2/22
from inspect import isgenerator, isasyncgen
from jack_framework.exceptions import TransformError


async def transform(func_res):
    """callback转换，得到的都是async generator"""
    if isgenerator(func_res):
        for r in func_res:
            yield r
    elif isasyncgen(func_res):
        async for r in func_res:
            yield r
    else:
        raise TransformError("callback must be a generator or async generator")
