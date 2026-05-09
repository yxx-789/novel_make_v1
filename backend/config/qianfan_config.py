# -*- coding: utf-8 -*-
"""
百度千帆平台 API 配置
"""

import os

# ==================== 百度千帆平台 API ====================
# 从环境变量读取 API Key（推荐方式）
QIANFAN_API_KEY = os.getenv("QIANFAN_API_KEY", "")
QIANFAN_API_URL = os.getenv("QIANFAN_API_URL", "https://qianfan.baidubce.com/v2/chat/completions")

# 可用模型列表
QIANFAN_MODELS = {
    "glm-5.1": {
        "model": "glm-5.1",
        "display_name": "智谱 GLM-5.1",
        "context_length": 128000,
        "supports_tool_calling": True
    },
    "qwen3.5-397b-a17b": {
        "model": "qwen3.5-397b-a17b",
        "display_name": "阿里 Qwen3.5-397B 旗舰",
        "context_length": 32000,
        "supports_tool_calling": True
    },
    "deepseek-v3.2": {
        "model": "deepseek-v3.2",
        "display_name": "DeepSeek-V3.2",
        "context_length": 128000,
        "supports_tool_calling": True
    }
}

# 默认模型
DEFAULT_MODEL = "glm-5.1"

# Embedding 模型
EMBEDDING_MODEL = "embedding-v1"

# ==================== 调用配置 ====================
REQUEST_TIMEOUT = 600  # 秒
MAX_RETRIES = 5
RETRY_DELAY = 2  # 秒

# ==================== 流式响应配置 ====================
STREAM_ENABLED = True
STREAM_BUFFER_SIZE = 1024

# ==================== 安全配置 ====================
RATE_LIMIT_PER_MINUTE = 60
RATE_LIMIT_PER_DAY = 10000

# ==================== 代理配置（可选） ====================
PROXY_SETTINGS = {
    "enabled": False,
    "http": "http://proxy_host:proxy_port",
    "https": "http://proxy_host:proxy_port"
}