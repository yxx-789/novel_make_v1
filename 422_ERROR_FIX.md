# 🐛 422 错误分析与修复

## 问题根源

**错误信息**: `422 Client Error: Unprocessable Entity`

**API 端点**: `POST /api/v1/novels/{novel_id}/chapters/{chapter_num}/generate`

---

## 根本原因

### 问题 1: 请求模型定义不匹配

**后端模型定义** (`backend/models/schemas.py` 第 252 行):

```python
class GenerateChapterRequest(BaseModel):
    """生成章节请求"""
    novel_id: str           # ❌ 问题：这个字段不应该在请求体中
    chapter_num: int        # ❌ 问题：这个字段不应该在请求体中
    additional_guidance: Optional[str] = None
    use_memory: bool = Field(default=True)
```

**后端路由定义** (`backend/api/routes.py` 第 226 行):

```python
@app.post("/api/v1/novels/{novel_id}/chapters/{chapter_num}/generate")
async def generate_chapter(
    novel_id: str,  # ✅ 从 URL 路径获取
    chapter_num: int,  # ✅ 从 URL 路径获取
    request: GenerateChapterRequest = None  # ❌ 问题：模型要求 novel_id 和 chapter_num
):
```

**冲突点**:
- `novel_id` 和 `chapter_num` 已经通过 URL 路径传递
- 但 `GenerateChapterRequest` 模型要求这两个字段必须出现在请求体中
- FastAPI 验证失败 → 422 错误

---

### 问题 2: 前端发送的请求体

**前端代码** (`frontend/utils/api.py` 第 189 行):

```python
def generate_chapter(self, novel_id: str, chapter_num: int, ...):
    data = {}
    if additional_guidance:
        data["additional_guidance"] = additional_guidance
    if use_memory is not None:
        data["use_memory"] = use_memory

    return self._request(
        "POST",
        f"/api/v1/novels/{novel_id}/chapters/{chapter_num}/generate",
        json=data if data else None  # ❌ 如果 data 为空，发送 None
    )
```

**问题**:
- 当用户没有填写 `additional_guidance` 时，`data = {}`
- 前端发送 `json=None`，即空请求体
- 但后端模型要求 `novel_id` 和 `chapter_num` 必须存在
- FastAPI 验证失败 → 422 错误

---

## 修复方案

### 方案 1: 修改请求模型（推荐）

**修改 `backend/models/schemas.py`**:

```python
class GenerateChapterRequest(BaseModel):
    """生成章节请求"""
    # ❌ 移除这两个字段（它们已经在 URL 中）
    # novel_id: str
    # chapter_num: int

    additional_guidance: Optional[str] = None
    use_memory: bool = Field(default=True)
```

**优点**:
- ✅ 符合 RESTful 设计
- ✅ 请求体只包含可选参数
- ✅ 前端无需修改

---

### 方案 2: 修改后端路由

**修改 `backend/api/routes.py`**:

```python
from pydantic import BaseModel
from typing import Optional

class ChapterGenerateBody(BaseModel):
    """章节生成请求体"""
    additional_guidance: Optional[str] = None
    use_memory: bool = True

@app.post("/api/v1/novels/{novel_id}/chapters/{chapter_num}/generate")
async def generate_chapter(
    novel_id: str,
    chapter_num: int,
    body: ChapterGenerateBody = None  # 使用新的请求体模型
):
    guidance = body.additional_guidance if body else None
    use_memory = body.use_memory if body else True

    # ...
```

---

### 方案 3: 修改前端请求

**修改 `frontend/utils/api.py`**:

```python
def generate_chapter(self, novel_id: str, chapter_num: int, ...):
    data = {
        "novel_id": novel_id,      # 添加到请求体
        "chapter_num": chapter_num  # 添加到请求体
    }
    if additional_guidance:
        data["additional_guidance"] = additional_guidance
    if use_memory is not None:
        data["use_memory"] = use_memory

    return self._request(
        "POST",
        f"/api/v1/novels/{novel_id}/chapters/{chapter_num}/generate",
        json=data  # 总是发送请求体
    )
```

**缺点**:
- ❌ URL 和请求体中都包含相同参数，冗余
- ❌ 不符合 RESTful 设计

---

## 推荐修复

**使用方案 1**：修改请求模型，移除 URL 中已经包含的字段。

这是最符合 RESTful 设计的方案，且无需修改前端代码。

---

## 其他潜在问题

### 问题 3: 数据存储问题

即使修复了 422 错误，生成的章节内容也无法持久化保存：

```python
class NovelEngine:
    def __init__(self, ...):
        self.projects: Dict[str, NovelProject] = {}  # 内存存储
```

**影响**:
- Railway 重启后数据丢失
- 切换页面后数据丢失

**解决方案**: 添加数据库持久化

---

## 立即修复

我可以立即：

1. **修复 422 错误** - 修改请求模型（5分钟）
2. **添加数据库** - SQLite 持久化存储（30分钟）
3. **测试验证** - 确保章节生成功能正常工作

是否开始修复？
