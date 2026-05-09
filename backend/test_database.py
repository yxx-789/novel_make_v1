#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库测试脚本
测试数据库初始化和基本功能
"""

import sys
import os
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from database import init_db, get_db_session
from database.models import NovelProjectDB, ChapterContentDB
from database.repository import NovelRepository, ChapterRepository


def test_database():
    """测试数据库功能"""
    print("=" * 60)
    print("🧪 数据库功能测试")
    print("=" * 60)

    # 1. 初始化数据库
    print("\n1️⃣ 初始化数据库...")
    try:
        init_db()
        print("✅ 数据库初始化成功")
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        return False

    # 2. 测试创建小说项目
    print("\n2️⃣ 测试创建小说项目...")
    try:
        with get_db_session() as db:
            test_project = NovelRepository.create_project(db, {
                "novel_id": "test123",
                "title": "测试小说",
                "genre": "玄幻",
                "topic": "这是一个测试小说",
                "total_chapters": 5,
                "target_word_count": 3000
            })
            print(f"✅ 创建成功: {test_project.title} (ID: {test_project.novel_id})")
    except Exception as e:
        print(f"❌ 创建失败: {e}")
        return False

    # 3. 测试读取项目
    print("\n3️⃣ 测试读取小说项目...")
    try:
        with get_db_session() as db:
            project = NovelRepository.get_project(db, "test123")
            if project:
                print(f"✅ 读取成功: {project.title}")
                print(f"   - 类型: {project.genre}")
                print(f"   - 主题: {project.topic}")
            else:
                print("❌ 项目未找到")
                return False
    except Exception as e:
        print(f"❌ 读取失败: {e}")
        return False

    # 4. 测试保存蓝图
    print("\n4️⃣ 测试保存蓝图...")
    try:
        with get_db_session() as db:
            blueprint_data = {
                "world_setting": {
                    "era": "上古时期",
                    "location": "仙界",
                    "power_system": "灵气修炼"
                },
                "characters": [
                    {
                        "name": "林动",
                        "role": "主角",
                        "personality": "坚韧不拔"
                    }
                ],
                "plot_blueprint": {
                    "main_conflict": "正邪对抗",
                    "climax": "决战巅峰"
                }
            }
            
            updated_project = NovelRepository.save_blueprint(db, "test123", blueprint_data)
            if updated_project:
                print("✅ 蓝图保存成功")
                print(f"   - 世界观: {updated_project.world_setting}")
            else:
                print("❌ 蓝图保存失败")
                return False
    except Exception as e:
        print(f"❌ 蓝图保存失败: {e}")
        return False

    # 5. 测试保存大纲
    print("\n5️⃣ 测试保存章节大纲...")
    try:
        with get_db_session() as db:
            outlines_data = [
                {
                    "chapter_num": 1,
                    "title": "第一章 测试",
                    "summary": "这是测试大纲"
                },
                {
                    "chapter_num": 2,
                    "title": "第二章 测试",
                    "summary": "继续测试"
                }
            ]
            
            updated_project = NovelRepository.save_chapter_outlines(db, "test123", outlines_data)
            if updated_project:
                print("✅ 大纲保存成功")
                print(f"   - 章节数: {len(updated_project.chapter_outlines)}")
            else:
                print("❌ 大纲保存失败")
                return False
    except Exception as e:
        print(f"❌ 大纲保存失败: {e}")
        return False

    # 6. 测试创建章节
    print("\n6️⃣ 测试创建章节内容...")
    try:
        with get_db_session() as db:
            chapter = ChapterRepository.create_chapter(db, {
                "chapter_id": "ch001",
                "novel_id": "test123",
                "chapter_num": 1,
                "title": "第一章 测试章节",
                "content": "这是测试章节内容..." * 100,
                "word_count": 600
            })
            print(f"✅ 章节创建成功: {chapter.title}")
            print(f"   - 字数: {chapter.word_count}")
    except Exception as e:
        print(f"❌ 章节创建失败: {e}")
        return False

    # 7. 测试读取章节
    print("\n7️⃣ 测试读取章节...")
    try:
        with get_db_session() as db:
            chapters = ChapterRepository.list_chapters(db, "test123")
            if chapters:
                print(f"✅ 章节读取成功，共 {len(chapters)} 章")
                for ch in chapters:
                    print(f"   - {ch.title}: {ch.word_count} 字")
            else:
                print("❌ 未找到章节")
                return False
    except Exception as e:
        print(f"❌ 章节读取失败: {e}")
        return False

    # 8. 测试列出所有项目
    print("\n8️⃣ 测试列出所有项目...")
    try:
        with get_db_session() as db:
            projects = NovelRepository.list_projects(db)
            print(f"✅ 找到 {len(projects)} 个项目")
            for p in projects:
                print(f"   - {p.title} (ID: {p.novel_id})")
    except Exception as e:
        print(f"❌ 列出项目失败: {e}")
        return False

    # 9. 测试删除项目
    print("\n9️⃣ 测试删除项目...")
    try:
        with get_db_session() as db:
            success = NovelRepository.delete_project(db, "test123")
            if success:
                print("✅ 项目删除成功")
                
                # 验证章节也被删除
                chapters = ChapterRepository.list_chapters(db, "test123")
                if len(chapters) == 0:
                    print("✅ 关联章节也已删除")
                else:
                    print("⚠️ 关联章节未删除")
            else:
                print("❌ 项目删除失败")
                return False
    except Exception as e:
        print(f"❌ 删除失败: {e}")
        return False

    print("\n" + "=" * 60)
    print("✅ 所有测试通过！数据库功能正常")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_database()
    sys.exit(0 if success else 1)
