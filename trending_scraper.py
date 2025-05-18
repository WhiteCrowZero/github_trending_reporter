#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Name   : trending_scraper.py
Author      : wzw
Date Created: 2025/5/18
Description : 爬 GitHub Trending 页面的基础信息
"""
import os
import time, requests
from lxml import etree
from log_utils import init_logger
from models import BaseRepo
from fake_useragent import UserAgent
from small_utils import ip_test

module_name = os.path.splitext(os.path.basename(__file__))[0]
logger = init_logger('github', module_name)


# 爬虫类
class TrendingScraper:
    BASE_URL_TEMPLATE = "https://github.com/trending/{language}"
    DEFAULT_PARAMS = {"since": "daily", "spoken_language_code": "zh"}
    PROXIES = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890",
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": UserAgent().random,
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept": "text/html,application/xhtml+xml"
        })

    def _request(self, language, params) -> str:
        ip_res, mode = ip_test(self.PROXIES)
        if not ip_res:
            logger.error(f'网络测试失败，停止请求')
            return ''
        else:
            if mode == 'DIRECT':
                proxies = None
            else:
                proxies = self.PROXIES

        url = self.BASE_URL_TEMPLATE.format(language=language)
        for i in range(3):
            try:
                resp = self.session.get(url, params=params, proxies=proxies, timeout=10)
                resp.raise_for_status()
                return resp.text
            except Exception as e:
                wait = (i + 1) ** 2
                logger.warning(f"[{language}] 请求失败({e})，{wait}s 后重试…")
                time.sleep(wait)
        logger.error(f"[{language}] 三次请求均失败，放弃")
        return ""

    @staticmethod
    def _parse(html: str, language: str, since: str) -> list[BaseRepo]:
        if not html:
            return []

        tree = etree.HTML(html)
        items = tree.xpath("//article[@class='Box-row']")
        repos = []
        for item in items:
            try:
                href = item.xpath("./h2/a/@href")[0].strip()
                _, owner, repo = href.split('/')
                url = f"https://github.com{href}"
                raw = item.xpath("./div[last()]/span[last()]/text()")
                stars = int(raw[-1].split()[0].replace(',', '')) if raw else 0
                desc = item.xpath("normalize-space(./p/text())")
                repos.append(BaseRepo(owner, repo, url, desc, stars, language, since))
                logger.info(f"解析：{owner}/{repo} +{stars}s")
            except Exception as e:
                logger.error(f"解析单条失败：{e}")
        return repos

    # 主函数
    def get_repos(self, language="python", since=None, spoken_language_code=None) -> list[BaseRepo]:
        params = self.DEFAULT_PARAMS.copy()
        if since: params["since"] = since
        if spoken_language_code: params["spoken_language_code"] = spoken_language_code

        html = self._request(language, params)
        return self._parse(html, language, params["since"])


# 脚本入口
if __name__ == "__main__":
    scraper = TrendingScraper()
    result = scraper.get_repos(language="python", since="weekly")
    for repo in result:
        print(repo)
