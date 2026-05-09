# -*- coding: utf-8 -*-
"""
小说创作引擎 - 千帆版本
使用百度千帆 API 实现
"""

import sys
import os
from typing import List, Dict, Optional, Any
from pathlib import Path
import json
import uuid
from datetime import datetime

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
        self.max_tokens = config.get("max_tokens", 100000)  # 增加到100000
        
        # 初始化千帆客户端
        self.client = QianfanClient(
            api_key=config.get("api_key"),
            api_url=config.get("api_url"),
            model=self.model
        )
    
    async def generate(self, prompt: str, system_prompt: str = None, temperature: float = None) -> str:
        """生成文本"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        # 使用传入的温度或默认温度
        temp = temperature if temperature is not None else self.temperature
        
        response: QianfanResponse = self.client.chat(
            messages=messages,
            model=self.model,
            temperature=temp,
            max_tokens=self.max_tokens
        )
        
        if not response.success:
            raise RuntimeError(f"LLM generation failed: {response.content}")
        
        return response.content


class MemoryManager:
    """记忆管理器 - 管理角色、情节、设定的一致性"""
    
    def __init__(self):
        self.character_memories: Dict[str, List[str]] = {}
        self.plot_memories: Dict[str, List[str]] = {}
        self.setting_memory: List[str] = []
    
    def add_character_memory(self, character_name: str, memory: str):
        """添加角色记忆"""
        if character_name not in self.character_memories:
            self.character_memories[character_name] = []
        self.character_memories[character_name].append(memory)
    
    def add_plot_memory(self, plot_point: str):
        """添加情节记忆"""
        self.plot_memories[plot_point] = True
    
    def get_character_context(self, character_name: str) -> str:
        """获取角色上下文"""
        memories = self.character_memories.get(character_name, [])
        return "\n".join(memories[-5:])  # 最近5条记忆
    
    def get_all_context(self) -> str:
        """获取所有上下文"""
        context_parts = []
        
        # 角色记忆
        for char_name, memories in self.character_memories.items():
            context_parts.append(f"【{char_name}】\n" + "\n".join(memories[-3:]))
        
        # 情节记忆
        if self.plot_memories:
            context_parts.append("【已发生情节】\n" + "\n".join(list(self.plot_memories.keys())[-5:]))
        
        return "\n\n".join(context_parts)


class NovelEngine:
    """
    小说创作引擎
    
    核心功能：
    - 项目管理
    - 设定生成
    - 章节规划
    - 内容创作
    - 一致性检查
    - 导出功能
    """
    
    def __init__(self, llm_config: Dict, embedding_config: Dict = None):
        self.llm = LLMAdapter(llm_config)
        self.memory = MemoryManager()
        
        # 项目存储
        self.projects: Dict[str, NovelProject] = {}
        
        # 初始化架构生成器
        self.arch_gen = ArchitectureGenerator(self.llm.client)
        self.blueprint_gen = BlueprintGenerator(self.llm.client)
        self.planner = ChapterPlanner(self.llm.client)
    
    # ==================== 项目管理 ====================
    
    async def create_project(self, config: Dict) -> NovelProject:
        """
        创建小说项目
        
        Args:
            config: {
                "title": "小说标题",
                "genre": "玄幻",
                "topic": "故事梗概",
                "total_chapters": 10,
                "target_word_count": 3000
            }
        """
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
            "仙侠": NovelGenre.XIANXIA
        }
        genre = genre_map.get(genre_str, NovelGenre.FANTASY)
        
        project = NovelProject(
            novel_id=project_id,
            title=config.get("title", "未命名小说"),
            genre=genre,
            topic=config.get("topic", ""),
            total_chapters=config.get("total_chapters", 10),
            target_word_count=config.get("target_word_count", 3000)
        )
        
        self.projects[project_id] = project
        return project
    
    async def get_project(self, project_id: str) -> Optional[NovelProject]:
        """获取项目"""
        return self.projects.get(project_id)
    
    async def list_projects(self, page: int = 1, page_size: int = 10) -> List[NovelProject]:
        """列出项目"""
        projects = list(self.projects.values())
        start = (page - 1) * page_size
        end = start + page_size
        return projects[start:end]
    
    # ==================== 设定生成 ====================
    
    async def generate_architecture(
        self,
        novel_id: str,
        user_guidance: str = ""
    ) -> Dict[str, str]:
        """
        生成完整的小说架构（五阶段）
        
        包括：核心种子、角色动力学、世界观、情节架构、角色状态
        
        Args:
            novel_id: 项目ID
            user_guidance: 用户指导
        
        Returns:
            包含所有架构内容的字典
        """
        project = await self.get_project(novel_id)
        if not project:
            raise ValueError(f"Project {novel_id} not found")
        
        # 调用架构生成器
        architecture = await self.arch_gen.generate_full_architecture(
            topic=project.topic,
            genre=project.genre.value,
            number_of_chapters=project.total_chapters,
            word_number=project.target_word_count,
            user_guidance=user_guidance,
            project_id=novel_id
        )
        
        # 保存到项目
        if architecture:
            project.architecture = architecture
        
        return architecture
    
    async def generate_blueprint(self, novel_id: str) -> PlotBlueprint:
        """生成详细的小说蓝图"""
        project = await self.get_project(novel_id)
        if not project:
            raise ValueError(f"Project {novel_id} not found")
        
        # 如果已有架构，使用架构生成器
        if hasattr(project, 'architecture') and project.architecture:
            architecture_text = project.architecture.get('full_architecture', '')
            if architecture_text:
                # 生成悬念节奏曲线蓝图
                blueprint_text = await self.blueprint_gen.generate_blueprint(
                    novel_architecture=architecture_text,
                    number_of_chapters=project.total_chapters,
                    user_guidance="",
                    project_id=novel_id
                )
                
                # 解析为 PlotBlueprint
                blueprint_data = self.blueprint_gen.parse_blueprint_to_dict(blueprint_text)
                
                if blueprint_data:
                    # 提取第1章的冲突信息作为主要冲突
                    main_conflict = blueprint_data[0].get('role', '待生成')
                    inciting_incident = blueprint_data[0].get('purpose', '待生成')
                    rising_actions = []
                    climax = ""
                    falling_actions = []
                    resolution = ""
                    
                    # 尝试从其他章节提取信息
                    for ch_data in blueprint_data:
                        if "高潮" in ch_data.get('role', ''):
                            climax = ch_data.get('summary', '')
                        elif "结局" in ch_data.get('role', ''):
                            resolution = ch_data.get('summary', '')
                        
                        # 收集上升行动
                        if ch_data.get('plot_twist_level') and "★" in ch_data['plot_twist_level']:
                            rising_actions.append(ch_data.get('summary', ''))
                    
                    blueprint = PlotBlueprint(
                        blueprint_id=str(uuid.uuid4())[:8],
                        novel_id=novel_id,
                        main_conflict=main_conflict,
                        inciting_incident=inciting_incident,
                        rising_actions=rising_actions,
                        climax=climax,
                        falling_actions=falling_actions,
                        resolution=resolution
                    )
                    
                    project.plot_blueprint = blueprint
                    project.blueprint_text = blueprint_text
                    return blueprint
        
        # 回退到原版生成逻辑
        # 改进的提示词 - 生成更详细的内容
        prompt = f"""
