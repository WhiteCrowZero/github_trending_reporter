#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Name   : output_generator.py
Author      : wzw
Date Created: 2025/5/18
Description : 每周生成项目推荐榜单（md/html）
"""
import os
import json
import requests
from pathlib import Path
from typing import List, Dict
from config_set import config
from log_utils import init_logger

# 模块名用于日志标识
module_name = os.path.splitext(os.path.basename(__file__))[0]
logger = init_logger('github', module_name)


class OutputGenerator:
    """
    从历史记录文件中读取最新记录，生成 Markdown 报告并推送至企业微信。
    """
    MSG_TEMPLATE = """\
    ## GitHub 趋势仓库报告（{date} {type}）

{rows}
    """

    def __init__(self, history_path):
        try:
            self.history_path = Path(history_path)
            if not self.history_path.exists():
                raise FileNotFoundError(f"[error] 未找到历史记录文件: {self.history_path}")
            logger.info(f"[success] 使用数据来源：{self.history_path}")
        except Exception as e:
            logger.error(e)

    def _load_latest(self) -> Dict:
        history = json.loads(self.history_path.read_text(encoding='utf-8'))
        return history if isinstance(history, dict) else history[-1]

    def _format_rows(self, repos: List[Dict]) -> str:
        """
        只保留：星星数、链接、描述，按有序列表输出前 10 条
        """
        lines = []
        for idx, r in enumerate(repos[:10], 1):
            desc = r.get('desc', '').strip()
            if not desc:
                desc = "暂无描述"
            desc = desc[:100]

            lines.append(
                f"{idx}. [{r['owner']}/{r['repo']}]({r['url']})  \n"
                f" - ⭐ {r['stars_today']}\n"
                f" - 📝 {desc}"
            )
        return "\n".join(lines)

    def generate_markdown(self) -> str:
        latest = self._load_latest()
        date = latest.get('date', '未知日期')
        _type = latest.get('type', '未知模式')
        rows = self._format_rows(latest.get('repos', []))
        return self.MSG_TEMPLATE.format(date=date, type=_type, rows=rows)

    def send_to_qiwei(self, markdown: str):
        try:
            webhook = config.qiwx_webhook_url
            if not webhook:
                raise RuntimeError("[error] 未设置企业微信 webhook，请在 config_set.py 中配置 qiwx_webhook_url")
            payload = {
                "msgtype": "markdown",
                "markdown": {"content": markdown}
            }
            resp = requests.post(webhook, json=payload)
            if resp.status_code == 200 and resp.json().get("errcode") == 0:
                logger.info("[success] 已成功发送到企业微信")
            else:
                raise RuntimeError(f"[error] 发送失败：{resp.text}")

        except Exception as e:
            logger.error(e)


if __name__ == '__main__':
    history_path = r"D:\ComputerScience\Python\temp\github_trending\github_trend_data\2025\05\2025-05-19_data.json"
    generator = OutputGenerator(history_path)
    markdown = generator.generate_markdown()
    print(markdown)
    generator.send_to_qiwei(markdown)
