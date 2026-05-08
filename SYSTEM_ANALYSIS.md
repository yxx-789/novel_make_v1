# 系统全面排查报告

**生成时间：** 2026-05-08 20:18 GMT+8
**分析范围：** 前后端架构、配置、函数调用关系

---

## 📁 项目目录结构

```
NOVEL_PLATFORM/
├── backend/                      # 后端服务
│   ├── api/
│   │   └── routes.py            # API 路由定义
│   ├── config/
│   │   └── qianfan_config.py    # 千帆配置（从环境变量读取）
│   ├── core/
│   │   ├── novel_engine.py           # 小说引擎（OpenAI版本）
│   │   ├── novel_engine_qianfan.py   # 小说引擎（千帆版本）✅
│   │   ├── drama_engine.py           # 剧本引擎
│   │   ├── architecture_generator.py # 架构生成器
│   │   ├── blueprint_generator.py    # 蓝图生成器
│   │   └── chapter_planner.py        # 章节规划器
│   ├── models/
│   │   └── schemas.py           # 数据模型定义
│   ├── utils/
│   │   └── qianfan_client.py    # 千帆API客户端 ✅
│   ├── main.py                  # 主入口（支持双配置）✅
│   ├── main_fixed.py            # 旧版本（待删除）
│   ├── main_simple.py           # 简化版（待删除）
│   ├── main_railway_test.py     # Railway测试应用
│   ├── .env                     # 环境变量（OpenAI配置）
│   ├── railway.json             # Railway部署配置
│   └── requirements.txt         # Python依赖
│
├── frontend/                    # 前端服务（Streamlit）
│   ├── app.py                   # 主入口
│   ├── pages/
│   │   ├── 1_🏠_首页.py
│   │   ├── 2_✍️_小说创作.py
│   │   ├── 3_📚_小说管理.py
│   │   ├── 4_🎬_剧本转换.py
│   │   ├── 5_💬_AI聊天.py
│   │   └── 6_⚙️_系统设置.py
│   └── utils/
│       ├── api.py               # API调用封装
│       ├── config.py            # 前端配置
│       └── global_styles.py     # 全局样式
│
└── [各种文档文件]
```

---

## 🔗 文件之间的调用关系

### 后端核心调用链

```
main.py (入口)
  ├── get_config()                     # 读取环境变量配置
  │   ├── os.getenv("QIANFAN_API_KEY") # 优先读取千帆配置
  │   └── os.getenv("OPENAI_API_KEY")  # 回退到OpenAI配置
  │
  ├── create_app()                     # 创建FastAPI应用
  │   └── init_engines(llm_config)     # 初始化引擎
  │       ├── NovelEngine(config)      # 创建小说引擎
  │       │   └── QianfanClient(       # 创建千帆客户端
  │       │       api_key=...,          # 使用配置中的API key
  │       │       api_url=...           # 使用配置中的API URL
  │       │   )
  │       └── DramaEngine(config)      # 创建剧本引擎
  │
  └── uvicorn.run()                    # 启动服务器

api/routes.py (API路由)
  ├── init_engines()                   # 初始化全局引擎实例
  │   ├── novel_engine (全局变量)
  │   └── drama_engine (全局变量)
  │
  ├── @app.post("/api/v1/novels")      # 创建小说
  │   └── novel_engine.create_novel()  # 调用引擎方法
  │
  ├── @app.post("/blueprint")          # 生成蓝图
  │   └── novel_engine.generate_blueprint()
  │       └── QianfanClient.chat()     # 调用千帆API
  │
  └── @app.get("/health")              # 健康检查
      └── 检查 novel_engine 和 drama_engine 是否为 None

utils/qianfan_client.py (千帆客户端)
  ├── __init__(api_key, api_url)
  │   ├── 从环境变量读取：os.getenv("QIANFAN_API_KEY")
  │   └── 验证：if not api_key: raise ValueError ⚠️
  │
  └── chat(messages, model, ...)
      └── requests.post(api_url, headers={Authorization: Bearer {api_key}})
```

### 前端调用链

```
app.py (主入口)
  ├── 读取配置：st.secrets['API_BASE_URL'] 或 os.environ['API_BASE_URL']
  └── 默认值：'http://localhost:8000'

utils/api.py (API客户端)
  ├── Config.API_BASE_URL = 'http://localhost:8000'  # 默认值
  │
  └── APIClient(base_url)
      ├── health_check()              # GET /health
      ├── create_novel()              # POST /api/v1/novels
      ├── generate_blueprint()        # POST /api/v1/novels/{id}/blueprint
      └── [其他API方法...]

pages/2_✍️_小说创作.py
  └── api_client.create_novel()
      └── POST https://novelmakev1-production.up.railway.app/api/v1/novels
```

---

## ⚙️ 配置变量分析

### 环境变量对照表

| 变量名 | backend/.env | Railway环境变量 | 用户提供的值 | 状态 |
|--------|--------------|----------------|-------------|------|
| QIANFAN_API_KEY | ❌ 未设置 | ❓ 未知 | ✅ 已提供 | ⚠️ 需要确认 |
| QIANFAN_API_URL | ❌ 未设置 | ❓ 未知 | ✅ 已提供 | ⚠️ 需要确认 |
| OPENAI_API_KEY | ✅ sk-test-key | ❌ 未设置 | ❌ 未提供 | - |
| OPENAI_BASE_URL | ✅ https://api.openai.com/v1 | ❌ 未设置 | ❌ 未提供 | - |
| LLM_MODEL | ✅ gpt-4o-mini | ❌ 未设置 | ❌ 未提供 | - |
| API_BASE_URL (前端) | ❌ 未设置 | ❓ 未知 | ❌ 未提供 | ⚠️ 需要设置 |

