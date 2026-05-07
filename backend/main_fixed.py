# -*- coding: utf-8 -*-
"""
Novel Creation API - 千帆版本主入口
完全使用百度千帆 API
"""

import os
import sys
from pathlib import Path
from typing import Dict
import uvicorn
from dotenv import load_dotenv

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 导入 API 路由
from api.routes import app as main_app

# 加载环境变量
load_dotenv()


def get_qianfan_config() -> Dict:
    """获取千帆配置"""
    return {
        "llm": {
            "api_key": os.getenv("QIANFAN_API_KEY", ""),  # 从环境变量读取
            "api_url": os.getenv("QIANFAN_API_URL", "https://qianfan.baidubce.com/v2/chat/completions"),
            "model": os.getenv("QIANFAN_MODEL", "glm-5.1"),
            "temperature": float(os.getenv("LLM_TEMPERATURE", "0.7")),
            "max_tokens": int(os.getenv("LLM_MAX_TOKENS", "4096"))
        },
        "embedding": {
            "embedding_api_key": os.getenv("QIANFAN_API_KEY", ""),  # 从环境变量读取
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
    """创建 FastAPI 应用"""
    app = FastAPI(
        title="Novel Creation API - 千帆版",
        description="AI小说创作 + 短剧剧本转换平台，使用百度千帆API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # CORS 配置
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 配置信息
    config = get_qianfan_config()
    app.state.config = config
    
    # 导入路由（覆盖原来的配置）
    from api import routes
    routes.init_engines(config)
    
    # 挂载路由
    app.include_router(routes.router, prefix="/api/v1")
    
    # 健康检查
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "timestamp": __import__("datetime").datetime.now().isoformat(),
            "config": {
                "llm": config["llm"]["model"],
                "provider": "百度千帆",
                "models": ["glm-5.1", "qwen3.5-397b-a17b", "deepseek-v3.2"]
            }
        }
    
    # 首页
    @app.get("/")
    async def root():
        return {
            "message": "Novel Creation API 已启动",
            "version": "1.0.0",
            "docs": "/docs",
            "health": "/health",
            "provider": "百度千帆平台"
        }
    
    return app


# 创建应用
app = create_app()


if __name__ == "__main__":
    config = get_qianfan_config()
    api_config = config["api"]
    
    print("\n" + "=" * 60)
    print("🚀 Novel Creation API - 千帆版启动")
    print("=" * 60)
    print(f"📡 AI 提供商: 百度千帆")
    print(f"🤖 默认模型: {config['llm']['model']}")
    print(f"🌐 服务地址: http://{api_config['host']}:{api_config['port']}")
    print(f"📚 API文档: http://{api_config['host']}:{api_config['port']}/docs")
    print("=" * 60)
    print("\n📢 注意：")
    print("✅ 已使用你的千帆 API Key")
    print("✅ 支持 GLM-5.1 / Qwen3.5 / DeepSeek-V3.2")
    print("✅ 无需额外配置 OpenAI 密钥\n")
    
    uvicorn.run(
        "main_fixed:app",
        host=api_config["host"],
        port=api_config["port"],
        reload=api_config["reload"],
        workers=api_config["workers"]
    )