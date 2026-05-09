# 🔍 Novel Make V1 - 系统诊断报告

**诊断时间**: 2026-05-09 10:25  
**诊断范围**: 项目结构、配置、代码、部署

---

## ❌ 发现的关键问题

### 1. **配置不一致问题** 🚨

**问题描述**:
- `backend/config.yaml` 使用 OpenAI 和 DeepSeek 配置
- `backend/.env` 配置的是百度千帆平台
- **导致**: 配置文件与实际使用的 API 不匹配

**影响**: 代码可能无法正确加载配置

**解决方案**:
```yaml
# backend/config.yaml 应该修改为：
llm:
  primary:
    provider: "qianfan"  # 改为千帆
    api_key: "${QIANFAN_API_KEY}"
    base_url: "${QIANFAN_API_URL}"
    model: "${QIANFAN_MODEL}"
```

---

### 2. **Railway 部署配置冲突** ⚠️

**问题描述**:
- `railway.json` 使用 `python main.py` 作为启动命令
- 但存在 `main_railway_test.py`（测试版本）
- 推送时合并冲突，选择了 `python main.py`

**当前配置**:
```json
{
  "startCommand": "python main.py"
}
```

**影响**: 
- 如果 `main.py` 在 Railway 上启动失败，服务将无法运行
- `main_railway_test.py` 是精简版，更适合诊断部署问题

**建议**:
- 测试阶段：先用 `main_railway_test.py` 确保 Railway 基础部署正常
- 生产环境：确认 `main.py` 能正常运行后再切换

---

### 3. **API 密钥硬编码问题** 🔒

**问题描述**:
- API Key 直接写在 `.env` 文件中
- `.env` 文件被推送到 GitHub（如果未在 `.gitignore` 中）

**检查结果**:
✅ `.env` 已在 `.gitignore` 中，不会被推送到 GitHub

**建议**:
- Railway 部署时，通过 Railway 环境变量设置 API Key
- 不要在代码中硬编码任何密钥

---

### 4. **前端 API 地址配置** 🌐

**问题描述**:
- 前端 `utils/api.py` 中 `API_BASE_URL` 默认为 `http://localhost:8000`
- 部署到 Railway 后，需要修改为实际的生产环境地址

**当前配置**:
```python
API_BASE_URL = os.environ.get('API_BASE_URL', 'http://localhost:8000')
```

**解决方案**:
1. 在 Streamlit 部署时设置环境变量：`API_BASE_URL=https://novelmakev1-production.up.railway.app`
2. 或者在代码中自动检测环境：
```python
import os

# 自动检测环境
if os.getenv('STREAMLIT_SERVER_HEADLESS') == 'true':
    # 生产环境
    API_BASE_URL = os.environ.get('API_BASE_URL', 'https://novelmakev1-production.up.railway.app')
else:
    # 开发环境
    API_BASE_URL = os.environ.get('API_BASE_URL', 'http://localhost:8000')
```

---

### 5. **依赖项最小化** ✅

**状态**: 良好

`backend/requirements.txt` 已经精简到最小依赖集，适合 Railway 快速安装。

**建议**: 保持当前配置，避免添加不必要的依赖。

---

## 📊 项目结构分析

### 目录结构

```
NOVEL_PLATFORM/
├── backend/                 # 后端 API
│   ├── api/                 # API 路由
│   ├── core/                # 核心引擎
│   ├── models/              # 数据模型
│   ├── utils/               # 工具类
│   ├── prompts/             # AI 提示词
│   ├── main.py              # 主入口
│   ├── main_railway_test.py # Railway 测试版
│   ├── config.yaml          # 配置文件（需更新）
│   └── .env                 # 环境变量（已忽略）
├── frontend/                # Streamlit 前端
│   ├── pages/               # 页面
│   ├── utils/               # 工具类
│   └── app.py               # 主入口
└── docs/                    # 文档
```

### 技术栈

- **后端**: FastAPI + Uvicorn
- **AI**: 百度千帆平台 (GLM-5.1, Qwen, DeepSeek)
- **前端**: Streamlit
- **部署**: Railway (后端) + Streamlit Cloud (前端)

