#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试生成大纲 - 诊断卡住的原因
"""

import sys
import os
import asyncio
import json

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.utils.qianfan_client import QianfanClient

async def test_outline_generation():
    """测试生成大纲"""
    print("=== 测试生成大纲 ===\n")
    
    # 模拟一个简单的生成大纲提示词
    prompt = """
你是一位专业的网络小说大纲师。请为以下小说生成简洁的章节大纲：

小说标题：测试小说
类型：玄幻
主题：主角逆袭
总章节数：3

【大纲要求】

请为每一章生成以下内容：

1. 章节标题（吸引人的标题）
2. 章节摘要（50-100字）
3. 关键事件（3个核心事件）

【输出格式要求】
请以JSON格式输出：

格式示例：
{
    "chapters": [
        {
            "chapter_num": 1,
            "title": "章节标题",
            "summary": "50-100字的简要概括",
            "key_events": [
                "事件1",
                "事件2",
                "事件3"
            ]
        }
    ]
}

请开始创作：
"""
    
    # 初始化客户端
    client = QianfanClient(
        api_key=os.getenv("QIANFAN_API_KEY", ""),
        timeout=120  # 2分钟超时
    )
    
    print("1. 测试 AI 生成...")
    print(f"提示词长度: {len(prompt)} 字符\n")
    
    try:
        # 调用 API
        messages = [{"role": "user", "content": prompt}]
        
        print("正在调用千帆 API...")
        response = client.chat(messages, model="glm-5.1", max_tokens=2000)
        
        if response.success:
            print(f"\n✅ API 调用成功！")
            print(f"生成内容长度: {len(response.content)} 字符\n")
            
            # 显示生成的内容
            print("=== 生成的内容 ===")
            print(response.content[:500])
            print("...\n")
            
            # 尝试解析 JSON
            print("2. 尝试解析 JSON...")
            import re
            json_match = re.search(r'\{[\s\S]*\}', response.content)
            
            if json_match:
                print("✅ 找到 JSON 格式")
                try:
                    data = json.loads(json_match.group())
                    chapters_data = data.get("chapters", [])
                    print(f"✅ JSON 解析成功，共 {len(chapters_data)} 章\n")
                    
                    # 显示解析结果
                    print("=== 解析结果 ===")
                    for chapter in chapters_data:
                        print(f"第 {chapter.get('chapter_num')} 章: {chapter.get('title')}")
                        print(f"  摘要: {chapter.get('summary', '')[:50]}...")
                        print()
                    
                    return True
                except json.JSONDecodeError as e:
                    print(f"❌ JSON 解析失败: {e}")
                    print(f"JSON 内容: {json_match.group()[:200]}...")
                    return False
            else:
                print("❌ 未找到 JSON 格式")
                print("生成的内容可能不是 JSON 格式")
                return False
        else:
            print(f"❌ API 调用失败: {response.content}")
            return False
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # 检查环境变量
    api_key = os.getenv("QIANFAN_API_KEY", "")
    if not api_key:
        print("❌ 未设置 QIANFAN_API_KEY 环境变量")
        print("请设置环境变量: export QIANFAN_API_KEY=your_api_key")
        sys.exit(1)
    
    print(f"API Key: {api_key[:10]}...\n")
    
    # 运行测试
    success = asyncio.run(test_outline_generation())
    
    if success:
        print("\n🎉 测试通过！大纲生成正常")
    else:
        print("\n❌ 测试失败，请检查 API 或提示词")