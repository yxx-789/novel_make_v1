#!/usr/bin/env python3
"""快速测试本地应用"""

import subprocess
import time
import requests
import os
import sys

# 设置环境变量
os.environ['QIANFAN_API_KEY'] = 'bce-v3/ALTAK-vnASNnJZQkPchN6JShUdi/38e23c1484e3b2ab42e15dd596dc85fd4328caf4'
os.environ['QIANFAN_API_URL'] = 'https://qianfan.baidubce.com/v2/chat/completions'
os.environ['QIANFAN_MODEL'] = 'glm-5.1'
os.environ['PORT'] = '8002'

print("🚀 启动应用...")

# 启动应用
proc = subprocess.Popen(
    ['python', 'main.py'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

# 等待应用启动
time.sleep(3)

# 测试健康检查
try:
    print("\n📋 测试健康检查...")
    response = requests.get('http://localhost:8002/health', timeout=5)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print("✅ 健康检查成功!")
except Exception as e:
    print(f"❌ 健康检查失败: {e}")

# 测试 API
try:
    print("\n📋 测试小说列表 API...")
    response = requests.get('http://localhost:8002/api/v1/novels', timeout=5)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print("✅ API 调用成功!")
except Exception as e:
    print(f"❌ API 调用失败: {e}")

# 停止应用
print("\n🛑 停止应用...")
proc.terminate()
proc.wait(timeout=5)
print("✅ 应用已停止")
