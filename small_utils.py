#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Name   : small_utils.py
Author      : wzw
Date Created: 2025/5/18
Description : 一些辅助函数
"""

import os
import time
import requests
from datetime import datetime
from log_utils import init_logger

module_name = os.path.splitext(os.path.basename(__file__))[0]
logger = init_logger('utils', module_name)


def ip_test(proxies):
    """
    先测试传入的代理 IP 能否正常访问，如果失败，则回退测试直连。
    """

    def _do_test(session_proxies):
        """
        内部函数：用给定的 proxies 测试 ip-api.com 和 github.com
        返回 True/False，表示是否测试成功
        """
        try:
            # 测试 IP 信息
            r = requests.get("http://ip-api.com/json", proxies=session_proxies, timeout=5)
            r.raise_for_status()
            data = r.json()
            ip = data.get("query")
            ip = ip.split('.')[:2] + ["xxx", "xxx"]
            logger.info("当前 IP=%s (%s)", '.'.join(ip), data.get("country"))

            # 测试能否访问 GitHub
            gh = requests.get("https://github.com", proxies=session_proxies, timeout=5)
            gh.raise_for_status()
            logger.info("访问 GitHub 成功")
            return True

        except Exception as e:
            logger.warning("测试失败: %s", e)
            return False

    # 测试直连
    logger.info("正在测试直连网络...")
    if _do_test(None):
        return True, "DIRECT"

    # 测试代理
    logger.warning("直连测试失败，尝试代理模式")
    time.sleep(2)
    logger.info("正在测试代理 IP：%s", proxies)
    if _do_test(proxies):
        return True, "PROXIES"

    logger.error("代理测试也失败，请检查网络或代理配置")
    return False, None


def get_current_date(format_str: str = "%Y-%m-%d") -> str:
    """生成当前日期的格式化字符串"""
    return datetime.now().strftime(format_str)


if __name__ == '__main__':
    # 测试1
    PROXIES = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890",
    }
    ip_test(PROXIES)

    # 测试2
    date_str = get_current_date()
    print(date_str)
