# Railway 环境变量配置指南

## 必需的环境变量

在 Railway Dashboard 中设置以下环境变量：

### 1. 百度千帆 API 配置

```bash
QIANFAN_API_KEY=bce-v3/ALTAK-vnASNnJZQkPchN6JShUdi/38e23c1484e3b2ab42e15dd596dc85fd4328caf4
QIANFAN_API_URL=https://qianfan.baidubce.com/v2/chat/completions
QIANFAN_MODEL=glm-5.1
```

### 2. 服务配置

```bash
PORT=8000
ENVIRONMENT=production
API_HOST=0.0.0.0
API_PORT=8000
```

### 3. Embedding 配置（可选）

```bash
EMBEDDING_MODEL=embedding-v1
```

### 4. 日志配置

```bash
LOG_LEVEL=INFO
```

---

## 如何在 Railway 中设置

### 方法 1: 通过 Dashboard

1. 打开 Railway 项目：https://railway.app/project/...
2. 选择服务 `novel_make_v1`
3. 点击 "Variables" 标签
4. 点击 "Add Variable"
5. 逐个添加上述环境变量

### 方法 2: 通过 CLI

```bash
# 安装 Railway CLI
npm install -g @railway/cli

# 登录
railway login

# 链接项目
railway link

# 设置环境变量
railway variables set QIANFAN_API_KEY="bce-v3/ALTAK-vnASNnJZQkPchN6JShUdi/38e23c1484e3b2ab42e15dd596dc85fd4328caf4"
railway variables set QIANFAN_API_URL="https://qianfan.baidubce.com/v2/chat/completions"
railway variables set QIANFAN_MODEL="glm-5.1"
railway variables set PORT="8000"
railway variables set ENVIRONMENT="production"
```

### 方法 3: 批量导入

创建文件 `.railway.env`:

```env
QIANFAN_API_KEY=bce-v3/ALTAK-vnASNnJZQkPchN6JShUdi/38e23c1484e3b2ab42e15dd596dc85fd4328caf4
QIANFAN_API_URL=https://qianfan.baidubce.com/v2/chat/completions
QIANFAN_MODEL=glm-5.1
PORT=8000
ENVIRONMENT=production
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
```

然后上传：

```bash
railway variables import .railway.env
```

---

## 验证配置

设置完成后，可以通过以下方式验证：

### 1. 检查健康状态

```bash
curl https://novelmakev1-production.up.railway.app/health
```

预期返回：

```json
{
  "status": "healthy",
  "timestamp": "2026-05-09T10:30:00",
  "engines": {
    "novel": true,
    "drama": true
  }
}
```

### 2. 测试 API

```bash
curl https://novelmakev1-production.up.railway.app/api/v1/novels
```

---

## 注意事项

⚠️ **安全提示**:
- 不要将 `.railway.env` 文件提交到 Git
- API Key 应该定期更换
- 生产环境建议使用只读权限的 API Key

✅ **部署后检查**:
1. 确认健康检查通过
2. 测试创建小说 API
3. 检查日志是否有错误

---

## Streamlit 前端部署

如果前端也部署到 Streamlit Cloud，需要设置：

```bash
API_BASE_URL=https://novelmakev1-production.up.railway.app
```

在 Streamlit Cloud 的 "Advanced settings" → "Environment variables" 中添加。

---

## 故障排查

如果部署失败，检查：

1. **Railway 日志**: 查看 Build Logs 和 Deploy Logs
2. **环境变量**: 确认所有必需变量已设置
3. **端口**: 确认 PORT 变量为 8000
4. **健康检查**: 确认 `/health` 端点返回正常

常见错误：

- `502 Bad Gateway`: 应用启动失败，检查日志
- `Timeout`: 健康检查超时，检查端口配置
- `API Key Error`: 环境变量未正确设置