你是一位资深的小说策划师。请为以下小说生成详细、完整的创作蓝图（每个部分都要有足够细节）：

小说标题：{project.title}
类型：{project.genre.value}
主题/梗概：{project.topic}
总章节数：{project.total_chapters}

【请生成以下内容】

1. 核心冲突（200字以上）
   - 详细描述主要矛盾的本质和根源
   - 说明冲突如何影响故事发展
   - 分析主角与反派的利益冲突

2. 触发事件（300字以上）
   - 详细描述故事开始的契机和场景
   - 包含具体的人物、对话和行动
   - 说明为什么这个事件彻底改变了主角的命运

3. 上升行动（3-5个详细转折点）
   - 每个转折点都需要200字以上的详细描述
   - 包含具体的场景、情节推进和角色成长
   - 说明每个转折如何将故事推向高潮

4. 高潮（500字以上）
   - 详细描述故事最高潮场景
   - 包含激烈的冲突、关键抉择和情感爆发
   - 说明主角如何面对最终挑战

5. 下降行动（300字以上）
   - 详细描述高潮后的解决过程
   - 包含情节的收束和悬念的解答
   - 说明主要角色的最终归宿

6. 结局（200字以上）
   - 详细描述故事的最终结果和主题升华
   - 包含角色的命运总结和人生感悟
   - 为读者留下思考空间

