# -*- coding:utf-8 -*-
# Author: Jack
# Date: 2024/2/27
"""
1. 获取配置相关
"""
import os
import sys

from jack_framework.settings.settings_manager import SettingManager


def get_setting_module_path(path='.'):
    path = os.path.abspath(path)
    print(path)
    project_path = os.path.dirname(path)
    sys.path.append(project_path)


def get_project_settings(settings="settings"):
    """获取项目配置"""
    _settings = SettingManager()
    get_setting_module_path()
    _settings.set_settings(settings)
    return _settings


def merge_settings(spider, settings):
    if hasattr(spider, "custom_settings"):
        custom_settings = getattr(spider, "custom_settings")
        settings.update_settings(custom_settings)
