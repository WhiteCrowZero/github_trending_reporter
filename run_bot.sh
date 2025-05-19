#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

CONDAPATH="$HOME/miniconda3/etc/profile.d/conda.sh"
CONDAENV="spider_base_py39"

# 加载 Conda 初始化脚本
source "$CONDAPATH"

# 激活的 Conda 环境
conda activate "$CONDAENV"

# 切换到脚本所在目录，防止 cron 定时任务时路径错误
cd "$(dirname "$0")"

# 运行的脚本
python main.py

exit 0