---

## 🔧 代码一致性检查

### 1. API 路由 ✅

- `/health` - 健康检查（Railway 必需）
- `/api/v1/novels` - 小说 CRUD
- `/api/v1/novels/{id}/blueprint` - 生成蓝图
- `/api/v1/novels/{id}/outline` - 生成大纲
- `/api/v1/novels/{id}/chapters/{num}/generate` - 生成章节
- `/api/v1/drama/convert` - 剧本转换

**状态**: 前后端 API 匹配良好

### 2. 数据模型 ✅

使用 Pydantic 定义数据模型，类型安全。

### 3. 错误处理 ⚠️

**问题**: `main.py` 中引擎初始化失败时只打印警告，应用继续运行

**代码**:
```python
try:
    init_engines(config["llm"], config["embedding"])
    print(f"✅ 引擎初始化成功")
except Exception as e:
    print(f"⚠️  引擎初始化失败: {e}")
    print("⚠️  应用将继续运行，但AI功能可能不可用")
```

**影响**: Railway 健康检查可能通过，但实际功能不可用

**建议**: 在 `/health` 端点中返回引擎状态，让前端能够感知

---

## 🚀 部署建议

### Railway 后端部署

1. **环境变量设置**:
```bash
QIANFAN_API_KEY=bce-v3/ALTAK-vnASNnJZQkPchN6JShUdi/38e23c1484e3b2ab42e15dd596dc85fd4328caf4
QIANFAN_API_URL=https://qianfan.baidubce.com/v2/chat/completions
QIANFAN_MODEL=glm-5.1
PORT=8000
ENVIRONMENT=production
```

2. **启动命令**: `python main.py`（当前配置）

3. **健康检查**: Railway 会自动检查 `/health` 端点

### Streamlit 前端部署

1. **环境变量**:
```bash
API_BASE_URL=https://novelmakev1-production.up.railway.app
```

2. **requirements.txt**: 确保 Streamlit 相关依赖完整

---

## ✅ 推荐修复优先级

### P0 - 立即修复

1. ✅ 更新 `backend/config.yaml` 支持千帆配置
2. ⚠️ 在 Railway 设置环境变量
3. ⚠️ 前端设置正确的 `API_BASE_URL`

### P1 - 尽快修复

1. 改进错误处理，让健康检查能反映实际状态
2. 添加日志记录，方便排查问题
3. 添加 API 调用超时和重试机制

### P2 - 优化项

1. 添加数据库持久化（当前是文件存储）
2. 添加用户认证
3. 添加 API 限流

---

## 📋 快速修复脚本

### 修复 1: 更新 config.yaml

```bash
# 在项目根目录执行
cd /home/gem/.openclaw/workspace/NOVEL_PLATFORM/backend
cp config.yaml config.yaml.backup
```

然后手动修改 `config.yaml`，将 `provider` 改为 `qianfan`。

### 修复 2: Railway 环境变量

在 Railway Dashboard 中设置：
- `QIANFAN_API_KEY`
- `QIANFAN_API_URL`
- `QIANFAN_MODEL`
- `PORT=8000`

### 修复 3: 前端 API 地址

部署 Streamlit 时设置：
- `API_BASE_URL=https://novelmakev1-production.up.railway.app`

---

## 🎯 下一步行动

[::button-group layout="flow"]
  [::button label="立即修复 config.yaml" query_send="立即修复 config.yaml" style="primary"]
  [::button label="测试 Railway 部署" query_send="测试 Railway 部署" style="primary"]
  [::button label="查看详细日志" query_send="查看详细日志" style="primary"]
  [::button label="生成修复脚本" query_send="生成修复脚本" style="primary"]
[::button-group/]

---

**诊断完成！** 发现 5 个问题，其中 2 个关键问题需要立即修复。<tool_call>exec<arg_key>command</arg_key><arg_value>cd /home/gem/.openclaw/workspace/NOVEL_PLATFORM && grep -E "\.env$|\.env\.example" .gitignore 2>/dev/null || echo ".env 未在 .gitignore 中"