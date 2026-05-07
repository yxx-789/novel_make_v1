#!/usr/bin/env python3
"""
端到端链路测试 - 超简化版
只验证每个环节都能调用成功
"""
import os
import sys
import asyncio
import json
from pathlib import Path

os.environ['QIANFAN_API_KEY'] = 'bce-v3/ALTAK-vnASNnJZQkPchN6JShUdi/38e23c1484e3b2ab42e15dd596dc85fd4328caf4'
sys.path.insert(0, str(Path(__file__).parent))

from core.novel_engine_qianfan import NovelEngine

async def test_chain():
    """测试端到端链路"""
    print("\n" + "="*80)
    print("端到端链路测试 - 小说创作")
    print("="*80)

    config = {
        "model": "glm-5.1",
        "temperature": 0.7,
        "max_tokens": 100000
    }
    engine = NovelEngine(config)

    # 步骤1: 创建项目
    print("\n[步骤1/5] 创建小说项目")
    try:
        project = await engine.create_project({
            "title": "修仙之路",
            "genre": "玄幻",
            "topic": "少年修仙的故事",
            "total_chapters": 2,
            "target_word_count": 200
        })
        novel_id = project.novel_id
        print(f"✅ 创建成功 - ID: {novel_id}")
    except Exception as e:
        print(f"❌ 创建失败: {e}")
        return False

    # 步骤2: 生成蓝图
    print("\n[步骤2/5] 生成小说蓝图")
    try:
        blueprint = await engine.generate_blueprint(novel_id)
        print(f"✅ 蓝图生成成功")
        print(f"   核心冲突: {blueprint.main_conflict[:50]}...")
        print(f"   触发事件: {blueprint.inciting_incident[:50]}...")
    except Exception as e:
        print(f"❌ 蓝图生成失败: {e}")
        return False

    # 步骤3: 生成章节大纲
    print("\n[步骤3/5] 生成章节大纲")
    try:
        outlines = await engine.generate_chapter_outline(novel_id)
        print(f"✅ 大纲生成成功 - 共 {len(outlines)} 章")
        if outlines:
            print(f"   第1章: {outlines[0].title}")
            print(f"   第2章: {outlines[1].title if len(outlines) > 1 else 'N/A'}")
    except Exception as e:
        print(f"❌ 大纲生成失败: {e}")
        return False

    # 步骤4: 生成第1章内容（缩短内容）
    print("\n[步骤4/5] 生成第1章内容（缩短版）")
    try:
        chapter = await engine.generate_chapter(
            novel_id, 1, 
            additional_guidance="请生成精简版，不超过100字",
            use_memory=False
        )
        print(f"✅ 第1章生成成功")
        print(f"   标题: {chapter.title}")
        print(f"   字数: {chapter.word_count}")
        print(f"   内容: {chapter.content[:80]}...")
    except Exception as e:
        print(f"❌ 第1章生成失败: {e}")
        return False

    # 步骤5: 导出小说
    print("\n[步骤5/5] 导出小说")
    try:
        content = await engine.export_novel(novel_id, "markdown")
        print(f"✅ 导出成功")
        print(f"   格式: markdown")
        print(f"   长度: {len(content)} 字符")
        return True
    except Exception as e:
        print(f"❌ 导出失败: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_chain())
    
    print("\n" + "="*80)
    if result:
        print("🎉 端到端链路测试通过！")
    else:
        print("⚠️  链路测试失败")
    print("="*80)