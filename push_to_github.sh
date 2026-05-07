#!/bin/bash
# 推送代码到 GitHub
# 执行方式：bash push_to_github.sh

cd /home/gem/.openclaw/workspace/NOVEL_PLATFORM

echo "开始推送代码到 GitHub..."

# 尝试推送
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ 推送成功！"
    echo ""
    echo "GitHub 仓库：https://github.com/yxx-789/novel_make_v1"
    echo ""
    echo "Railway 会自动检测并重新部署"
    echo "后端地址：https://novelmakev1-production.up.railway.app"
else
    echo "❌ 推送失败，请检查网络连接"
    echo "你可以尝试："
    echo "1. 检查网络连接"
    echo "2. 使用 VPN 或代理"
    echo "3. 稍后重试"
fi
