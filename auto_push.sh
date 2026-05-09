#!/bin/bash
# 后台推送脚本 - 每 30 秒尝试一次

LOG_FILE="/home/gem/.openclaw/workspace/NOVEL_PLATFORM/push_log.txt"
REPO_DIR="/home/gem/.openclaw/workspace/NOVEL_PLATFORM"

echo "$(date '+%Y-%m-%d %H:%M:%S') - 开始后台推送任务" >> "$LOG_FILE"
echo "等待网络恢复..." >> "$LOG_FILE"

attempt=1
max_attempts=120  # 最多尝试 60 分钟（每 30 秒一次）

while [ $attempt -le $max_attempts ]; do
    echo "$(date '+%Y-%m-%d %H:%M:%S') - 尝试 $attempt/$max_attempts" >> "$LOG_FILE"
    
    cd "$REPO_DIR"
    if timeout 30 git push origin main 2>&1 >> "$LOG_FILE"; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') - ✅ 推送成功！" >> "$LOG_FILE"
        exit 0
    else
        echo "$(date '+%Y-%m-%d %H:%M:%S') - ❌ 推送失败，等待 30 秒..." >> "$LOG_FILE"
        sleep 30
        attempt=$((attempt+1))
    fi
done

echo "$(date '+%Y-%m-%d %H:%M:%S') - ❌ 超过最大尝试次数，停止推送" >> "$LOG_FILE"
exit 1