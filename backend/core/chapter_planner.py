# core/chapter_planner.py
# -*- coding: utf-8 -*-
"""
章节规划器
迁移自 AI_NovelGenerator 的 chapter_planner.py
包含：场景规划、冲突设计、约束检查
"""
import os
import json
import re
import logging
from typing import Dict, List, Optional
from pathlib import Path

# 导入 prompts
from prompts.planning_prompts import chapter_plan_prompt

# 导入 LLM 适配器
from utils.qianfan_client import QianfanClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ChapterPlanner:
    """章节规划器 - 详细场景规划"""
    
    def __init__(self, llm_client: QianfanClient, output_dir: str = None):
        """
        初始化章节规划器
        
        Args:
            llm_client: 千帆 LLM 客户端
            output_dir: 输出目录
        """
        self.llm = llm_client
        self.output_dir = output_dir or "./output"
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def generate_chapter_plan(
        self,
        chapter_number: int,
        chapter_title: str,
        chapter_role: str,
        chapter_purpose: str,
        suspense_level: str,
        recent_summaries: str,
        recent_events: str,
        relevant_rules: str,
        character_states: str,
        target_word_number: int = 3000,
        project_id: str = None
    ) -> Dict:
        """
        生成章节规划
        
        Args:
            chapter_number: 章节号
            chapter_title: 章节标题
            chapter_role: 章节定位
            chapter_purpose: 核心作用
            suspense_level: 悬念等级
            recent_summaries: 最近章节摘要
            recent_events: 最近发生的事件
            relevant_rules: 相关世界规则
            character_states: 角色当前状态
            target_word_number: 目标字数
            project_id: 项目ID
        
        Returns:
            章节规划字典
        """
        logger.info(f"开始生成第 {chapter_number} 章规划...")
        
        prompt = chapter_plan_prompt.format(
            chapter_number=chapter_number,
            chapter_title=chapter_title,
            chapter_role=chapter_role,
            chapter_purpose=chapter_purpose,
            suspense_level=suspense_level,
            recent_summaries=recent_summaries,
            recent_events=recent_events,
            relevant_rules=relevant_rules,
            character_states=character_states,
            target_word_number=target_word_number
        )
        
        result = await self.llm.generate(prompt)
        
        # 解析 JSON
        plan_data = self._parse_plan_json(result)
        
        if not plan_data:
            logger.warning(f"第 {chapter_number} 章规划解析失败")
            return self._create_default_plan(chapter_number, chapter_title, target_word_number)
        
        # 保存规划
        if project_id:
            plan_file = os.path.join(
                self.output_dir, project_id, 
                f"chapter_{chapter_number}_plan.json"
            )
            os.makedirs(os.path.dirname(plan_file), exist_ok=True)
            with open(plan_file, "w", encoding="utf-8") as f:
                json.dump(plan_data, f, ensure_ascii=False, indent=2)
            logger.info(f"✅ 第 {chapter_number} 章规划已保存: {plan_file}")
        
        logger.info(f"✅ 第 {chapter_number} 章规划生成完成")
        return plan_data
    
    def _parse_plan_json(self, text: str) -> Optional[Dict]:
        """
        解析规划 JSON
        
        Args:
            text: LLM 返回的文本
        
        Returns:
            解析后的字典，失败返回 None
        """
        try:
            # 尝试直接解析
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # 尝试提取 JSON 块
        json_match = re.search(r'```json\s*(\{[\s\S]*?\})\s*```', text)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # 尝试提取裸 JSON
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        return None
    
    def _create_default_plan(
        self,
        chapter_number: int,
        chapter_title: str,
        target_word_number: int
    ) -> Dict:
        """创建默认规划（解析失败时使用）"""
        return {
            "chapter_goal": f"第{chapter_number}章的核心目标",
            "scenes": [
                {
                    "scene_id": 1,
                    "location": "主要场景",
                    "participants": ["主角"],
                    "scene_type": "dialogue",
                    "purpose": "推进剧情",
                    "key_content": "本章的核心场景",
                    "estimated_length": str(target_word_number // 2)
                },
                {
                    "scene_id": 2,
                    "location": "次要场景",
                    "participants": ["主角", "配角"],
                    "scene_type": "action",
                    "purpose": "塑造人物",
                    "key_content": "次要场景内容",
                    "estimated_length": str(target_word_number // 2)
                }
            ],
            "core_conflict": {
                "type": "external",
                "description": "本章的核心冲突",
                "resolution_direction": "冲突的解决方向"
            },
            "character_development": {
                "主角变化": "本章主角的变化",
                "配角互动": "配角的作用"
            },
            "foreshadowing": {
                "to_plant": ["本章要埋下的伏笔"],
                "to_resolve": ["本章要回收的伏笔"]
            },
            "strict_constraints": [
                "避免与前文设定冲突"
            ],
            "transitions": {
                "opening": "自然承接上一章",
                "closing": "为下一章留悬念"
            }
        }
    
    def validate_plan(self, plan: Dict, character_states: str) -> List[str]:
        """
        验证规划的一致性
        
        Args:
            plan: 章节规划
            character_states: 角色状态
        
        Returns:
            问题列表
        """
        issues = []
        
        # 检查场景数量
        scenes = plan.get("scenes", [])
        if len(scenes) < 2:
            issues.append("场景数量过少，建议至少2个场景")
        elif len(scenes) > 5:
            issues.append("场景数量过多，建议不超过5个场景")
        
        # 检查核心冲突
        conflict = plan.get("core_conflict", {})
        if not conflict.get("description"):
            issues.append("缺少核心冲突描述")
        
        # 检查伏笔
        foreshadowing = plan.get("foreshadowing", {})
        if not foreshadowing.get("to_plant") and not foreshadowing.get("to_resolve"):
            issues.append("缺少伏笔设计")
        
        return issues
    
    async def batch_generate_plans(
        self,
        blueprint_data: List[Dict],
        architecture: str,
        character_states: str,
        project_id: str = None
    ) -> List[Dict]:
        """
        批量生成章节规划
        
        Args:
            blueprint_data: 蓝图数据列表
            architecture: 小说架构
            character_states: 角色状态
            project_id: 项目ID
        
        Returns:
            规划列表
        """
        plans = []
        
        for i, chapter_info in enumerate(blueprint_data):
            # 准备上下文
            recent_summaries = "\n".join([
                f"第{p['chapter_num']}章: {p.get('summary', '无摘要')}"
                for p in plans[-3:]  # 最近3章
            ]) if plans else "这是第一章"
            
            recent_events = "故事开始" if i == 0 else "待提取事件"
            relevant_rules = architecture  # 简化处理
            
            # 生成规划
            plan = await self.generate_chapter_plan(
                chapter_number=chapter_info["chapter_num"],
                chapter_title=chapter_info["title"],
                chapter_role=chapter_info.get("role", ""),
                chapter_purpose=chapter_info.get("purpose", ""),
                suspense_level=chapter_info.get("suspense_level", ""),
                recent_summaries=recent_summaries,
                recent_events=recent_events,
                relevant_rules=relevant_rules,
                character_states=character_states,
                target_word_number=3000,
                project_id=project_id
            )
            
            plans.append(plan)
        
        logger.info(f"✅ 批量规划完成，共 {len(plans)} 章")
        return plans
