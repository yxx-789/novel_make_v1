# JSON 格式错误修复说明

## 修复时间
2026-05-09 17:55 GMT+8

## 问题描述

### 症状
- ✅ 生成蓝图成功
- ❌ 生成大纲卡在"正在解析 AI 生成的内容"（80%进度）
- ❌ 没有错误提示
- ❌ 前端显示"生成成功"，但没有内容

### 根本原因

**AI 生成的 JSON 格式错误**：

**错误格式**（AI实际输出）：
```json
{
  "rising_actions": [
    0: "转折点1...",  ← 错误！带索引号
    1: "转折点2...",
    2: "转折点3..."
  ]
}
```

**正确格式**（应该是）：
```json
{
  "rising_actions": [
    "转折点1...",  ← 正确！
    "转折点2...",
    "转折点3..."
  ]
}
```

### 问题链

1. **蓝图生成** → AI 输出错误格式的 JSON（带索引号）
2. **保存到数据库** → 错误格式被保存
3. **生成大纲** → AI 学习错误格式，也输出错误 JSON
4. **后端解析** → `json.loads()` 失败
5. **返回空列表** → 前端显示"成功"，但没有内容

---

## 修复方案

### 1. 修改提示词，明确禁止索引号

**文件**: `backend/core/novel_engine_qianfan.py`

**蓝图生成提示词**：
```python
【输出要求】
请以JSON格式输出，确保每个字段都有足够的细节和字数。

**重要提示：数组中的元素不要添加索引号！**

格式示例：
{
    "rising_actions": [
        "转折点1的300字详细描述...",
        "转折点2的300字详细描述...",
        "转折点3的300字详细描述..."
    ],
    ...
}
```

**大纲生成提示词**：
```python
【输出格式要求】
请以JSON格式输出，确保每个章节都有足够的细节和吸引力。

**重要提示：数组中的元素不要添加索引号！**

格式示例：
{
    "chapters": [
        {
            "key_events": [
                "事件1的50-100字详细描述",
                "事件2的50-100字详细描述"
            ]
        }
    ]
}
```

---

### 2. 创建 JSON 工具函数

**文件**: `backend/utils/json_utils.py`

**功能**：
- 清理 JSON 字符串中的不规范格式
- 移除数组中的索引号
- 处理尾随逗号
- 多重解析尝试（标准解析 → 清理解析 → 正则提取）

**核心函数**：
```python
def clean_json_string(json_str: str) -> str:
    """清理 JSON 字符串中的不规范格式"""
    # 移除数组中的索引号
    json_str = re.sub(r'(\d+)\s*:\s*"', '"', json_str)
    # 移除尾随逗号
    json_str = re.sub(r',\s*([}\]])', r'\1', json_str)
    return json_str

def parse_ai_json(text: str) -> Dict[str, Any]:
    """解析 AI 生成的 JSON，处理不规范格式"""
    # 多重尝试解析
    ...
```

---

### 3. 修改后端代码使用新的 JSON 解析工具

**蓝图生成**：
```python
# 旧代码
try:
    json_match = re.search(r'\{[\s\S]*\}', result)
    if json_match:
        data = json.loads(json_match.group())
except:
    data = {}

# 新代码
from utils.json_utils import parse_ai_json
data = parse_ai_json(result)
```

**大纲生成**：
```python
# 旧代码
try:
    json_match = re.search(r'\{[\s\S]*\}', result)
    if json_match:
        data = json.loads(json_match.group())
        chapters_data = data.get("chapters", [])
except:
    chapters_data = []

# 新代码
from utils.json_utils import parse_ai_json
data = parse_ai_json(result)
chapters_data = data.get("chapters", [])
```

---

## 修改的文件

1. **backend/core/novel_engine_qianfan.py**
   - 修改蓝图生成提示词（第 380 行附近）
   - 修改大纲生成提示词（第 480 行附近）
   - 修改蓝图生成 JSON 解析（第 370 行附近）
   - 修改大纲生成 JSON 解析（第 510 行附近）

2. **backend/utils/json_utils.py**（新建）
   - 创建 JSON 工具函数
   - 处理不规范的 JSON 格式

---

## 测试方法

### 测试 1: 测试 JSON 工具函数

```bash
cd novel_make_v1

# 测试 JSON 工具
python3 backend/utils/json_utils.py
```

**预期输出**：
```
=== 测试 1 ===
输入: {"rising_actions": [0: "转折点1", 1: "转折点2"]}
输出: {"rising_actions": ["转折点1", "转折点2"]}
```

### 测试 2: 测试生成大纲

1. 推送代码到 Railway
2. 访问前端页面
3. 创建小说项目
4. 生成蓝图
5. 生成大纲
6. 验证大纲内容是否正常显示

---

## 推送命令

```bash
cd novel_make_v1

# 查看修改
git status
git diff backend/core/novel_engine_qianfan.py

# 推送代码
git add backend/core/novel_engine_qianfan.py
git add backend/utils/json_utils.py
git commit -m "Fix: Handle AI-generated JSON with array indices"
git push origin main
```

---

## 预期效果

修复后：
- ✅ AI 生成的 JSON 格式正确
- ✅ 后端能够正确解析 JSON
- ✅ 生成大纲成功返回内容
- ✅ 前端显示大纲内容

---

## 注意事项

1. **AI 仍可能生成错误格式**：
   - 即使修改了提示词，AI 仍可能偶尔生成带索引号的 JSON
   - 新的 JSON 工具函数会自动清理这些问题

2. **向后兼容**：
   - 新的解析方法可以处理标准 JSON
   - 也可以处理带索引号的 JSON
   - 不会影响现有功能

3. **错误处理**：
   - 如果解析失败，返回空字典
   - 不会导致程序崩溃
   - 用户会看到"待生成"的默认值