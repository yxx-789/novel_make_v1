#!/usr/bin/env python3
"""
剧本转换链路测试
"""
import os
import sys
import asyncio
import json
from pathlib import Path

os.environ['QIANFAN_API_KEY'] = 'bce-v3/ALTAK-vnASNnJZQkPchN6JShUdi/38e23c1484e3b2ab42e15dd596dc85fd4328caf4'
sys.path.insert(0, str(Path(__file__).parent))

from core.drama_engine import DramaEngine

async def test_drama():
    """测试剧本转换链路"""
    print("\n" + "="*80)
    print("剧本转换链路测试")
    print("="*80)

    config = {
        "model": "glm-5.1",
        "temperature": 0.7,
        "max_tokens": 100000
    }
    engine = DramaEngine(config)

    # 步骤1: 创建剧本项目
    print("\n[步骤1/4] 创建剧本项目")
    try:
        project = await engine.create_project({
            "title": "修仙传说短剧",
            "episode_duration": 90,
            "chapters_per_episode": 1
        })
        drama_id = project.project_id
        print(f"✅ 创建成功 - ID: {drama_id}")
    except Exception as e:
        print(f"❌ 创建失败: {e}")
        return False

    # 步骤2: 解析小说
    print("\n[步骤2/4] 解析小说文本")
    novel_text = """
第一章：灵根觉醒

青石村后山，林风刚采到一株灵芝，胖恶霸赵虎便一脚踩烂："穷鬼，东西交出来！"

林风咬牙不退，被一掌拍落悬崖。剧痛中他坠入幽暗山洞，意外摸到一块冰冷玉佩。

指尖鲜血滴落，玉佩骤然爆发璀璨光芒！

"凡人，你唤醒了我。"苍老声音在脑海响起，"我乃上古仙帝，今日赐你造化！"

林风感到一股暖流涌遍全身，他的修为开始飞速提升。
    """

    try:
        parsed = await engine.parse_novel(novel_text)
        print(f"✅ 解析成功")
        print(f"   主要角色: {parsed.get('main_characters', [])}")
    except Exception as e:
        print(f"❌ 解析失败: {e}")
        return False

    # 步骤3: 生成剧本
    print("\n[步骤3/4] 生成分镜头剧本")
    try:
        # 先生成大纲
        outline = await engine.map_to_episode_outline(
            novel_text=novel_text,
            characters=[{"name": "林风"}, {"name": "赵虎"}, {"name": "仙帝"}],
            episode_num=1,
            chapter_range="1"
        )
        print(f"   大纲映射成功")

        # 生成剧本
        script = await engine.generate_script(
            outline=outline,
            novel_text=novel_text,
            characters=[{"name": "林风"}, {"name": "赵虎"}, {"name": "仙帝"}]
        )
        print(f"✅ 剧本生成成功")
        print(f"   剧本ID: {script.script_id}")
        print(f"   场景数: {len(script.scenes)}")
        if script.scenes and script.scenes[0].shots:
            shot = script.scenes[0].shots[0]
            print(f"   第1镜头: {shot.shot_type} - {shot.visual[:50]}...")
    except Exception as e:
        print(f"❌ 剧本生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False

    # 步骤4: 导出剧本
    print("\n[步骤4/4] 导出剧本")
    try:
        output_files = await engine.export_script(script, ["json", "markdown"])
        print(f"✅ 导出成功")
        print(f"   输出格式: {list(output_files.keys())}")
        return True
    except Exception as e:
        print(f"❌ 导出失败: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_drama())
    
    print("\n" + "="*80)
    if result:
        print("🎉 剧本转换链路测试通过！")
    else:
        print("⚠️  剧本转换链路失败")
    print("="*80)