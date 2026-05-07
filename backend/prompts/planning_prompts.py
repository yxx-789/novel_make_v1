# prompts/planning_prompts.py
# -*- coding: utf-8 -*-
"""
规划期Prompt - 用于生成章节写作计划
迁移自 AI_NovelGenerator
"""

# ==================== 章节规划 Prompt ====================

chapter_plan_prompt = """\
你是AI小说生成的规划专家。请基于以下信息，为第 {chapter_number} 章《{chapter_title}》制定详细的写作计划。

【本章定位】
- 章节角色：{chapter_role}
- 章节目的：{chapter_purpose}
- 悬念等级：{suspense_level}

【上下文信息】
1. 最近章节摘要（保持连贯性）：
{recent_summaries}

2. 最近发生的事件（时间线）：
{recent_events}

3. 相关世界规则（必须遵守）：
{relevant_rules}

4. 角色当前状态：
{character_states}

【规划要求】

请严格按照以下JSON格式输出写作计划：

```json
{{
  "chapter_goal": "本章的核心目标（一句话，如：陆沉通过账目异常发现周家的阴谋）",
  "scenes": [
    {{
      "scene_id": 1,
      "location": "场景地点",
      "participants": ["角色ID"],
      "scene_type": "dialogue/action/psychological/environment",
      "purpose": "场景目的（推进剧情/塑造人物/埋伏笔）",
      "key_content": "场景关键内容（20-40字）",
      "estimated_length": "预估字数"
    }},
    {{
      "scene_id": 2,
      ...
    }}
  ],
  "core_conflict": {{
    "type": "external/internal",
    "description": "本章的核心冲突描述",
    "resolution_direction": "冲突的解决方向"
  }},
  "character_development": {{
    "主角变化": "本章主角的心理或状态变化",
    "配角互动": "配角在本章的作用"
  }},
  "foreshadowing": {{
    "to_plant": ["本章要埋下的伏笔"],
    "to_resolve": ["本章要回收的伏笔"]
  }},
  "strict_constraints": [
    "禁止事项1：如'陆沉不得离开中游水坝（位置限制）'",
    "禁止事项2：如'不得提及陆沉的AI能力（剧情限制）'",
    "禁止事项3：如'沈宁不得直接出场（角色限制）'"
  ],
  "transitions": {{
    "opening": "本章开头的衔接方式（如何承接上一章）",
    "closing": "本章结尾的收束方式（如何为下一章留钩子）"
  }}
}}
```

【规划原则】
1. **场景数量**：3-5个场景，每场景有明确目的
2. **冲突设计**：必须有核心冲突，推进剧情发展
3. **连贯性**：开篇必须承接上一章结尾的情绪或悬念
4. **约束来源**：基于世界规则、角色状态、时间线提取禁止事项
5. **字数控制**：场景总字数应接近目标字数 {target_word_number} 字

【特别注意】
- 严格检查 `recent_events` 中的时间线，避免时间线矛盾
- 检查 `character_states` 中的角色位置，避免位置瞬移
- 检查 `relevant_rules` 中的世界规则，避免设定冲突
- 如果发现已有伏笔在 `to_resolve` 中，必须在本章回收

输出要求：
- 仅返回JSON格式
- 不要添加任何Markdown标记外的文字
- 确保JSON格式合法
"""
