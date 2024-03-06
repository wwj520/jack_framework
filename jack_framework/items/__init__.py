# -*- coding:utf-8 -*-
# Author: Jack
# Date: 2024/3/5
"""
数据容器
"""
from abc import ABCMeta, abstractmethod


class Field(dict):

    pass


class ItemMeta(ABCMeta):

    def __new__(mcs, name, bases, attrs):
        """
        元类继承 控制类的产生
        :param name:  类名
        :param bases: 父类的元组（对于继承，可以为空）
        :param attrs: 包含属性名称和值的字典
        """

        field = {}
        for k, v in attrs.items():
            if isinstance(v, Field):
                field[k] = v
        # 生成类
        cls_instance = super().__new__(mcs, name, bases, attrs)
        cls_instance.FIELDS = field
        return cls_instance
