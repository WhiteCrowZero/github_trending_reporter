#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Name   : models.py
Author      : wzw
Date Created: 2025/5/18
Description : 数据类型
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class BaseRepo:
    """GitHub 仓库基础信息"""
    owner: str  # 仓库所有者用户名
    repo: str  # 仓库名称
    url: str  # 仓库GitHub页面URL
    desc: str  # 仓库描述
    stars_today: int  # 今日新增star数（根据趋势计算）
    language: str  # 主要编程语言
    since: str  # 统计时间范围


@dataclass
class RichRepo(BaseRepo):
    """GitHub 仓库详细信息"""
    # 统计信息
    stargazers_count: int = 0  # 总star数
    forks_count: int = 0  # fork总数
    open_issues_count: int = 0  # 当前open状态的issue数
    subscribers_count: int = 0  # 订阅者数（watchers）

    # 元信息
    license: str = ""  # 许可证名称
    created_at: str = ""  # 仓库创建时间（ISO8601格式）
    updated_at: str = ""  # 最近更新时间
    pushed_at: str = ""  # 最近代码push时间

    # 分类信息
    topics: List[str] = field(default_factory=list)  # 仓库标签列表
    homepage: str = ""  # 项目官网/演示地址
