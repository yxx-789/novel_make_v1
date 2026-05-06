# -*- coding: utf-8 -*-
"""
剧本转换引擎
封装 Novel to Drama 的核心功能
"""

import sys
from typing import List, Dict, Optional, Any
from pathlib import Path
import json
import re
from datetime import datetime

# 添加 novel_to_drama 到路径
DRAMA_CONVERTER_PATH = Path(__file__).parent.parent.parent / "novel_to_drama" / "novel_to_drama"
if DRAMA_CONVERTER_PATH.exists():
    sys.path.insert(0, str(DRAMA_CONVERTER_PATH / "scripts"))

# 导入模型
sys.path.insert(0, str(Path(__file__).parent.parent))
from models.schemas import (
    DramaProject, DramaScript, EpisodeOutline, SceneInfo, ShotInfo,
    DramaFormat, DramaStatus
)


class DramaEngine:
    """
    剧本转换引擎
    
    整合 Novel to Drama 的核心功能：
    - 小说解析
    - 短剧大纲映射
    - 分镜头脚本生成
    - 多格式导出
    """
    
    # 短剧节奏配置
    DRAMA_CONFIG = {
        "episode_duration": 90,  # 每集90秒
        "hook_duration": 3,      # 开局钩子3秒
        "cliffhanger_duration": 5,  # 结尾悬念5秒
        "max_scenes_per_episode": 8,
        "max_shots_per_scene": 5,
        
        # 压缩比例
        "compression_ratio": {
            "action": 0.3,      # 打斗压缩到30%
            "dialogue": 0.8,    # 对话保留80%
            "emotion": 1.5,     # 情绪扩展到150%
            "flashback": 2.0    # 回忆闪回扩展200%
        },
        
        # 爽点标签
        "cool_point_tags": [
            "打脸", "逆袭", "身份曝光", "实力碾压",
            "误会解除", "感情升温", "复仇成功", "真相大白"
        ]
    }
    
    def __init__(self, llm_config: Dict):
        self.llm_config = llm_config
        self._init_llm_client()
        
        # 项目存储
        self.projects: Dict[str, DramaProject] = {}
    
    def _init_llm_client(self):
        """初始化 LLM 客户端 - 使用千帆 API"""
        try:
            # 使用千帆客户端
            import sys
            sys.path.insert(0, str(Path(__file__).parent.parent))
            from utils.qianfan_client import QianfanClient
            
            self.client = QianfanClient(
                api_key=self.llm_config.get("api_key"),
                model=self.llm_config.get("model", "glm-5.1")
            )
            self.model = self.llm_config.get("model", "glm-5.1")
        except Exception as e:
            print(f"Warning: Could not initialize Qianfan client: {e}")
            self.client = None
    
    async def _call_llm(self, prompt: str, system_prompt: str = None) -> str:
        """调用 LLM - 使用千帆 API"""
        if not self.client:
            raise RuntimeError("LLM client not initialized")
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        # 调用千帆 API
        response = self.client.chat(
            messages=messages,
            model=self.model,
            temperature=0.7,
            max_tokens=4096
        )
        
        if not response.success:
            raise RuntimeError(f"LLM call failed: {response.content}")
        
        return response.content
    
    # ==================== 项目管理 ====================
    
    async def create_project(self, config: Dict) -> DramaProject:
        """
        创建剧本项目
        
        Args:
            config: 项目配置
                - title: 项目标题
                - source_novel_id: 来源小说ID（可选）
                - source_file: 来源文件路径（可选）
                - episode_duration: 每集时长
                - chapters_per_episode: 每集章节数
        """
        import uuid
        
        project_id = str(uuid.uuid4())[:8]
        
        project = DramaProject(
            project_id=project_id,
            title=config.get("title", "未命名剧本"),
            source_novel_id=config.get("source_novel_id"),
            source_file=config.get("source_file"),
            episode_duration=config.get("episode_duration", 90.0),
            chapters_per_episode=config.get("chapters_per_episode", 3)
        )
        
        self.projects[project_id] = project
        return project
    
    async def get_project(self, project_id: str) -> Optional[DramaProject]:
        """获取项目"""
        return self.projects.get(project_id)
    
    # ==================== 小说解析 ====================
    
    async def parse_novel(
        self,
        novel_text: str,
        characters: List[Dict] = None
    ) -> Dict[str, Any]:
        """
        解析小说内容
        
        提取：
        - 章节结构
        - 角色信息
        - 情节节拍
        - 爽点识别
        """
        prompt = f"""
请分析以下小说内容，提取关键信息：

{novel_text[:5000]}  # 限制长度

请输出JSON格式：
{{
  "total_chapters": 章节数,
  "total_words": 字数,
  "main_characters": ["主角", "配角1", ...],
  "genre": "类型",
  "core_conflict": "核心冲突",
  "cool_points": ["爽点1", "爽点2", ...],
  "pacing_analysis": {{
    "action_scenes": 动作场景数,
    "dialogue_scenes": 对话场景数,
    "emotion_scenes": 情感场景数
  }}
}}
"""
        
        result = await self._call_llm(prompt)
        
        try:
            # 尝试解析JSON
            json_match = re.search(r'\{[\s\S]*\}', result)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        # 返回基础结构
        return {
            "total_chapters": 1,
            "total_words": len(novel_text),
            "main_characters": characters or [],
            "genre": "未知",
            "core_conflict": "待分析",
            "cool_points": []
        }
    
    # ==================== 大纲映射 ====================
    
    async def map_to_episode_outline(
        self,
        novel_text: str,
        characters: List[Dict],
        episode_num: int,
        chapter_range: str
    ) -> EpisodeOutline:
        """
        将小说章节映射为短剧大纲
        
        核心任务：
        - 压缩比控制
        - 爽点提取
        - 钩子设计
        - 悬念设置
        """
        prompt = f"""
你是一位专业的短剧编剧。请将以下小说内容转换为竖屏微短剧大纲。

【小说内容】
{novel_text[:3000]}

【角色设定】
{json.dumps(characters, ensure_ascii=False, indent=2)}

【短剧要求】
1. 总时长：90秒
2. 开局3秒必须有钩子（立即抓住观众）
3. 结尾5秒必须有悬念（让观众想看下一集）
4. 至少2次反转
5. 爽点密集（打脸、逆袭、身份曝光等）
6. 避免心理描写，全部转为视觉动作或台词

【输出格式】
请严格按以下JSON格式输出：
{{
  "episode_num": {episode_num},
  "title": "本集标题（有冲击力）",
  "duration_estimate": 90,
  "hook": {{
    "first_3s": {{
      "visual": "画面描述",
      "action": "人物动作",
      "dialogue": "开场台词"
    }}
  }},
  "story_beats": [
    {{
      "beat_num": 1,
      "duration": 15,
      "description": "节拍描述",
      "key_action": "关键动作",
      "emotional_tone": "情绪基调"
    }}
  ],
  "cliffhanger": {{
    "last_5s": {{
      "visual": "画面描述",
      "action": "人物动作",
      "dialogue": "结尾台词或旁白",
      "suspense_element": "悬念元素"
    }}
  }},
  "reversal_count": 2,
  "cool_points": ["打脸", "逆袭"],
  "compression_notes": "压缩说明（哪些内容被压缩/扩展）"
}}

请开始生成：
"""
        
        result = await self._call_llm(
            prompt,
            system_prompt="你是一位精通短剧节奏的专业编剧，擅长将小说改编为高爽点的竖屏短剧。"
        )
        
        # 解析结果
        try:
            json_match = re.search(r'\{[\s\S]*\}', result)
            if json_match:
                data = json.loads(json_match.group())
                return EpisodeOutline(
                    episode_num=data.get("episode_num", episode_num),
                    title=data.get("title", f"第{episode_num}集"),
                    total_duration=data.get("duration_estimate", 90.0),
                    hook=data.get("hook", {}),
                    story_beats=data.get("story_beats", []),
                    cliffhanger=data.get("cliffhanger", {}),
                    reversal_count=data.get("reversal_count", 0),
                    cool_points=data.get("cool_points", []),
                    total_shots=0,
                    source_chapters=chapter_range
                )
        except Exception as e:
            print(f"Warning: Could not parse episode outline: {e}")
        
        # 返回默认大纲
        return EpisodeOutline(
            episode_num=episode_num,
            title=f"第{episode_num}集",
            hook={"first_3s": {"visual": "开场画面"}},
            story_beats=[],
            cliffhanger={"last_5s": {"visual": "结尾悬念"}},
            source_chapters=chapter_range
        )
    
    # ==================== 剧本生成 ====================
    
    async def generate_script(
        self,
        outline: EpisodeOutline,
        novel_text: str,
        characters: List[Dict]
    ) -> DramaScript:
        """
        根据大纲生成分镜头脚本
        
        核心原则：
        - ❌ 绝对禁止心理描写
        - ✅ 心理描写转为视觉动作或台词
        - ✅ 台词人设化，冲突感强
        - ✅ 镜头时长1-6秒，快速切换
        """
        import uuid
        
        prompt = f"""
你是一位专业的短剧导演。请根据以下大纲生成分镜头脚本。

【剧集大纲】
{json.dumps(outline.dict(), ensure_ascii=False, indent=2)}

【原始小说】
{novel_text[:2000]}

【角色设定】
{json.dumps(characters, ensure_ascii=False, indent=2)}

【镜头要求】
1. 景别：多用特写、中景，少用远景（竖屏适配）
2. 时长：每个镜头1-6秒
3. 运镜：固定、推、拉、摇、移
4. 构图：纵向构图，底部1/3预留字幕
5. 动作：必须具体，避免抽象描述

【转换规则】
❌ "他心里很难过" → ✅ "他眼眶泛红，拳头攥紧"
❌ "她想起了往事" → ✅ "镜头闪回：她凝视照片，泪水滑落"
❌ "两人陷入了沉默" → ✅ "两人对视，时钟滴答声放大"

【输出格式】
请严格按以下JSON格式输出：
{{
  "script_id": "auto_generated",
  "episode_num": {outline.episode_num},
  "title": "{outline.title}",
  "scenes": [
    {{
      "scene_num": 1,
      "location": "办公室",
      "time_of_day": "夜",
      "interior_exterior": "内",
      "characters": ["林枫", "赵明"],
      "atmosphere": "紧张",
      "shots": [
        {{
          "shot_num": 1,
          "shot_type": "特写",
          "duration": 2.0,
          "visual": "林枫眼神锐利，嘴角紧抿",
          "action": "攥紧拳头",
          "camera_movement": "固定",
          "dialogue": {{
            "speaker": "林枫",
            "content": "你以为我会怕你？",
            "emotion_tone": "坚定"
          }},
          "sound_effects": ["心跳声"],
          "bgm": "紧张弦乐"
        }}
      ]
    }}
  ],
  "total_shots": 总镜头数,
  "total_duration": 总时长
}}

请开始生成：
"""
        
        result = await self._call_llm(
            prompt,
            system_prompt="你是一位精通竖屏短剧拍摄的专业导演，擅长将文字转化为具体的镜头语言。"
        )
        
        # 解析结果
        try:
            json_match = re.search(r'\{[\s\S]*\}', result)
            if json_match:
                data = json.loads(json_match.group())
                
                scenes = []
                for scene_data in data.get("scenes", []):
                    shots = []
                    for shot_data in scene_data.get("shots", []):
                        shots.append(ShotInfo(
                            shot_num=shot_data.get("shot_num", 1),
                            shot_type=shot_data.get("shot_type", "中景"),
                            duration=shot_data.get("duration", 3.0),
                            visual=shot_data.get("visual", ""),
                            action=shot_data.get("action"),
                            camera_movement=shot_data.get("camera_movement"),
                            dialogue=shot_data.get("dialogue"),
                            emotion_tone=shot_data.get("emotion_tone"),
                            sound_effects=shot_data.get("sound_effects", []),
                            bgm=shot_data.get("bgm")
                        ))
                    
                    scenes.append(SceneInfo(
                        scene_num=scene_data.get("scene_num", 1),
                        location=scene_data.get("location", "未知"),
                        time_of_day=scene_data.get("time_of_day", "日"),
                        interior_exterior=scene_data.get("interior_exterior", "内"),
                        characters=scene_data.get("characters", []),
                        atmosphere=scene_data.get("atmosphere"),
                        shots=shots
                    ))
                
                return DramaScript(
                    script_id=str(uuid.uuid4())[:8],
                    episode_num=data.get("episode_num", outline.episode_num),
                    title=data.get("title", outline.title),
                    status=DramaStatus.COMPLETED,
                    outline=outline,
                    scenes=scenes,
                    total_shots=data.get("total_shots", 0),
                    total_duration=data.get("total_duration", 0.0)
                )
        except Exception as e:
            print(f"Warning: Could not parse script: {e}")
        
        # 返回空脚本
        return DramaScript(
            script_id=str(uuid.uuid4())[:8],
            episode_num=outline.episode_num,
            title=outline.title,
            outline=outline
        )
    
    # ==================== 导出功能 ====================
    
    async def export_script(
        self,
        script: DramaScript,
        formats: List[DramaFormat],
        output_dir: str = "./output"
    ) -> List[str]:
        """
        导出剧本为多种格式
        
        支持：JSON, Markdown, CSV
        """
        output_files = []
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        for fmt in formats:
            if fmt == DramaFormat.JSON:
                file_path = await self._export_as_json(script, output_dir)
                output_files.append(file_path)
            
            elif fmt == DramaFormat.MARKDOWN:
                file_path = await self._export_as_markdown(script, output_dir)
                output_files.append(file_path)
            
            elif fmt == DramaFormat.CSV:
                file_path = await self._export_as_csv(script, output_dir)
                output_files.append(file_path)
        
        return output_files
    
    async def _export_as_json(self, script: DramaScript, output_dir: str) -> str:
        """导出为 JSON"""
        filename = f"episode_{script.episode_num:03d}.json"
        file_path = Path(output_dir) / filename
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(script.dict(), f, ensure_ascii=False, indent=2)
        
        return str(file_path)
    
    async def _export_as_markdown(self, script: DramaScript, output_dir: str) -> str:
        """导出为 Markdown"""
        filename = f"episode_{script.episode_num:03d}.md"
        file_path = Path(output_dir) / filename
        
        lines = [
            f"# 第{script.episode_num}集：{script.title}",
            f"\n**集数**: 第 {script.episode_num} 集",
            f"**总时长**: {script.total_duration} 秒",
            f"**总镜头数**: {script.total_shots}",
            "\n---\n"
        ]
        
        for scene in script.scenes:
            lines.append(f"\n## 场景 {scene.scene_num}")
            lines.append(f"- **地点**: {scene.location}")
            lines.append(f"- **时间**: {scene.time_of_day}")
            lines.append(f"- **内外**: {scene.interior_exterior}")
            lines.append(f"- **人物**: {', '.join(scene.characters)}")
            if scene.atmosphere:
                lines.append(f"- **氛围**: {scene.atmosphere}")
            lines.append("")
            
            for shot in scene.shots:
                lines.append(f"### 镜头 {shot.shot_num} ({shot.duration}秒)")
                lines.append(f"- **类型**: {shot.shot_type}")
                lines.append(f"- **画面**: {shot.visual}")
                if shot.action:
                    lines.append(f"- **动作**: {shot.action}")
                if shot.camera_movement:
                    lines.append(f"- **运镜**: {shot.camera_movement}")
                if shot.dialogue:
                    lines.append(f"\n**{shot.dialogue.get('speaker', '角色')}**:")
                    lines.append(f"> {shot.dialogue.get('content', '')}")
                    if shot.emotion_tone:
                        lines.append(f"> *{shot.emotion_tone}*")
                if shot.sound_effects:
                    lines.append(f"\n**音效**:")
                    lines.append(f"- SFX: {', '.join(shot.sound_effects)}")
                if shot.bgm:
                    lines.append(f"- BGM: {shot.bgm}")
                lines.append("")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        
        return str(file_path)
    
    async def _export_as_csv(self, script: DramaScript, output_dir: str) -> str:
        """导出为 CSV（剪辑软件友好）"""
        import csv
        
        filename = f"episode_{script.episode_num:03d}.csv"
        file_path = Path(output_dir) / filename
        
        rows = []
        for scene in script.scenes:
            for shot in scene.shots:
                rows.append({
                    "集数": script.episode_num,
                    "场景号": scene.scene_num,
                    "镜头号": shot.shot_num,
                    "景别": shot.shot_type,
                    "时长(秒)": shot.duration,
                    "地点": scene.location,
                    "时间": scene.time_of_day,
                    "内外景": scene.interior_exterior,
                    "人物": ", ".join(scene.characters),
                    "画面": shot.visual,
                    "动作": shot.action or "",
                    "台词角色": shot.dialogue.get("speaker", "") if shot.dialogue else "",
                    "台词内容": shot.dialogue.get("content", "") if shot.dialogue else "",
                    "情绪": shot.emotion_tone or "",
                    "运镜": shot.camera_movement or "",
                    "音效": ", ".join(shot.sound_effects),
                    "BGM": shot.bgm or ""
                })
        
        with open(file_path, "w", encoding="utf-8-sig", newline="") as f:
            if rows:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
        
        return str(file_path)
    
    # ==================== 批量处理 ====================
    
    async def batch_convert(
        self,
        novel_text: str,
        characters: List[Dict],
        chapters_per_episode: int = 3,
        output_formats: List[DramaFormat] = None
    ) -> List[DramaScript]:
        """
        批量转换小说为短剧
        
        自动按章节分组，生成多集剧本
        """
        # 按章节分割
        chapters = self._split_chapters(novel_text)
        total_chapters = len(chapters)
        
        # 分组
        episode_groups = []
        for start in range(0, total_chapters, chapters_per_episode):
            end = min(start + chapters_per_episode, total_chapters)
            episode_groups.append({
                "start": start + 1,
                "end": end,
                "chapters": chapters[start:end]
            })
        
        scripts = []
        for idx, group in enumerate(episode_groups, 1):
            print(f"Processing episode {idx}/{len(episode_groups)}...")
            
            # 合并章节文本
            combined_text = "\n\n".join(group["chapters"])
            
            # 生成大纲
            outline = await self.map_to_episode_outline(
                combined_text,
                characters,
                idx,
                f"{group['start']}-{group['end']}"
            )
            
            # 生成剧本
            script = await self.generate_script(outline, combined_text, characters)
            scripts.append(script)
        
        return scripts
    
    def _split_chapters(self, novel_text: str) -> List[str]:
        """分割章节"""
        # 常见章节标题模式
        patterns = [
            r'第[一二三四五六七八九十百千万零\d]+章',
            r'Chapter\s+\d+',
            r'【第\d+章】',
            r'第\d+章'
        ]
        
        for pattern in patterns:
            if re.search(pattern, novel_text):
                chapters = re.split(pattern, novel_text)
                return [c.strip() for c in chapters if c.strip()]
        
        # 如果没有明确的章节标记，按段落分割
        paragraphs = novel_text.split("\n\n")
        return [p for p in paragraphs if len(p) > 100]
