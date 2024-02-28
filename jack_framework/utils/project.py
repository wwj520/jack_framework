# -*- coding:utf-8 -*-
# Author: Jack
# Date: 2024/2/27
from jack_framework.settings.settings_manager import SettingManager


def get_project_settings(settings="settings"):
    """获取项目配置"""
    _settings = SettingManager()
    _settings.set_settings(settings)
    return _settings
