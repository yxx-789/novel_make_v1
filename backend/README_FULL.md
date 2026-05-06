# Novel Creation Platform - 完整版本

## 📦 项目组成

本项目整合了两个原有项目：
1. **AI Novel Generator** - 完整的 AI 小说创作引擎
2. **Novel to Drama** - 小说转短剧剧本系统
3. **百度千帆 API** - 完全集成的 AI 模型调用

## 🚀 快速启动

### 1. 环境准备
```bash
# 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
pip install python-multipart
```

### 2. 启动 API 服务
```bash
# 方法1：使用修复版（推荐）
python main_fixed.py

# 方法2：使用原版
python main.py
```

### 3. 访问 API
```
API 地址: http://localhost:8000
文档地址: http://localhost:8000/docs
健康检查: http://localhost:8000/health
```

## 🎯 完整功能列表

### 📚 AI 小说创作引擎
- ✅ 小说项目管理
- ✅ 世界观设定生成
- ✅ 角色设定生成
- ✅ 情节蓝图生成
- ✅ 章节大纲规划
- ✅ 章节内容生成
- ✅ 记忆系统（角色一致性）
- ✅ 多格式导出（Markdown/JSON）

### 🎬 小说转剧本系统
- ✅ 小说内容解析
- ✅ 短剧节奏规划
- ✅ 场景划分
- ✅ 分镜头设计
- ✅ 剧本格式转换
- ✅ 多格式导出（JSON/Markdown/CSV）

### 🔗 百度千帆集成
- ✅ GLM-5.1 模型
- ✅ Qwen3.5-397B 模型
- ✅ DeepSeek-V3.2 模型
- ✅ 自动错误重试
- ✅ 流式响应支持

## 🧪 测试方法

### 1. 基础测试
```bash
# 测试 API 连接
curl http://localhost:8000/health

# 测试千帆 API
python utils/qianfan_client.py
```

### 2. 小说创作测试
```python
# 使用 quick_test.py
python quick_test.py

# 端到端测试
python test_end_to_end.py
```

### 3. 交互测试
访问 `http://localhost:8000/docs`，点击"Try it out"进行交互测试。

## 📁 项目结构

```
novel_creation_api/
├── README_FULL.md                    # 完整说明（当前文件）
├── README.md                         # 项目简介
├── main.py                          # 原主入口
├── main_fixed.py                    # 修复版主入口（推荐）
├── requirements.txt                 # 依赖列表
├── Dockerfile                       # Docker 配置
├── config/
│   ├── config.yaml                  # 配置文件
│   └── qianfan_config.py           # 千帆 API 配置
├── core/
│   ├── novel_engine.py             # 原小说引擎
│   ├── novel_engine_qianfan.py     # 千帆版小说引擎
│   └── drama_engine.py             # 剧本转换引擎
├── models/
│   └── schemas.py                  # 数据模型
├── api/
│   └── routes.py                   # API 路由
├── utils/
│   └── qianfan_client.py           # 千帆 API 客户端
├── pipelines/
│   └── novel_creation_pipeline.py  # Open WebUI Pipeline
├── deploy/
│   └── docker-compose.production.yml # 生产环境部署
└── 测试脚本/
    ├── quick_test.py               # 快速测试
    ├── test_end_to_end.py          # 端到端测试
    ├── verify_integration.py       # 集成验证
    └── test_full_pipeline.py       # 完整流程测试
```

## 🛠️ 常见问题

### 1. "Could not initialize OpenAI client"
这是正常现象，因为我们使用千帆 API。相关代码已替换。

### 2. "utils is not a package"
确保从项目根目录运行：`python main_fixed.py`

### 3. API 响应超时
千帆 API 生成较长内容可能需要时间。建议：
- 设置较小的 `max_tokens`
- 使用流式响应
- 适当重试

### 4. 如何切换模型？
修改 `config/qianfan_config.py` 中的 `DEFAULT_MODEL`：
```python
DEFAULT_MODEL = "glm-5.1"  # 可改为 "qwen3.5-397b-a17b" 或 "deepseek-v3.2"
```

## 🐳 Docker 部署

```bash
cd deploy
docker-compose -f docker-compose.production.yml up -d
```

包含服务：
- `novel_api` (8000端口) - 小说创作 API
- `chromadb` (8001端口) - 向量数据库
- `openwebui` (8080端口) - Web 界面
- `ollama` (11434端口) - 本地模型

## 🔗 原项目地址

1. **AI Novel Generator** - 完整的桌面小说创作工具
2. **Novel to Drama** - 小说转短剧脚本工具

注：本项目是两者的功能整合 + 千帆 API 适配版本。

## 📞 技术支持

如果有任何问题，请检查：
1. 网络连接（能访问千帆 API）
2. API Key 有效性
3. 端口是否被占用
4. Python 依赖是否完整安装

## 📄 License

MIT License - 基于原项目功能整合开发