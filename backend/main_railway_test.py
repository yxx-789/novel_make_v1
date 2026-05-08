#!/usr/bin/env python3
"""
Railway 测试应用 - 最小化版本
用于诊断 Railway 部署问题
"""

import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime

# 创建 FastAPI 应用
app = FastAPI(
    title="Novel Creation API - Railway Test",
    description="测试 Railway 部署的最小化应用",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 根路径
@app.get("/")
async def root():
    return {
        "message": "Novel Creation API - Railway Test Version",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "docs": "/docs",
        "health": "/health"
    }

# 健康检查端点
@app.get("/health")
async def health_check():
    """健康检查 - Railway 需要这个端点"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "novel-creation-api",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "port": os.getenv("PORT", "8000")
    }

# 测试端点
@app.get("/test")
async def test():
    return {
        "test": "passed",
        "message": "Railway 测试应用运行正常",
        "env_vars": {
            "PORT": os.getenv("PORT", "未设置"),
            "ENVIRONMENT": os.getenv("ENVIRONMENT", "未设置"),
            "API_HOST": os.getenv("API_HOST", "未设置")
        }
    }

# 模拟一些 API 端点
@app.get("/api/v1/novels")
async def get_novels():
    """模拟获取小说列表"""
    return {
        "novels": [
            {"id": "test-1", "title": "测试小说", "status": "draft"}
        ],
        "total": 1,
        "page": 1,
        "page_size": 10,
        "message": "测试数据 - 实际应用需要连接数据库"
    }

@app.post("/api/v1/novels")
async def create_novel():
    """模拟创建小说"""
    return {
        "success": True,
        "message": "测试创建成功",
        "data": {
            "id": "new-test-id",
            "title": "测试创建的小说"
        }
    }

def main():
    """主函数"""
    # 读取 Railway 环境变量
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    
    print("=" * 60)
    print("🚀 Railway 测试应用启动")
    print("=" * 60)
    print(f"📡 监听地址: http://{host}:{port}")
    print(f"🔧 环境变量:")
    print(f"   PORT: {os.getenv('PORT', '未设置 (默认: 8000)')}")
    print(f"   ENVIRONMENT: {os.getenv('ENVIRONMENT', '未设置 (默认: development)')}")
    print(f"🌐 可用端点:")
    print(f"   /          - 根路径")
    print(f"   /health    - 健康检查 (Railway 需要)")
    print(f"   /test      - 测试端点")
    print(f"   /docs      - API 文档")
    print(f"   /api/v1/novels - 模拟小说 API")
    print("=" * 60)
    
    # 启动服务
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )

if __name__ == "__main__":
    main()