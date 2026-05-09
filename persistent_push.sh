#!/bin/bash
# 持续推送脚本 - 每 60 秒尝试一次，持续 2 小时

LOG_FILE="/home/gem/.openclaw/workspace/NOVEL_PLATFORM/push_retry.log"
REPO_DIR="/home/gem/.openclaw/workspace/NOVEL_PLATFORM"

echo "$(date '+%Y-%m-%d %H:%M:%S') - 启动持续推送任务" >> "$LOG_FILE"

attempt=1
max_attempts=120  # 2 小时

while [ $attempt -le $max_attempts ]; do
    echo "$(date '+%Y-%m-%d %H:%M:%S') - 尝试 $attempt/$max_attempts" >> "$LOG_FILE"
    
    cd "$REPO_DIR"
    if timeout 45 git push origin main 2>&1 >> "$LOG_FILE"; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') - ✅ 推送成功！" >> "$LOG_FILE"
        echo "推送成功于第 $attempt 次尝试" >> "$LOG_FILE"
        exit 0
    else
        echo "$(date '+%Y-%m-%d %H:%M:%S') - ❌ 推送失败，等待 60 秒..." >> "$LOG_FILE"
        sleep 60
        attempt=$((attempt+1))
    fi
done

echo "$(date '+%Y-%m-%d %H:%M:%S') - ❌ 超过最大尝试次数" >> "$LOG_FILE"
exit 1