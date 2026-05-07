#!/usr/bin/env python3
"""
快速功能测试 - 简化版
"""
import os
import sys
import asyncio
from pathlib import Path

# 设置环境变量
os.environ['QIANFAN_API_KEY'] = 'bce-v3/ALTAK-vnASNnJZQkPchN6JShUdi/38e23c1484e3b2ab42e15dd596dc85fd4328caf4'

# 添加路径
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("快速功能测试")
print("=" * 70)

# 测试 1: 导入和初始化
print("\n[测试 1/3] 导入模块")
try:
    from utils.qianfan_client import QianfanClient
    from core.novel_engine_qianfan import NovelEngine
    from core.drama_engine import DramaEngine
    print("✅ 模块导入成功")
except Exception as e:
    print(f"❌ 导入失败: {e}")
    sys.exit(1)

# 测试 2: 测试千帆客户端
print("\n[测试 2/3] 测试千帆客户端")
try:
    client = QianfanClient(
        api_key=os.environ['QIANFAN_API_KEY'],
        model="glm-5.1"
    )
    
    messages = [
        {"role": "user", "content": "你好，请回复'测试成功'"}
    ]
    response = client.chat(messages, temperature=0.7, max_tokens=20)
    
    if response.success:
        print(f"✅ API 调用成功")
        print(f"   响应: {response.content}")
        print(f"   模型: {response.model}")
    else:
        print(f"❌ API 调用失败: {response.content}")
except Exception as e:
    print(f"❌ 客户端测试失败: {e}")

# 测试 3: 测试小说引擎创建
print("\n[测试 3/3] 测试小说引擎创建")
try:
    config = {
        "model": "glm-5.1",
        "temperature": 0.7,
        "max_tokens": 100000
    }
    engine = NovelEngine(config)
    print("✅ 小说引擎创建成功")
except Exception as e:
    print(f"❌ 小说引擎创建失败: {e}")

print("\n" + "=" * 70)
print("基础测试完成")
print("=" * 70)