# -*- coding: utf-8 -*-
"""
数据库模型定义
使用 SQLAlchemy ORM
"""

from sqlalchemy import Column, String, Integer, Text, DateTime, JSON, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class NovelProjectDB(Base):
    """小说项目数据库模型"""
    __tablename__ = "novel_projects"

    novel_id = Column(String(50), primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    genre = Column(String(50), nullable=False)
    topic = Column(Text)
    theme = Column(Text)
    style_guide = Column(Text)
    total_chapters = Column(Integer, default=10)
    target_word_count = Column(Integer, default=3000)
    status = Column(String(50), default="draft")

    # 蓝图数据 (JSON)
    world_setting = Column(JSON)
    characters = Column(JSON)
    plot_blueprint = Column(JSON)

    # 章节大纲 (JSON)
    chapter_outlines = Column(JSON)

    # 元数据
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """转换为字典"""
        return {
            "novel_id": self.novel_id,
            "title": self.title,
            "genre": self.genre,
            "topic": self.topic,
            "theme": self.theme,
            "style_guide": self.style_guide,
            "total_chapters": self.total_chapters,
            "target_word_count": self.target_word_count,
            "status": self.status,
            "world_setting": self.world_setting,
            "characters": self.characters,
            "plot_blueprint": self.plot_blueprint,
            "chapter_outlines": self.chapter_outlines,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class ChapterContentDB(Base):
    """章节内容数据库模型"""
    __tablename__ = "chapter_contents"

    chapter_id = Column(String(50), primary_key=True, index=True)
    novel_id = Column(String(50), nullable=False, index=True)
    chapter_num = Column(Integer, nullable=False)
    title = Column(String(200))
    content = Column(Text)
    word_count = Column(Integer, default=0)

    # 章节元数据
    key_events = Column(JSON)
    characters_involved = Column(JSON)

    # 状态
    is_finalized = Column(Boolean, default=False)

    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """转换为字典"""
        return {
            "chapter_id": self.chapter_id,
            "novel_id": self.novel_id,
            "chapter_num": self.chapter_num,
            "title": self.title,
            "content": self.content,
            "word_count": self.word_count,
            "key_events": self.key_events,
            "characters_involved": self.characters_involved,
            "is_finalized": self.is_finalized,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
