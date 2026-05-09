# -*- coding: utf-8 -*-
"""
小说创作引擎 - 数据库版本
使用 SQLite/PostgreSQL 持久化存储
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

# 导入架构生成器
from core.architecture_generator import ArchitectureGenerator
from core.blueprint_generator import BlueprintGenerator
from core.chapter_planner import ChapterPlanner

# 导入 prompts
from prompts.architecture_prompts import (
    core_seed_prompt,
    character_dynamics_prompt,
    world_building_prompt,
    plot_architecture_prompt,
    create_character_state_prompt
)
from prompts.blueprint_prompts import (
    chapter_blueprint_prompt,
    chunked_chapter_blueprint_prompt
)
from prompts.planning_prompts import chapter_plan_prompt
from prompts.chapter_prompts import (
    first_chapter_draft_prompt,
    next_chapter_draft_prompt,
    summarize_recent_chapters_prompt
)


class LLMAdapter:
    """LLM 适配器 - 使用千帆 API"""

    def __init__(self, config: Dict[str, Any]):
        self.model = config.get("model", "glm-5.1")
        self.temperature = config.get("temperature", 0.7)
        self.max_tokens = config.get("max_tokens", 100000)

        # 初始化千帆客户端
        self.client = QianfanClient(
            api_key=config.get("api_key"),
            api_url=config.get("api_url"),
            model=self.model
        )

    async def generate(self, prompt: str, system_prompt: str = None) -> str:
        """生成文本"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response: QianfanResponse = self.client.chat(
            messages=messages,
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )

        if not response.success:
            raise RuntimeError(f"LLM generation failed: {response.content}")

        return response.content


