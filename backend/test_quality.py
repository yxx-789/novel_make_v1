#!/usr/bin/env python3
"""
测试生成质量和字数
"""
import os
import sys
import asyncio
import json
from pathlib import Path

os.environ['QIANFAN_API_KEY'] = 'bce-v3/ALTAK-vnASNnJZQkPchN6JShUdi/38e23c1484e3b2ab42e15dd596dc85fd4328caf4'
sys.path.insert(0, str(Path(__file__).parent))

from core.novel_engine_qianfan import NovelEngine

async def test_generation_quality():
    """测试生成质量和字数"""
    print("\n" + "="*80)
    print("生成质量和字数测试")
    print("="*80)

    config = {
        "model": "glm-5.1",
        "temperature": 0.7,
        "max_tokens": 100000
    }
    engine = NovelEngine(config)

    # 创建项目
    print("\n[创建项目]")
    project = await engine.create_project({
        "title": "修仙传说",
        "genre": "玄幻",
        "topic": "一个少年从凡人修成仙帝的故事",
        "total_chapters": 3,
        "target_word_count": 3000  # 正常字数
    })
    print(f"✅ 项目创建成功 - ID: {project.novel_id}")
    print(f"   目标字数/章: {project.target_word_count}")

    # 生成蓝图
    print("\n[生成蓝图]")
    blueprint = await engine.generate_blueprint(project.novel_id)
    print(f"✅ 蓝图生成成功")
    print(f"   核心冲突字数: {len(blueprint.main_conflict)} 字")
    print(f"   触发事件字数: {len(blueprint.inciting_incident)} 字")
    print(f"   高潮字数: {len(blueprint.climax)} 字")
    print(f"   转折点数: {len(blueprint.rising_actions)}")
    print(f"\n   核心冲突内容:\n{blueprint.main_conflict}")

    # 生成大纲
    print("\n[生成章节大纲]")
    outlines = await engine.generate_chapter_outline(project.novel_id)
    print(f"✅ 大纲生成成功 - 共 {len(outlines)} 章")
    for o in outlines:
        print(f"\n   第{o.chapter_num}章: {o.title}")
        print(f"   摘要字数: {len(o.summary)} 字")
        print(f"   摘要: {o.summary}")
        print(f"   关键事件数: {len(o.key_events)}")

    # 生成第1章（正常字数）
    print("\n[生成第1章内容]")
    chapter = await engine.generate_chapter(project.novel_id, 1, use_memory=False)
    print(f"✅ 第1章生成成功")
    print(f"   标题: {chapter.title}")
    print(f"   实际字数: {chapter.word_count}")
    print(f"   目标字数: {project.target_word_count}")
    print(f"   完成率: {chapter.word_count / project.target_word_count * 100:.1f}%")
    print(f"\n   内容预览（前300字）:\n{chapter.content[:300]}...")

    # 保存完整内容
    output_file = Path(__file__).parent / "test_generation_quality.md"
    output_file.write_text(f"# {project.title}\n\n" + chapter.content, encoding='utf-8')
    print(f"\n   完整内容已保存到: {output_file}")

    return blueprint, chapter

asyncio.run(test_generation_quality())
