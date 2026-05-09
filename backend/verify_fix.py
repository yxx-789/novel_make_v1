#!/usr/bin/env python3
"""
快速验证脚本 - 检查修复是否成功
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath: str) -> bool:
    """检查文件是否存在"""
    return Path(filepath).exists()

def check_env_vars():
    """检查环境变量"""
    print("\n=== 检查环境变量 ===")
    
    required_vars = [
        "QIANFAN_API_KEY",
        "QIANFAN_API_URL",
        "QIANFAN_MODEL"
    ]
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # 隐藏 API Key 的部分内容
            if "KEY" in var:
                display_value = value[:20] + "..." if len(value) > 20 else value
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: 未设置")

def check_config_yaml():
    """检查 config.yaml 配置"""
    print("\n=== 检查 config.yaml ===")
    
    config_path = Path(__file__).parent / "backend" / "config.yaml"
    if not config_path.exists():
        config_path = Path(__file__).parent / "config.yaml"
    
    if not config_path.exists():
        print("❌ config.yaml 文件不存在")
        return False
    
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查关键配置
    checks = [
        ("provider: \"qianfan\"", "主模型配置为千帆"),
        ("${QIANFAN_API_KEY}", "使用环境变量 QIANFAN_API_KEY"),
        ("${QIANFAN_API_URL}", "使用环境变量 QIANFAN_API_URL"),
        ("${QIANFAN_MODEL}", "使用环境变量 QIANFAN_MODEL")
    ]
    
    all_ok = True
    for pattern, desc in checks:
        if pattern in content:
            print(f"✅ {desc}")
        else:
            print(f"❌ {desc}")
            all_ok = False
    
    return all_ok

def check_frontend_config():
    """检查前端配置"""
    print("\n=== 检查前端配置 ===")
    
    api_path = Path(__file__).parent / "frontend" / "utils" / "api.py"
    if not api_path.exists():
        print("❌ 前端 API 配置文件不存在")
        return False
    
    with open(api_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = [
        ("STREAMLIT_SERVER_HEADLESS", "自动检测环境"),
        ("novelmakev1-production.up.railway.app", "生产环境地址")
    ]
    
    all_ok = True
    for pattern, desc in checks:
        if pattern in content:
            print(f"✅ {desc}")
        else:
            print(f"❌ {desc}")
            all_ok = False
    
    return all_ok

def check_files():
    """检查必需文件"""
    print("\n=== 检查必需文件 ===")
    
    required_files = [
        "backend/main.py",
        "backend/main_railway_test.py",
        "backend/config.yaml",
        "backend/.env.example",
        "backend/railway.json",
        "frontend/app.py",
        "frontend/requirements.txt",
        "RAILWAY_ENV_VARS.md",
        "FRONTEND_DEPLOY.md"
    ]
    
    all_ok = True
    for file in required_files:
        if check_file_exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            all_ok = False
    
    return all_ok

def main():
    """主函数"""
    print("=" * 60)
    print("🔍 Novel Make V1 - 修复验证脚本")
    print("=" * 60)
    
    # 切换到项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 执行检查
    check_files()
    check_config_yaml()
    check_frontend_config()
    check_env_vars()
    
    print("\n" + "=" * 60)
    print("✅ 验证完成！")
    print("=" * 60)
    print("\n下一步:")
    print("1. 在 Railway 设置环境变量（参考 RAILWAY_ENV_VARS.md）")
    print("2. 重新部署后端")
    print("3. 部署前端到 Streamlit Cloud（参考 FRONTEND_DEPLOY.md）")
    print("4. 测试 API 连接")

if __name__ == "__main__":
    main()
