# -*- coding:utf-8 -*-
# Author: Jack
# Date: 2024/3/5

from jack_framework.items import Field, ItemMeta
from typing import Dict


class Item(metaclass=ItemMeta):

    FIELDS: Dict[str, Field] = {}

    def __init__(self):
        self._values = {}
        print(self.FIELDS)

    def __setitem__(self, key, value):
        if key in self.FIELDS:
            self._values[key] = value
        else:
            raise KeyError(key)

    def __getitem__(self, key):
        pass


if __name__ == '__main__':
    class TestItem(Item):
        url = Field()
        title = Field()


    class TestItem2(Item):
        name = Field()
        title = Field()
    x = TestItem()
    y = TestItem2()