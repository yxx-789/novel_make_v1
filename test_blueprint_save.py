#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试蓝图保存和读取
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.models.schemas import PlotBlueprint
import json


def test_blueprint_dict():
    """测试蓝图序列化"""
    print("=" * 60)
    print("测试：PlotBlueprint 序列化")
    print("=" * 60)

    # 创建蓝图对象
    blueprint = PlotBlueprint(
        blueprint_id="test123",
        novel_id="test_novel",
        main_conflict="核心冲突描述",
        inciting_incident="触发事件描述",
        rising_actions=["转折点1", "转折点2", "转折点3"],
        climax="高潮描述",
        falling_actions=["解决过程1", "解决过程2"],
        resolution="结局描述"
    )

    print("\n1. 蓝图对象:")
    print(f"  - main_conflict: {blueprint.main_conflict}")
    print(f"  - rising_actions: {blueprint.rising_actions}")

    # 序列化为字典
    blueprint_dict = blueprint.model_dump()

    print("\n2. 序列化后的字典:")
    print(json.dumps(blueprint_dict, ensure_ascii=False, indent=2))

    # 检查是否有 world_setting 和 characters 字段
    print("\n3. 检查字段:")
    print(f"  - world_setting 存在: {'world_setting' in blueprint_dict}")
    print(f"  - characters 存在: {'characters' in blueprint_dict}")
    print(f"  - plot_blueprint 字段:")
    for key in blueprint_dict.keys():
        print(f"    - {key}: {type(blueprint_dict[key])}")

    # 模拟保存逻辑
    print("\n4. 模拟保存逻辑:")
    save_data = {
        "world_setting": blueprint_dict.get("world_setting", {}),
        "characters": blueprint_dict.get("characters", []),
        "plot_blueprint": blueprint_dict
    }

    print("保存数据:")
    print(f"  - world_setting: {save_data['world_setting']}")
    print(f"  - characters: {save_data['characters']}")
    print(f"  - plot_blueprint (keys): {list(save_data['plot_blueprint'].keys())}")

    # 检查 plot_blueprint 是否包含正确数据
    plot_bp = save_data["plot_blueprint"]
    if "main_conflict" in plot_bp and "rising_actions" in plot_bp:
        print("\n✅ plot_blueprint 数据正确！")
        print(f"  - main_conflict: {plot_bp['main_conflict']}")
        print(f"  - rising_actions: {plot_bp['rising_actions']}")
    else:
        print("\n❌ plot_blueprint 数据错误！")

    return True


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("测试蓝图保存逻辑")
    print("=" * 60)

    test_blueprint_dict()

    print("\n" + "=" * 60)
    print("结论")
    print("=" * 60)
    print("问题：")
    print("1. world_setting 和 characters 字段不存在")
    print("2. 但 plot_blueprint 字段应该保存成功")
    print("\n需要检查：")
    print("- 前端是否正确读取 plot_blueprint 字段")
    print("- 数据库中的 plot_blueprint 是否为空")


if __name__ == "__main__":
    main()