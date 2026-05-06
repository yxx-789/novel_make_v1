# -*- coding: utf-8 -*-
"""
修复脚本 - 用于在本地正确设置项目
"""

import os
import sys
from pathlib import Path


def setup_project():
    """设置项目环境"""
    
    project_root = Path(__file__).parent
    
    print("=" * 60)
    print("🔧 Novel Creation Platform - 本地环境修复")
    print("=" * 60)
    
    # 1. 创建必要的 __init__.py 文件
    init_dirs = ["utils", "config", "core", "models", "api", "pipelines"]
    
    print("\n1️⃣ 修复 Python 包结构...")
    for dir_name in init_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            init_file = dir_path / "__init__.py"
            if not init_file.exists():
                init_file.write_text("# Package marker\n")
                print(f"   ✅ 创建 {dir_name}/__init__.py")
            else:
                print(f"   ✓ {dir_name}/__init__.py 已存在")
        else:
            print(f"   ❌ {dir_name}/ 目录不存在")
    
    # 2. 修复 main.py 中的导入问题
    print("\n2️⃣ 修复主程序...")
    
    main_file = project_root / "main_fixed.py"
    if not main_file.exists():
        print("   ❌ main_fixed.py 不存在，正在创建...")
        
        # 创建修复版
        fixed_content = '''# -*- coding: utf-8 -*-
"""
Novel Creation API - 千帆版本主入口
"""

import sys
from pathlib import Path
import uvicorn

# 修复导入路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI

# 创建应用
app = FastAPI(
    title="Novel Creation API - 千帆版",
    description="AI小说创作 + 短剧剧本转换平台",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

@app.get("/")
async def root():
    return {
        "message": "Novel Creation API 已启动",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "provider": "百度千帆平台"
    }

@app.get("/health")
async def health_check():
    import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat(),
        "provider": "百度千帆",
        "models": ["glm-5.1", "qwen3.5-397b-a17b", "deepseek-v3.2"]
    }

# 导入路由
try:
    from api.routes import router
    app.include_router(router, prefix="/api/v1")
    print("✅ API 路由已加载")
except Exception as e:
    print(f"⚠️ 路由加载失败: {e}")

if __name__ == "__main__":
    print("🚀 服务启动中...")
    print("📡 API: http://localhost:8000")
    print("📚 文档: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
'''
        
        main_file.write_text(fixed_content)
        print("   ✅ main_fixed.py 已创建")
    
    # 3. 创建启动脚本
    print("\n3️⃣ 创建启动脚本...")
    
    startup_script = project_root / "start.py"
    startup_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动脚本 - 简化的启动方式
"""

import sys
import os
from pathlib import Path

# 设置项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 确保必要的 __init__.py 存在
for dir_name in ["utils", "config", "core", "models", "api", "pipelines"]:
    dir_path = project_root / dir_name
    if dir_path.exists() and not (dir_path / "__init__.py").exists():
        (dir_path / "__init__.py").write_text("# Package marker\\n")

print("=" * 60)
print("🚀 Novel Creation Platform")
print("=" * 60)
print("📡 AI 提供商: 百度千帆")
print("🤖 默认模型: glm-5.1")
print("🌐 服务端口: 8000")
print("=" * 60)

# 导入并启动
from main_fixed import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
'''
    
    startup_script.write_text(startup_content)
    startup_script.chmod(0o755)  # 可执行权限
    print("   ✅ start.py 已创建（可执行）")
    
    # 4. 创建测试脚本
    print("\n4️⃣ 创建测试脚本...")
    
    test_script = project_root / "test_local.py"
    test_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地测试脚本
"""

import sys
from pathlib import Path
import requests
import time

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("=" * 60)
print("🧪 Novel Creation Platform - 本地测试")
print("=" * 60)

# 等待服务启动
print("等待服务启动...")
time.sleep(2)

# 测试端点
test_endpoints = [
    ("/", "首页"),
    ("/health", "健康检查"),
    ("/docs", "API文档"),
    ("/openapi.json", "OpenAPI规范")
]

base_url = "http://localhost:8000"

for endpoint, name in test_endpoints:
    try:
        response = requests.get(f"{base_url}{endpoint}", timeout=5)
        if response.status_code == 200:
            print(f"✅ {name:12s} {endpoint} - 正常")
        else:
            print(f"⚠️ {name:12s} {endpoint} - {response.status_code}")
    except Exception as e:
        print(f"❌ {name:12s} {endpoint} - 连接失败: {e}")

print("\\n🎯 建议:")
print("1. 打开浏览器访问: http://localhost:8000/docs")
print("2. 点击 'Try it out' 进行交互测试")
print("3. 从简单接口开始测试: /health")
'''
    
    test_script.write_text(test_content)
    test_script.chmod(0o755)
    print("   ✅ test_local.py 已创建")
    
    # 5. 创建 requirements-minimal.txt
    print("\n5️⃣ 创建最小依赖列表...")
    
    requirements = project_root / "requirements-minimal.txt"
    requirements_content = '''fastapi>=0.104.0
uvicorn>=0.24.0
requests>=2.31.0
python-multipart>=0.0.6
python-dotenv>=1.0.0
'''
    
    requirements.write_text(requirements_content)
    print("   ✅ requirements-minimal.txt 已创建")
    
    # 完成
    print("\n" + "=" * 60)
    print("🎉 项目修复完成！")
    print("=" * 60)
    
    print("\n📋 使用指南：")
    print("1. 安装依赖:")
    print("   pip install -r requirements-minimal.txt")
    print("")
    print("2. 启动服务:")
    print("   python start.py")
    print("   或")
    print("   python main_fixed.py")
    print("")
    print("3. 测试服务:")
    print("   python test_local.py")
    print("   或")
    print("   访问 http://localhost:8000/docs")
    print("")
    print("4. 检查日志:")
    print("   - 服务启动时会显示端口和地址")
    print("   - 查看是否有报错信息")
    print("")
    print("🛠️ 如果遇到问题：")
    print("1. 确保端口 8000 未被占用")
    print("2. 检查网络连接（能访问百度千帆）")
    print("3. 确认 Python 版本 >= 3.8")


if __name__ == "__main__":
    setup_project()