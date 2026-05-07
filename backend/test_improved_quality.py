#!/usr/bin/env python3
"""
测试改进后的生成质量
"""
import os
import sys
import asyncio
import json
from pathlib import Path

os.environ['QIANFAN_API_KEY'] = 'bce-v3/ALTAK-vnASNnJZQkPchN6JShUdi/38e23c1484e3b2ab42e15dd596dc85fd4328caf4'
sys.path.insert(0, str(Path(__file__).parent))

from core.novel_engine_qianfan import NovelEngine

async def test_improved_quality():
    """测试改进后的生成质量"""
    print("\n" + "="*80)
    print("改进后的生成质量测试")
    print("="*80)

    config = {
        "model": "glm-5.1",
        "temperature": 0.7,
        "max_tokens": 100000
    }
    engine = NovelEngine(config)

    # 创建项目（正常字数）
    print("\n[1. 创建项目]")
    project = await engine.create_project({
        "title": "修仙传说",
        "genre": "玄幻",
        "topic": "一个少年从凡人修成仙帝的故事，包含奇遇、修炼、战斗、情感等丰富元素",
        "total_chapters": 3,
        "target_word_count": 3000
    })
    print(f"✅ 项目创建成功")
    print(f"   ID: {project.novel_id}")
    print(f"   标题: {project.title}")
    print(f"   目标字数/章: {project.target_word_count}")

    # 生成蓝图（改进后）
    print("\n[2. 生成详细蓝图]")
    blueprint = await engine.generate_blueprint(project.novel_id)
    
    print(f"✅ 蓝图生成成功")
    print(f"   核心冲突字数: {len(blueprint.main_conflict)} 字")
    print(f"   触发事件字数: {len(blueprint.inciting_incident)} 字")
    print(f"   转折点数: {len(blueprint.rising_actions)}")
    print(f"   高潮字数: {len(blueprint.climax)} 字")
    print(f"   下降行动数: {len(blueprint.falling_actions)}")
    print(f"   结局字数: {len(blueprint.resolution)} 字")
    
    # 计算总字数
    total_words = (
        len(blueprint.main_conflict) +
        len(blueprint.inciting_incident) +
        sum(len(action) for action in blueprint.rising_actions) +
        len(blueprint.climax) +
        sum(len(action) for action in blueprint.falling_actions) +
        len(blueprint.resolution)
    )
    print(f"   蓝图总字数: {total_words} 字")
    
    print(f"\n📋 蓝图预览：")
    print(f"   核心冲突: {blueprint.main_conflict[:100]}...")
    print(f"   触发事件: {blueprint.inciting_incident[:100]}...")
    if blueprint.rising_actions:
        print(f"   第1个转折: {blueprint.rising_actions[0][:80]}...")

    # 生成大纲（改进后）
    print("\n[3. 生成详细大纲]")
    outlines = await engine.generate_chapter_outline(project.novel_id)
    print(f"✅ 大纲生成成功 - 共 {len(outlines)} 章")
    
    if outlines:
        first_outline = outlines[0]
        print(f"\n📋 第1章大纲：")
        print(f"   标题: {first_outline.title}")
        print(f"   摘要字数: {len(first_outline.summary)} 字")
        print(f"   摘要预览: {first_outline.summary[:100]}...")
        print(f"   关键事件数: {len(first_outline.key_events)}")
        if first_outline.key_events:
            print(f"   第1个事件: {first_outline.key_events[0][:60]}...")

    # 生成第1章（正常字数）
    print("\n[4. 生成第1章]")
    chapter = await engine.generate_chapter(project.novel_id, 1, use_memory=False)
    print(f"✅ 第1章生成成功")
    print(f"   标题: {chapter.title}")
    print(f"   实际字数: {chapter.word_count}")
    print(f"   目标字数: {project.target_word_count}")
    print(f"   完成率: {chapter.word_count / project.target_word_count * 100:.1f}%")
    
    # 保存结果
    output_dir = Path(__file__).parent / "output_improved"
    output_dir.mkdir(exist_ok=True)
    
    # 保存蓝图
    blueprint_file = output_dir / "blueprint.json"
    blueprint_data = {
        "main_conflict": blueprint.main_conflict,
        "inciting_incident": blueprint.inciting_incident,
        "rising_actions": blueprint.rising_actions,
        "climax": blueprint.climax,
        "falling_actions": blueprint.falling_actions,
        "resolution": blueprint.resolution
    }
    blueprint_file.write_text(json.dumps(blueprint_data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\n💾 蓝图已保存: {blueprint_file}")
    
    # 保存大纲
    outlines_file = output_dir / "outlines.json"
    outlines_data = [o.dict() for o in outlines]
    outlines_file.write_text(json.dumps(outlines_data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"💾 大纲已保存: {outlines_file}")
    
    # 保存章节
    chapter_file = output_dir / "chapter_1.md"
    chapter_content = f"# {chapter.title}\n\n{chapter.content}"
    chapter_file.write_text(chapter_content, encoding='utf-8')
    print(f"💾 第1章已保存: {chapter_file}")
    
    print("\n" + "="*80)
    print("🎉 改进后的生成质量测试完成")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(test_improved_quality())