# -*- coding: utf-8 -*-
"""
JSON 工具函数
处理 AI 生成的不规范 JSON 格式
"""

import re
import json
from typing import Dict, List, Any


def clean_json_string(json_str: str) -> str:
    """
    清理 JSON 字符串中的不规范格式
    
    主要处理：
    1. 数组中的索引号（如 ["0": "value"] -> ["value"]）
    2. 尾随逗号
    3. 注释
    """
    # 移除数组中的索引号
    # 匹配模式：[数字]: "内容"
    # 替换为："内容"
    
    # 匹配 "key": [ 之后的索引号
    # 例如：[0: "value", 1: "value"] -> ["value", "value"]
    
    # 使用正则表达式移除索引号
    # 匹配：数字后跟冒号和空格，然后是引号
    json_str = re.sub(r'(\d+)\s*:\s*"', '"', json_str)
    
    # 移除尾随逗号（在 ] 或 } 之前的逗号）
    json_str = re.sub(r',\s*([}\]])', r'\1', json_str)
    
    # 移除单行注释
    json_str = re.sub(r'//.*$', '', json_str, flags=re.MULTILINE)
    
    # 移除多行注释
    json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)
    
    return json_str


def parse_ai_json(text: str) -> Dict[str, Any]:
    """
    解析 AI 生成的 JSON，处理不规范格式
    
    Args:
        text: AI 生成的文本，可能包含 JSON
        
    Returns:
        解析后的字典
    """
    try:
        # 尝试提取 JSON 内容
        json_match = re.search(r'\{[\s\S]*\}', text)
        
        if not json_match:
            return {}
        
        json_str = json_match.group()
        
        # 清理 JSON 字符串
        cleaned_json = clean_json_string(json_str)
        
        # 尝试解析
        try:
            data = json.loads(cleaned_json)
            return data
        except json.JSONDecodeError as e:
            # 如果仍然失败，尝试更激进的清理
            print(f"JSON 解析失败，尝试更激进的清理: {e}")
            
            # 移除所有换行和多余空格
            cleaned_json = re.sub(r'\s+', ' ', cleaned_json)
            
            # 再次尝试
            try:
                data = json.loads(cleaned_json)
                return data
            except:
                # 最后的尝试：使用正则表达式手动提取
                print("使用正则表达式手动提取")
                return extract_json_manually(cleaned_json)
    
    except Exception as e:
        print(f"解析 JSON 时出错: {e}")
        return {}


def extract_json_manually(text: str) -> Dict[str, Any]:
    """
    手动提取 JSON 内容（最后的手段）
    """
    result = {}
    
    try:
        # 提取字符串字段
        string_pattern = r'"([^"]+)"\s*:\s*"([^"]*)"'
        for match in re.finditer(string_pattern, text):
            key, value = match.groups()
            result[key] = value
        
        # 提取数组字段
        array_pattern = r'"([^"]+)"\s*:\s*\[([^\]]*)\]'
        for match in re.finditer(array_pattern, text):
            key = match.group(1)
            array_content = match.group(2)
            
            # 提取数组中的字符串
            items = re.findall(r'"([^"]*)"', array_content)
            result[key] = items
    
    except Exception as e:
        print(f"手动提取失败: {e}")
    
    return result


if __name__ == "__main__":
    # 测试
    test_cases = [
        # 测试带索引号的数组
        '''{
            "rising_actions": [
                0: "转折点1",
                1: "转折点2"
            ]
        }''',
        
        # 测试标准 JSON
        '''{
            "main_conflict": "核心冲突描述",
            "rising_actions": [
                "转折点1",
                "转折点2"
            ]
        }''',
        
        # 测试尾随逗号
        '''{
            "key": "value",
        }'''
    ]
    
    for i, test in enumerate(test_cases):
        print(f"\n=== 测试 {i+1} ===")
        print(f"输入: {test}")
        result = parse_ai_json(test)
        print(f"输出: {json.dumps(result, ensure_ascii=False, indent=2)}")