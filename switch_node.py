#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Name   : a_switch_node.py
Author      : wzw
Date Created: 2025/4/21
Description : Add your script's purpose here.
"""
import time
import random
import requests
import urllib.parse
from log_utils import init_logger


class ClashManager:
    def __init__(
            self,
            clash_api_url="http://127.0.0.1:9090",
            selector_name="GLOBAL",
            group_map=None,
            socks5_host="127.0.0.1",
            socks5_port=7891,
            secret="",
            max_delay=1000,
            min_limit=5,
            exclude_nodes=None,
    ):
        # 使用类名创建 logger，输出时会带上类名作为日志源
        self.logger = init_logger('github', self.__class__.__name__)

        # Clash 控制面板 API 地址
        self.api = clash_api_url
        # 要操作的策略组名称
        self.selector = selector_name
        # 策略组到显示名的映射，若未传入则使用默认
        self.group_map = group_map or {"GLOBAL": "国外流量"}

        # 本地 SOCKS5 代理，用于访问网络时走代理
        self.proxies = {
            "http": f"socks5h://{socks5_host}:{socks5_port}",
            "https": f"socks5h://{socks5_host}:{socks5_port}",
        }

        # API 鉴权头，如果 secret 为空则不添加 Authorization
        self.headers = {"Authorization": f"Bearer {secret}"} if secret else {}

        # 延迟阈值：只有历史延迟都小于等于该值的节点才会被视为可用
        self.max_delay = max_delay
        # 最少可用节点数，不足时不执行切换
        self.min_limit = min_limit

        # 需要排除的节点列表，不希望自动选择这些节点
        self.exclude_nodes = exclude_nodes or [
            '国外流量', 'ChatGPT', '香港负载组', '台湾负载组',
            '新加坡负载组', '日本负载组', '美国负载组', '直接连接',
        ]

        # 当前已切换到的节点名称，初始时为空
        self.cur_node = None

    # 显示所有策略组及其所有节点和状态
    def show_group(self):
        res = requests.get(f"{self.api}/proxies", headers=self.headers)
        proxies = res.json().get("proxies", {})
        for name, info in proxies.items():
            if isinstance(info, dict) and "all" in info:
                self.logger.info("策略组 %s: 类型=%s 当前=%s 可选=%s",
                                 name, info.get("type"), info.get("now"), info["all"])

    # 获取所有节点
    def get_all_nodes(self):
        res = requests.get(f"{self.api}/proxies", headers=self.headers)
        if res.status_code != 200:
            self.logger.error("获取代理列表失败: %s", res.text)
            return []

        proxies = res.json().get("proxies", {})
        nodes = proxies.get(self.selector, {}).get("all", [])
        valid = []
        for node in nodes:
            if any(ex in node for ex in self.exclude_nodes):
                continue
            hist = proxies.get(node, {}).get("history", [])
            if not hist:
                continue
            # 全部延迟都在合理范围
            if all(0 < item.get("delay", 0) <= self.max_delay for item in hist):
                valid.append(node)

        self.logger.info("有效节点列表: %s", valid)
        return valid

    # 随机切换到另一个节点
    def change_random_node(self):
        candidates = self.get_all_nodes()
        if len(candidates) < self.min_limit:
            self.logger.error("有效节点不足(%d)，无法切换。", len(candidates))
            return False

        sel = random.choice(candidates)
        payload = {"name": sel}
        group = urllib.parse.quote(self.group_map[self.selector])
        res = requests.put(f"{self.api}/proxies/{group}",
                           headers=self.headers, json=payload)
        if res.status_code == 204:
            self.cur_node = sel
            self.logger.info("切换到节点: %s", sel)
            return True
        else:
            self.logger.error("切换节点失败: %s", res.text)
            return False

    # 测试当前 IP
    def ip_test(self):
        self.logger.info("正在测试当前 IP...")
        time.sleep(1)
        try:
            r = requests.get("http://ip-api.com/json", proxies=self.proxies, timeout=5)
            data = r.json()
            self.logger.info("IP=%s, Country=%s", data.get("query"), data.get("country"))
        except Exception as e:
            self.logger.error("IP 测试出错: %s", e)


if __name__ == '__main__':
    # 创建 ClashManager 实例
    group_map = {
        # "GLOBAL": "FlyintPro",
        # "GLOBAL": "蛋挞云",
        "GLOBAL": "两元店",
        # "GLOBAL": "🌀 手动选择",
    }
    node_manager = ClashManager(group_map=group_map)
    node_manager.show_group()
    node_manager.change_random_node()
    node_manager.ip_test()
