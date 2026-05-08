# -*- coding: utf-8 -*-
"""
Novel Creation API - 主入口
启动 FastAPI 服务
"""

import os
import sys
from pathlib import Path
import asyncio
from typing import Dict

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv

# 导入 API 路由
from api.routes import app, init_engines

# 加载环境变量
load_dotenv()


def get_config() -> Dict:
    """获取配置 - 支持百度千帆和 OpenAI 两种配置"""
    # 优先使用千帆配置
    qianfan_api_key = os.getenv("QIANFAN_API_KEY", "")
    qianfan_api_url = os.getenv("QIANFAN_API_URL", "https://qianfan.baidubce.com/v2/chat/completions")
    qianfan_model = os.getenv("QIANFAN_MODEL", "glm-5.1")
    
    # 如果没有千帆配置，使用 OpenAI 配置
    if not qianfan_api_key:
        openai_api_key = os.getenv("OPENAI_API_KEY", "")
        openai_base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        openai_model = os.getenv("LLM_MODEL", "gpt-4o-mini")
        
        if openai_api_key:
            # 使用 OpenAI 配置
            api_key = openai_api_key
            api_url = openai_base_url
            model = openai_model
            platform = "OpenAI"
        else:
            # 都没有设置，使用千帆默认值（但 API key 为空）
            api_key = qianfan_api_key
            api_url = qianfan_api_url
            model = qianfan_model
            platform = "Qianfan (no API key)"
    else:
        # 使用千帆配置
        api_key = qianfan_api_key
        api_url = qianfan_api_url
        model = qianfan_model
        platform = "Qianfan"
    
    return {
        "llm": {
            "api_key": api_key,
            "api_url": api_url,
            "model": model,
            "temperature": float(os.getenv("LLM_TEMPERATURE", "0.7")),
            "max_tokens": int(os.getenv("LLM_MAX_TOKENS", "4096")),
            "platform": platform
        },
        "embedding": {
            "embedding_api_key": api_key,
            "embedding_url": api_url,
            "embedding_model": os.getenv("EMBEDDING_MODEL", "embedding-v1")
        },
        "api": {
            "host": os.getenv("API_HOST", "0.0.0.0"),
            "port": int(os.getenv("PORT", os.getenv("API_PORT", "8000"))),
            "workers": int(os.getenv("API_WORKERS", "1")),
            "reload": os.getenv("ENVIRONMENT", "development") == "development"
        }
    }


def create_app() -> FastAPI:
    """创建并配置应用"""
    config = get_config()
    
    # 初始化引擎
    init_engines(config["llm"], config["embedding"])
    
    return app


def main():
    """主函数"""
    config = get_config()
    api_config = config["api"]
    
    print(f"""
╔═══════════════════════════════════════════╗
║    Novel Creation API v1.0.0              ║
║    AI 小说创作 + 短剧剧本转换               ║
║    {config['llm']['platform']} 版本               ║
╚═══════════════════════════════════════════╝

🚀 服务启动中...
📍 地址: http://{api_config['host']}:{api_config['port']}
📚 API文档: http://{api_config['host']}:{api_config['port']}/docs
🔧 环境: {os.getenv('ENVIRONMENT', 'development')}
🤖 模型: {config['llm']['model']} ({config['llm']['platform']})
    """)
    
    # 启动服务
    uvicorn.run(
        "main:app",
        host=api_config["host"],
        port=api_config["port"],
        workers=api_config["workers"],
        reload=api_config["reload"],
        log_level="info"
    )


if __name__ == "__main__":
    # 创建应用
    app = create_app()
    
    # 启动
    main()
