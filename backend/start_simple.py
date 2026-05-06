#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
极简启动脚本 - 解决所有配置问题
"""

import sys
import os
from pathlib import Path

# 设置项目根目录
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("=" * 60)
print("🚀 Novel Creation Platform - 极简启动")
print("=" * 60)

# 确保必要的包结构
required_dirs = ["utils", "config", "core", "models", "api"]
for dir_name in required_dirs:
    dir_path = project_root / dir_name
    if dir_path.exists() and not (dir_path / "__init__.py").exists():
        (dir_path / "__init__.py").write_text("# Package marker\n")

# 设置千帆 API 环境变量（避免 OpenAI 错误）
os.environ["QIANFAN_MODEL"] = "glm-5.1"
os.environ["LLM_TEMPERATURE"] = "0.7"
os.environ["LLM_MAX_TOKENS"] = "2048"

print("✅ 环境配置完成")
print("🤖 使用模型: 百度千帆 GLM-5.1")
print("🔑 API Key: 已内置（你的千帆Key）")

# 导入千帆客户端测试
try:
    from utils.qianfan_client import QianfanClient
    client = QianfanClient()
    if client.test_connection():
        print("✅ 千帆 API 连接成功")
    else:
        print("❌ 千帆 API 连接失败")
        sys.exit(1)
except Exception as e:
    print(f"⚠️ 千帆客户端测试失败: {e}")
    print("继续启动服务...")

# 创建简化的 FastAPI 应用
from fastapi import FastAPI
import uvicorn
import datetime

app = FastAPI(
    title="Novel Creation API",
    description="AI小说创作 + 短剧剧本转换平台",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "message": "Novel Creation API 已启动",
        "version": "1.0.0",
        "provider": "百度千帆",
        "timestamp": datetime.datetime.now().isoformat()
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "novel_creation",
        "model": "百度千帆 GLM-5.1",
        "time": datetime.datetime.now().isoformat()
    }

# 尝试导入真实的路由
try:
    from api.routes import router
    app.include_router(router, prefix="/api/v1")
    print("✅ 加载 API 路由成功")
except Exception as e:
    print(f"⚠️ 路由加载失败: {e}")
    print("⚠️ 仅提供基础健康检查接口")

# 启动参数
port = 8000
for arg in sys.argv[1:]:
    if arg.startswith("--port="):
        port = int(arg.split("=")[1])
    elif arg.startswith("-p"):
        port = int(arg[2:])

print("=" * 60)
print(f"🌐 服务地址: http://localhost:{port}")
print(f"📚 API文档: http://localhost:{port}/docs")
print(f"🩺 健康检查: http://localhost:{port}/health")
print("=" * 60)

if __name__ == "__main__":
    try:
        uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"\n❌ 错误: 端口 {port} 已被占用")
            print(f"\n解决方法:")
            print(f"1. 使用不同端口: python {__file__} --port=8001")
            print(f"2. 查看占用进程:")
            print(f"   macOS/Linux: lsof -i :{port}")
            print(f"   Windows: netstat -ano | findstr :{port}")
            print(f"3. 杀掉占用进程: kill -9 <PID>")
            sys.exit(1)
        else:
            raise e