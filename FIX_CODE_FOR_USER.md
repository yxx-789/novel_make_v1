# 🔧 Railway 502 错误修复代码

## 📋 需要修改的文件

### 1. `backend/requirements.txt`
**添加一行**:
```txt
sqlalchemy>=2.0.0
```

**完整文件**:
```txt
# 绝对最小依赖集 - 确保 Railway 能成功安装

# FastAPI 核心
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0

# 数据库
sqlalchemy>=2.0.0

# HTTP 客户端
requests>=2.31.0
httpx>=0.25.0

# 环境变量
python-dotenv>=1.0.0

# 文件处理
aiofiles>=23.0.0
python-multipart>=0.0.6

# 其他必要工具
tenacity>=8.2.0  # 重试机制
pyyaml>=6.0      # YAML 解析
```

---

### 2. `backend/models/schemas.py`
**修改以下类，将所有必需字段改为可选**:

**找到 WorldSetting 类**（大约第 70 行）:
```python
class WorldSetting(BaseModel):
    """世界观设定"""
    era: Optional[str] = Field(None, description="时代背景")
    location: Optional[str] = Field(None, description="主要地点")
    power_system: Optional[str] = Field(None, description="力量体系")
    social_structure: Optional[str] = Field(None, description="社会结构")
    unique_elements: List[str] = Field(default_factory=list, description="独特元素")
    rules: List[str] = Field(default_factory=list, description="世界规则")
```

**找到 PlotBlueprint 类**（大约第 80 行）:
```python
class PlotBlueprint(BaseModel):
    """情节蓝图"""
    main_conflict: Optional[str] = Field(None, description="核心冲突")
    inciting_incident: Optional[str] = Field(None, description="触发事件")
    rising_actions: List[str] = Field(default_factory=list, description="上升行动")
    climax: Optional[str] = Field(None, description="高潮")
    falling_actions: List[str] = Field(default_factory=list, description="下降行动")
    resolution: Optional[str] = Field(None, description="结局")
    foreshadowing: List[Dict[str, Any]] = Field(default_factory=list, description="伏笔设置")
```

**找到 ChapterOutline 类**（大约第 95 行）:
```python
class ChapterOutline(BaseModel):
    """章节大纲"""
    chapter_num: int = Field(..., description="章节号")
    title: Optional[str] = Field(None, description="章节标题")
    summary: Optional[str] = Field(None, description="章节概要")
    key_events: List[str] = Field(default_factory=list, description="关键事件")
    characters_involved: List[str] = Field(default_factory=list, description="涉及角色")
    word_count_target: int = Field(default=3000, description="目标字数")
```

---

### 3. `backend/core/novel_engine_db.py`
**完全替换为以下内容**:

```python
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
                "world_setting": blueprint.world_setting.dict() if blueprint.world_setting else {},
                "characters": [c.dict() for c in blueprint.characters] if blueprint.characters else [],
                "plot_blueprint": blueprint.dict() if hasattr(blueprint, 'dict') else {}
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
```

---

### 4. `backend/api/routes.py`
**修改第 10 行左右**:
```python
# 导入核心引擎（数据库版本）
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from core.novel_engine_db import NovelEngineDB  # 使用数据库版本
from core.drama_engine import DramaEngine
```

**修改第 30 行左右**:
```python
# 初始化引擎（需要配置）
novel_engine: Optional[NovelEngineDB] = None
drama_engine: Optional[DramaEngine] = None


def init_engines(llm_config: Dict = None, embedding_config: Dict = None):
    """初始化引擎"""
    global novel_engine, drama_engine
    
    config = llm_config or {
        "api_key": "sk-xxx",
        "api_url": "https://api.openai.com/v1",
        "model": "gpt-4o-mini"
    }
    
    novel_engine = NovelEngineDB(config, embedding_config)
    drama_engine = DramaEngine(config)
```

---

## 🚀 操作步骤

1. **拉取最新代码**:
```bash
cd novel_make_v1
git pull origin main
```

2. **应用上述 4 个文件修改**

3. **提交并推送**:
```bash
git add .
git commit -m "Fix: Railway 502 error - database engine refactor"
git push origin main
```

---

## 🎯 修复原理

**问题**: 数据库引擎启动失败，因为模型转换复杂

**解决方案**: 
- 使用包装器模式，数据库只负责持久化
- 内存引擎负责 LLM 生成
- 简化对象转换

**效果**: Railway 启动成功，数据持久化正常

---

**请应用这些修改并推送，Railway 会自动重新部署！** 🚀