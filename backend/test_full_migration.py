#!/usr/bin/env python3
"""
测试完整的架构迁移系统
包含：架构生成 → 蓝图生成 → 章节规划 → 章节生成
"""
import os
import sys
import asyncio
from pathlib import Path

os.environ['QIANFAN_API_KEY'] = 'bce-v3/ALTAK-vnASNnJZQkPchN6JShUdi/38e23c1484e3b2ab42e15dd596dc85fd4328caf4'
sys.path.insert(0, str(Path(__file__).parent))

from core.novel_engine_qianfan import NovelEngine

async def test_full_pipeline():
    """测试完整管道：架构→蓝图→大纲→章节"""
    print("\n" + "="*80)
    print("完整架构迁移系统测试")
    print("="*80)
    
    # 配置
    config = {
        "model": "glm-5.1",
        "temperature": 0.7,
        "max_tokens": 100000
    }
    
    engine = NovelEngine(config)
    
    # Step 1: 创建项目
    print("\n[Step 1: 创建项目]")
    print("-" * 80)
    project = await engine.create_project({
        "title": "仙道长生",
        "genre": "玄幻",
        "topic": "一个少年从凡人修成仙帝的故事，包含奇遇、修炼、战斗、情感等丰富元素",
        "total_chapters": 5,
        "target_word_count": 3000
    })
    print(f"✅ 项目创建成功")
    print(f"   ID: {project.novel_id}")
    print(f"   标题: {project.title}")
    print(f"   类型: {project.genre.value}")
    
    # Step 2: 生成完整架构
    print("\n[Step 2: 生成完整架构]")
    print("-" * 80)
    print("正在生成五阶段架构...")
    print("   1/5 核心种子（雪花写作法）")
    print("   2/5 角色动力学（角色弧光模型）")
    print("   3/5 世界观构建（三维交织法）")
    print("   4/5 情节架构（三幕式悬念）")
    print("   5/5 角色状态初始化")
    
    architecture = await engine.generate_architecture(
        novel_id=project.novel_id,
        user_guidance="主角性格坚韧，有正义感，但也会面临道德困境"
    )
    
    if architecture:
        print(f"\n✅ 架构生成成功！")
        print(f"   核心种子字数: {len(architecture['core_seed'])}")
        print(f"   角色动力学字数: {len(architecture['character_dynamics'])}")
        print(f"   世界观字数: {len(architecture['world_building'])}")
        print(f"   情节架构字数: {len(architecture['plot_architecture'])}")
        print(f"   角色状态字数: {len(architecture['character_state'])}")
        print(f"   总架构字数: {len(architecture['full_architecture'])}")
        
        # 显示核心种子
        print(f"\n📋 核心种子预览:")
        print(f"   {architecture['core_seed']}")
        
        # 显示角色状态预览
        print(f"\n📋 角色状态预览（前300字）:")
        print(f"   {architecture['character_state'][:300]}...")
    else:
        print("❌ 架构生成失败")
        return
    
    # Step 3: 生成章节蓝图
    print("\n[Step 3: 生成章节蓝图]")
    print("-" * 80)
    print("正在生成悬念节奏曲线蓝图...")
    
    blueprint = await engine.generate_blueprint(project.novel_id)
    
    if blueprint:
        print(f"\n✅ 蓝图生成成功！")
        print(f"   核心冲突: {blueprint.main_conflict}")
        print(f"   触发事件: {blueprint.inciting_incident[:100]}...")
        
        if project.blueprint_text:
            print(f"   详细蓝图字数: {len(project.blueprint_text)}")
            
            # 显示蓝图预览
            lines = project.blueprint_text.split('\n')
            print(f"\n📋 章节蓝图预览（前5章）:")
            for line in lines[:30]:
                if line.strip():
                    print(f"   {line}")
    else:
        print("❌ 蓝图生成失败")
        return
    
    # Step 4: 生成章节大纲
    print("\n[Step 4: 生成章节大纲]")
    print("-" * 80)
    
    outlines = await engine.generate_chapter_outline(project.novel_id)
    print(f"✅ 大纲生成成功 - 共 {len(outlines)} 章")
    
    if outlines:
        print(f"\n📋 第1章大纲：")
        ch1 = outlines[0]
        print(f"   标题: {ch1.title}")
        print(f"   摘要字数: {len(ch1.summary)}")
        print(f"   摘要预览: {ch1.summary[:100]}...")
        print(f"   关键事件数: {len(ch1.key_events)}")
    
    # Step 5: 生成第1章
    print("\n[Step 5: 生成第1章]")
    print("-" * 80)
    
    chapter = await engine.generate_chapter(
        project.novel_id, 
        1, 
        use_memory=False
    )
    
    print(f"✅ 第1章生成成功")
    print(f"   标题: {chapter.title}")
    print(f"   实际字数: {chapter.word_count}")
    print(f"   目标字数: {project.target_word_count}")
    print(f"   完成率: {chapter.word_count / project.target_word_count * 100:.1f}%")
    
    # 显示章节预览
    print(f"\n📋 章节预览（前200字）:")
    print(f"   {chapter.content[:200]}...")
    
    # 最终总结
    print("\n" + "="*80)
    print("🎉 完整架构迁移系统测试成功！")
    print("="*80)
    
    print(f"\n📊 测试总结:")
    print(f"   ✅ 架构生成: 五阶段完整")
    print(f"   ✅ 蓝图生成: 悬念节奏曲线")
    print(f"   ✅ 大纲生成: 详细章节大纲")
    print(f"   ✅ 章节生成: 结合架构信息")
    
    print(f"\n📂 生成文件:")
    print(f"   - Novel_architecture.txt (完整架构)")
    print(f"   - character_state.txt (角色状态表)")
    print(f"   - Novel_directory.txt (章节蓝图)")

if __name__ == "__main__":
    asyncio.run(test_full_pipeline())
