# 使用轻量级 Python 镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 拷贝项目代码（不包括私密配置）
COPY . /app

# 安装依赖（requirements.txt 需包含 requests、transformers 等）
RUN pip install --no-cache-dir -r requirements.txt

# 可选：创建数据目录（挂载用）
RUN mkdir -p /app/github_data

# 默认运行主程序（你也可以换成 trending_runner.py / main.py）
CMD ["python", "main.py"]