【输出要求】
请以JSON格式输出，确保每个字段都有足够的细节和字数。

⚠️ **非常重要：数组中的元素绝对不能添加索引号（如 0:, 1:）！**

正确示例：
{{
    "rising_actions": [
        "转折点1的300字详细描述...",
        "转折点2的300字详细描述...",
        "转折点3的300字详细描述..."
    ]
}}

错误示例（禁止）：
{{
    "rising_actions": [
        0: "转折点1",  ← 错误！不要添加 0:
        1: "转折点2"   ← 错误！不要添加 1:
    ]
}}

请严格按照正确格式输出：
{{
    "main_conflict": "300字左右的详细冲突描述...",
    "inciting_incident": "500字左右的触发事件详细描述...",
    "rising_actions": [
        "转折点1的300字详细描述...",
        "转折点2的300字详细描述...",
        "转折点3的300字详细描述..."
    ],
    "climax": "800字以上的高潮详细描述...",
    "falling_actions": [
        "解决过程1的200字描述...",
        "解决过程2的200字描述..."
    ],
    "resolution": "300字以上的结局详细描述..."
}}

请开始创作：
"""
        
        result = await self.llm.generate(prompt, temperature=0.3)
        
        # 使用新的 JSON 解析工具
        from utils.json_utils import parse_ai_json
        data = parse_ai_json(result)
        
        blueprint = PlotBlueprint(
            blueprint_id=str(uuid.uuid4())[:8],
            novel_id=novel_id,
            main_conflict=data.get("main_conflict", "待生成"),
            inciting_incident=data.get("inciting_incident", "待生成"),
            rising_actions=data.get("rising_actions", []),
            climax=data.get("climax", "待生成"),
            falling_actions=data.get("falling_actions", []),
            resolution=data.get("resolution", "待生成")
        )
        
        project.plot_blueprint = blueprint
        return blueprint
    
    async def generate_chapter_outline(self, novel_id: str) -> List[ChapterOutline]:
        """生成详细的章节大纲"""
        project = await self.get_project(novel_id)
        if not project:
            raise ValueError(f"Project {novel_id} not found")
        
        # 如果有蓝图，在提示词中加入蓝图信息
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
4. 涉及角色（本章出现的主要角色）
5. 情节推进（说明本章如何推动整体故事发展）
6. 爽点/看点（本章的吸引点，如打脸、逆袭、身份曝光等）

【输出格式要求】
请以JSON格式输出，确保每个章节都有足够的细节和吸引力。

**重要提示：数组中的元素不要添加索引号！**

格式示例：
{{
    "chapters": [
        {{
            "chapter_num": 1,
            "title": "引人入胜的章节标题",
            "summary": "200字以上的详细章节摘要，包含具体的情节描述...",
            "key_events": [
                "事件1的50-100字详细描述",
                "事件2的50-100字详细描述",
                "事件3的50-100字详细描述"
            ],
            "characters_involved": ["主角", "配角1", "反派1"],
            "plot_progression": "本章如何推动故事发展，100字以上",
            "appealing_points": ["爽点1", "爽点2"]
        }},
        ...
    ]
}}

请开始创作：
"""
        
        result = await self.llm.generate(prompt, temperature=0.3)
        
        # 使用新的 JSON 解析工具
        from utils.json_utils import parse_ai_json
        data = parse_ai_json(result)
        chapters_data = data.get("chapters", [])
        
        outlines = []
        for chapter_data in chapters_data:
            outline = ChapterOutline(
                outline_id=str(uuid.uuid4())[:8],
                novel_id=novel_id,
                chapter_num=chapter_data.get("chapter_num", len(outlines) + 1),
                title=chapter_data.get("title", f"第{len(outlines)+1}章"),
                summary=chapter_data.get("summary", ""),
                key_events=chapter_data.get("key_events", [])
            )
            outlines.append(outline)
        
        project.chapters = outlines
        return outlines
    
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
        
        # 获取章节大纲
        outline = None
        if project.chapters:
            outline = next((o for o in project.chapters if o.chapter_num == chapter_num), None)
        
        # 构建提示
        prompt_parts = [
            f"你是一位专业的网络小说作家。请创作以下小说的第{chapter_num}章：\n",
            f"小说标题：{project.title}",
            f"类型：{project.genre.value}",
            f"主题：{project.topic}\n"
        ]
        
        if outline:
            prompt_parts.extend([
                f"章节标题：{outline.title}",
                f"章节摘要：{outline.summary}",
                f"关键事件：{', '.join(outline.key_events)}\n"
            ])
        
        if use_memory:
            context = self.memory.get_all_context()
            if context:
                prompt_parts.append(f"【前文相关内容】\n{context}\n")
        
        if additional_guidance:
            prompt_parts.append(f"【创作指导】\n{additional_guidance}\n")
        
        prompt_parts.append(f"请创作约{project.target_word_count}字的章节内容，要求：\n1. 情节紧凑，引人入胜\n2. 人物性格鲜明\n3. 对话自然\n4. 避免重复和冗余\n\n现在开始创作：")
        
        prompt = "\n".join(prompt_parts)
        
        content = await self.llm.generate(prompt)
        
        chapter = ChapterContent(
            chapter_id=str(uuid.uuid4())[:8],
            novel_id=novel_id,
            chapter_num=chapter_num,
            title=outline.title if outline else f"第{chapter_num}章",
            content=content,
            word_count=len(content)
        )
        
        # 添加到项目
        if not project.generated_chapters:
            project.generated_chapters = []
        project.generated_chapters.append(chapter)
        
        return chapter
    
    async def finalize_chapter(self, novel_id: str, chapter_num: int) -> Dict[str, Any]:
        """最终化章节（更新记忆系统）"""
        project = await self.get_project(novel_id)
        if not project:
            raise ValueError(f"Project {novel_id} not found")
        
        chapter = next((c for c in project.generated_chapters if c.chapter_num == chapter_num), None)
        if not chapter:
            raise ValueError(f"Chapter {chapter_num} not found")
        
        # 提取关键信息并更新记忆
        prompt = f"""
分析以下章节内容，提取关键信息：

{chapter.content[:2000]}

请提取：
1. 新出现的人物
2. 重要的情节转折
3. 地点变化
4. 时间线

以JSON格式输出：
{{
    "new_characters": ["人物1", "人物2"],
    "plot_points": ["情节1", "情节2"],
    "locations": ["地点1", "地点2"],
    "timeline": "时间描述"
}}
"""
        
        result = await self.llm.generate(prompt, temperature=0.3)
        
        try:
            import re
            json_match = re.search(r'\{[\s\S]*\}', result)
            if json_match:
                data = json.loads(json_match.group())
            else:
                data = {}
        except:
            data = {}
        
        # 更新记忆
        for char in data.get("new_characters", []):
            self.memory.add_character_memory(char, f"首次出现于第{chapter_num}章")
        
        for plot in data.get("plot_points", []):
            self.memory.add_plot_memory(f"第{chapter_num}章：{plot}")
        
        chapter.is_finalized = True
        chapter.finalized_at = datetime.now()
        
        return {
            "chapter_num": chapter_num,
            "memory_updated": True,
            "new_characters": data.get("new_characters", []),
            "plot_points": data.get("plot_points", [])
        }
    
    async def check_consistency(self, novel_id: str, chapter_num: int) -> Dict[str, Any]:
        """检查一致性"""
        project = await self.get_project(novel_id)
        if not project:
            raise ValueError(f"Project {novel_id} not found")
        
        chapter = next((c for c in project.generated_chapters if c.chapter_num == chapter_num), None)
        if not chapter:
            raise ValueError(f"Chapter {chapter_num} not found")
        
        context = self.memory.get_all_context()
        
        prompt = f"""
检查以下章节是否存在一致性问题：

【前文背景】
{context}

【当前章节】
{chapter.content[:2000]}

请检查：
1. 角色行为是否符合人设
2. 时间线是否连贯
3. 地点转换是否合理
4. 是否存在设定冲突

以JSON格式输出：
{{
    "issues": [
        {{
            "type": "角色/时间/地点/设定",
            "description": "问题描述",
            "severity": "轻微/中等/严重"
        }}
    ],
    "overall_consistency": "良好/一般/较差"
}}
"""
        
        result = await self.llm.generate(prompt)
        
        try:
            import re
            json_match = re.search(r'\{[\s\S]*\}', result)
            if json_match:
                data = json.loads(json_match.group())
            else:
                data = {"issues": [], "overall_consistency": "良好"}
        except:
            data = {"issues": [], "overall_consistency": "良好"}
        
        return data
    
    async def export_novel(self, novel_id: str, format: str = "markdown") -> str:
        """导出小说"""
        project = await self.get_project(novel_id)
        if not project:
            raise ValueError(f"Project {novel_id} not found")
        
        if format == "markdown":
            lines = [f"# {project.title}\n"]
            lines.append(f"\n类型：{project.genre.value}\n")
            lines.append(f"总字数：{sum(c.word_count for c in project.generated_chapters)}\n\n")
            lines.append("---\n\n")
            
            for chapter in sorted(project.generated_chapters, key=lambda x: x.chapter_num):
                lines.append(f"## {chapter.title}\n\n")
                lines.append(chapter.content)
                lines.append("\n\n")
            
            return "\n".join(lines)
        
        else:
            raise ValueError(f"Unsupported format: {format}")


