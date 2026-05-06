# AI 小说创作平台 - 完整部署包

## 📋 项目说明

本项目是一个完整的 AI 小说创作平台，包括：
- **后端**: FastAPI + Baidu Qianfan AI 模型
- **前端**: Streamlit 多页面应用

---

## 🚀 快速启动

### 方式一：一键启动（推荐）

```bash
# 1. 解压项目
tar -xzf novel_platform_complete.tar.gz
cd novel_platform_complete

# 2. 安装后端依赖
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的 API Key

# 4. 安装前端依赖
cd ../frontend
pip install -r requirements.txt

# 5. 启动服务
cd ..
./start.sh  # Linux/Mac
# 或 start.bat  # Windows
```

### 方式二：分别启动

**启动后端：**
```bash
cd backend
source .venv/bin/activate
python main.py
```

**启动前端：**
```bash
cd frontend
streamlit run app.py
```

---

## 📁 项目结构

```
novel_platform_complete/
├── backend/                 # 后端代码
│   ├── api/                 # API 路由
│   ├── core/                # 核心引擎
│   ├── models/              # 数据模型
│   ├── utils/               # 工具函数
│   ├── main.py              # 主入口
│   ├── requirements.txt     # 后端依赖
│   └── .env.example         # 环境变量示例
│
├── frontend/                # 前端代码
│   ├── pages/               # 页面文件
│   ├── utils/               # 工具模块
│   ├── app.py               # 主入口
│   └── requirements.txt     # 前端依赖
│
├── start.sh                 # 一键启动脚本 (Linux/Mac)
├── start.bat                # 一键启动脚本 (Windows)
└── README.md                # 本文档
```

---

## 🔧 配置说明

### 后端配置 (backend/.env)

```bash
# AI 模型配置
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini

# API 服务配置
API_HOST=0.0.0.0
API_PORT=8000
```

### 前端配置

前端会自动连接到 `http://localhost:8000`，如需修改：
- 访问前端页面：http://localhost:8501
- 进入"⚙️ 系统设置"页面
- 修改 API 地址

---

## 📚 功能说明

### 1. 🏠 首页
- 系统状态监控
- 快速开始指南

### 2. ✍️ 小说创作
- 创建小说项目
- 生成故事蓝图
- 生成章节大纲
- 生成章节内容

### 3. 📚 小说管理
- 查看所有小说
- 搜索和筛选
- 查看详情
- 删除小说

### 4. 🎬 剧本转换
- 将小说转换为剧本格式
- 支持电影、电视剧、舞台剧、短视频格式

### 5. 💬 AI 聊天
- 与 AI 助手聊天
- 获取创作建议

### 6. ⚙️ 系统设置
- 配置 API 地址
- 测试连接
- 查看可用模型

---

## 🔌 API 文档

启动后端后，访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## ❓ 常见问题

### 1. 前端无法连接后端
- 检查后端是否启动：访问 http://localhost:8000/health
- 检查防火墙设置
- 在前端"系统设置"页面修改 API 地址

### 2. 创建小说失败
- 检查 API Key 是否正确
- 查看后端日志：`tail -f backend/logs/app.log`
- 确认 AI 模型可用

### 3. 前端页面报错
- 检查 Python 版本（需要 3.8+）
- 重新安装依赖：`pip install -r requirements.txt`
- 清除 Streamlit 缓存：`streamlit cache clear`

---

## 📞 技术支持

- 后端日志：`backend/logs/`
- 前端日志：浏览器控制台 (F12)
- API 文档：http://localhost:8000/docs

---

## 🎉 开始使用

1. 按照上面的步骤启动服务
2. 打开浏览器访问：http://localhost:8501
3. 在"系统设置"页面测试 API 连接
4. 开始创作你的第一本小说！

---

**版本**: v1.0.0  
**更新日期**: 2026-05-06  
**技术栈**: FastAPI + Streamlit + Baidu Qianfan
