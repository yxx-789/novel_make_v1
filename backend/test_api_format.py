#!/usr/bin/env python3
"""
测试千帆 API 响应格式
"""
import os
import sys
import json
from pathlib import Path

os.environ['QIANFAN_API_KEY'] = 'bce-v3/ALTAK-vnASNnJZQkPchN6JShUdi/38e23c1484e3b2ab42e15dd596dc85fd4328caf4'
sys.path.insert(0, str(Path(__file__).parent))

from utils.qianfan_client import QianfanClient

print("=" * 80)
print("测试千帆 API JSON 响应格式")
print("=" * 80)

client = QianfanClient(
    api_key=os.environ['QIANFAN_API_KEY'],
    model="glm-5.1"
)

# 测试蓝图生成的 prompt
prompt = """
你是一位专业的小说策划师。请为以下小说生成详细的创作蓝图：

小说标题：修仙传说
类型：玄幻
主题/梗概：一个少年从凡人修成仙帝的故事
总章节数：2

请生成：
1. 核心冲突（一句话概括主要矛盾）
2. 触发事件（故事开始的契机）
3. 上升行动（3-5个关键转折点）
4. 高潮（故事最高潮）
5. 下降行动（高潮后的解决过程）
6. 结局（最终结果）

以JSON格式输出：
{
    "main_conflict": "核心冲突描述",
    "inciting_incident": "触发事件描述",
    "rising_actions": ["转折1", "转折2", "转折3"],
    "climax": "高潮描述",
    "falling_actions": ["解决过程1", "解决过程2"],
    "resolution": "结局描述"
}
"""

print("\n发送请求...")
messages = [{"role": "user", "content": prompt}]

response = client.chat(
    messages=messages,
    temperature=0.7,
    max_tokens=1000
)

if response.success:
    print(f"✅ API 调用成功")
    print(f"\n原始响应:\n{response.content}\n")

    # 尝试解析 JSON
    import re
    json_match = re.search(r'\{[\s\S]*\}', response.content)

    if json_match:
        print("=" * 80)
        print("找到 JSON 部分:")
        print("=" * 80)
        print(json_match.group())
        print()

        try:
            data = json.loads(json_match.group())
            print("✅ JSON 解析成功:")
            print(json.dumps(data, ensure_ascii=False, indent=2))
        except Exception as e:
            print(f"❌ JSON 解析失败: {e}")
    else:
        print("❌ 未找到 JSON 格式")
else:
    print(f"❌ API 调用失败: {response.content}")

print("\n" + "=" * 80)
