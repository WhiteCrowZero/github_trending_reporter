#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Name   : main.py
Author      : wzw
Date Created: 2025/5/18
Description : Add your script's purpose here.
"""
import os
from log_utils import init_logger
from trending_scraper import TrendingScraper
from history_recorder import HistoryRecorder
from output_generator import OutputGenerator

module_name = os.path.splitext(os.path.basename(__file__))[0]
logger = init_logger('github', module_name)


def main(language="python", since="daily"):
    # 抓取信息
    scraper = TrendingScraper()
    result = scraper.get_repos(language, since)

    # 存储信息
    recorder = HistoryRecorder()
    save_path = recorder.save(result)

    # 报告信息
    generator = OutputGenerator(save_path)
    markdown = generator.generate_markdown()
    generator.send_to_qiwei(markdown)


if __name__ == '__main__':
    main()
