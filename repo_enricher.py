#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Name   : repo_enricher.py
Author      : wzw
Date Created: 2025/5/18
Description : 用 API 补全每个项目的详细数据（stars, issues, 活跃度）
"""

import requests
from models import BaseRepo, RichRepo

def enrich_repo_info(base: BaseRepo, token) -> RichRepo:
    """
    根据 BaseRepo 补全信息，生成 RichRepo（使用 GitHub API）
    """
    github_api_base = "https://api.github.com/repos"
    url = f"{github_api_base}/{base.owner}/{base.repo}"

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "GithubTrendingBot"
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        rich = RichRepo(**vars(base))  # 基础字段继承

        # 补全字段（与 GitHub API 对应字段名一致）
        rich.stargazers_count = data.get("stargazers_count", 0)
        rich.forks_count = data.get("forks_count", 0)
        rich.open_issues_count = data.get("open_issues_count", 0)
        rich.subscribers_count = data.get("subscribers_count", 0)
        rich.license = data.get("license", {}).get("name", "")
        rich.created_at = data.get("created_at", "")
        rich.updated_at = data.get("updated_at", "")
        rich.pushed_at = data.get("pushed_at", "")
        rich.topics = data.get("topics", [])
        rich.homepage = data.get("homepage", "")

        return rich

    except Exception as e:
        print(f"[ERROR] enrich_repo_info: 请求失败 {base.owner}/{base.repo}：{e}")
        return RichRepo(**vars(base))  # 返回基础信息作为 fallback
