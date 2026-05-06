# 快速启动指南

## 方式一：一键启动（推荐）

```bash
cd /Users/xingyao/Desktop/novel_creation
chmod +x novel_frontend/start.sh
./novel_frontend/start.sh
```

## 方式二：手动启动

### 1. 启动后端

```bash
cd /Users/xingyao/Desktop/novel_creation
source .venv/bin/activate
python start.py
```

后端将运行在：http://localhost:8000

### 2. 启动前端（新终端窗口）

```bash
cd /Users/xingyao/Desktop/novel_creation
source .venv/bin/activate
cd novel_frontend
streamlit run app.py
```

前端将运行在：http://localhost:8501

## 方式三：仅启动前端（后端已运行）

```bash
cd /Users/xingyao/Desktop/novel_creation/novel_frontend
chmod +x quick_start.sh
./quick_start.sh
```

## 访问地址

- **前端界面**: http://localhost:8501
- **后端 API**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

## 常见问题

### 1. 端口被占用

```bash
# 查看 8501 端口占用
lsof -i:8501

# 查看 8000 端口占用
lsof -i:8000

# 终止进程
kill -9 <PID>
```

### 2. 依赖缺失

```bash
pip install -r novel_frontend/requirements.txt
```

### 3. 后端连接失败

- 检查后端是否启动
- 确认 API 地址配置正确
- 查看防火墙设置

## 目录结构

```
novel_creation/
├── start.py              # 后端启动文件
├── .venv/                # Python 虚拟环境
├── novel_frontend/       # 前端目录
│   ├── app.py           # 主入口
│   ├── pages/           # 多页面
│   ├── utils/           # 工具模块
│   ├── requirements.txt # 前端依赖
│   ├── start.sh         # 一键启动脚本
│   └── quick_start.sh   # 快速启动脚本
└── requirements.txt     # 后端依赖
```
