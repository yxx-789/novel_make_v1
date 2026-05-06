# Novel Creation API - 项目文件结构

novel_creation_api/
├── 📁 api/                      # API 层
│   ├── 📄 routes.py             # FastAPI 路由定义
│   ├── 📄 middleware.py         # 中间件（认证、日志等）
│   └── 📄 dependencies.py       # 依赖注入
│
├── 📁 core/                     # 核心业务逻辑
│   ├── 📄 novel_engine.py       # 小说创作引擎
│   ├── 📄 drama_engine.py       # 剧本转换引擎
│   ├── 📄 memory_manager.py     # 记忆管理器
│   └── 📄 consistency_checker.py # 一致性检查器
│
├── 📁 models/                   # 数据模型
│   ├── 📄 schemas.py            # Pydantic 模型定义
│   ├── 📄 database.py           # 数据库模型（可选）
│   └── 📄 enums.py              # 枚举类型
│
├── 📁 utils/                    # 工具函数
│   ├── 📄 file_utils.py         # 文件操作
│   ├── 📄 llm_utils.py          # LLM 工具
│   ├── 📄 vectorstore_utils.py  # 向量存储工具
│   └── 📄 logger.py             # 日志配置
│
├── 📁 pipelines/                # Open WebUI Pipelines
│   ├── 📄 novel_creation_pipeline.py
│   ├── 📄 drama_conversion_pipeline.py
│   └── 📄 hybrid_pipeline.py
│
├── 📁 data/                     # 数据存储
│   ├── 📁 vectorstore/          # 向量数据库
│   ├── 📁 projects/             # 项目数据
│   ├── 📁 cache/               # 缓存数据
│   └── 📁 logs/                # 日志文件
│
├── 📁 scripts/                  # 脚本
│   ├── 📄 setup.py              # 安装脚本
│   ├── 📄 config_generator.py   # 配置生成
│   └── 📄 docker_build.py       # Docker 构建
│
├── 📄 requirements.txt          # Python 依赖
├── 📄 requirements-dev.txt      # 开发依赖
├── 📄 config.yaml              # 配置文件
├── 📄 main.py                  # 主入口文件
├── 📄 docker-compose.yml       # Docker Compose
└── 📄 README.md                # 项目说明

# ==================== 依赖文件 ====================

# requirements.txt
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.5.0
openai>=1.0.0
chromadb>=0.4.0
langchain>=0.1.0
python-dotenv>=1.0.0
httpx>=0.25.0
tenacity>=8.2.0
aiofiles>=23.0.0
python-multipart>=0.0.6
pyyaml>=6.0
python-docx>=1.1.0  # Word 导出
markdown>=3.5.0
pandas>=2.1.0  # CSV 导出

# requirements-dev.txt
pytest>=7.4.0
pytest-asyncio>=0.21.0
black>=23.0.0
isort>=5.12.0
mypy>=1.5.0
flake8>=6.0.0
pre-commit>=3.5.0
httpx>=0.25.0
pytest-cov>=4.1.0

# ==================== Docker 文件 ====================

# docker-compose.yml
version: '3.8'

services:
  novel_api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ENVIRONMENT=production
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # 可选：向量数据库服务
  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8001:8000"
    volumes:
      - chroma_data:/chroma/chroma
    environment:
      - ALLOW_RESET=true
      - ANONYMIZED_TELEMETRY=false

  # 可选：Open WebUI
  openwebui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "8080:8080"
    volumes:
      - openwebui_data:/app/backend/data
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
    depends_on:
      - ollama

  # 可选：Ollama 服务
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama

volumes:
  chroma_data:
  openwebui_data:
  ollama_data:

# ==================== 环境变量示例 ====================

# .env.example
OPENAI_API_KEY=sk-xxx
DEEPSEEK_API_KEY=sk-yyy
DATABASE_URL=sqlite:///data/projects.db
ENVIRONMENT=development
LOG_LEVEL=INFO
VECTORSTORE_TYPE=chromadb
ENABLE_CACHE=true