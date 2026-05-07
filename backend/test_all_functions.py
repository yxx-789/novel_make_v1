#!/usr/bin/env python3
"""
完整功能测试脚本
测试所有 API 接口和引擎功能
"""
import os
import sys
import asyncio
import json
from pathlib import Path

# 设置环境变量
os.environ['QIANFAN_API_KEY'] = 'bce-v3/ALTAK-vnASNnJZQkPchN6JShUdi/38e23c1484e3b2ab42e15dd596dc85fd4328caf4'

# 添加路径
sys.path.insert(0, str(Path(__file__).parent))

from core.novel_engine_qianfan import NovelEngine
from core.drama_engine import DramaEngine


def print_section(title):
    """打印分节标题"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_success(msg):
    """打印成功信息"""
    print(f"✅ {msg}")


def print_error(msg):
    """打印错误信息"""
    print(f"❌ {msg}")


def print_info(msg):
    """打印信息"""
    print(f"ℹ️  {msg}")


async def test_novel_engine():
    """测试小说创作引擎"""
    print_section("小说创作引擎测试")

    # 配置
    config = {
        "model": "glm-5.1",
        "temperature": 0.7,
        "max_tokens": 100000
    }

    engine = NovelEngine(config)

    # 测试 1: 创建项目
    print("\n[测试 1/7] 创建小说项目")
    try:
        project = await engine.create_project({
            "title": "修仙之路",
            "genre": "玄幻",
            "topic": "一个少年从凡人修成仙帝的故事",
            "total_chapters": 3,
            "target_word_count": 500
        })
        print_success(f"项目创建成功 - ID: {project.novel_id}")
        print_info(f"标题: {project.title}")
        print_info(f"类型: {project.genre.value}")
        novel_id = project.novel_id
    except Exception as e:
        print_error(f"创建失败: {e}")
        return False

    # 测试 2: 生成蓝图
    print("\n[测试 2/7] 生成小说蓝图")
    try:
        blueprint = await engine.generate_blueprint(novel_id)
        print_success("蓝图生成成功")
        print_info(f"核心冲突: {blueprint.main_conflict}")
        print_info(f"触发事件: {blueprint.inciting_incident}")
        print_info(f"转折点数: {len(blueprint.rising_actions)}")
    except Exception as e:
        print_error(f"蓝图生成失败: {e}")
        return False

    # 测试 3: 生成章节大纲
    print("\n[测试 3/7] 生成章节大纲")
    try:
        outlines = await engine.generate_chapter_outline(novel_id)
        print_success(f"大纲生成成功 - 共 {len(outlines)} 章")
        for o in outlines:
            print_info(f"  第{o.chapter_num}章: {o.title}")
    except Exception as e:
        print_error(f"大纲生成失败: {e}")
        return False

    # 测试 4: 生成第 1 章内容
    print("\n[测试 4/7] 生成第 1 章内容")
    try:
        chapter = await engine.generate_chapter(novel_id, 1, use_memory=False)
        print_success("章节生成成功")
        print_info(f"标题: {chapter.title}")
        print_info(f"字数: {chapter.word_count}")
        print_info(f"内容预览: {chapter.content[:100]}...")
    except Exception as e:
        print_error(f"章节生成失败: {e}")
        return False

    # 测试 5: 最终化章节
    print("\n[测试 5/7] 最终化章节")
    try:
        result = await engine.finalize_chapter(novel_id, 1)
        print_success("章节最终化成功")
        print_info(f"新角色: {result.get('new_characters', [])}")
        print_info(f"情节点: {result.get('plot_points', [])}")
    except Exception as e:
        print_error(f"最终化失败: {e}")
        return False

    # 测试 6: 一致性检查
    print("\n[测试 6/7] 一致性检查")
    try:
        result = await engine.check_consistency(novel_id, 1)
        print_success("一致性检查完成")
        print_info(f"整体一致性: {result.get('overall_consistency', '良好')}")
        issues = result.get('issues', [])
        if issues:
            print_info(f"发现 {len(issues)} 个问题")
        else:
            print_info("未发现一致性问题")
    except Exception as e:
        print_error(f"一致性检查失败: {e}")
        return False

    # 测试 7: 导出小说
    print("\n[测试 7/7] 导出小说")
    try:
        content = await engine.export_novel(novel_id, "markdown")
        print_success("小说导出成功")
        print_info(f"导出格式: markdown")
        print_info(f"内容长度: {len(content)} 字符")
    except Exception as e:
        print_error(f"导出失败: {e}")
        return False

    return True


async def test_drama_engine():
    """测试剧本转换引擎"""
    print_section("剧本转换引擎测试")

    # 配置
    config = {
        "model": "glm-5.1",
        "temperature": 0.7,
        "max_tokens": 100000
    }

    engine = DramaEngine(config)

    # 测试 1: 创建剧本项目
    print("\n[测试 1/5] 创建剧本项目")
    try:
        project = await engine.create_project({
            "title": "修仙之路短剧",
            "episode_duration": 90,
            "chapters_per_episode": 1
        })
        print_success(f"剧本项目创建成功 - ID: {project.project_id}")
        print_info(f"标题: {project.title}")
        print_info(f"每集时长: {project.episode_duration}秒")
        drama_id = project.project_id
    except Exception as e:
        print_error(f"创建失败: {e}")
        return False

    # 测试 2: 解析小说
    print("\n[测试 2/5] 解析小说文本")
    try:
        novel_text = """
