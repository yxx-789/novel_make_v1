#!/usr/bin/env python3
"""
简化版测试 - 验证架构系统基本功能
"""
import os
import sys
import asyncio
from pathlib import Path

os.environ['QIANFAN_API_KEY'] = 'bce-v3/ALTAK-vnASNnJZQkPchN6JShUdi/38e23c1484e3b2ab42e15dd596dc85fd4328caf4'
sys.path.insert(0, str(Path(__file__).parent))

from utils.qianfan_client import QianfanClient
from core.novel_engine_qianfan import NovelEngine

def test_basic_functionality():
    """测试基本功能"""
    print("\n" + "="*80)
    print("简化版功能测试")
    print("="*80)
    
    # 配置
    config = {
        "model": "glm-5.1",
        "temperature": 0.7,
        "max_tokens": 100000
    }
    
    engine = NovelEngine(config)
    
    # 测试1：创建项目
    print("\n[测试1: 创建项目]")
    project = asyncio.run(engine.create_project({
        "title": "测试小说",
        "genre": "玄幻",
        "topic": "测试主题",
        "total_chapters": 3,
        "target_word_count": 2000
    }))
    print(f"✅ 项目创建成功: {project.novel_id}")
    
    # 测试2：生成蓝图（简化版）
    print("\n[测试2: 生成蓝图]")
    try:
        blueprint = asyncio.run(engine.generate_blueprint(project.novel_id))
        print(f"✅ 蓝图生成成功")
        print(f"   核心冲突: {blueprint.main_conflict[:50]}...")
    except Exception as e:
        print(f"⚠️ 蓝图生成失败: {e}")
    
    # 测试3：生成大纲
    print("\n[测试3: 生成大纲]")
    try:
        outlines = asyncio.run(engine.generate_chapter_outline(project.novel_id))
        print(f"✅ 大纲生成成功: {len(outlines)} 章")
        if outlines:
            print(f"   第1章: {outlines[0].title}")
    except Exception as e:
        print(f"⚠️ 大纲生成失败: {e}")
    
    # 测试4：生成章节
    print("\n[测试4: 生成章节]")
    try:
        chapter = asyncio.run(engine.generate_chapter(project.novel_id, 1, use_memory=False))
        print(f"✅ 章节生成成功")
        print(f"   标题: {chapter.title}")
        print(f"   字数: {chapter.word_count}")
    except Exception as e:
        print(f"⚠️ 章节生成失败: {e}")
    
    print("\n" + "="*80)
    print("🎉 基本功能测试完成")
    print("="*80)

if __name__ == "__main__":
    test_basic_functionality()
