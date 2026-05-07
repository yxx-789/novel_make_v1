# core/architecture_generator.py
# -*- coding: utf-8 -*-
"""
小说架构生成器
迁移自 AI_NovelGenerator 的 architecture.py
包含：核心种子、角色动力学、世界观、情节架构、角色状态
"""
import os
import json
import logging
from typing import Dict, Optional
from pathlib import Path

# 导入 prompts
from prompts.architecture_prompts import (
    core_seed_prompt,
    character_dynamics_prompt,
    world_building_prompt,
    plot_architecture_prompt,
    create_character_state_prompt
)

# 导入 LLM 适配器
from utils.qianfan_client import QianfanClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ArchitectureGenerator:
    """小说架构生成器 - 完整的五阶段架构生成"""
    
    def __init__(self, llm_client: QianfanClient, output_dir: str = None):
        """
        初始化架构生成器
        
        Args:
            llm_client: 千帆 LLM 客户端
            output_dir: 输出目录，用于保存架构文件
        """
        self.llm = llm_client
        self.output_dir = output_dir or "./output"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 临时存储各阶段结果
        self.partial_data = {}
    
    def load_partial_data(self, project_id: str) -> Dict:
        """加载已生成的阶段性数据"""
        partial_file = os.path.join(self.output_dir, project_id, "partial_architecture.json")
        if not os.path.exists(partial_file):
            return {}
        try:
            with open(partial_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load partial_architecture.json: {e}")
            return {}
    
    def save_partial_data(self, project_id: str, data: Dict):
        """保存阶段性数据"""
        partial_file = os.path.join(self.output_dir, project_id, "partial_architecture.json")
        os.makedirs(os.path.dirname(partial_file), exist_ok=True)
        try:
            with open(partial_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"Failed to save partial_architecture.json: {e}")
    
    async def generate_core_seed(
        self,
        topic: str,
        genre: str,
        number_of_chapters: int,
        word_number: int = 3000,
        user_guidance: str = ""
    ) -> str:
        """
        Step 1: 生成核心种子（雪花写作法第1层）
        
        Args:
            topic: 小说主题/梗概
            genre: 小说类型
            number_of_chapters: 总章节数
            word_number: 每章字数
            user_guidance: 用户指导
        
        Returns:
            核心种子文本
        """
        if "core_seed_result" in self.partial_data:
            logger.info("Step 1 already done. Skipping...")
            return self.partial_data["core_seed_result"]
        
        logger.info("Step 1: Generating core_seed_prompt (核心种子) ...")
        
        prompt = core_seed_prompt.format(
            topic=topic,
            genre=genre,
            number_of_chapters=number_of_chapters,
            word_number=word_number
        )
        
        result = await self.llm.generate(prompt)
        
        if not result.strip():
            logger.warning("core_seed_prompt generation failed and returned empty.")
            return ""
        
        self.partial_data["core_seed_result"] = result.strip()
        logger.info(f"✅ 核心种子生成完成: {len(result)} 字")
        
        return result.strip()
    
    async def generate_character_dynamics(
        self,
        core_seed: str,
        user_guidance: str = ""
    ) -> str:
        """
        Step 2: 生成角色动力学设定
        
        Args:
            core_seed: 核心种子
            user_guidance: 用户指导
        
        Returns:
            角色动力学文本
        """
        if "character_dynamics_result" in self.partial_data:
            logger.info("Step 2 already done. Skipping...")
            return self.partial_data["character_dynamics_result"]
        
        logger.info("Step 2: Generating character_dynamics_prompt ...")
        
        prompt = character_dynamics_prompt.format(
            core_seed=core_seed,
            user_guidance=user_guidance
        )
        
        result = await self.llm.generate(prompt)
        
        if not result.strip():
            logger.warning("character_dynamics_prompt generation failed.")
            return ""
        
        self.partial_data["character_dynamics_result"] = result.strip()
        logger.info(f"✅ 角色动力学生成完成: {len(result)} 字")
        
        return result.strip()
    
    async def generate_world_building(
        self,
        core_seed: str,
        user_guidance: str = ""
    ) -> str:
        """
        Step 3: 生成世界观构建
        
        Args:
            core_seed: 核心种子
            user_guidance: 用户指导
        
        Returns:
            世界观文本
        """
        if "world_building_result" in self.partial_data:
            logger.info("Step 3 already done. Skipping...")
            return self.partial_data["world_building_result"]
        
        logger.info("Step 3: Generating world_building_prompt ...")
        
        prompt = world_building_prompt.format(
            core_seed=core_seed,
            user_guidance=user_guidance
        )
        
        result = await self.llm.generate(prompt)
        
        if not result.strip():
            logger.warning("world_building_prompt generation failed.")
            return ""
        
        self.partial_data["world_building_result"] = result.strip()
        logger.info(f"✅ 世界观构建完成: {len(result)} 字")
        
        return result.strip()
    
    async def generate_plot_architecture(
        self,
        core_seed: str,
        character_dynamics: str,
        world_building: str,
        user_guidance: str = ""
    ) -> str:
        """
        Step 4: 生成情节架构（三幕式）
        
        Args:
            core_seed: 核心种子
            character_dynamics: 角色动力学
            world_building: 世界观
            user_guidance: 用户指导
        
        Returns:
            情节架构文本
        """
        if "plot_arch_result" in self.partial_data:
            logger.info("Step 4 already done. Skipping...")
            return self.partial_data["plot_arch_result"]
        
        logger.info("Step 4: Generating plot_architecture_prompt ...")
        
        prompt = plot_architecture_prompt.format(
            core_seed=core_seed,
            character_dynamics=character_dynamics,
            world_building=world_building,
            user_guidance=user_guidance
        )
        
        result = await self.llm.generate(prompt)
        
        if not result.strip():
            logger.warning("plot_architecture_prompt generation failed.")
            return ""
        
        self.partial_data["plot_arch_result"] = result.strip()
        logger.info(f"✅ 情节架构生成完成: {len(result)} 字")
        
        return result.strip()
    
    async def generate_character_state(
        self,
        character_dynamics: str
    ) -> str:
        """
        Step 5: 生成角色状态初始化表
        
        Args:
            character_dynamics: 角色动力学设定
        
        Returns:
            角色状态表文本
        """
        if "character_state_result" in self.partial_data:
            logger.info("Step 5 already done. Skipping...")
            return self.partial_data["character_state_result"]
        
        logger.info("Step 5: Generating initial character state ...")
        
        prompt = create_character_state_prompt.format(
            character_dynamics=character_dynamics
        )
        
        result = await self.llm.generate(prompt)
        
        if not result.strip():
            logger.warning("create_character_state_prompt generation failed.")
            return ""
        
        self.partial_data["character_state_result"] = result.strip()
        logger.info(f"✅ 角色状态表生成完成: {len(result)} 字")
        
        return result.strip()
    
    async def generate_full_architecture(
        self,
        topic: str,
        genre: str,
        number_of_chapters: int,
        word_number: int = 3000,
        user_guidance: str = "",
        project_id: str = None
    ) -> Dict[str, str]:
        """
        生成完整的小说架构（五阶段）
        
        Args:
            topic: 小说主题/梗概
            genre: 小说类型
            number_of_chapters: 总章节数
            word_number: 每章字数
            user_guidance: 用户指导
            project_id: 项目ID（用于保存进度）
        
        Returns:
            包含所有架构内容的字典
        """
        # 加载已有进度
        if project_id:
            self.partial_data = self.load_partial_data(project_id)
        
        logger.info("="*80)
        logger.info("开始生成完整小说架构...")
        logger.info("="*80)
        
        # Step 1: 核心种子
        core_seed = await self.generate_core_seed(
            topic, genre, number_of_chapters, word_number, user_guidance
        )
        if not core_seed:
            return {}
        
        # 保存进度
        if project_id:
            self.save_partial_data(project_id, self.partial_data)
        
        # Step 2: 角色动力学
        character_dynamics = await self.generate_character_dynamics(
            core_seed, user_guidance
        )
        if not character_dynamics:
            return {}
        
        # 保存进度
        if project_id:
            self.save_partial_data(project_id, self.partial_data)
        
        # Step 3: 世界观
        world_building = await self.generate_world_building(
            core_seed, user_guidance
        )
        if not world_building:
            return {}
        
        # 保存进度
        if project_id:
            self.save_partial_data(project_id, self.partial_data)
        
        # Step 4: 情节架构
        plot_architecture = await self.generate_plot_architecture(
            core_seed, character_dynamics, world_building, user_guidance
        )
        if not plot_architecture:
            return {}
        
        # 保存进度
        if project_id:
            self.save_partial_data(project_id, self.partial_data)
        
        # Step 5: 角色状态
        character_state = await self.generate_character_state(character_dynamics)
        if not character_state:
            return {}
        
        # 保存进度
        if project_id:
            self.save_partial_data(project_id, self.partial_data)
        
        # 生成最终架构文档
        final_content = self._format_final_architecture(
            topic, genre, number_of_chapters, word_number,
            core_seed, character_dynamics, world_building,
            plot_architecture, character_state
        )
        
        # 保存最终文档
        if project_id:
            arch_file = os.path.join(self.output_dir, project_id, "Novel_architecture.txt")
            os.makedirs(os.path.dirname(arch_file), exist_ok=True)
            with open(arch_file, "w", encoding="utf-8") as f:
                f.write(final_content)
            logger.info(f"✅ 最终架构文档已保存: {arch_file}")
            
            # 保存角色状态表
            state_file = os.path.join(self.output_dir, project_id, "character_state.txt")
            with open(state_file, "w", encoding="utf-8") as f:
                f.write(character_state)
            logger.info(f"✅ 角色状态表已保存: {state_file}")
            
            # 清理临时文件
            partial_file = os.path.join(self.output_dir, project_id, "partial_architecture.json")
            if os.path.exists(partial_file):
                os.remove(partial_file)
                logger.info("✅ 临时进度文件已清理")
        
        logger.info("="*80)
        logger.info("🎉 完整架构生成成功！")
        logger.info("="*80)
        
        return {
            "core_seed": core_seed,
            "character_dynamics": character_dynamics,
            "world_building": world_building,
            "plot_architecture": plot_architecture,
            "character_state": character_state,
            "full_architecture": final_content
        }
    
    def _format_final_architecture(
        self,
        topic: str,
        genre: str,
        number_of_chapters: int,
        word_number: int,
        core_seed: str,
        character_dynamics: str,
        world_building: str,
        plot_architecture: str,
        character_state: str
    ) -> str:
        """格式化最终架构文档"""
        return f"""#=== 0) 小说设定 ===
主题：{topic}
类型：{genre}
篇幅：约{number_of_chapters}章（每章{word_number}字）

#=== 1) 核心种子 ===
{core_seed}

#=== 2) 角色动力学 ===
{character_dynamics}

#=== 3) 世界观 ===
{world_building}

#=== 4) 三幕式情节架构 ===
{plot_architecture}

#=== 5) 角色状态表 ===
{character_state}
"""
