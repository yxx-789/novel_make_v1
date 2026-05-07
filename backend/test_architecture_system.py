#!/usr/bin/env python3
"""
测试完整的架构生成系统
"""
import os
import sys
import asyncio
from pathlib import Path

os.environ['QIANFAN_API_KEY'] = 'bce-v3/ALTAK-vnASNnJZQkPchN6JShUdi/38e23c1484e3b2ab42e15dd596dc85fd4328caf4'
sys.path.insert(0, str(Path(__file__).parent))

from utils.qianfan_client import QianfanClient
from core.architecture_generator import ArchitectureGenerator
from core.blueprint_generator import BlueprintGenerator
from core.chapter_planner import ChapterPlanner

async def test_full_architecture():
    """测试完整架构生成"""
    print("\n" + "="*80)
    print("完整架构生成系统测试")
    print("="*80)
    
    # 初始化 LLM 客户端
    llm_config = {
        "model": "glm-5.1",
        "temperature": 0.7,
        "max_tokens": 4096
    }
    llm_client = QianfanClient(llm_config)
    
    # 创建输出目录
    output_dir = Path(__file__).parent / "output_architecture_test"
    output_dir.mkdir(exist_ok=True)
    
    # 测试参数
    test_params = {
        "topic": "一个少年从凡人修成仙帝的故事，包含奇遇、修炼、战斗、情感等丰富元素",
        "genre": "玄幻",
        "number_of_chapters": 10,
        "word_number": 3000,
        "user_guidance": "主角性格坚韧，有正义感，但也会面临道德困境",
        "project_id": "test_novel_001"
    }
    
    print("\n[1. 测试架构生成器]")
    print("-" * 80)
    
    # 创建架构生成器
    arch_gen = ArchitectureGenerator(llm_client, str(output_dir))
    
    # 生成完整架构
    architecture = await arch_gen.generate_full_architecture(
        topic=test_params["topic"],
        genre=test_params["genre"],
        number_of_chapters=test_params["number_of_chapters"],
        word_number=test_params["word_number"],
        user_guidance=test_params["user_guidance"],
        project_id=test_params["project_id"]
    )
    
    if architecture:
        print(f"\n✅ 架构生成成功！")
        print(f"   核心种子字数: {len(architecture['core_seed'])}")
        print(f"   角色动力学字数: {len(architecture['character_dynamics'])}")
        print(f"   世界观字数: {len(architecture['world_building'])}")
        print(f"   情节架构字数: {len(architecture['plot_architecture'])}")
        print(f"   角色状态字数: {len(architecture['character_state'])}")
        print(f"   总架构字数: {len(architecture['full_architecture'])}")
        
        # 显示核心种子预览
        print(f"\n📋 核心种子预览:")
        print(f"   {architecture['core_seed'][:100]}...")
        
        # 显示角色状态预览
        print(f"\n📋 角色状态预览:")
        print(f"   {architecture['character_state'][:200]}...")
    else:
        print("❌ 架构生成失败")
        return
    
    print("\n[2. 测试蓝图生成器]")
    print("-" * 80)
    
    # 创建蓝图生成器
    blueprint_gen = BlueprintGenerator(llm_client, str(output_dir))
    
    # 生成章节蓝图
    blueprint = await blueprint_gen.generate_blueprint(
        novel_architecture=architecture['full_architecture'],
        number_of_chapters=test_params["number_of_chapters"],
        user_guidance=test_params["user_guidance"],
        project_id=test_params["project_id"]
    )
    
    if blueprint:
        print(f"\n✅ 蓝图生成成功！")
        print(f"   蓝图总字数: {len(blueprint)}")
        
        # 解析蓝图
        blueprint_data = blueprint_gen.parse_blueprint_to_dict(blueprint)
        print(f"   解析章节数: {len(blueprint_data)}")
        
        if blueprint_data:
            print(f"\n📋 第1章信息:")
            ch1 = blueprint_data[0]
            print(f"   标题: {ch1['title']}")
            print(f"   定位: {ch1['role']}")
            print(f"   作用: {ch1['purpose']}")
            print(f"   悬念: {ch1['suspense_level']}")
            print(f"   伏笔: {ch1['foreshadowing']}")
            print(f"   认知颠覆: {ch1['plot_twist_level']}")
            print(f"   简述: {ch1['summary']}")
    else:
        print("❌ 蓝图生成失败")
        return
    
    print("\n[3. 测试章节规划器]")
    print("-" * 80)
    
    # 创建章节规划器
    planner = ChapterPlanner(llm_client, str(output_dir))
    
    # 为第1章生成规划
    if blueprint_data:
        ch1_plan = await planner.generate_chapter_plan(
            chapter_number=1,
            chapter_title=blueprint_data[0]['title'],
            chapter_role=blueprint_data[0]['role'],
            chapter_purpose=blueprint_data[0]['purpose'],
            suspense_level=blueprint_data[0]['suspense_level'],
            recent_summaries="这是第一章",
            recent_events="故事开始",
            relevant_rules=architecture['world_building'][:500],
            character_states=architecture['character_state'][:500],
            target_word_number=3000,
            project_id=test_params["project_id"]
        )
        
        print(f"\n✅ 第1章规划生成成功！")
        print(f"   章节目标: {ch1_plan.get('chapter_goal', '无')}")
        print(f"   场景数: {len(ch1_plan.get('scenes', []))}")
        print(f"   核心冲突: {ch1_plan.get('core_conflict', {}).get('description', '无')}")
        
        if ch1_plan.get('scenes'):
            print(f"\n📋 场景列表:")
            for scene in ch1_plan['scenes']:
                print(f"   场景{scene['scene_id']}: {scene['scene_type']} - {scene['key_content']}")
    
    print("\n" + "="*80)
    print("🎉 完整架构系统测试完成！")
    print("="*80)
    
    # 显示文件列表
    print(f"\n📂 生成的文件:")
    project_dir = output_dir / test_params["project_id"]
    if project_dir.exists():
        for file in sorted(project_dir.iterdir()):
            if file.is_file():
                size = file.stat().st_size
                print(f"   {file.name}: {size} bytes")

if __name__ == "__main__":
    asyncio.run(test_full_architecture())
