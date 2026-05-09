#!/bin/bash
# 推送重试脚本
cd /home/gem/.openclaw/workspace/NOVEL_PLATFORM
max_retries=5
retry_count=0

echo "开始尝试推送代码到 GitHub..."

while [ $retry_count -lt $max_retries ]; do
    echo "尝试 $((retry_count+1))/$max_retries..."
    if git push origin main 2>&1; then
        echo "✅ 推送成功！"
        exit 0
    else
        echo "❌ 推送失败，等待 5 秒后重试..."
        sleep 5
        retry_count=$((retry_count+1))
    fi
done

echo "❌ 经过 $max_retries 次尝试后推送失败"
echo "最后一次错误信息："
git push origin main 2>&1
exit 1