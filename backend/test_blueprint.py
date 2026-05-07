#!/usr/bin/env python3
"""
核心功能测试 - 创建项目和生成蓝图
"""
import os
import sys
import asyncio
from pathlib import Path

# 设置环境变量
os.environ['QIANFAN_API_KEY'] = 'bce-v3/ALTAK-vnASNnJZQkPchN6JShUdi/38e23c1484e3b2ab42e15dd596dc85fd4328caf4'

# 添加路径
sys.path.insert(0, str(Path(__file__).parent))

from core.novel_engine_qianfan import NovelEngine

print("=" * 70)
print("核心功能测试")
print("=" * 70)


async def test_blueprint():
    """测试蓝图生成"""
    config = {
        "model": "glm-5.1",
        "temperature": 0.7,
        "max_tokens": 100000
    }

    engine = NovelEngine(config)

    # 测试 1: 创建项目
    print("\n[测试 1/3] 创建小说项目")
    try:
        project = await engine.create_project({
            "title": "测试小说",
            "genre": "玄幻",
            "topic": "一个少年修仙的故事",
            "total_chapters": 1,
            "target_word_count": 500
        })
        print(f"✅ 项目创建成功 - ID: {project.novel_id}")
        novel_id = project.novel_id
    except Exception as e:
        print(f"❌ 创建失败: {e}")
        import traceback
        traceback.print_exc()
        return

    # 测试 2: 生成蓝图
    print("\n[测试 2/3] 生成小说蓝图")
    try:
        blueprint = await engine.generate_blueprint(novel_id)
        print(f"✅ 蓝图生成成功")
        print(f"   核心冲突: {blueprint.main_conflict[:50]}...")
        print(f"   触发事件: {blueprint.inciting_incident[:50]}...")
        print(f"   转折点数: {len(blueprint.rising_actions)}")
    except Exception as e:
        print(f"❌ 蓝图生成失败: {e}")
        import traceback
        traceback.print_exc()
        return

    # 测试 3: 生成大纲
    print("\n[测试 3/3] 生成章节大纲")
    try:
        outlines = await engine.generate_chapter_outline(novel_id)
        print(f"✅ 大纲生成成功 - 共 {len(outlines)} 章")
        for o in outlines:
            print(f"   第{o.chapter_num}章: {o.title}")
    except Exception as e:
        print(f"❌ 大纲生成失败: {e}")
        import traceback
        traceback.print_exc()
        return

    print("\n" + "=" * 70)
    print("🎉 所有核心功能测试通过！")
    print("=" * 70)


asyncio.run(test_blueprint())
