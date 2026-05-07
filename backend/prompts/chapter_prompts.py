# prompts/chapter_prompts.py
# -*- coding: utf-8 -*-
"""
章节生成Prompt - 用于生成章节正文和摘要
迁移自 AI_NovelGenerator
"""

# =============== 章节摘要生成提示词 ===================
summarize_recent_chapters_prompt = """\
作为一名专业的小说编辑和知识管理专家，正在基于已完成的前三章内容和本章信息生成当前章节的精准摘要。请严格遵循以下工作流程：

前三章内容：
{combined_text}

当前章节信息：
第{novel_number}章《{chapter_title}》：
├── 本章定位：{chapter_role}
├── 核心作用：{chapter_purpose}
├── 悬念密度：{suspense_level}
├── 伏笔操作：{foreshadowing}
├── 认知颠覆：{plot_twist_level}
└── 本章简述：{chapter_summary}

下一章信息：
第{next_chapter_number}章《{next_chapter_title}》：
├── 本章定位：{next_chapter_role}
├── 核心作用：{next_chapter_purpose}
├── 悬念密度：{next_chapter_suspense_level}
├── 伏笔操作：{next_chapter_foreshadowing}
├── 认知颠覆：{next_chapter_plot_twist_level}
└── 本章简述：{next_chapter_summary}

【上下文分析阶段】
1. 回顾前三章核心内容：
   - 第一章核心要素：[章节标题]→[核心冲突/理论]→[关键人物/概念]
   - 第二章发展路径：[已建立的人物关系]→[技术/情节进展]→[遗留伏笔]
   - 第三章转折点：[新出现的变量]→[世界观扩展]→[待解决问题]

2. 提取延续性要素：
   - 必继承要素：列出前3章中必须延续的3个核心设定
   - 可调整要素：识别2个允许适度变化的辅助设定

【当前章节摘要生成规则】
1. 内容架构：
   - 继承权重：70%内容需与前3章形成逻辑递进
   - 创新空间：30%内容可引入新要素，但需标注创新类型

2. 结构控制：
   - 采用"承继→发展→铺垫"三段式结构
   - 每段含1个前文呼应点+1个新进展

3. 预警机制：
   - 若检测到与前3章设定冲突，用[!]标记并说明
   - 对开放式发展路径，提供2种合理演化方向

现在请你基于目前故事的进展，用最多800字，写一个简洁明了的「当前章节摘要」。

请按如下格式输出（不需要额外解释）：
当前章节摘要: <这里写当前章节摘要>
"""

# =============== 第一章草稿提示 ===================
first_chapter_draft_prompt = """\
即将创作：第 {novel_number} 章《{chapter_title}》

【本章定位】
- 章节角色：{chapter_role}
- 核心作用：{chapter_purpose}
- 悬念密度：{suspense_level}
- 伏笔操作：{foreshadowing}
- 认知颠覆：{plot_twist_level}
- 本章简述：{chapter_summary}

【可用元素】
- 核心人物：{characters_involved}
- 关键道具：{key_items}
- 空间坐标：{scene_location}
- 时间压力：{time_constraint}

【参考文档】
小说设定：
{novel_setting}

【创作要求】
完成第 {novel_number} 章的正文，字数要求 {word_number} 字。

至少设计2个或以上具有动态张力的场景：

1. **对话场景**：
   - 潜台词冲突（表面谈论A，实际博弈B）
   - 权力关系变化（通过非对称对话长度体现）

2. **动作场景**：
   - 环境交互细节（至少3个感官描写）
   - 节奏控制（短句加速+比喻减速）
   - 动作揭示人物隐藏特质

3. **心理场景**：
   - 认知失调的具体表现（行为矛盾）
   - 隐喻系统的运用（连接世界观符号）
   - 决策前的价值天平描写

4. **环境场景**：
   - 空间透视变化（宏观→微观→异常焦点）
   - 非常规感官组合（如"听见阳光的重量"）
   - 动态环境反映心理（环境与人物心理对应）

【格式要求】
- 仅返回章节正文文本
- 不使用分章节小标题
- 不要使用markdown格式
- 确保内容与小说设定一致

【额外指导】
{user_guidance}
"""

# =============== 后续章节草稿提示 ===================
next_chapter_draft_prompt = """\
【参考文档】
├── 前文摘要：
│   {global_summary}
│
├── 前章结尾段：
│   {previous_chapter_excerpt}
│
├── 用户指导：
│   {user_guidance}
│
├── 角色状态：
│   {character_state}
│
├── 当前章节摘要：
│   {short_summary}
│
└── 结构化历史上下文：
    {memory_context}

【当前章节信息】
第{novel_number}章《{chapter_title}》：
├── 章节定位：{chapter_role}
├── 核心作用：{chapter_purpose}
├── 悬念密度：{suspense_level}
├── 伏笔设计：{foreshadowing}
├── 转折程度：{plot_twist_level}
├── 章节简述：{chapter_summary}
├── 字数要求：{word_number}字
├── 核心人物：{characters_involved}
├── 关键道具：{key_items}
├── 场景地点：{scene_location}
└── 时间压力：{time_constraint}

【下一章预告】
第{next_chapter_number}章《{next_chapter_title}》：
├── 章节定位：{next_chapter_role}
├── 核心作用：{next_chapter_purpose}
├── 悬念密度：{next_chapter_suspense_level}
└── 章节简述：{next_chapter_summary}

【知识库参考】
{filtered_context}

【本章写作计划】（必须严格遵循）
{chapter_plan}

【知识库应用规则】
1. 内容分级：
   - 写作技法类（优先）：场景构建模板、对话技巧、悬念手法
   - 设定资料类（选择性）：独特世界观、未使用技术细节
   - 禁忌项类（必须规避）：已出现的情节、重复的关系发展

2. 使用限制：
   ● 禁止直接复制已有章节的情节模式
   ● 历史章节内容仅允许：
     → 参照叙事节奏（不超过20%相似度）
     → 延续必要的人物反应模式（需改编30%以上）

3. 冲突检测：
   ⚠️ 若检测到与历史章节重复：
     - 相似度>40%：必须重构叙事角度
     - 相似度20-40%：替换至少3个关键要素
     - 相似度<20%：允许保留核心概念但改变表现形式

【创作要求】
依据前面所有设定，开始完成第 {novel_number} 章的正文，字数要求 {word_number} 字。

内容生成严格遵循：
- 用户指导
- 当前章节摘要
- 当前章节信息
- 无逻辑漏洞
- 确保章节内容与前文摘要、前章结尾段衔接流畅
- 保证上下文完整性

【格式要求】
- 仅返回章节正文文本
- 不使用分章节小标题
- 不要使用markdown格式
"""
