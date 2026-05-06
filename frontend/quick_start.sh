#!/bin/bash

# 简化版启动脚本 - 仅启动前端

echo "🎨 启动 Streamlit 前端..."
echo "📌 请确保后端已在运行: python start.py"
echo ""

cd "$(dirname "$0")"
streamlit run app.py