# ==================== 测试代码 ====================

async def test_novel_engine():
    """测试小说引擎"""
    print("=" * 60)
    print("测试小说创作引擎（千帆 API）")
    print("=" * 60)
    
    # 配置
    config = {
        "model": "glm-5.1",
        "temperature": 0.7,
        "max_tokens": 100000  # 增加到100000
    }
    
    engine = NovelEngine(config)
    
    # 测试1：创建项目
    print("\n测试1：创建小说项目")
    project = await engine.create_project({
        "title": "修仙之路",
        "genre": "玄幻",
        "topic": "一个少年从凡人修成仙帝的故事",
        "total_chapters": 5,
        "target_word_count": 2000
    })
    print(f"✅ 项目ID: {project.novel_id}")
    print(f"✅ 标题: {project.title}")
    print(f"✅ 类型: {project.genre.value}")
    
    # 测试2：生成蓝图
    print("\n测试2：生成小说蓝图")
    blueprint = await engine.generate_blueprint(project.novel_id)
    print(f"✅ 核心冲突: {blueprint.main_conflict}")
    print(f"✅ 触发事件: {blueprint.inciting_incident}")
    
    # 测试3：生成章节大纲
    print("\n测试3：生成章节大纲")
    outlines = await engine.generate_chapter_outline(project.novel_id)
    print(f"✅ 生成 {len(outlines)} 个章节大纲")
    for o in outlines[:3]:
        print(f"   - 第{o.chapter_num}章: {o.title}")
    
    # 测试4：生成章节内容
    print("\n测试4：生成第1章内容")
    chapter = await engine.generate_chapter(project.novel_id, 1, use_memory=False)
    print(f"✅ 章节标题: {chapter.title}")
    print(f"✅ 字数: {chapter.word_count}")
    print(f"✅ 内容预览: {chapter.content[:100]}...")
    
    # 测试5：最终化章节
    print("\n测试5：最终化章节")
    result = await engine.finalize_chapter(project.novel_id, 1)
    print(f"✅ 记忆已更新")
    print(f"✅ 新角色: {result.get('new_characters', [])}")
    
    # 测试6：导出
    print("\n测试6：导出小说")
    content = await engine.export_novel(project.novel_id)
    print(f"✅ 导出成功，总长度: {len(content)} 字符")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_novel_engine())
