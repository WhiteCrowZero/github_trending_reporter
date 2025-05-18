#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Name   : config_set.py
Author      : wzw
Date Created: 2025/5/18
Description : Add your script's purpose here.
"""

import configparser
from pathlib import Path

# —— 1. 读取配置文件 ——
CONFIG_FILE = './github_config.ini'
parser = configparser.ConfigParser(interpolation=None)
parser.read(CONFIG_FILE, encoding='utf-8')


# —— 2. 配置类 ——
class Config:
    """
    集中管理配置项：Token、代理、路径、Webhook 等
    """

    def __init__(self):
        # GitHub Token
        self.github_token = parser.get('github', 'token', fallback='')

        # 代理配置
        self.proxies = {
            "http": parser.get('proxy', 'http', fallback=''),
            "https": parser.get('proxy', 'https', fallback=''),
        }

        # 存储路径
        self.base_dir = Path(parser.get('path', 'base_dir', fallback='/tmp/github_data'))

        # 企业微信通知
        self.qiwx_webhook_url = parser.get('notify', 'qiwx_webhook_url', fallback='')


# 全局可用配置对象
config = Config()
