# -*- coding: utf-8 -*-
"""
数据库仓库层
提供数据库操作的封装
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from .models import NovelProjectDB, ChapterContentDB


class NovelRepository:
    """小说项目仓库"""

    @staticmethod
    def create_project(db: Session, project_data: Dict[str, Any]) -> NovelProjectDB:
        """创建小说项目"""
        db_project = NovelProjectDB(
            novel_id=project_data["novel_id"],
            title=project_data["title"],
            genre=project_data["genre"],
            topic=project_data.get("topic"),
            theme=project_data.get("theme"),
            style_guide=project_data.get("style_guide"),
            total_chapters=project_data.get("total_chapters", 10),
            target_word_count=project_data.get("target_word_count", 3000),
            status=project_data.get("status", "draft")
        )
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project

    @staticmethod
    def get_project(db: Session, novel_id: str) -> Optional[NovelProjectDB]:
        """获取小说项目"""
        return db.query(NovelProjectDB).filter(NovelProjectDB.novel_id == novel_id).first()

    @staticmethod
    def list_projects(db: Session, page: int = 1, page_size: int = 10) -> List[NovelProjectDB]:
        """列出小说项目"""
        offset = (page - 1) * page_size
        return db.query(NovelProjectDB).order_by(NovelProjectDB.created_at.desc()).offset(offset).limit(page_size).all()

    @staticmethod
    def update_project(db: Session, novel_id: str, update_data: Dict[str, Any]) -> Optional[NovelProjectDB]:
        """更新小说项目"""
        db_project = NovelRepository.get_project(db, novel_id)
        if not db_project:
            return None

        for key, value in update_data.items():
            if hasattr(db_project, key) and value is not None:
                setattr(db_project, key, value)

        db.commit()
        db.refresh(db_project)
        return db_project

    @staticmethod
    def delete_project(db: Session, novel_id: str) -> bool:
        """删除小说项目"""
        db_project = NovelRepository.get_project(db, novel_id)
        if not db_project:
            return False

        # 同时删除所有章节内容
        db.query(ChapterContentDB).filter(ChapterContentDB.novel_id == novel_id).delete()

        db.delete(db_project)
        db.commit()
        return True

    @staticmethod
    def save_blueprint(db: Session, novel_id: str, blueprint_data: Dict[str, Any]) -> Optional[NovelProjectDB]:
        """保存蓝图数据"""
        db_project = NovelRepository.get_project(db, novel_id)
        if not db_project:
            return None

        db_project.world_setting = blueprint_data.get("world_setting")
        db_project.characters = blueprint_data.get("characters")
        db_project.plot_blueprint = blueprint_data.get("plot_blueprint")

        db.commit()
        db.refresh(db_project)
        return db_project

    @staticmethod
    def save_chapter_outlines(db: Session, novel_id: str, outlines_data: List[Dict[str, Any]]) -> Optional[NovelProjectDB]:
        """保存章节大纲"""
        db_project = NovelRepository.get_project(db, novel_id)
        if not db_project:
            return None

        db_project.chapter_outlines = outlines_data

        db.commit()
        db.refresh(db_project)
        return db_project


class ChapterRepository:
    """章节内容仓库"""

    @staticmethod
    def create_chapter(db: Session, chapter_data: Dict[str, Any]) -> ChapterContentDB:
        """创建章节内容"""
        db_chapter = ChapterContentDB(
            chapter_id=chapter_data["chapter_id"],
            novel_id=chapter_data["novel_id"],
            chapter_num=chapter_data["chapter_num"],
            title=chapter_data.get("title"),
            content=chapter_data.get("content"),
            word_count=chapter_data.get("word_count", 0),
            key_events=chapter_data.get("key_events"),
            characters_involved=chapter_data.get("characters_involved"),
            is_finalized=chapter_data.get("is_finalized", False)
        )
        db.add(db_chapter)
        db.commit()
        db.refresh(db_chapter)
        return db_chapter

    @staticmethod
    def get_chapter(db: Session, novel_id: str, chapter_num: int) -> Optional[ChapterContentDB]:
        """获取章节内容"""
        return db.query(ChapterContentDB).filter(
            and_(
                ChapterContentDB.novel_id == novel_id,
                ChapterContentDB.chapter_num == chapter_num
            )
        ).first()

    @staticmethod
    def list_chapters(db: Session, novel_id: str) -> List[ChapterContentDB]:
        """列出小说的所有章节"""
        return db.query(ChapterContentDB).filter(
            ChapterContentDB.novel_id == novel_id
        ).order_by(ChapterContentDB.chapter_num).all()

    @staticmethod
    def update_chapter(db: Session, chapter_id: str, update_data: Dict[str, Any]) -> Optional[ChapterContentDB]:
        """更新章节内容"""
        db_chapter = db.query(ChapterContentDB).filter(ChapterContentDB.chapter_id == chapter_id).first()
        if not db_chapter:
            return None

        for key, value in update_data.items():
            if hasattr(db_chapter, key) and value is not None:
                setattr(db_chapter, key, value)

        db.commit()
        db.refresh(db_chapter)
        return db_chapter

    @staticmethod
    def delete_chapter(db: Session, chapter_id: str) -> bool:
        """删除章节"""
        db_chapter = db.query(ChapterContentDB).filter(ChapterContentDB.chapter_id == chapter_id).first()
        if not db_chapter:
            return False

        db.delete(db_chapter)
        db.commit()
        return True
