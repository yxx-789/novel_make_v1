# 🔧 Railway 环境变量修复方案

## ❌ 发现的问题

### 问题 1: QIANFAN_API_URL 路径不完整 ⭐

**当前设置**:
```bash
QIANFAN_API_URL="https://qianfan.baidubce.com/v2"
```

**正确设置**:
```bash
QIANFAN_API_URL="https://qianfan.baidubce.com/v2/chat/completions"
```

**原因**:
- 千帆 API 客户端直接使用这个 URL 发送请求
- 缺少 `/chat/completions` 路径会导致 404 错误
- 应用启动时会尝试连接 API，路径错误导致初始化失败

---

### 问题 2: 缺少 PORT 环境变量 ⭐

**当前设置**:
```bash
API_PORT="8000"
```

**需要添加**:
```bash
PORT="8000"
```

**原因**:
- Railway 要求应用监听 `PORT` 环境变量指定的端口
- 代码优先使用 `PORT`，如果没有才使用 `API_PORT`
- Railway 可能会动态分配端口，必须设置 `PORT`

---

## ✅ 修复方案

### 方案 1: 修改现有变量（推荐）

在 Railway Raw Editor 中修改：

```bash
LLM_TEMPERATURE="0.7"
LLM_MAX_TOKENS="100000"
API_HOST="0.0.0.0"
API_PORT="8000"
PORT="8000"
ENVIRONMENT="production"
QIANFAN_API_KEY="bce-v3/ALTAK-vnASNnJZQkPchN6JShUdi/38e23c1484e3b2ab42e15dd596dc85fd4328caf4"
QIANFAN_API_URL="https://qianfan.baidubce.com/v2/chat/completions"
QIANFAN_MODEL="glm-5.1"
```

**修改的地方**:
1. 添加 `PORT="8000"`
2. 修改 `QIANFAN_API_URL` 添加 `/chat/completions` 路径

---

### 方案 2: 完整环境变量列表

复制以下内容到 Railway Raw Editor：

```bash
# ==================== 必需变量 ====================
QIANFAN_API_KEY="bce-v3/ALTAK-vnASNnJZQkPchN6JShUdi/38e23c1484e3b2ab42e15dd596dc85fd4328caf4"
QIANFAN_API_URL="https://qianfan.baidubce.com/v2/chat/completions"
QIANFAN_MODEL="glm-5.1"

# ==================== 端口配置 ====================
PORT="8000"
API_HOST="0.0.0.0"
API_PORT="8000"

# ==================== 模型参数 ====================
LLM_TEMPERATURE="0.7"
LLM_MAX_TOKENS="100000"

# ==================== 环境配置 ====================
ENVIRONMENT="production"
LOG_LEVEL="INFO"
```

---

## 📋 操作步骤

### 步骤 1: 打开 Railway Dashboard

1. 访问 https://railway.app/dashboard
2. 找到项目 `novel_make_v1`
3. 点击服务进入详情页

### 步骤 2: 修改环境变量

**方式 A: 使用 Raw Editor（推荐）**

1. 点击 "Variables" 标签
2. 点击 "Raw Editor" 按钮
3. 删除现有内容，粘贴上述完整配置
4. 点击 "Update Variables"

**方式 B: 逐个修改**

1. 点击 "Variables" 标签
2. 找到 `QIANFAN_API_URL`，修改为：
   ```
   https://qianfan.baidubce.com/v2/chat/completions
   ```
3. 点击 "Add Variable"，添加：
   ```
   PORT = 8000
   ```

### 步骤 3: 触发重新部署

修改环境变量后，Railway 会自动触发重新部署。

如果没有自动触发：
1. 点击 "Deployments" 标签
2. 点击最新部署右侧的 "..." 按钮
3. 选择 "Redeploy"

---

## 🧪 验证修复

### 1. 检查部署日志

在 Railway Dashboard 查看部署日志，应该看到：

```
✅ 引擎初始化成功 - 平台: Qianfan
╔═══════════════════════════════════════════╗
║    Novel Creation API v1.0.0              ║
║    AI 小说创作 + 短剧剧本转换               ║
║    Qianfan 版本                           ║
╚═══════════════════════════════════════════╝
🚀 服务启动中...
📍 地址: http://0.0.0.0:8000
🤖 模型: glm-5.1 (Qianfan)
```

### 2. 测试健康检查

部署成功后，运行：

```bash
curl https://novelmakev1-production.up.railway.app/health
```

预期返回：

```json
{
  "status": "healthy",
  "timestamp": "2026-05-09T...",
  "engines": {
    "novel": true,
    "drama": true
  }
}
```

---

## ⚠️ 常见错误

### 错误 1: 404 Not Found

**原因**: `QIANFAN_API_URL` 路径不完整

**解决**: 确保包含 `/chat/completions` 路径

### 错误 2: 502 Bad Gateway

**原因**: 应用未启动或端口配置错误

**解决**:
1. 确认设置了 `PORT` 环境变量
2. 检查部署日志查看具体错误

### 错误 3: 引擎初始化失败

**原因**: API Key 错误或网络问题

**解决**:
1. 确认 API Key 正确
2. 检查 Railway 网络连接

---

## 📊 对比表

| 变量 | 修改前 | 修改后 | 说明 |
|------|--------|--------|------|
| `QIANFAN_API_URL` | `.../v2` | `.../v2/chat/completions` | ✅ 添加完整路径 |
| `PORT` | ❌ 未设置 | ✅ `8000` | ✅ Railway 必需 |

---

## ✅ 修复完成后

1. 应用成功部署
2. 健康检查通过
3. API 可以正常访问
4. 前端可以连接后端

---

**立即修改这两个地方，应用就能正常部署了！**
