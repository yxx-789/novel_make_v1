#!/bin/bash

# AI 小说创作平台 - 停止服务脚本

echo "🛑 停止 AI 小说创作平台服务..."

# 获取项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT/logs"

# 停止后端
if [ -f "backend.pid" ]; then
    BACKEND_PID=$(cat backend.pid)
    kill $BACKEND_PID 2>/dev/null
    echo "✅ 后端已停止 (PID: $BACKEND_PID)"
    rm backend.pid
fi

# 停止前端
if [ -f "frontend.pid" ]; then
    FRONTEND_PID=$(cat frontend.pid)
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ 前端已停止 (PID: $FRONTEND_PID)"
    rm frontend.pid
fi

echo ""
echo "✅ 所有服务已停止"
