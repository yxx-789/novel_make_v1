# -*- coding: utf-8 -*-
"""
统一数据模型定义
整合 AI Novel Generator 和 Novel to Drama 的数据结构
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime


# ==================== 枚举定义 ====================

class NovelGenre(str, Enum):
    """小说类型"""
    FANTASY = "玄幻"
    URBAN = "都市"
    ROMANCE = "言情"
    SCIFI = "科幻"
    HISTORY = "历史"
    SUSPENSE = "悬疑"
    WUXIA = "武侠"
    XIANXIA = "仙侠"
    OTHER = "其他"


class DramaFormat(str, Enum):
    """剧本格式"""
    JSON = "json"
    MARKDOWN = "markdown"
    CSV = "csv"
    FDX = "fdx"  # Final Draft 格式


class NovelStatus(str, Enum):
    """小说状态"""
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FINALIZED = "finalized"


class DramaStatus(str, Enum):
    """剧本状态"""
    PENDING = "pending"
    MAPPING = "mapping"
    GENERATING = "generating"
    COMPLETED = "completed"


# ==================== 小说创作模型 ====================

class CharacterProfile(BaseModel):
    """角色档案"""
    name: str = Field(..., description="角色名称")
    role: str = Field(..., description="角色定位（主角/配角/反派）")
    age: Optional[int] = Field(None, description="年龄")
    gender: Optional[str] = Field(None, description="性别")
    personality: List[str] = Field(default_factory=list, description="性格特点")
    background: Optional[str] = Field(None, description="背景故事")
    abilities: List[str] = Field(default_factory=list, description="能力/技能")
    relationships: Dict[str, str] = Field(default_factory=dict, description="人物关系")
    avatar_url: Optional[str] = Field(None, description="头像URL")


class WorldSetting(BaseModel):
    """世界观设定"""
    era: str = Field(..., description="时代背景")
    location: str = Field(..., description="主要地点")
    power_system: Optional[str] = Field(None, description="力量体系")
    social_structure: Optional[str] = Field(None, description="社会结构")
    unique_elements: List[str] = Field(default_factory=list, description="独特元素")
    rules: List[str] = Field(default_factory=list, description="世界规则")


class PlotBlueprint(BaseModel):
    """情节蓝图"""
    main_conflict: str = Field(..., description="核心冲突")
    inciting_incident: str = Field(..., description="触发事件")
    rising_actions: List[str] = Field(default_factory=list, description="上升行动")
    climax: str = Field(..., description="高潮")
    falling_actions: List[str] = Field(default_factory=list, description="下降行动")
    resolution: str = Field(..., description="结局")
    foreshadowing: List[Dict[str, Any]] = Field(default_factory=list, description="伏笔设置")  # 改为Any，允许int或str


class ChapterOutline(BaseModel):
    """章节大纲"""
    chapter_num: int = Field(..., description="章节号")
    title: str = Field(..., description="章节标题")
    summary: str = Field(..., description="章节概要")
    key_events: List[str] = Field(default_factory=list, description="关键事件")
    characters_involved: List[str] = Field(default_factory=list, description="涉及角色")
    word_count_target: int = Field(default=3000, description="目标字数")


class ChapterContent(BaseModel):
    """章节内容"""
    chapter_num: int
    title: str
    content: str
    word_count: int
    summary: Optional[str] = None
    characters_updated: List[str] = Field(default_factory=list)
    plot_points: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)


class NovelProject(BaseModel):
    """小说项目"""
    novel_id: str = Field(..., description="项目ID")
    title: str = Field(..., description="小说标题")
    author: str = Field(default="AI", description="作者")
    genre: NovelGenre = Field(..., description="类型")
    status: NovelStatus = Field(default=NovelStatus.DRAFT)
    
    # 设定
    topic: str = Field(..., description="主题")
    theme: Optional[str] = Field(None, description="核心主题")
    world_setting: Optional[WorldSetting] = None
    characters: List[CharacterProfile] = Field(default_factory=list)
    plot_blueprint: Optional[PlotBlueprint] = None
    
    # 新增：架构和蓝图文本
    architecture: Optional[Dict[str, str]] = Field(None, description="完整架构（核心种子、角色动力学、世界观、情节架构、角色状态）")
    blueprint_text: Optional[str] = Field(None, description="详细章节蓝图文本")
    
    # 章节
    total_chapters: int = Field(default=0, description="总章节数")
    chapters: List[ChapterOutline] = Field(default_factory=list)
    generated_chapters: List[ChapterContent] = Field(default_factory=list)
    
    # 配置
    target_word_count: int = Field(default=3000, description="每章目标字数")
    style_guide: Optional[str] = Field(None, description="风格指南")
    
    # 元数据
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    word_count: int = Field(default=0)
    
    class Config:
        arbitrary_types_allowed = True


# ==================== 剧本转换模型 ====================

class ShotInfo(BaseModel):
    """镜头信息"""
    shot_num: int = Field(..., description="镜头编号")
    shot_type: str = Field(..., description="景别（特写/中景/远景）")
    duration: float = Field(..., description="时长（秒）")
    visual: str = Field(..., description="画面描述")
    action: Optional[str] = Field(None, description="人物动作")
    camera_movement: Optional[str] = Field(None, description="运镜方式")
    dialogue: Optional[Dict[str, str]] = Field(None, description="台词 {speaker: content}")
    emotion_tone: Optional[str] = Field(None, description="情绪基调")
    sound_effects: List[str] = Field(default_factory=list, description="音效")
    bgm: Optional[str] = Field(None, description="背景音乐")


class SceneInfo(BaseModel):
    """场景信息"""
    scene_num: int = Field(..., description="场景编号")
    location: str = Field(..., description="地点")
    time_of_day: str = Field(default="日", description="时间（日/夜）")
    interior_exterior: str = Field(default="内", description="内景/外景")
    characters: List[str] = Field(default_factory=list, description="出场人物")
    atmosphere: Optional[str] = Field(None, description="氛围")
    shots: List[ShotInfo] = Field(default_factory=list, description="镜头列表")


class EpisodeOutline(BaseModel):
    """剧集大纲"""
    episode_num: int = Field(..., description="集数")
    title: str = Field(..., description="标题")
    total_duration: float = Field(default=90.0, description="总时长（秒）")
    
    # 结构
    hook: Dict[str, Any] = Field(..., description="开局钩子（前3秒）")
    story_beats: List[Dict[str, Any]] = Field(default_factory=list, description="故事节拍")
    cliffhanger: Dict[str, Any] = Field(..., description="结尾悬念（后5秒）")
    
    # 统计
    reversal_count: int = Field(default=0, description="反转次数")
    cool_points: List[str] = Field(default_factory=list, description="爽点标签")
    total_shots: int = Field(default=0, description="总镜头数")
    
    # 来源
    source_chapters: str = Field(..., description="来源章节（如 '1-3'）")


class DramaScript(BaseModel):
    """剧本脚本"""
    script_id: str = Field(..., description="脚本ID")
    episode_num: int = Field(..., description="集数")
    title: str = Field(..., description="标题")
    status: DramaStatus = Field(default=DramaStatus.PENDING)
    
    # 大纲
    outline: Optional[EpisodeOutline] = None
    
    # 场景
    scenes: List[SceneInfo] = Field(default_factory=list, description="场景列表")
    total_shots: int = Field(default=0)
    total_duration: float = Field(default=0.0)
    
    # 元数据
    source_novel_id: Optional[str] = Field(None, description="来源小说ID")
    source_chapters: Optional[str] = Field(None, description="来源章节")
    created_at: datetime = Field(default_factory=datetime.now)


class DramaProject(BaseModel):
    """剧本项目"""
    project_id: str = Field(..., description="项目ID")
    title: str = Field(..., description="项目标题")
    source_novel_id: Optional[str] = Field(None, description="来源小说ID")
    source_file: Optional[str] = Field(None, description="来源文件路径")
    
    # 配置
    episode_duration: float = Field(default=90.0, description="每集时长")
    total_episodes: int = Field(default=0, description="总集数")
    chapters_per_episode: int = Field(default=3, description="每集章节数")
    
    # 剧本
    episodes: List[DramaScript] = Field(default_factory=list, description="剧集列表")
    
    # 角色映射
    character_mapping: Dict[str, str] = Field(default_factory=dict, description="小说角色→剧本角色映射")
    
    # 元数据
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


# ==================== API 请求/响应模型 ====================

class CreateNovelRequest(BaseModel):
    """创建小说请求"""
    title: str
    genre: NovelGenre
    topic: str
    theme: Optional[str] = None
    total_chapters: int = Field(default=10, ge=1, le=1000)
    target_word_count: int = Field(default=3000, ge=500, le=10000)
    style_guide: Optional[str] = None
    initial_characters: Optional[List[CharacterProfile]] = None


class GenerateChapterRequest(BaseModel):
    """生成章节请求"""
    novel_id: str
    chapter_num: int
    additional_guidance: Optional[str] = None
    use_memory: bool = Field(default=True)


class CreateDramaRequest(BaseModel):
    """创建剧本请求"""
    title: str
    source_novel_id: Optional[str] = None
    source_file: Optional[str] = None
    episode_duration: float = Field(default=90.0)
    chapters_per_episode: int = Field(default=3)
    output_formats: List[DramaFormat] = Field(default=[DramaFormat.JSON, DramaFormat.MARKDOWN])


class ConvertToDramaRequest(BaseModel):
    """小说转剧本请求"""
    novel_id: str
    chapter_range: Optional[str] = None  # 如 "1-3" 或 "all"
    episode_num: Optional[int] = None
    output_formats: List[DramaFormat] = Field(default=[DramaFormat.JSON])


class APIResponse(BaseModel):
    """通用API响应"""
    success: bool
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None


class NovelListResponse(BaseModel):
    """小说列表响应"""
    novels: List[NovelProject]
    total: int
    page: int
    page_size: int


class DramaListResponse(BaseModel):
    """剧本列表响应"""
    projects: List[DramaProject]
    total: int
    page: int
    page_size: int
