# 🔍 问题分析与解决方案

## 📋 问题总结

### 问题 1: 生成大纲功能是否存在？

**答案**: ✅ **功能存在**

后端已实现 `generate_chapter_outline` 方法，位于 `backend/core/novel_engine_qianfan.py` 第 389 行。

**实现逻辑**:
1. 获取小说项目
2. 使用千帆 API 生成章节大纲
3. 解析 JSON 格式的大纲数据
4. 返回章节大纲列表

**可能的问题**:
- ❌ 前端调用 API 后没有正确显示结果
- ❌ 后端数据存储在内存中，重启后丢失
- ❌ API 响应格式不匹配

---

### 问题 2: 切换页面后内容丢失

**根本原因**: 

#### A. 后端数据存储在内存中
```python
# backend/core/novel_engine_qianfan.py 第 138 行
class NovelEngine:
    def __init__(self, llm_config: Dict, embedding_config: Dict = None):
        # 项目存储 - 存储在内存中
        self.projects: Dict[str, NovelProject] = {}
```

**影响**:
- ⚠️ Railway 服务重启后，所有数据丢失
- ⚠️ 每次部署都会清空数据
- ⚠️ 无法持久化保存

#### B. 前端状态管理问题
- Streamlit 的 `session_state` 在切换页面时会重置
- 没有持久化存储机制

---

### 问题 3: 数据库存储

**当前状态**: ❌ **没有数据库**

后端使用 **内存存储** (`self.projects = {}`)，存在以下问题：
- 重启服务后数据丢失
- 无法持久化保存
- 不支持多用户
- 不支持数据备份

---

## 🔧 解决方案

### 方案 1: 添加数据库持久化（推荐）

#### 选项 A: SQLite（轻量级，适合单用户）

**优点**:
- 无需额外服务
- 部署简单
- 数据持久化
- 适合 Railway

**实现步骤**:

1. **创建数据库模型**

```python
# backend/database/models.py
from sqlalchemy import Column, String, Integer, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class NovelProjectDB(Base):
    __tablename__ = "novel_projects"
    
    novel_id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    topic = Column(Text)
    theme = Column(Text)
    total_chapters = Column(Integer, default=10)
    target_word_count = Column(Integer, default=3000)
    status = Column(String, default="draft")
    blueprint = Column(JSON)  # 存储蓝图 JSON
    chapter_outlines = Column(JSON)  # 存储大纲 JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

2. **添加数据库配置**

```python
# backend/database/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./novels.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
```

3. **修改引擎使用数据库**

```python
# backend/core/novel_engine_qianfan.py
from database.database import SessionLocal
from database.models import NovelProjectDB

class NovelEngine:
    def __init__(self, llm_config: Dict, embedding_config: Dict = None):
        self.llm = LLMAdapter(llm_config)
        # 不再使用内存存储
        # self.projects: Dict[str, NovelProject] = {}
        
    async def create_project(self, config: Dict) -> NovelProject:
        db = SessionLocal()
        try:
            # 保存到数据库
            db_project = NovelProjectDB(**config)
            db.add(db_project)
            db.commit()
            db.refresh(db_project)
            return NovelProject.from_orm(db_project)
        finally:
            db.close()
```

---

#### 选项 B: PostgreSQL（推荐用于生产环境）

**优点**:
- 支持多用户
- 高性能
- Railway 原生支持
- 数据可靠

**Railway 配置**:
1. 在 Railway 添加 PostgreSQL 服务
2. 获取 `DATABASE_URL` 环境变量
3. 数据库自动创建和管理

---

### 方案 2: JSON 文件存储（快速方案）

**优点**:
- 无需数据库
- 实现简单
- 数据持久化

**缺点**:
- 不适合高并发
- 无事务支持

**实现步骤**:

```python
# backend/utils/file_storage.py
import json
from pathlib import Path
from typing import Dict, Any

class FileStorage:
    def __init__(self, storage_dir: str = "data"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
    
    def save_project(self, novel_id: str, data: Dict[Any, Any]):
        file_path = self.storage_dir / f"{novel_id}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_project(self, novel_id: str) -> Dict[Any, Any]:
        file_path = self.storage_dir / f"{novel_id}.json"
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def list_projects(self):
        return [f.stem for f in self.storage_dir.glob("*.json")]
```

---

### 方案 3: 修复前端状态管理

**问题**: Streamlit 切换页面时 `session_state` 重置

**解决方案**: 使用 URL 参数或数据库持久化

```python
# frontend/pages/2_✍️_小说创作.py
import streamlit as st
from utils.api import api_client

# 从 URL 参数获取小说 ID
query_params = st.query_params
novel_id_from_url = query_params.get("novel_id")

if novel_id_from_url:
    # 从后端 API 获取小说详情
    novel_detail = api_client.get_novel(novel_id_from_url)
    if novel_detail.get("success"):
        st.session_state.current_novel = novel_detail.get("data")
```

---

## 📊 推荐方案

### 短期方案（快速修复）

1. **添加 JSON 文件存储** - 让数据持久化
2. **修复前端调用** - 确保大纲生成后正确显示
3. **添加错误处理** - 提供友好的错误提示

### 长期方案（推荐）

1. **使用 PostgreSQL 数据库** - Railway 原生支持
2. **实现用户系统** - 支持多用户
3. **添加数据备份** - 定期备份数据库

---

## 🚀 立即可执行的修复

我可以帮你：

1. **添加 SQLite 数据库支持** - 30分钟内完成
2. **修复大纲生成显示问题** - 检查 API 调用逻辑
3. **添加数据持久化** - 确保数据不会丢失

你想让我先做哪一个？
