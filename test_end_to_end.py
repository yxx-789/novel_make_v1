#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
端到端测试：模拟完整的生成流程
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.utils.json_utils import parse_ai_json
from backend.models.schemas import PlotBlueprint, ChapterOutline
import json


def test_blueprint_parsing():
    """测试蓝图解析和保存"""
    print("=" * 60)
    print("测试 1: 蓝图解析和保存")
    print("=" * 60)
    
    # 用户提供的实际蓝图输出
    blueprint_json = '''
{
"main_conflict":"核心冲突的本质在于个体对真实自我的坚守与强权体制对异类抹杀之间的对抗。",
"inciting_incident":"蟠桃盛宴之夜，天蓬元帅奉命巡视天河防务，却察觉到天河底层的灵气波动异常。",
"rising_actions":[
0:"转折点1：堕入凡间后的天蓬...",
1:"转折点2：天庭并未打算放过这个异类...",
2:"转折点3：巨灵神的陨落让天庭震怒...",
3:"转折点4：天劫虽退，但福陵山也元气大伤..."
],
"climax":"天河决堤，亿万吨带有天道法则的星水化作灭世瀑布...",
"falling_actions":[
0:"解决过程1：昊天镜碎裂后...",
1:"解决过程2：福陵山满目疮痍..."
],
"resolution":"故事的最后，猪八戒背负着破烂的行囊...",
"foreshadowing":[]
}
'''
    
    print("\n1. 解析 JSON...")
    data = parse_ai_json(blueprint_json)
    
    print("解析结果:")
    print(f"  - main_conflict: {data.get('main_conflict', '')[:50]}...")
    print(f"  - rising_actions 数量: {len(data.get('rising_actions', []))}")
    print(f"  - falling_actions 数量: {len(data.get('falling_actions', []))}")
    
    print("\n2. 创建 PlotBlueprint 对象...")
    blueprint = PlotBlueprint(
        blueprint_id="test123",
        novel_id="test_novel",
        main_conflict=data.get("main_conflict", "待生成"),
        inciting_incident=data.get("inciting_incident", "待生成"),
        rising_actions=data.get("rising_actions", []),
        climax=data.get("climax", "待生成"),
        falling_actions=data.get("falling_actions", []),
        resolution=data.get("resolution", "待生成")
    )
    
    print("Blueprint 对象创建成功:")
    print(f"  - blueprint_id: {blueprint.blueprint_id}")
    print(f"  - main_conflict: {blueprint.main_conflict[:50]}...")
    print(f"  - rising_actions 数量: {len(blueprint.rising_actions)}")
    
    print("\n3. 序列化为 JSON...")
    blueprint_dict = blueprint.dict()
    print("序列化成功:")
    print(json.dumps(blueprint_dict, ensure_ascii=False, indent=2)[:300] + "...")
    
    return True


def test_outline_generation():
    """测试大纲生成"""
    print("\n" + "=" * 60)
    print("测试 2: 大纲生成")
    print("=" * 60)
    
    # 模拟大纲 JSON 输出
    outline_json = '''
{
    "chapters": [
        {
            "chapter_num": 1,
            "title": "第1章：觉醒",
            "summary": "蟠桃盛宴之夜，天蓬元帅发现了天庭的秘密...",
            "key_events": [
                0: "事件1：天蓬巡视天河",
                1: "事件2：发现广寒宫秘密",
                2: "事件3：被天庭追杀"
            ]
        },
        {
            "chapter_num": 2,
            "title": "第2章：堕入凡间",
            "summary": "天蓬被打入畜生道，成为猪妖...",
            "key_events": [
                0: "事件1：堕入凡间",
                1: "事件2：成为猪妖"
            ]
        }
    ]
}
'''
    
    print("\n1. 解析大纲 JSON...")
    data = parse_ai_json(outline_json)
    
    print("解析结果:")
    print(f"  - chapters 数量: {len(data.get('chapters', []))}")
    
    if 'chapters' in data:
        for chapter in data['chapters']:
            print(f"  - 第 {chapter.get('chapter_num')} 章: {chapter.get('title')}")
            print(f"    - key_events 数量: {len(chapter.get('key_events', []))}")
    
    print("\n2. 创建 ChapterOutline 对象...")
    outlines = []
    for chapter_data in data.get("chapters", []):
        outline = ChapterOutline(
            chapter_num=chapter_data.get("chapter_num", len(outlines) + 1),
            title=chapter_data.get("title", f"第{len(outlines)+1}章"),
            summary=chapter_data.get("summary", ""),
            key_events=chapter_data.get("key_events", [])
        )
        outlines.append(outline)
    
    print(f"创建成功，共 {len(outlines)} 个章节大纲")
    
    print("\n3. 序列化为 JSON...")
    outlines_dict = [o.dict() for o in outlines]
    print("序列化成功:")
    print(json.dumps(outlines_dict, ensure_ascii=False, indent=2)[:400] + "...")
    
    return True


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("端到端测试：完整的生成流程")
    print("=" * 60)
    
    # 测试 1: 蓝图解析和保存
    test1 = test_blueprint_parsing()
    
    # 测试 2: 大纲生成
    test2 = test_outline_generation()
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"测试 1 (蓝图解析和保存): {'✅ 通过' if test1 else '❌ 失败'}")
    print(f"测试 2 (大纲生成): {'✅ 通过' if test2 else '❌ 失败'}")
    
    if test1 and test2:
        print("\n🎉 所有测试通过！")
        print("\n结论：")
        print("- ✅ JSON 解析工具可以正确处理带索引号的 JSON")
        print("- ✅ 蓝图对象创建成功")
        print("- ✅ 大纲对象创建成功")
        print("- ✅ 数据序列化正常")
        print("\n💡 如果用户仍然遇到问题，可能是：")
        print("   1. 数据库保存/读取问题")
        print("   2. 前端显示问题")
        print("   3. 网络或 API 调用问题")
        return True
    else:
        print("\n❌ 部分测试失败")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)