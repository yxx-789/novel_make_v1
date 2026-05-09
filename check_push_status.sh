#!/bin/bash
# 检查推送状态

REPO_DIR="/home/gem/.openclaw/workspace/NOVEL_PLATFORM"
LOG_FILE="$REPO_DIR/push_log.txt"

echo "=== 推送状态检查 ==="
echo ""

if [ -f "$LOG_FILE" ]; then
    echo "📋 最新推送日志（最后 20 行）:"
    tail -20 "$LOG_FILE"
else
    echo "❌ 日志文件不存在"
fi

echo ""
echo "=== 待推送的提交 ==="
cd "$REPO_DIR"
git log --oneline origin/main..HEAD 2>&1 | head -5

echo ""
echo "=== 网络状态 ==="
if ping -c 1 github.com > /dev/null 2>&1; then
    echo "✅ GitHub 可达"
else
    echo "❌ GitHub 不可达"
fi