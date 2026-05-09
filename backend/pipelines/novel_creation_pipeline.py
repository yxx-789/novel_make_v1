# -*- coding: utf-8 -*-
"""
Open WebUI Pipeline - 小说创作流水线
将小说创作引擎集成到 Open WebUI
"""

import sys
import os
from typing import List, Dict, Optional, Any, Callable, Awaitable
from pydantic import BaseModel
import json
import asyncio
import re

# Open WebUI Pipeline 基类
try:
    from openwebui.pipelines import Pipeline
    PIPELINE_AVAILABLE = True
except ImportError:
    # 如果没有安装 openwebui，创建一个基类用于测试
    PIPELINE_AVAILABLE = False
    class Pipeline:
        """Mock Pipeline class for testing"""
        def __init__(self):
            self.name = "Mock Pipeline"
            self.description = "For testing without Open WebUI"
        
        async def pipe(self, user_message: str, model_id: str, messages: List[dict], body: dict) -> str:
            raise NotImplementedError

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.novel_engine_db import NovelEngineDB  # 使用数据库版本
from core.drama_engine import DramaEngine
from models.schemas import NovelGenre, DramaFormat


class IntentType:
    """用户意图类型"""
    CREATE_NOVEL = "create_novel"
    GENERATE_CHAPTER = "generate_chapter"
    CONVERT_TO_DRAMA = "convert_to_drama"
    GENERAL_CHAT = "general_chat"
    UNKNOWN = "unknown"


class ParsedIntent(BaseModel):
    """解析后的用户意图"""
    intent_type: str
    params: Dict[str, Any] = {}
    confidence: float = 0.0


