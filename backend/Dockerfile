# Novel Creation API - Docker 镜像构建

# 基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PATH="/home/app/.local/bin:$PATH"

# 安装系统依赖
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        curl \
        git \
        libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 创建非root用户
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# 复制依赖文件
COPY --chown=app:app requirements.txt .

# 安装Python依赖
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# 复制应用代码
COPY --chown=app:app . .

# 创建必要的目录
RUN mkdir -p data/vectorstore data/projects data/cache logs output

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "main.py"]