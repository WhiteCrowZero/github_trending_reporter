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

module_name = os.path.splitext(os.path.basename(__file__))[0]
logger = init_logger('github', module_name)


scraper = TrendingScraper()
result = scraper.get_repos(language="python", since="weekly")
for repo in result:
    print(repo)
