#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试千帆 API 是否正常工作
"""

import sys
import os
import asyncio

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.utils.qianfan_client import QianfanClient

async def test_qianfan_api():
    """测试千帆 API 是否正常工作"""
    print("=== 测试千帆 API ===")
    
    # 初始化客户端
    client = QianfanClient(
        api_key=os.getenv("QIANFAN_API_KEY", ""),
        timeout=30  # 30秒超时
    )
    
    print("1. 测试简单对话...")
    
    try:
        # 测试简单的对话
        messages = [
            {"role": "user", "content": "你好，请回复一个简单的问候。"}
        ]
        
        response = client.chat(messages, model="glm-5.1", max_tokens=100)
        
        if response.success:
            print(f"✅ API 正常，回复: {response.content[:100]}...")
            return True
        else:
            print(f"❌ API 失败: {response.content}")
            return False
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

async def test_async_generate():
    """测试异步生成"""
    print("\n2. 测试异步生成...")
    
    client = QianfanClient(
        api_key=os.getenv("QIANFAN_API_KEY", ""),
        timeout=30
    )
    
    try:
        result = await client.async_generate("你好，请回复一个简短的问候。", max_tokens=50)
        print(f"✅ 异步生成正常: {result[:100]}...")
        return True
    except Exception as e:
        print(f"❌ 异步生成失败: {e}")
        return False

if __name__ == "__main__":
    # 检查环境变量
    api_key = os.getenv("QIANFAN_API_KEY", "")
    if not api_key:
        print("❌ 未设置 QIANFAN_API_KEY 环境变量")
        print("请设置环境变量: export QIANFAN_API_KEY=your_api_key")
        sys.exit(1)
    
    print(f"API Key: {api_key[:10]}...")
    
    # 运行测试
    sync_success = asyncio.run(test_qianfan_api())
    async_success = asyncio.run(test_async_generate())
    
    if sync_success and async_success:
        print("\n🎉 所有测试通过！千帆 API 正常工作")
    else:
        print("\n❌ 测试失败，请检查 API 配置")