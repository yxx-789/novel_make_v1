# -*- coding: utf-8 -*-
"""
小说创作引擎 - 数据库版本（简化版）
暂时只持久化基本数据，避免复杂对象转换问题
"""

import sys
import os
from typing import List, Dict, Optional, Any
from pathlib import Path
import json
import uuid
from datetime import datetime

# 导入数据库模块
sys.path.insert(0, str(Path(__file__).parent.parent))
from database import get_db_session, init_db
from database.repository import NovelRepository, ChapterRepository

# 导入千帆客户端
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.qianfan_client import QianfanClient, QianfanResponse

# 导入模型
sys.path.insert(0, str(Path(__file__).parent.parent))
from models.schemas import (
    NovelProject, CharacterProfile, WorldSetting, PlotBlueprint,
    ChapterOutline, ChapterContent, NovelGenre, NovelStatus
)

# 导入原版引擎（用于LLM生成）
from core.novel_engine_qianfan import NovelEngine as NovelEngineMemory


class NovelEngineDB:
    """
    小说创作引擎 - 数据库版本（包装器模式）

    策略：使用原版内存引擎进行LLM生成，用数据库持久化结果
    """

    def __init__(self, llm_config: Dict, embedding_config: Dict = None):
        # 初始化数据库
        init_db()

        # 初始化内存引擎（用于LLM生成）
        self.memory_engine = NovelEngineMemory(llm_config, embedding_config)

    # ==================== 项目管理 ====================

    async def create_project(self, config: Dict) -> NovelProject:
        """创建小说项目"""
        # 使用内存引擎创建项目
        project = await self.memory_engine.create_project(config)

        # 保存到数据库
        with get_db_session() as db:
            NovelRepository.create_project(db, {
                "novel_id": project.novel_id,
                "title": project.title,
                "genre": project.genre.value,
                "topic": project.topic,
                "theme": project.theme,
                "style_guide": project.style_guide,
                "total_chapters": project.total_chapters,
                "target_word_count": project.target_word_count
            })

        return project

    async def get_project(self, project_id: str) -> Optional[NovelProject]:
        """获取项目"""
        # 先从数据库读取
        with get_db_session() as db:
            db_project = NovelRepository.get_project(db, project_id)
            if db_project:
                # 从数据库恢复项目状态
                project = await self._restore_project_from_db(db_project)
                # 同步到内存引擎
                self.memory_engine.projects[project_id] = project
                return project

        return None

    async def _restore_project_from_db(self, db_project) -> NovelProject:
        """从数据库恢复项目对象"""
        # 解析类型
        genre_str = db_project.genre
        genre_map = {
            "玄幻": NovelGenre.FANTASY,
            "都市": NovelGenre.URBAN,
            "言情": NovelGenre.ROMANCE,
            "科幻": NovelGenre.SCIFI,
            "历史": NovelGenre.HISTORY,
            "奇幻": NovelGenre.FANTASY,
            "仙侠": NovelGenre.XIANXIA,
            "武侠": NovelGenre.WUXIA,
            "悬疑": NovelGenre.SUSPENSE,
            "其他": NovelGenre.OTHER
        }
        genre = genre_map.get(genre_str, NovelGenre.FANTASY)

        # 创建 NovelProject 对象
        project = NovelProject(
            novel_id=db_project.novel_id,
            title=db_project.title,
            genre=genre,
            topic=db_project.topic,
            theme=db_project.theme,
            style_guide=db_project.style_guide,
            total_chapters=db_project.total_chapters,
            target_word_count=db_project.target_word_count
        )

        # 恢复蓝图数据
        if db_project.world_setting:
            project.world_setting = WorldSetting(**db_project.world_setting)

        if db_project.characters:
            project.characters = [CharacterProfile(**c) for c in db_project.characters]

        if db_project.plot_blueprint:
            project.plot_blueprint = PlotBlueprint(**db_project.plot_blueprint)

        # 恢复章节大纲
        if db_project.chapter_outlines:
            project.chapters = [ChapterOutline(**o) for o in db_project.chapter_outlines]

        return project

    async def list_projects(self, page: int = 1, page_size: int = 10) -> List[NovelProject]:
        """列出项目"""
        with get_db_session() as db:
            db_projects = NovelRepository.list_projects(db, page, page_size)

            projects = []
            for db_p in db_projects:
                project = await self._restore_project_from_db(db_p)
                projects.append(project)
                # 同步到内存引擎
                self.memory_engine.projects[project.novel_id] = project

            return projects

    async def delete_project(self, project_id: str) -> bool:
        """删除项目"""
        # 从内存引擎删除
        if project_id in self.memory_engine.projects:
            del self.memory_engine.projects[project_id]

        # 从数据库删除
        with get_db_session() as db:
            return NovelRepository.delete_project(db, project_id)

    # ==================== 蓝图生成 ====================

    async def generate_blueprint(self, novel_id: str) -> PlotBlueprint:
        """生成小说蓝图"""
        # 确保项目已加载到内存
        project = await self.get_project(novel_id)
        if not project:
            raise ValueError(f"Project {novel_id} not found")

        # 使用内存引擎生成蓝图
        blueprint = await self.memory_engine.generate_blueprint(novel_id)

        # 保存到数据库
        with get_db_session() as db:
            blueprint_data = {
                "world_setting": blueprint.dict().get("world_setting", {}) if blueprint else {},
                "characters": blueprint.dict().get("characters", []) if blueprint else [],
                "plot_blueprint": blueprint.dict() if blueprint else {}
            }
            NovelRepository.save_blueprint(db, novel_id, blueprint_data)

        return blueprint

    # ==================== 章节大纲 ====================

    async def generate_chapter_outline(self, novel_id: str) -> List[ChapterOutline]:
        """生成详细的章节大纲"""
        # 确保项目已加载到内存
        project = await self.get_project(novel_id)
        if not project:
            raise ValueError(f"Project {novel_id} not found")

        # 使用内存引擎生成大纲
        outlines = await self.memory_engine.generate_chapter_outline(novel_id)

        # 保存到数据库
        with get_db_session() as db:
            outlines_data = [o.dict() for o in outlines]
            NovelRepository.save_chapter_outlines(db, novel_id, outlines_data)

        return outlines

    # ==================== 章节内容生成 ====================

    async def generate_chapter(
            self,
            novel_id: str,
            chapter_num: int,
            additional_guidance: str = None,
            use_memory: bool = True
    ) -> ChapterContent:
        """生成章节内容"""
        # 确保项目已加载到内存
        project = await self.get_project(novel_id)
        if not project:
            raise ValueError(f"Project {novel_id} not found")

        # 使用内存引擎生成章节
        chapter = await self.memory_engine.generate_chapter(
            novel_id, chapter_num, additional_guidance, use_memory
        )

        # 保存到数据库
        chapter_id = str(uuid.uuid4())[:8]
        with get_db_session() as db:
            ChapterRepository.create_chapter(db, {
                "chapter_id": chapter_id,
                "novel_id": novel_id,
                "chapter_num": chapter_num,
                "title": chapter.title,
                "content": chapter.content,
                "word_count": chapter.word_count
            })

        return chapter

    # ==================== 其他方法委托给内存引擎 ====================

    async def finalize_chapter(self, novel_id: str, chapter_num: int):
        """最终化章节"""
        return await self.memory_engine.finalize_chapter(novel_id, chapter_num)

    async def check_consistency(self, novel_id: str, chapter_num: int):
        """检查章节一致性"""
        return await self.memory_engine.check_consistency(novel_id, chapter_num)

    async def export_novel(self, novel_id: str, format: str = "markdown") -> str:
        """导出小说"""
        return await self.memory_engine.export_novel(novel_id, format)