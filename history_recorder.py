#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Name   : history_recorder.py
Author      : wzw
Date Created: 2025/5/18
Description : 记录每天项目数据
"""

import json
from dataclasses import asdict
from typing import List
from pathlib import Path
import os
from log_utils import init_logger
from models import BaseRepo
from small_utils import get_current_date
from config_set import config

# 模块名用于日志标识
module_name = os.path.splitext(os.path.basename(__file__))[0]
logger = init_logger('github', module_name)


class HistoryRecorder:
    """
    负责将一系列 BaseRepo 实例保存到本地 JSON 文件，以便后续比对历史变化。
    """

    def __init__(self):
        self.base_dir = config.base_dir
        self.save_path: Path = self._generate_dated_path()

        # 确保目录结构存在
        self.save_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"存储目录已初始化：{self.save_path}")

    def _generate_dated_path(self) -> Path:
        """生成带日期的层级路径"""
        date_str = get_current_date()  # eg: 2025-05-18
        year, month, _ = date_str.split('-')

        return (
                self.base_dir
                / year
                / month
                / f"{date_str}_data.json"
        )

    def save(self, repos: List[BaseRepo]):
        """将 BaseRepo 列表保存为 json 文件"""
        if not repos:
            logger.warning("无数据可保存")
            return

        today_record = {
            "date": repos[0].since,  # eg: "weekly"
            "repos": [asdict(r) for r in repos]
        }

        with open(self.save_path, 'w', encoding='utf-8') as f:
            json.dump(today_record, f, ensure_ascii=False, indent=2)

        logger.info(f"已保存 {len(repos)} 条记录到 {self.save_path}")
        return self.save_path


# 示例调用
if __name__ == '__main__':
    item = BaseRepo(
        owner='PantsuDango',
        repo='Dango-Translator',
        url='https://github.com/PantsuDango/Dango-Translator',
        desc='团子翻译器 —— 个人兴趣制作的一款基于OCR技术的翻译器',
        stars_today=22,
        language='python',
        since='weekly'
    )

    recorder = HistoryRecorder()
    recorder.save([item])