class NovelEngineDB:
    """
    小说创作引擎 - 数据库版本

    核心功能：
    - 项目管理（数据库持久化）
    - 设定生成
    - 章节规划
    - 内容创作
    - 一致性检查
    - 导出功能
    """

    def __init__(self, llm_config: Dict, embedding_config: Dict = None):
        self.llm = LLMAdapter(llm_config)

        # 初始化数据库
        init_db()

        # 初始化架构生成器
        self.arch_gen = ArchitectureGenerator(self.llm.client)
        self.blueprint_gen = BlueprintGenerator(self.llm.client)
        self.planner = ChapterPlanner(self.llm.client)

    # ==================== 项目管理 ====================

    async def create_project(self, config: Dict) -> NovelProject:
        """创建小说项目"""
        project_id = str(uuid.uuid4())[:8]

        # 解析类型
        genre_str = config.get("genre", "玄幻")
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

        # 保存到数据库
        with get_db_session() as db:
            db_project = NovelRepository.create_project(db, {
                "novel_id": project_id,
                "title": config.get("title", "未命名小说"),
                "genre": genre.value,
                "topic": config.get("topic", ""),
                "theme": config.get("theme"),
                "style_guide": config.get("style_guide"),
                "total_chapters": config.get("total_chapters", 10),
                "target_word_count": config.get("target_word_count", 3000)
            })

        return NovelProject(**db_project.to_dict())

    async def get_project(self, project_id: str) -> Optional[NovelProject]:
        """获取项目"""
        with get_db_session() as db:
            db_project = NovelRepository.get_project(db, project_id)
            if db_project:
                return NovelProject(**db_project.to_dict())
        return None

    async def list_projects(self, page: int = 1, page_size: int = 10) -> List[NovelProject]:
        """列出项目"""
        with get_db_session() as db:
            db_projects = NovelRepository.list_projects(db, page, page_size)
            return [NovelProject(**p.to_dict()) for p in db_projects]

    async def delete_project(self, project_id: str) -> bool:
        """删除项目"""
        with get_db_session() as db:
            return NovelRepository.delete_project(db, project_id)

    # ==================== 蓝图生成 ====================

    async def generate_blueprint(self, novel_id: str) -> PlotBlueprint:
        """生成小说蓝图"""
        project = await self.get_project(novel_id)
        if not project:
            raise ValueError(f"Project {novel_id} not found")

        # 调用 LLM 生成蓝图
        blueprint_data = await self._generate_blueprint_with_llm(project)

        # 保存到数据库
        with get_db_session() as db:
            NovelRepository.save_blueprint(db, novel_id, blueprint_data)

        return PlotBlueprint(**blueprint_data)

    async def _generate_blueprint_with_llm(self, project: NovelProject) -> Dict:
        """使用 LLM 生成蓝图"""
        prompt = f"""
你是一位专业的网络小说策划师。请为以下小说生成详细的世界观、角色和情节蓝图：

小说标题：{project.title}
类型：{project.genre.value}
主题：{project.topic}
总章节数：{project.total_chapters}

【世界观设定要求】
- 时代背景
- 地点设定
- 力量体系（如果有）
- 社会结构

【角色设定要求】
- 主角（姓名、性格、背景、目标）
- 配角（至少3个）
- 反派（如果需要）

【情节蓝图要求】
- 核心冲突
- 触发事件
- 故事发展
- 高潮
- 结局

请以 JSON 格式输出：
{{
    "world_setting": {{
        "era": "时代",
        "location": "地点",
        "power_system": "力量体系",
        "social_structure": "社会结构"
    }},
    "characters": [
        {{
            "name": "姓名",
            "role": "主角/配角/反派",
            "personality": "性格",
            "background": "背景",
            "goal": "目标"
        }}
    ],
    "plot_blueprint": {{
        "main_conflict": "核心冲突",
        "inciting_incident": "触发事件",
        "rising_action": "故事发展",
        "climax": "高潮",
        "resolution": "结局"
    }}
}}
"""

        result = await self.llm.generate(prompt)

        try:
            import re
            json_match = re.search(r'\{[\s\S]*\}', result)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        # 返回默认结构
        return {
            "world_setting": {},
            "characters": [],
            "plot_blueprint": {}
        }

    # ==================== 章节大纲 ====================

    async def generate_chapter_outline(self, novel_id: str) -> List[ChapterOutline]:
        """生成详细的章节大纲"""
        project = await self.get_project(novel_id)
        if not project:
            raise ValueError(f"Project {novel_id} not found")

        # 调用 LLM 生成大纲
        outlines_data = await self._generate_outline_with_llm(project)

        # 保存到数据库
        with get_db_session() as db:
            NovelRepository.save_chapter_outlines(db, novel_id, outlines_data)

        # 转换为 ChapterOutline 对象
        outlines = []
        for outline_data in outlines_data:
            outline = ChapterOutline(
                outline_id=str(uuid.uuid4())[:8],
                novel_id=novel_id,
                chapter_num=outline_data.get("chapter_num", len(outlines) + 1),
                title=outline_data.get("title", f"第{len(outlines)+1}章"),
                summary=outline_data.get("summary", ""),
                key_events=outline_data.get("key_events", [])
            )
            outlines.append(outline)

        return outlines

    async def _generate_outline_with_llm(self, project: NovelProject) -> List[Dict]:
        """使用 LLM 生成章节大纲"""
        # 从数据库获取蓝图信息
        blueprint_info = ""
        if project.plot_blueprint:
            blueprint = project.plot_blueprint
            blueprint_info = f"""
【蓝图信息】
核心冲突：{blueprint.main_conflict[:200]}
触发事件：{blueprint.inciting_incident[:200]}
高潮：{blueprint.climax[:200]}
结局：{blueprint.resolution[:200]}
"""

        prompt = f"""
你是一位专业的网络小说大纲师。请为以下小说生成详细、引人入胜的章节大纲：

小说标题：{project.title}
类型：{project.genre.value}
主题：{project.topic}
总章节数：{project.total_chapters}
{blueprint_info}
【大纲要求】

请为每一章生成以下内容：

1. 章节标题（吸引人的标题）
2. 章节摘要（200字以上，详细的情节概括）
3. 关键事件（5-8个具体事件，每个事件50-100字）

【输出格式要求】
请以JSON格式输出：

{{
    "chapters": [
        {{
            "chapter_num": 1,
            "title": "引人入胜的章节标题",
            "summary": "200字以上的详细章节摘要...",
            "key_events": ["事件1", "事件2", "事件3"]
        }}
    ]
}}

请开始创作：
"""

        result = await self.llm.generate(prompt)

        try:
            import re
            json_match = re.search(r'\{[\s\S]*\}', result)
            if json_match:
                data = json.loads(json_match.group())
                return data.get("chapters", [])
        except:
            pass

        return []

    # ==================== 章节内容生成 ====================

    async def generate_chapter(
        self,
        novel_id: str,
        chapter_num: int,
        additional_guidance: str = None,
        use_memory: bool = True
    ) -> ChapterContent:
        """生成章节内容"""
        project = await self.get_project(novel_id)
        if not project:
            raise ValueError(f"Project {novel_id} not found")

        # 检查是否已有该章节
        with get_db_session() as db:
            existing_chapter = ChapterRepository.get_chapter(db, novel_id, chapter_num)
            if existing_chapter:
                # 返回已存在的章节
                return ChapterContent(**existing_chapter.to_dict())

        # 调用 LLM 生成章节内容
        chapter_data = await self._generate_chapter_content_with_llm(
            project, chapter_num, additional_guidance
        )

        # 保存到数据库
        chapter_id = str(uuid.uuid4())[:8]
        with get_db_session() as db:
            db_chapter = ChapterRepository.create_chapter(db, {
                "chapter_id": chapter_id,
                "novel_id": novel_id,
                "chapter_num": chapter_num,
                "title": chapter_data.get("title"),
                "content": chapter_data.get("content"),
                "word_count": len(chapter_data.get("content", "")),
                "key_events": chapter_data.get("key_events"),
                "characters_involved": chapter_data.get("characters_involved")
            })

        return ChapterContent(**db_chapter.to_dict())

    async def _generate_chapter_content_with_llm(
        self,
        project: NovelProject,
        chapter_num: int,
        additional_guidance: str = None
    ) -> Dict:
        """使用 LLM 生成章节内容"""
        # 获取章节大纲
        outline_info = ""
        if project.chapter_outlines:
            for outline in project.chapter_outlines:
                if outline.chapter_num == chapter_num:
                    outline_info = f"""
【章节大纲】
标题：{outline.title}
摘要：{outline.summary}
关键事件：{outline.key_events}
"""
                    break

        prompt = f"""
你是一位专业的网络小说作家。请为以下小说生成第 {chapter_num} 章的内容：

小说标题：{project.title}
类型：{project.genre.value}
主题：{project.topic}
{outline_info}
{f"【额外指导】{additional_guidance}" if additional_guidance else ""}

【要求】
- 字数：{project.target_word_count} 字左右
- 风格：{project.style_guide if project.style_guide else "标准网文风格"}
- 情节紧凑，有吸引力
- 人物性格鲜明
- 对话生动自然

请直接输出章节内容（不需要标题）：
"""

        result = await self.llm.generate(prompt)

        return {
            "title": f"第 {chapter_num} 章",
            "content": result,
            "key_events": [],
            "characters_involved": []
        }

    # ==================== 导出功能 ====================

    async def export_novel(self, novel_id: str, format: str = "markdown") -> str:
        """导出小说"""
        project = await self.get_project(novel_id)
        if not project:
            raise ValueError(f"Project {novel_id} not found")

        # 获取所有章节
        with get_db_session() as db:
            chapters = ChapterRepository.list_chapters(db, novel_id)

        if format == "markdown":
            output = f"# {project.title}\n\n"
            output += f"**类型**: {project.genre.value}\n\n"
            output += f"**主题**: {project.topic}\n\n"
            output += "---\n\n"

            for chapter in chapters:
                output += f"## {chapter.title}\n\n"
                output += chapter.content + "\n\n"

            return output

        # 其他格式...
        return ""
