# -*- coding:utf-8 -*-
# Author: Jack
# Date: 2024/3/5

from jack_framework.items import Field
from typing import Dict


class Item:

    FIELDS: Dict = dict()

    def __init__(self):
        for cls_attr, value in self.__class__.__dict__.items():
            if isinstance(value, Field):
                self.FIELDS[cls_attr] = value
        print(self.FIELDS)

    def __setitem__(self, key, value):
        pass

    def __getitem__(self, key):
        pass


if __name__ == '__main__':
    class TestItem(Item):
        url = Field()
        title = Field()

    x = TestItem()