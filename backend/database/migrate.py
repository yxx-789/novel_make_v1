#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库迁移和初始化脚本
用于初始化数据库和迁移现有数据
"""

import sys
import os
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from database import init_db, get_db_session
from database.models import NovelProjectDB, ChapterContentDB
from sqlalchemy import text


def create_tables():
    """创建数据库表"""
    print("📦 创建数据库表...")
    init_db()
    print("✅ 数据库表创建完成")


def check_database():
    """检查数据库状态"""
    print("\n📊 检查数据库状态...")

    with get_db_session() as db:
        # 检查小说项目数量
        novel_count = db.query(NovelProjectDB).count()
        print(f"   小说项目数量: {novel_count}")

        # 检查章节数量
        chapter_count = db.query(ChapterContentDB).count()
        print(f"   章节数量: {chapter_count}")

        # 列出所有项目
        if novel_count > 0:
            print("\n   📚 已有小说项目:")
            projects = db.query(NovelProjectDB).all()
            for p in projects:
                print(f"      - {p.title} (ID: {p.novel_id})")


def test_database_connection():
    """测试数据库连接"""
    print("\n🔍 测试数据库连接...")

    try:
        with get_db_session() as db:
            # 执行简单查询
            result = db.execute(text("SELECT 1"))
            print("✅ 数据库连接成功")
            return True
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 50)
    print("🗄️  数据库初始化和迁移工具")
    print("=" * 50)

    # 测试连接
    if not test_database_connection():
        print("\n❌ 数据库连接失败，请检查配置")
        sys.exit(1)

    # 创建表
    create_tables()

    # 检查状态
    check_database()

    print("\n" + "=" * 50)
    print("✅ 数据库初始化完成")
    print("=" * 50)


if __name__ == "__main__":
    main()
