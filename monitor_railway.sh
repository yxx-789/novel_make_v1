#!/bin/bash
# 监控 Railway 部署状态

API_URL="https://novelmakev1-production.up.railway.app"
LOG_FILE="/home/gem/.openclaw/workspace/NOVEL_PLATFORM/railway_deployment.log"

echo "$(date '+%Y-%m-%d %H:%M:%S') - 开始监控 Railway 部署状态" >> "$LOG_FILE"

attempt=1
max_attempts=20  # 最多尝试 10 分钟

while [ $attempt -le $max_attempts ]; do
    echo "$(date '+%Y-%m-%d %H:%M:%S') - 尝试 $attempt/$max_attempts - 测试后端服务..." >> "$LOG_FILE"

    # 测试健康检查端点
    response=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 10 --max-time 15 "$API_URL/health" 2>&1)

    if [ "$response" = "200" ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') - ✅ 后端服务启动成功！HTTP 200" >> "$LOG_FILE"

        # 测试 API 端点
        echo "$(date '+%Y-%m-%d %H:%M:%S') - 测试 API 端点..." >> "$LOG_FILE"
        api_response=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 10 --max-time 15 "$API_URL/api/v1/novels" 2>&1)

        if [ "$api_response" = "200" ] || [ "$api_response" = "405" ]; then
            echo "$(date '+%Y-%m-%d %H:%M:%S') - ✅ API 端点正常工作！HTTP $api_response" >> "$LOG_FILE"
            echo "$(date '+%Y-%m-%d %H:%M:%S') - 🎉 Railway 部署成功！" >> "$LOG_FILE"
            exit 0
        fi
    fi

    echo "$(date '+%Y-%m-%d %H:%M:%S') - ❌ 服务未就绪，HTTP $response，等待 30 秒..." >> "$LOG_FILE"
    sleep 30
    attempt=$((attempt+1))
done

echo "$(date '+%Y-%m-%d %H:%M:%S') - ⏱️ 超过最大等待时间" >> "$LOG_FILE"
exit 1