### 用户提供的配置

```python
# 百度千帆平台 API
API_KEY = "bce-v3/ALTAK-vnASNnJZQkPchN6JShUdi/38e23c1484e3b2ab42e15dd596dc85fd4328caf4"
API_URL = "https://qianfan.baidubce.com/v2/chat/completions"
```

**⚠️ 问题：这些值需要设置到环境变量中！**

---

## 🔧 需要统一的配置

### 1. API Key 配置 ⚠️ 关键问题

**当前状态：**
- ❌ `.env` 文件使用 OpenAI 配置
- ❓ Railway 环境变量未知
- ✅ 用户提供了千帆 API key

**需要统一为：**

```bash
# backend/.env 或 Railway 环境变量
QIANFAN_API_KEY=bce-v3/ALTAK-vnASNnJZQkPchN6JShUdi/38e23c1484e3b2ab42e15dd596dc85fd4328caf4
QIANFAN_API_URL=https://qianfan.baidubce.com/v2/chat/completions
QIANFAN_MODEL=glm-5.1
```

### 2. 前端 API 地址配置

**当前状态：**
- ❌ 前端默认 `http://localhost:8000`
- ✅ Railway 后端地址 `https://novelmakev1-production.up.railway.app`

**需要设置：**

```bash
# Streamlit Secrets 或环境变量
API_BASE_URL=https://novelmakev1-production.up.railway.app
```

### 3. 多个 main 文件的混乱

**当前有 4 个 main 文件：**

| 文件 | 用途 | 状态 |
|------|------|------|
| main.py | 主应用（支持双配置）| ✅ 保留 |
| main_fixed.py | 旧版本 | ❌ 删除 |
| main_simple.py | 简化版 | ❌ 删除 |
| main_railway_test.py | Railway测试 | ✅ 保留（测试用）|

---

## 🎯 函数和变量的相互关联

### 关键全局变量

```python
# api/routes.py
novel_engine = None    # 小说引擎实例
drama_engine = None    # 剧本引擎实例

# 初始化函数
def init_engines(llm_config, embedding_config):
    global novel_engine, drama_engine
    novel_engine = NovelEngine(llm_config, embedding_config)
    drama_engine = DramaEngine(llm_config)
```

### 配置流向

```
1. 环境变量 (.env 或 Railway)
   ↓
2. main.py → get_config()
   ↓
3. create_app() → init_engines(config)
   ↓
4. novel_engine = NovelEngine(config)
   ↓
5. QianfanClient(api_key=config['api_key'], api_url=config['api_url'])
   ↓
6. 所有API路由使用 novel_engine 调用千帆API
```

### API调用流程

```
前端 → api_client.create_novel(title, genre, topic)
  ↓
POST https://novelmakev1-production.up.railway.app/api/v1/novels
  ↓
routes.py → create_novel(request)
  ↓
novel_engine.create_novel(title, genre, topic, ...)
  ↓
QianfanClient.chat(messages=[{"role": "user", "content": "..."}])
  ↓
requests.post("https://qianfan.baidubce.com/v2/chat/completions",
              headers={"Authorization": f"Bearer {api_key}"})
  ↓
返回AI生成的内容
```

---

## 🚨 发现的问题

### 问题1：环境变量未正确设置

**影响：** 应用启动时可能找不到千帆API key，导致引擎初始化失败

**解决方案：**
1. 在 Railway 设置环境变量 `QIANFAN_API_KEY`
2. 在 Railway 设置环境变量 `QIANFAN_API_URL`
3. 或更新 `.env` 文件

### 问题2：前端未配置后端地址

**影响：** 前端默认调用 `http://localhost:8000`，无法连接到 Railway 后端

**解决方案：**
1. 在 Streamlit Cloud 设置 Secrets：`API_BASE_URL = "https://novelmakev1-production.up.railway.app"`
2. 或设置环境变量

### 问题3：多个 main 文件共存

**影响：** 代码混乱，不确定使用哪个版本

**解决方案：** 删除 `main_fixed.py` 和 `main_simple.py`

### 问题4：railway.json 未推送到 GitHub

**影响：** Railway 仍使用旧的启动命令

**解决方案：** 推送代码或手动修改 Railway 启动命令

---

## ✅ 立即需要做的

### 优先级1：设置千帆API配置

**在 Railway 环境变量中设置：**
```bash
QIANFAN_API_KEY=bce-v3/ALTAK-vnASNnJZQkPchN6JShUdi/38e23c1484e3b2ab42e15dd596dc85fd4328caf4
QIANFAN_API_URL=https://qianfan.baidubce.com/v2/chat/completions
QIANFAN_MODEL=glm-5.1
```

### 优先级2：设置前端API地址

**在 Streamlit Cloud Secrets 中设置：**
```toml
API_BASE_URL = "https://novelmakev1-production.up.railway.app"
```

### 优先级3：推送代码修改

```bash
git push origin main
```

### 优先级4：清理多余文件

```bash
rm backend/main_fixed.py backend/main_simple.py
```

---

## 📊 总结

**核心问题：**
1. ❌ 千帆 API key 未设置到环境变量
2. ❌ 前端未配置后端地址
3. ❌ railway.json 修改未推送
4. ⚠️ 多个 main 文件共存

**已解决：**
1. ✅ 代码支持双配置（千帆/OpenAI）
2. ✅ 端口配置正确
3. ✅ 异常处理改进
4. ✅ 依赖简化

**下一步：**
按照优先级列表逐一解决问题，确保配置统一且正确。