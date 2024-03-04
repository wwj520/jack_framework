# -*- coding:utf-8 -*-
# Author: Jack
# Date: 2024/2/28

"""
配置管理
"""
from copy import deepcopy
from importlib import import_module
from jack_framework.settings import default_settings
from collections.abc import MutableMapping


class SettingManager(MutableMapping):

    def __init__(self, value_settings=None):
        self.attributes = {}
        self.set_settings(default_settings)  # 先导入默认的配置，再用自己的配置更新
        self.update_settings(value_settings)

    def __iter__(self):
        return iter(self.attributes)

    def __len__(self):
        return len(self.attributes)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __getitem__(self, key):
        # 'in' 在解释器内调用的__contains__函数，not in self.attributes就可以写为 not in self
        if key not in self:
            return None
        return self.attributes[key]

    def __contains__(self, key):
        return key in self.attributes

    def __delitem__(self, key):
        del self.attributes[key]

    def set(self, name, value):
        self.attributes[name] = value

    def get(self, name, default=None):
        return self[name] if name in self else default

    def getint(self, name, default=0):
        return int(self.get(name, default))

    def getfloat(self, name, default=0.0):
        return float(self.get(name, default))

    def get_list(self, name, default=None):
        value = self.get(name, default or [])
        if isinstance(value, str):
            value = value .split(',')
        return list(value)

    def getbool(self, name, default=False): # noqa
        """兼容获取到的属性值：TRUE 'TRUE' FALSE 'FALSE' ... """
        got = self.get(name, default=default)
        try:
            return bool(int(got))
        except ValueError:
            if got.lower() == 'true':
                return True
            elif got.lower() == 'false':
                return False
            raise ValueError('获取配置属性为布尔值的位置异常')

    def set_settings(self, module):
        """
        动态读取模块并设置
        :param module: 可以是字符串也可是模块对象
        :return:
        """
        if isinstance(module, str):
            module = import_module(module)
        for key in dir(module):
            if key.isupper():
                self.set(key, getattr(module, key))

    def update_settings(self, value_settings: dict): # noqa
        """
        兼容在 SettingManager类中实例化时，直接传入配置项
        eg:
              _settings = SettingManager({"TIMEOUT": 5})
        """
        if value_settings:
            for key, value in value_settings.items():
                self.set(key, value)

    def __str__(self):
        return f"[settings vale: {self.attributes}]"

    def copy(self):
        """深拷贝可变对象，解决同时多个脚本并发配置"""
        return deepcopy(self)

    __repr__ = __str__


