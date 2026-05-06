#!/bin/bash

# AI 小说创作平台 - 一键启动脚本

echo "╔════════════════════════════════════════════════╗"
echo "║     AI 小说创作平台 - 启动脚本                ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3"
    exit 1
fi

# 获取项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

echo "📁 项目目录: $PROJECT_ROOT"
echo ""

# 启动后端
echo "🚀 启动后端服务..."
cd backend

# 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv .venv
fi

# 激活虚拟环境
source .venv/bin/activate

# 安装依赖
if [ ! -f ".installed" ]; then
    echo "📥 安装后端依赖..."
    pip install -r requirements.txt
    touch .installed
fi

# 启动后端（后台运行）
echo "🌐 后端启动中... (http://localhost:8000)"
nohup python main.py > logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "后端 PID: $BACKEND_PID"

# 等待后端启动
sleep 3

# 检查后端是否启动成功
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ 后端启动成功"
else
    echo "⚠️  后端可能未完全启动，请检查日志: backend/logs/backend.log"
fi

echo ""

# 启动前端
echo "🚀 启动前端服务..."
cd ../frontend

# 安装依赖
if [ ! -f ".installed" ]; then
    echo "📥 安装前端依赖..."
    pip install -r requirements.txt
    touch .installed
fi

# 启动前端
echo "🎨 前端启动中... (http://localhost:8501)"
streamlit run app.py --server.headless true > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "前端 PID: $FRONTEND_PID"

echo ""
echo "╔════════════════════════════════════════════════╗"
echo "║          🎉 服务启动成功！                    ║"
echo "╠════════════════════════════════════════════════╣"
echo "║  前端地址: http://localhost:8501              ║"
echo "║  后端地址: http://localhost:8000              ║"
echo "║  API文档:  http://localhost:8000/docs         ║"
echo "╠════════════════════════════════════════════════╣"
echo "║  后端PID: $BACKEND_PID"
echo "║  前端PID: $FRONTEND_PID"
echo "╠════════════════════════════════════════════════╣"
echo "║  停止服务: ./stop.sh                          ║"
echo "║  查看日志: tail -f logs/*.log                 ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# 保存 PID
echo $BACKEND_PID > ../logs/backend.pid
echo $FRONTEND_PID > ../logs/frontend.pid
