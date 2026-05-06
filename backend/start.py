#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动脚本 - 简化的启动方式
"""

import sys
import os
from pathlib import Path

# 设置项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 确保必要的 __init__.py 存在
for dir_name in ["utils", "config", "core", "models", "api", "pipelines"]:
    dir_path = project_root / dir_name
    if dir_path.exists() and not (dir_path / "__init__.py").exists():
        (dir_path / "__init__.py").write_text("# Package marker\n")

print("=" * 60)
print("🚀 Novel Creation Platform")
print("=" * 60)
print("📡 AI 提供商: 百度千帆")
print("🤖 默认模型: glm-5.1")
print("🌐 服务端口: 8000")
print("=" * 60)

# 导入并启动
from main_fixed import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
