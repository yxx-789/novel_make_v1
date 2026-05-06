#!/bin/bash

# AI 小说创作平台 - 一键启动脚本

echo "🚀 AI 小说创作平台启动脚本"
echo "================================"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="$PROJECT_ROOT"
FRONTEND_DIR="$PROJECT_ROOT/novel_frontend"

echo "📁 项目目录: $PROJECT_ROOT"
echo "📁 后端目录: $BACKEND_DIR"
echo "📁 前端目录: $FRONTEND_DIR"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 未找到 Python3，请先安装 Python${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python3 已安装: $(python3 --version)${NC}"

# 检查虚拟环境
if [ ! -d "$BACKEND_DIR/.venv" ]; then
    echo -e "${YELLOW}⚠️  未找到虚拟环境，正在创建...${NC}"
    cd "$BACKEND_DIR"
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt 2>/dev/null || echo "⚠️  requirements.txt 不存在，跳过依赖安装"
else
    echo -e "${GREEN}✅ 虚拟环境已存在${NC}"
fi

# 激活虚拟环境
echo ""
echo "🔧 激活虚拟环境..."
source "$BACKEND_DIR/.venv/bin/activate"

# 安装前端依赖
echo ""
echo "📦 检查前端依赖..."
if [ -f "$FRONTEND_DIR/requirements.txt" ]; then
    pip install -r "$FRONTEND_DIR/requirements.txt" -q
    echo -e "${GREEN}✅ 前端依赖安装完成${NC}"
fi

# 启动后端
echo ""
echo "🚀 启动后端 API 服务..."
cd "$BACKEND_DIR"

# 检查 start.py 是否存在
if [ -f "start.py" ]; then
    python start.py &
    BACKEND_PID=$!
    echo -e "${GREEN}✅ 后端服务已启动 (PID: $BACKEND_PID)${NC}"
    echo "   访问地址: http://localhost:8000"
    echo "   API 文档: http://localhost:8000/docs"
else
    echo -e "${YELLOW}⚠️  未找到 start.py，跳过后端启动${NC}"
    echo "   请手动启动后端服务"
fi

# 等待后端启动
echo ""
echo "⏳ 等待后端服务启动..."
sleep 3

# 启动前端
echo ""
echo "🎨 启动 Streamlit 前端..."
cd "$FRONTEND_DIR"

# 检查 app.py 是否存在
if [ -f "app.py" ]; then
    streamlit run app.py --server.port=8501 --server.address=localhost
else
    echo -e "${RED}❌ 未找到 app.py${NC}"
    exit 1
fi

# 清理函数
cleanup() {
    echo ""
    echo "🛑 停止服务..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo -e "${GREEN}✅ 后端服务已停止${NC}"
    fi
    exit 0
}

# 捕获退出信号
trap cleanup SIGINT SIGTERM
