#!/usr/bin/env python3
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

print("\n🎯 建议:")
print("1. 打开浏览器访问: http://localhost:8000/docs")
print("2. 点击 'Try it out' 进行交互测试")
print("3. 从简单接口开始测试: /health")
