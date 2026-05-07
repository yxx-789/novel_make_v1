# core/blueprint_generator.py
# -*- coding: utf-8 -*-
"""
章节蓝图生成器
迁移自 AI_NovelGenerator 的 blueprint.py
包含：悬念节奏曲线、伏笔操作、认知颠覆强度
"""
import os
import re
import logging
from typing import List, Dict, Optional
from pathlib import Path

# 导入 prompts
from prompts.blueprint_prompts import (
    chapter_blueprint_prompt,
    chunked_chapter_blueprint_prompt
)

# 导入 LLM 适配器
from utils.qianfan_client import QianfanClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BlueprintGenerator:
    """章节蓝图生成器 - 悬念节奏曲线设计"""
    
    def __init__(self, llm_client: QianfanClient, output_dir: str = None):
        """
        初始化蓝图生成器
        
        Args:
            llm_client: 千帆 LLM 客户端
            output_dir: 输出目录
        """
        self.llm = llm_client
        self.output_dir = output_dir or "./output"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def compute_chunk_size(self, number_of_chapters: int, max_tokens: int = 4096) -> int:
        """
        计算分块大小
        
        Args:
            number_of_chapters: 总章节数
            max_tokens: 最大 token 数
        
        Returns:
            每块章节数
        """
        tokens_per_chapter = 200.0
        ratio = max_tokens / tokens_per_chapter
        ratio_rounded_to_10 = int(ratio // 10) * 10
        chunk_size = ratio_rounded_to_10 - 10
        
        if chunk_size < 1:
            chunk_size = 1
        if chunk_size > number_of_chapters:
            chunk_size = number_of_chapters
        
        return chunk_size
    
    def limit_chapter_blueprint(self, blueprint_text: str, limit_chapters: int = 100) -> str:
        """
        限制章节蓝图的章节数（避免 prompt 过长）
        
        Args:
            blueprint_text: 完整蓝图文本
            limit_chapters: 最大章节数
        
        Returns:
            限制后的蓝图文本
        """
        pattern = r"(第\s*\d+\s*章.*?)(?=第\s*\d+\s*章|$)"
        chapters = re.findall(pattern, blueprint_text, flags=re.DOTALL)
        
        if not chapters:
            return blueprint_text
        
        if len(chapters) <= limit_chapters:
            return blueprint_text
        
        selected = chapters[-limit_chapters:]
        return "\n\n".join(selected).strip()
    
    async def generate_blueprint(
        self,
        novel_architecture: str,
        number_of_chapters: int,
        user_guidance: str = "",
        project_id: str = None
    ) -> str:
        """
        生成章节蓝图
        
        Args:
            novel_architecture: 小说架构文本
            number_of_chapters: 总章节数
            user_guidance: 用户指导
            project_id: 项目ID
        
        Returns:
            章节蓝图文本
        """
        logger.info("="*80)
        logger.info("开始生成章节蓝图...")
        logger.info("="*80)
        
        # 检查是否已有部分蓝图
        existing_blueprint = ""
        if project_id:
            blueprint_file = os.path.join(self.output_dir, project_id, "Novel_directory.txt")
            if os.path.exists(blueprint_file):
                with open(blueprint_file, "r", encoding="utf-8") as f:
                    existing_blueprint = f.read().strip()
        
        # 计算分块大小
        chunk_size = self.compute_chunk_size(number_of_chapters)
        logger.info(f"总章节数: {number_of_chapters}, 分块大小: {chunk_size}")
        
        # 如果已有蓝图，从断点继续
        if existing_blueprint:
            logger.info("检测到已有蓝图，从断点继续生成...")
            pattern = r"第\s*(\d+)\s*章"
            existing_chapter_numbers = re.findall(pattern, existing_blueprint)
            existing_chapter_numbers = [int(x) for x in existing_chapter_numbers if x.isdigit()]
            max_existing_chap = max(existing_chapter_numbers) if existing_chapter_numbers else 0
            logger.info(f"已生成到第 {max_existing_chap} 章")
            
            final_blueprint = existing_blueprint
            current_start = max_existing_chap + 1
        else:
            final_blueprint = ""
            current_start = 1
        
        # 分块生成
        while current_start <= number_of_chapters:
            current_end = min(current_start + chunk_size - 1, number_of_chapters)
            
            # 限制已有蓝图的长度
            limited_blueprint = self.limit_chapter_blueprint(final_blueprint, 100)
            
            # 生成当前块
            if current_start == 1:
                # 第一块，使用完整 prompt
                prompt = chapter_blueprint_prompt.format(
                    novel_architecture=novel_architecture,
                    number_of_chapters=number_of_chapters,
                    user_guidance=user_guidance
                )
            else:
                # 后续块，使用分块 prompt
                prompt = chunked_chapter_blueprint_prompt.format(
                    novel_architecture=novel_architecture,
                    chapter_list=limited_blueprint,
                    number_of_chapters=number_of_chapters,
                    n=current_start,
                    m=current_end,
                    user_guidance=user_guidance
                )
            
            logger.info(f"正在生成第 [{current_start}..{current_end}] 章...")
            
            result = await self.llm.generate(prompt)
            
            if not result.strip():
                logger.warning(f"第 [{current_start}..{current_end}] 章生成失败")
                # 保存已有内容
                if project_id and final_blueprint.strip():
                    blueprint_file = os.path.join(self.output_dir, project_id, "Novel_directory.txt")
                    os.makedirs(os.path.dirname(blueprint_file), exist_ok=True)
                    with open(blueprint_file, "w", encoding="utf-8") as f:
                        f.write(final_blueprint.strip())
                break
            
            if final_blueprint.strip():
                final_blueprint += "\n\n" + result.strip()
            else:
                final_blueprint = result.strip()
            
            # 保存进度
            if project_id:
                blueprint_file = os.path.join(self.output_dir, project_id, "Novel_directory.txt")
                os.makedirs(os.path.dirname(blueprint_file), exist_ok=True)
                with open(blueprint_file, "w", encoding="utf-8") as f:
                    f.write(final_blueprint.strip())
            
            current_start = current_end + 1
        
        logger.info("="*80)
        logger.info(f"✅ 章节蓝图生成完成，共 {len(final_blueprint)} 字")
        logger.info("="*80)
        
        return final_blueprint
    
    def parse_blueprint_to_dict(self, blueprint_text: str) -> List[Dict]:
        """
        解析蓝图文本为结构化数据
        
        Args:
            blueprint_text: 蓝图文本
        
        Returns:
            章节信息列表
        """
        chapters = []
        pattern = r"第\s*(\d+)\s*章\s*[-—]\s*(.+?)(?=\n本章定位)"
        
        chapter_blocks = re.split(r'(?=第\s*\d+\s*章)', blueprint_text)
        
        for block in chapter_blocks:
            if not block.strip():
                continue
            
            # 提取章节号和标题
            title_match = re.search(r'第\s*(\d+)\s*章\s*[-—]\s*(.+?)(?:\n|$)', block)
            if not title_match:
                continue
            
            chapter_num = int(title_match.group(1))
            title = title_match.group(2).strip()
            
            # 提取各字段
            def extract_field(field_name: str) -> str:
                pattern = rf"{field_name}[：:]\s*(.+?)(?=\n|$)"
                match = re.search(pattern, block)
                return match.group(1).strip() if match else ""
            
            chapter_info = {
                "chapter_num": chapter_num,
                "title": title,
                "role": extract_field("本章定位"),
                "purpose": extract_field("核心作用"),
                "suspense_level": extract_field("悬念密度"),
                "foreshadowing": extract_field("伏笔操作"),
                "plot_twist_level": extract_field("认知颠覆"),
                "summary": extract_field("本章简述")
            }
            
            chapters.append(chapter_info)
        
        return chapters
