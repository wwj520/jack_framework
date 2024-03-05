# -*- coding:utf-8 -*-
# Author: Jack
# Date: 2024/3/5
from jack_framework.items import Field
from jack_framework import Item


class BaiduSpiderItem(Item):

    url = Field()
    title = Field()