class NovelCreationPipeline(Pipeline):
    """
    小说创作流水线
    
    功能：
    - 检测用户意图（小说创作/章节生成/剧本转换/普通对话）
    - 路由到对应引擎
    - 返回格式化结果
    """
    
    def __init__(self):
        self.name = "小说创作流水线"
        self.description = "AI小说创作 + 短剧剧本转换"
        self.version = "1.0.0"
        
        # 初始化引擎
        self._init_engines()
        
        # 项目存储
        self.current_novel_id: Optional[str] = None
        self.current_drama_id: Optional[str] = None
    
    def _init_engines(self):
        """初始化引擎"""
        config = self._get_llm_config()
        
        self.novel_engine = NovelEngine(config)
        self.drama_engine = DramaEngine(config)
    
    def _get_llm_config(self) -> Dict:
        """获取 LLM 配置"""
        return {
            "api_key": os.getenv("OPENAI_API_KEY", "sk-xxx"),
            "base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            "model": os.getenv("LLM_MODEL", "gpt-4o-mini"),
            "temperature": 0.7,
            "max_tokens": 4096
        }
    
    # ==================== 核心管道方法 ====================
    
    async def pipe(
        self,
        user_message: str,
        model_id: str,
        messages: List[dict],
        body: dict
    ) -> str:
        """
        Open WebUI 主入口
        
        Args:
            user_message: 用户消息
            model_id: 模型ID
            messages: 对话历史
            body: 请求体
        
        Returns:
            str: 响应内容
        """
        try:
            # 1. 解析用户意图
            intent = await self.parse_intent(user_message, messages)
            
            # 2. 路由到对应处理器
            if intent.intent_type == IntentType.CREATE_NOVEL:
                return await self.handle_create_novel(intent.params, messages)
            
            elif intent.intent_type == IntentType.GENERATE_CHAPTER:
                return await self.handle_generate_chapter(intent.params, messages)
            
            elif intent.intent_type == IntentType.CONVERT_TO_DRAMA:
                return await self.handle_convert_to_drama(intent.params, messages)
            
            else:
                # 普通对话，返回提示
                return self._get_help_message()
        
        except Exception as e:
            return f"❌ 处理失败: {str(e)}"
    
    # ==================== 意图解析 ====================
    
    async def parse_intent(self, user_message: str, messages: List[dict]) -> ParsedIntent:
        """
        解析用户意图
        
        支持的意图：
        - /novel 创作一部玄幻小说，主题是...
        - /chapter 生成第3章
        - /drama 转换为短剧剧本
        - 普通对话
        """
        message_lower = user_message.lower().strip()
        
        # 命令格式检测
        if message_lower.startswith("/novel") or "创作小说" in user_message or "写一部小说" in user_message:
            params = self._parse_novel_params(user_message)
            return ParsedIntent(
                intent_type=IntentType.CREATE_NOVEL,
                params=params,
                confidence=0.9
            )
        
        elif message_lower.startswith("/chapter") or "生成第" in user_message and "章" in user_message:
            params = self._parse_chapter_params(user_message)
            return ParsedIntent(
                intent_type=IntentType.GENERATE_CHAPTER,
                params=params,
                confidence=0.9
            )
        
        elif message_lower.startswith("/drama") or "转换为剧本" in user_message or "生成短剧" in user_message:
            params = self._parse_drama_params(user_message)
            return ParsedIntent(
                intent_type=IntentType.CONVERT_TO_DRAMA,
                params=params,
                confidence=0.9
            )
        
        # 自然语言检测
        elif any(keyword in user_message for keyword in ["小说", "创作", "故事"]):
            return ParsedIntent(
                intent_type=IntentType.CREATE_NOVEL,
                params={"topic": user_message},
                confidence=0.6
            )
        
        return ParsedIntent(
            intent_type=IntentType.GENERAL_CHAT,
            confidence=0.5
        )
    
    def _parse_novel_params(self, message: str) -> Dict[str, Any]:
        """解析小说创作参数"""
        params = {
            "title": "未命名小说",
            "genre": "玄幻",
            "topic": "",
            "total_chapters": 10
        }
        
        # 提取类型
        genre_keywords = {
            "玄幻": ["玄幻", "修仙", "仙侠"],
            "都市": ["都市", "现代", "职场"],
            "言情": ["言情", "爱情", "恋爱"],
            "科幻": ["科幻", "未来", "星际"],
            "历史": ["历史", "穿越", "古代"]
        }
        
        for genre, keywords in genre_keywords.items():
            if any(kw in message for kw in keywords):
                params["genre"] = genre
                break
        
        # 提取主题
        patterns = [
            r"主题[是为：:\s]+(.+?)(?:\n|$|，)",
            r"故事[是为：:\s]+(.+?)(?:\n|$|，)",
            r"关于(.+?)的小说",
            r"写一部(.+?)小说"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message)
            if match:
                params["topic"] = match.group(1).strip()
                break
        
        # 提取章节数
        chapter_match = re.search(r"(\d+)\s*章", message)
        if chapter_match:
            params["total_chapters"] = int(chapter_match.group(1))
        
        return params
    
    def _parse_chapter_params(self, message: str) -> Dict[str, Any]:
        """解析章节生成参数"""
        params = {
            "chapter_num": 1,
            "guidance": None
        }
        
        # 提取章节号
        chapter_match = re.search(r"第\s*(\d+)\s*章", message)
        if chapter_match:
            params["chapter_num"] = int(chapter_match.group(1))
        
        # 提取额外指导
        if "要求" in message or "注意" in message:
            guidance_match = re.search(r"[要求注意：:\s]+(.+?)(?:\n|$)", message)
            if guidance_match:
                params["guidance"] = guidance_match.group(1).strip()
        
        return params
    
    def _parse_drama_params(self, message: str) -> Dict[str, Any]:
        """解析剧本转换参数"""
        params = {
            "chapter_range": "all",
            "episode_duration": 90,
            "output_format": "markdown"
        }
        
        # 提取章节范围
        range_match = re.search(r"第\s*(\d+)-(\d+)\s*章", message)
        if range_match:
            params["chapter_range"] = f"{range_match.group(1)}-{range_match.group(2)}"
        
        # 提取时长
        duration_match = re.search(r"(\d+)\s*秒", message)
        if duration_match:
            params["episode_duration"] = int(duration_match.group(1))
        
        return params
    
    # ==================== 意图处理器 ====================
    
    async def handle_create_novel(self, params: Dict, messages: List[dict]) -> str:
        """处理小说创作"""
        try:
            # 创建项目
            project = await self.novel_engine.create_project(params)
            self.current_novel_id = project.novel_id
            
            # 生成蓝图
            blueprint = await self.novel_engine.generate_blueprint(project.novel_id)
            
            # 生成章节大纲
            outlines = await self.novel_engine.generate_chapter_outline(project.novel_id)
            
            # 格式化输出
            output = f"""
✅ **小说项目创建成功！**

📖 **项目信息**
- 标题：{project.title}
- 类型：{project.genre.value}
- 总章节：{project.total_chapters}
- 项目ID：{project.novel_id}

🌐 **世界观设定**
- 时代背景：{project.world_setting.era if project.world_setting else '待生成'}
- 主要地点：{project.world_setting.location if project.world_setting else '待生成'}

👥 **主要角色**
{self._format_characters(project.characters)}

📋 **情节蓝图**
- 核心冲突：{blueprint.main_conflict}
- 触发事件：{blueprint.inciting_incident}

📝 **章节大纲**（前5章预览）
{self._format_outlines(outlines[:5])}

---
💡 **下一步操作**
- 输入 `/chapter 第1章` 开始生成章节
- 输入 `/drama` 转换为短剧剧本
"""
            return output
        
        except Exception as e:
            return f"❌ 小说创作失败: {str(e)}"
    
    async def handle_generate_chapter(self, params: Dict, messages: List[dict]) -> str:
        """处理章节生成"""
        if not self.current_novel_id:
            return "❌ 请先创建小说项目！输入 `/novel` 开始创作。"
        
        try:
            chapter_num = params.get("chapter_num", 1)
            guidance = params.get("guidance")
            
            # 生成章节
            chapter = await self.novel_engine.generate_chapter(
                self.current_novel_id,
                chapter_num,
                guidance,
                use_memory=True
            )
            
            # 最终化章节
            await self.novel_engine.finalize_chapter(self.current_novel_id, chapter_num)
            
            # 格式化输出
            output = f"""
## {chapter.title}

{chapter.content[:500]}...

---
📊 **章节信息**
- 字数：{chapter.word_count}
- 状态：已最终化

💡 **下一步**
- 输入 `/chapter 第{chapter_num + 1}章` 继续创作
- 输入 `/drama 第{chapter_num}章` 转换为剧本
"""
            return output
        
        except Exception as e:
            return f"❌ 章节生成失败: {str(e)}"
    
    async def handle_convert_to_drama(self, params: Dict, messages: List[dict]) -> str:
        """处理剧本转换"""
        if not self.current_novel_id:
            return "❌ 请先创建小说项目！"
        
        try:
            # 获取小说项目
            novel = await self.novel_engine.get_project(self.current_novel_id)
            if not novel or not novel.generated_chapters:
                return "❌ 小说项目中没有已生成的章节！"
            
            # 转换为剧本
            chapter_range = params.get("chapter_range", "1-3")
            start, end = map(int, chapter_range.split("-"))
            
            chapters = [c for c in novel.generated_chapters if start <= c.chapter_num <= end]
            if not chapters:
                return f"❌ 没有找到第 {start}-{end} 章的内容！"
            
            combined_text = "\n\n".join([c.content for c in chapters])
            characters = [c.dict() for c in novel.characters]
            
            # 生成大纲
            outline = await self.drama_engine.map_to_episode_outline(
                combined_text,
                characters,
                1,
                chapter_range
            )
            
            # 生成剧本
            script = await self.drama_engine.generate_script(outline, combined_text, characters)
            
            # 导出
            output_files = await self.drama_engine.export_script(
                script,
                [DramaFormat.MARKDOWN],
                "./output"
            )
            
            # 格式化输出
            output = f"""
🎬 **短剧剧本生成成功！**

📺 **剧集信息**
- 集数：第 {script.episode_num} 集
- 标题：{script.title}
- 时长：{script.total_duration} 秒
- 场景数：{len(script.scenes)}
- 总镜头：{script.total_shots}

🎯 **节奏分析**
- 反转次数：{outline.reversal_count}
- 爽点标签：{', '.join(outline.cool_points)}
- 来源章节：第 {chapter_range} 章

🎬 **场景预览**
{self._format_scenes(script.scenes[:3])}

---
📁 **导出文件**
- Markdown：{output_files[0] if output_files else '未导出'}

💡 **下一步**
- 输入 `/drama 第{end + 1}-{end + 3}章` 继续转换
"""
            return output
        
        except Exception as e:
            return f"❌ 剧本转换失败: {str(e)}"
    
    # ==================== 辅助方法 ====================
    
    def _format_characters(self, characters: List) -> str:
        """格式化角色列表"""
        if not characters:
            return "待生成"
        
        lines = []
        for char in characters[:5]:  # 最多显示5个
            lines.append(f"- **{char.name}** ({char.role})")
        
        return "\n".join(lines)
    
    def _format_outlines(self, outlines: List) -> str:
        """格式化章节大纲"""
        if not outlines:
            return "待生成"
        
        lines = []
        for outline in outlines:
            lines.append(f"- 第{outline.chapter_num}章：{outline.title}")
        
        return "\n".join(lines)
    
    def _format_scenes(self, scenes: List) -> str:
        """格式化场景列表"""
        if not scenes:
            return "无"
        
        lines = []
        for scene in scenes:
            lines.append(f"- 场景{scene.scene_num}：{scene.location}（{len(scene.shots)}个镜头）")
        
        return "\n".join(lines)
    
    def _get_help_message(self) -> str:
        """获取帮助信息"""
        return """
📚 **小说创作流水线**

我可以帮你：
1. 🎨 创作小说（玄幻/都市/言情/科幻等）
2. 📖 生成章节内容
3. 🎬 转换为短剧剧本

**使用方式**：
- `/novel 创作一部玄幻小说，主题是修仙者重生回到少年时代`
- `/chapter 第1章`
- `/drama 第1-3章`

试试对我说："创作一部都市重生小说" ✨
"""


# ==================== 独立测试入口 ====================

async def test_pipeline():
    """测试 Pipeline"""
    pipeline = NovelCreationPipeline()
    
    # 测试1：创作小说
    print("=" * 50)
    print("测试1：创作小说")
    result = await pipeline.pipe(
        user_message="/novel 创作一部玄幻小说，主题是少年修仙，共10章",
        model_id="gpt-4o-mini",
        messages=[],
        body={}
    )
    print(result[:500])
    
    # 测试2：生成章节
    print("\n" + "=" * 50)
    print("测试2：生成章节")
    result = await pipeline.pipe(
        user_message="/chapter 第1章",
        model_id="gpt-4o-mini",
        messages=[],
        body={}
    )
    print(result[:500])
    
    # 测试3：转换剧本
    print("\n" + "=" * 50)
    print("测试3：转换剧本")
    result = await pipeline.pipe(
        user_message="/drama 第1-3章",
        model_id="gpt-4o-mini",
        messages=[],
        body={}
    )
    print(result[:500])


if __name__ == "__main__":
    asyncio.run(test_pipeline())