第一章：少年觉醒

少年林风站在悬崖边，望着远方的云海。他虽然出身平凡，但心中燃烧着修仙的梦想。

"我一定要成为仙帝！"林风握紧拳头，眼中闪烁着坚定的光芒。

突然，一道金光从天而降，直接钻入林风的眉心。这是传说中的仙缘！

林风感到体内涌起一股强大的力量，他的修为开始飞速提升。
        """

        parsed = await engine.parse_novel(novel_text)
        print_success("小说解析成功")
        print_info(f"主要角色: {parsed.get('main_characters', [])}")
        print_info(f"章节数: {len(parsed.get('chapters', []))}")
    except Exception as e:
        print_error(f"解析失败: {e}")
        return False

    # 测试 3: 大纲映射
    print("\n[测试 3/5] 大纲映射到剧集")
    try:
        outline = await engine.map_to_episode_outline(
            novel_id=drama_id,
            episode_num=1,
            chapter_range="1"
        )
        print_success("大纲映射成功")
        print_info(f"集数: {outline.episode_num}")
        print_info(f"场景数: {len(outline.scenes)}")
    except Exception as e:
        print_error(f"大纲映射失败: {e}")
        return False

    # 测试 4: 生成剧本
    print("\n[测试 4/5] 生成分镜头剧本")
    try:
        script = await engine.generate_script(
            outline=outline,
            novel_chapter_text=novel_text,
            characters=["林风"]
        )
        print_success("剧本生成成功")
        print_info(f"剧本ID: {script.script_id}")
        print_info(f"场景数: {len(script.scenes)}")
        if script.scenes:
            print_info(f"第1场景镜头数: {len(script.scenes[0].shots)}")
    except Exception as e:
        print_error(f"剧本生成失败: {e}")
        return False

    # 测试 5: 导出剧本
    print("\n[测试 5/5] 导出剧本")
    try:
        output_files = await engine.export_script(script, ["json", "markdown"])
        print_success("剧本导出成功")
        print_info(f"导出文件: {output_files}")
    except Exception as e:
        print_error(f"导出失败: {e}")
        return False

    return True


async def test_qianfan_client():
    """测试千帆客户端"""
    print_section("千帆 API 客户端测试")

    from utils.qianfan_client import QianfanClient

    print("\n[测试 1/2] 初始化客户端")
    try:
        client = QianfanClient(
            api_key=os.environ['QIANFAN_API_KEY'],
            model="glm-5.1"
        )
        print_success("客户端初始化成功")
    except Exception as e:
        print_error(f"初始化失败: {e}")
        return False

    print("\n[测试 2/2] 发送测试请求")
    try:
        messages = [
            {"role": "system", "content": "你是一个有帮助的助手。"},
            {"role": "user", "content": "请用一句话介绍你自己。"}
        ]
        response = client.chat(messages, temperature=0.7, max_tokens=50)

        if response.success:
            print_success("API 调用成功")
            print_info(f"响应: {response.content}")
            print_info(f"模型: {response.model}")
            print_info(f"Token 使用: {response.usage}")
        else:
            print_error(f"API 调用失败: {response.content}")
            return False
    except Exception as e:
        print_error(f"请求失败: {e}")
        return False

    return True


async def main():
    """主测试函数"""
    print("\n" + "🚀" * 35)
    print("  小说创作平台 - 完整功能测试")
    print("🚀" * 35)

    results = {}

    # 测试千帆客户端
    results['千帆客户端'] = await test_qianfan_client()

    # 测试小说引擎
    results['小说引擎'] = await test_novel_engine()

    # 测试剧本引擎
    results['剧本引擎'] = await test_drama_engine()

    # 打印总结
    print_section("测试结果总结")

    all_passed = True
    for name, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{name:20s} {status}")
        if not passed:
            all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("🎉 所有测试通过！系统功能完整！")
    else:
        print("⚠️  部分测试失败，请检查错误信息")
    print("=" * 70 + "\n")

    return all_passed


if __name__ == "__main__":
    asyncio.run(main())
