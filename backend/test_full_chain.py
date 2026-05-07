#!/usr/bin/env python3
"""
完整链路测试 - 从创建到生成全流程
"""
import os
import sys
import asyncio
import json
from pathlib import Path

# 设置环境变量
os.environ['QIANFAN_API_KEY'] = 'bce-v3/ALTAK-vnASNnJZQkPchN6JShUdi/38e23c1484e3b2ab42e15dd596dc85fd4328caf4'

sys.path.insert(0, str(Path(__file__).parent))

from core.novel_engine_qianfan import NovelEngine
from core.drama_engine import DramaEngine

print("\n" + "="*80)
print("完整链路测试 - 小说创作 + 剧本转换")
print("="*80)

novel_id = None
drama_id = None

async def test_novel_chain():
    """测试小说创作完整链路"""
    global novel_id

    print("\n" + "="*80)
    print("【小说创作链路】")
    print("="*80)

    config = {
        "model": "glm-5.1",
        "temperature": 0.7,
        "max_tokens": 100000
    }
    engine = NovelEngine(config)

    # 步骤1: 创建项目
    print("\n[步骤1/6] 创建小说项目")
    try:
        project = await engine.create_project({
            "title": "修仙传说",
            "genre": "玄幻",
            "topic": "一个少年从凡人修成仙帝的故事",
            "total_chapters": 2,
            "target_word_count": 300  # 降低字数以加快测试
        })
        novel_id = project.novel_id
        print(f"✅ 项目创建成功")
        print(f"   ID: {novel_id}")
        print(f"   标题: {project.title}")
        print(f"   类型: {project.genre.value}")
        print(f"   总章节: {project.total_chapters}")
    except Exception as e:
        print(f"❌ 创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False

    # 步骤2: 生成蓝图
    print("\n[步骤2/6] 生成小说蓝图")
    try:
        blueprint = await engine.generate_blueprint(novel_id)
        print(f"✅ 蓝图生成成功")
        print(f"   核心冲突: {blueprint.main_conflict[:80]}...")
        print(f"   触发事件: {blueprint.inciting_incident[:80]}...")
        print(f"   高潮: {blueprint.climax[:80]}...")
        print(f"   转折点: {len(blueprint.rising_actions)} 个")
    except Exception as e:
        print(f"❌ 蓝图生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False

    # 步骤3: 生成章节大纲
    print("\n[步骤3/6] 生成章节大纲")
    try:
        outlines = await engine.generate_chapter_outline(novel_id)
        print(f"✅ 大纲生成成功")
        print(f"   总章节: {len(outlines)}")
        for o in outlines:
            print(f"   第{o.chapter_num}章: {o.title}")
            print(f"     摘要: {o.summary[:50]}...")
    except Exception as e:
        print(f"❌ 大纲生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False

    # 步骤4: 生成第1章内容
    print("\n[步骤4/6] 生成第1章内容")
    try:
        chapter1 = await engine.generate_chapter(novel_id, 1, use_memory=False)
        print(f"✅ 第1章生成成功")
        print(f"   标题: {chapter1.title}")
        print(f"   字数: {chapter1.word_count}")
        print(f"   内容预览: {chapter1.content[:100]}...")
    except Exception as e:
        print(f"❌ 第1章生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False

    # 步骤5: 生成第2章内容
    print("\n[步骤5/6] 生成第2章内容")
    try:
        chapter2 = await engine.generate_chapter(novel_id, 2, use_memory=True)
        print(f"✅ 第2章生成成功")
        print(f"   标题: {chapter2.title}")
        print(f"   字数: {chapter2.word_count}")
        print(f"   内容预览: {chapter2.content[:100]}...")
    except Exception as e:
        print(f"❌ 第2章生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False

    # 步骤6: 导出小说
    print("\n[步骤6/6] 导出小说")
    try:
        content = await engine.export_novel(novel_id, "markdown")
        print(f"✅ 导出成功")
        print(f"   格式: markdown")
        print(f"   总长度: {len(content)} 字符")

        # 保存到文件
        output_file = Path(__file__).parent / "test_output_novel.md"
        output_file.write_text(content, encoding='utf-8')
        print(f"   已保存到: {output_file}")
    except Exception as e:
        print(f"❌ 导出失败: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True


async def test_drama_chain():
    """测试剧本转换完整链路"""
    global drama_id

    print("\n" + "="*80)
    print("【剧本转换链路】")
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
        print(f"✅ 剧本项目创建成功")
        print(f"   ID: {drama_id}")
        print(f"   标题: {project.title}")
    except Exception as e:
        print(f"❌ 创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False

    # 步骤2: 解析小说文本
    print("\n[步骤2/4] 解析小说文本")
    novel_text = """
第一章：少年觉醒

少年林风站在悬崖边，望着远方的云海。他虽然出身平凡，但心中燃烧着修仙的梦想。

"我一定要成为仙帝！"林风握紧拳头，眼中闪烁着坚定的光芒。

突然，一道金光从天而降，直接钻入林风的眉心。这是传说中的仙缘！

林风感到体内涌起一股强大的力量，他的修为开始飞速提升。
    """

    try:
        parsed = await engine.parse_novel(novel_text)
        print(f"✅ 小说解析成功")
        print(f"   主要角色: {parsed.get('main_characters', [])}")
        print(f"   场景数: {len(parsed.get('scenes', []))}")
    except Exception as e:
        print(f"❌ 解析失败: {e}")
        import traceback
        traceback.print_exc()
        return False

    # 步骤3: 生成剧本
    print("\n[步骤3/4] 生成分镜头剧本")
    try:
        # 先生成大纲
        outline = await engine.map_to_episode_outline(
            novel_id=drama_id,
            episode_num=1,
            chapter_range="1"
        )
        print(f"   大纲映射成功")

        # 生成剧本
        script = await engine.generate_script(
            outline=outline,
            novel_chapter_text=novel_text,
            characters=["林风"]
        )
        print(f"✅ 剧本生成成功")
        print(f"   剧本ID: {script.script_id}")
        print(f"   场景数: {len(script.scenes)}")
        if script.scenes:
            scene = script.scenes[0]
            print(f"   第1场景: {scene.location}")
            print(f"   镜头数: {len(scene.shots)}")
            if scene.shots:
                shot = scene.shots[0]
                print(f"   第1镜头: {shot.shot_type} - {shot.description[:50]}...")
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
        print(f"   输出文件: {output_files}")

        # 保存到本地
        output_dir = Path(__file__).parent / "test_output_drama"
        output_dir.mkdir(exist_ok=True)

        if "json" in output_files:
            json_file = output_dir / "script.json"
            json_file.write_text(json.dumps(script.dict(), ensure_ascii=False, indent=2), encoding='utf-8')
            print(f"   JSON已保存: {json_file}")

        if "markdown" in output_files:
            md_file = output_dir / "script.md"
            md_file.write_text(output_files["markdown"], encoding='utf-8')
            print(f"   Markdown已保存: {md_file}")
    except Exception as e:
        print(f"❌ 导出失败: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True


async def main():
    """主测试"""
    print("\n开始测试...")

    # 测试小说创作链路
    novel_ok = await test_novel_chain()

    # 测试剧本转换链路
    drama_ok = await test_drama_chain()

    # 总结
    print("\n" + "="*80)
    print("测试结果总结")
    print("="*80)

    print(f"\n小说创作链路: {'✅ 通过' if novel_ok else '❌ 失败'}")
    print(f"剧本转换链路: {'✅ 通过' if drama_ok else '❌ 失败'}")

    if novel_ok and drama_ok:
        print("\n🎉 完整链路测试通过！所有功能正常！")
    else:
        print("\n⚠️  部分链路失败，请检查错误信息")

    print("="*80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
