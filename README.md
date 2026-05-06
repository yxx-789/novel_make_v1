# 🎨 AI 小说创作平台

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.24%2B-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

**一个基于AI的小说创作与剧本转换平台**

[在线演示](#) | [快速开始](#-快速开始) | [部署指南](#-部署到-streamlit-cloud)

</div>

---

## 📖 项目简介

AI小说创作平台是一个前后端分离的Web应用，支持：

- ✨ **AI小说创作**：自动生成世界观、角色、情节蓝图
- 📚 **智能章节生成**：AI生成章节大纲和内容
- 🎬 **剧本转换**：将小说转换为短视频剧本
- 💬 **AI聊天助手**：智能对话辅助创作
- 📊 **小说管理**：查看、搜索、导出小说

---

## 🎯 核心功能

### 1️⃣ 小说创作流程

```
创建小说 → 生成蓝图 → 生成大纲 → 生成章节 → 导出小说
```

**详细说明**：

- **蓝图生成**：世界观设定、角色档案、情节蓝图
- **大纲生成**：自动生成章节大纲（标题、摘要、关键事件）
- **章节生成**：AI根据大纲生成完整章节内容（3000字/章）
- **导出功能**：支持Markdown、TXT、Word格式

### 2️⃣ 剧本转换

将小说转换为短视频剧本格式：

- 📹 场景分解（地点、时间）
- 🎬 镜头脚本（远景、中景、特写）
- ⏱️ 时长估算
- 🎨 视觉描述

### 3️⃣ 小说管理

- 📋 小说列表查看
- 🔍 搜索和筛选
- 📊 创作进度追踪
- 📥 导出和备份

---

## 🛠️ 技术栈

### 后端

- **框架**: FastAPI 0.104+
- **AI集成**: OpenAI API / DeepSeek API
- **数据存储**: 内存存储（可扩展为数据库）
- **API文档**: 自动生成Swagger文档

### 前端

- **框架**: Streamlit 1.24+
- **架构**: 多页面应用
- **UI设计**: 响应式布局、Material Design风格

---

## 📦 项目结构

```
novel_make_v1/
├── backend/                 # FastAPI后端
│   ├── api/                # API路由
│   │   └── routes.py       # 主要API端点
│   ├── core/               # 核心引擎
│   │   ├── novel_engine.py # 小说生成引擎
│   │   └── drama_engine.py # 剧本转换引擎
│   ├── models/             # 数据模型
│   │   └── schemas.py      # Pydantic模型
│   ├── main.py             # 应用入口
│   ├── mock_api.py         # 模拟API（测试用）
│   └── requirements.txt    # Python依赖
│
├── frontend/               # Streamlit前端
│   ├── pages/              # 功能页面
│   │   ├── 1_🏠_首页.py
│   │   ├── 2_✍️_小说创作.py
│   │   ├── 3_📚_小说管理.py
│   │   ├── 4_🎬_剧本转换.py
│   │   ├── 5_💬_AI聊天.py
│   │   └── 6_⚙️_系统设置.py
│   ├── utils/              # 工具模块
│   │   ├── api.py          # API客户端
│   │   └── config.py       # 配置管理
│   ├── .streamlit/         # Streamlit配置
│   │   └── config.toml
│   ├── app.py              # 主应用
│   └── requirements.txt    # Python依赖
│
├── start.sh                # 一键启动脚本
├── stop.sh                 # 停止脚本
├── README.md               # 项目说明
└── STREAMLIT_DEPLOY.md     # Streamlit部署指南
```

---

## 🚀 快速开始

### 前提条件

- Python 3.10 或更高版本
- pip 包管理器
- OpenAI API Key 或其他AI服务密钥

### 安装步骤

#### 1. 克隆仓库

```bash
git clone https://github.com/yxx-789/novel_make_v1.git
cd novel_make_v1
```

#### 2. 配置环境变量

```bash
# 进入后端目录
cd backend

# 复制示例配置
cp .env.example .env

# 编辑配置文件
nano .env
```

**配置示例**：

```bash
# AI模型配置
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=4096

# API服务配置
API_HOST=0.0.0.0
API_PORT=8000
```

#### 3. 安装依赖

```bash
# 安装后端依赖
pip install -r backend/requirements.txt

# 安装前端依赖
pip install -r frontend/requirements.txt
```

#### 4. 启动服务

**方式一：一键启动**

```bash
./start.sh
```

**方式二：分别启动**

```bash
# 终端1：启动后端
cd backend
python main.py

# 终端2：启动前端
cd frontend
streamlit run app.py
```

#### 5. 访问应用

- 🌐 **前端界面**: http://localhost:8501
- 📚 **API文档**: http://localhost:8000/docs
- 🏥 **健康检查**: http://localhost:8000/health

---

## 📱 使用指南

### 第一步：配置系统

1. 访问 **⚙️ 系统设置** 页面
2. 检查API地址（默认：http://localhost:8000）
3. 点击 **"测试连接"** 确认后端正常

### 第二步：创作小说

1. 进入 **✍️ 小说创作** 页面
2. 填写小说信息：
   - 标题、类型、故事梗概
   - 写作风格（可选）
   - 章节数、每章字数
3. 点击 **"创建小说"**

### 第三步：生成内容

**按顺序执行**：

1. **生成蓝图** → 世界观、角色、情节（20-40秒）
2. **生成大纲** → 章节标题和摘要（30-50秒）
3. **生成章节** → 完整章节内容（30-60秒/章）

### 第四步：管理和导出

- 在 **📚 小说管理** 页面查看所有小说
- 支持搜索、筛选、导出（Markdown格式）

---

## 🌐 部署到 Streamlit Cloud

### 快速部署（推荐）

详细步骤请查看：[STREAMLIT_DEPLOY.md](./STREAMLIT_DEPLOY.md)

**简要步骤**：

1. 登录 [Streamlit Cloud](https://streamlit.io/cloud)
2. 创建新应用：
   - Repository: `yxx-789/novel_make_v1`
   - Branch: `main`
   - Main file: `frontend/app.py`
3. 配置环境变量：
   ```
   API_BASE_URL = https://your-backend-api.com
   OPENAI_API_KEY = sk-your-api-key
   ```
4. 点击 **Deploy**

**注意**：Streamlit Cloud只能部署前端，后端需要单独部署到云服务器。

### 后端部署建议

- [Railway](https://railway.app/) - 简单易用
- [Render](https://render.com/) - 免费套餐
- [Fly.io](https://fly.io/) - 全球CDN

---

## 🔧 API 端点

| 端点 | 方法 | 描述 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/api/v1/novels` | POST | 创建小说 |
| `/api/v1/novels` | GET | 获取小说列表 |
| `/api/v1/novels/{id}` | GET | 获取小说详情 |
| `/api/v1/novels/{id}/blueprint` | POST | 生成蓝图 |
| `/api/v1/novels/{id}/outline` | POST | 生成大纲 |
| `/api/v1/novels/{id}/chapters/{num}/generate` | POST | 生成章节 |
| `/api/v1/novels/{id}/export` | GET | 导出小说 |
| `/api/v1/drama/convert` | POST | 剧本转换 |

完整API文档：http://localhost:8000/docs

---

## 🧪 测试

### 测试API

```bash
# 健康检查
curl http://localhost:8000/health

# 创建小说
curl -X POST http://localhost:8000/api/v1/novels \
  -H "Content-Type: application/json" \
  -d '{
    "title": "测试小说",
    "genre": "玄幻",
    "topic": "一个修仙故事",
    "total_chapters": 10
  }'
```

### 模拟API（无需真实API Key）

```bash
# 使用模拟后端
cd backend
python mock_api.py
```

---

## 🐛 常见问题

### Q1: 前端无法连接后端？

**解决**：
1. 确认后端已启动
2. 检查 `frontend/utils/config.py` 中的API地址
3. 在系统设置页面测试连接

### Q2: AI生成失败？

**解决**：
1. 检查API Key是否正确
2. 确认网络连接正常
3. 查看后端日志：`tail -f logs/backend.log`

### Q3: 部署到Streamlit Cloud后API连接失败？

**解决**：
1. 后端需要单独部署到云服务器
2. 在Streamlit Cloud设置环境变量 `API_BASE_URL`
3. 确保后端API支持跨域（CORS）

---

## 📈 性能优化

### 缓存优化

```python
from utils.api import api_client

@st.cache_data(ttl=3600)
def get_novels():
    return api_client.get_novels()
```

### 异步处理

```python
import asyncio

async def generate_content():
    result = await api_client.generate_blueprint(novel_id)
    return result
```

---

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

---

## 📞 联系方式

- 📧 Email: xingyao@baidu.com
- 💬 GitHub Issues: [提交问题](https://github.com/yxx-789/novel_make_v1/issues)

---

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的Web框架
- [Streamlit](https://streamlit.io/) - 优秀的数据应用框架
- [OpenAI](https://openai.com/) - 强大的AI能力

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给一个Star！⭐**

Made with ❤️ by [yxx-789](https://github.com/yxx-789)

</div>
