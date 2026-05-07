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
    """获取配置 - 使用百度千帆 API"""
    return {
        "llm": {
            "api_key": os.getenv("QIANFAN_API_KEY", ""),  # 千帆 API Key
            "api_url": os.getenv("QIANFAN_API_URL", "https://qianfan.baidubce.com/v2/chat/completions"),
            "model": os.getenv("QIANFAN_MODEL", "glm-5.1"),  # 千帆模型
            "temperature": float(os.getenv("LLM_TEMPERATURE", "0.7")),
            "max_tokens": int(os.getenv("LLM_MAX_TOKENS", "4096"))
        },
        "embedding": {
            "embedding_api_key": os.getenv("QIANFAN_API_KEY", ""),  # 千帆 API Key
            "embedding_url": os.getenv("QIANFAN_API_URL", "https://qianfan.baidubce.com/v2/chat/completions"),
            "embedding_model": os.getenv("EMBEDDING_MODEL", "embedding-v1")
        },
        "api": {
            "host": os.getenv("API_HOST", "0.0.0.0"),
            "port": int(os.getenv("API_PORT", "8000")),
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
║    百度千帆 API 版本                        ║
╚═══════════════════════════════════════════╝

🚀 服务启动中...
📍 地址: http://{api_config['host']}:{api_config['port']}
📚 API文档: http://{api_config['host']}:{api_config['port']}/docs
🔧 环境: {os.getenv('ENVIRONMENT', 'development')}
🤖 模型: {config['llm']['model']} (百度千帆)
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
