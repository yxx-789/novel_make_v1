# AI_NovelGenerator 架构迁移计划

## 📊 当前状态分析

### 原始 AI_NovelGenerator 架构

```
阶段1：架构期（Architecture）
├── core_seed_prompt (核心种子)
├── character_dynamics_prompt (角色动力学)
├── world_building_prompt (世界构建)
├── plot_architecture_prompt (情节架构)
└── create_character_state_prompt (角色状态初始化)

阶段2：蓝图期（Blueprint）
├── chapter_blueprint_prompt (章节目录)
└── chunked_chapter_blueprint_prompt (分块章节目录)

阶段3：规划期（Planning）
└── chapter_plan_prompt (章节规划)

阶段4：写作期（Writing）
├── first_chapter_draft_prompt (第一章草稿)
├── subsequent_chapter_draft_prompt (后续章节草稿)
└── summarize_recent_chapters_prompt (章节摘要)
```

### 当前 NOVEL_PLATFORM 架构

```
简化版架构：
├── generate_blueprint (蓝图生成) - 太简单
├── generate_chapter_outline (大纲生成) - 太简单
└── generate_chapter (章节生成) - 缺少架构支持
```

---

## 🎯 迁移目标

### 完整迁移 5 个核心模块

#### 1. 架构生成模块 (Architecture Generator)

**功能：**
- 核心种子生成（雪花写作法）
- 角色动力学设定（角色弧光模型）
- 世界观构建（三维交织法）
- 情节架构（三幕式悬念）
- 角色状态初始化

**输出文件：**
- `Novel_architecture.txt` - 完整架构文档
- `character_state.txt` - 角色状态表

#### 2. 蓝图生成模块 (Blueprint Generator)

**改进内容：**
- 悬念节奏曲线设计
- 章节集群划分（3-5章一个悬念单元）
- 伏笔操作规划（埋设/强化/回收）
- 认知颠覆强度评级（1-5星）
- 分块生成支持（长篇小说）

**输出文件：**
- `Novel_directory.txt` - 详细章节蓝图

#### 3. 章节规划模块 (Chapter Planner)

**新增功能：**
- 场景级规划（3-5个场景/章）
- 核心冲突设计
- 角色发展路径
- 伏笔管理
- 约束检查

**输出格式：**
- JSON 格式的详细规划

#### 4. 章节生成模块 (Chapter Generator)

**改进内容：**
- 结合架构信息生成
- 多场景设计（对话/动作/心理/环境）
- 动态张力场景
- 感官描写
- 节奏控制

#### 5. 记忆系统 (Memory System)

**已实现功能：**
- 角色状态追踪
- 时间线管理
- 伏笔追踪
- 一致性检查

---

## 📋 迁移步骤

### Phase 1：创建 Prompts 文件结构

```
backend/prompts/
├── __init__.py
├── architecture_prompts.py (核心种子、角色动力学、世界观、情节架构)
├── blueprint_prompts.py (章节蓝图)
├── planning_prompts.py (章节规划)
└── chapter_prompts.py (章节生成)
```

### Phase 2：创建架构生成器

```
backend/core/
├── architecture_generator.py (架构生成主逻辑)
└── novel_engine_qianfan.py (修改，集成架构生成)
```

### Phase 3：改进蓝图生成器

```
backend/core/
└── blueprint_generator.py (改进蓝图生成逻辑)
```

### Phase 4：创建章节规划器

```
backend/core/
└── chapter_planner.py (新增规划模块)
```

### Phase 5：改进章节生成

```
backend/core/
└── novel_engine_qianfan.py (改进章节生成逻辑)
```

---

## 🔄 迁移优先级

### 高优先级（必须立即迁移）

1. ✅ **架构生成** - 这是基础，必须首先迁移
   - 核心种子
   - 角色动力学
   - 世界观构建
   - 情节架构

2. ✅ **蓝图生成改进** - 影响后续所有环节
   - 悬念节奏曲线
   - 伏笔操作
   - 认知颠覆

3. ✅ **章节规划** - 提升生成质量
   - 场景级规划
   - 冲突设计

### 中优先级（逐步完善）

4. ⚠️ **章节生成改进** - 结合架构信息
5. ⚠️ **角色状态管理** - 已有基础

### 低优先级（优化改进）

6. ⏸️ **记忆系统优化** - 已有基础
7. ⏸️ **一致性检查优化** - 已有基础

---

## 📊 预期效果对比

### 蓝图生成字数对比

| 项目 | 当前实现 | 迁移后 |
|------|---------|--------|
| 核心冲突 | 200-300字 | **完整的三幕式架构** |
| 角色设定 | ❌ 缺失 | **3-6个详细角色卡** |
| 世界观 | ❌ 缺失 | **三维交织世界观** |
| 情节架构 | ❌ 缺失 | **完整三幕式设计** |
| 章节蓝图 | 简单列表 | **悬念节奏曲线** |

### 章节质量对比

| 项目 | 当前实现 | 迁移后 |
|------|---------|--------|
| 场景设计 | 单一场景 | **3-5个动态场景** |
| 冲突设计 | 随机 | **精心设计的核心冲突** |
| 伏笔管理 | ❌ 无 | **完整的伏笔系统** |
| 一致性检查 | ⚠️ 基础 | **基于架构的严格检查** |

---

## ⏱️ 预计工作量

- **Phase 1** (Prompts): 2-3小时
- **Phase 2** (架构生成器): 3-4小时
- **Phase 3** (蓝图改进): 2-3小时
- **Phase 4** (章节规划): 2-3小时
- **Phase 5** (章节生成): 2-3小时
- **测试和调试**: 3-4小时

**总计**: 约 14-20 小时

---

## 🚀 下一步行动

**立即开始 Phase 1：创建 Prompts 文件结构**

迁移顺序：
1. architecture_prompts.py
2. blueprint_prompts.py
3. planning_prompts.py
4. chapter_prompts.py

然后继续 Phase 2-5 的实现。
