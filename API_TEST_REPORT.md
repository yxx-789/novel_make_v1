# 🔴 API 连接测试报告

**测试时间**: 2026-05-09 13:33  
**测试目标**: https://novelmakev1-production.up.railway.app

---

## ❌ 测试结果：失败

### 错误信息

```json
{
  "status": "error",
  "code": 502,
  "message": "Application failed to respond",
  "request_id": "YZXdVVGMSIq8Rz2XacI7Nw"
}
```

---

## 🔍 问题诊断

### 1. 连接状态
✅ **SSL/TLS 连接**: 正常  
✅ **DNS 解析**: 正常 (66.33.22.73)  
✅ **Railway 边缘节点**: 正常 (asia-southeast1-eqsg3a)  
❌ **应用响应**: 失败 (502 Bad Gateway)

### 2. 测试的端点
- `/health` - ❌ 502 错误
- `/` - ❌ 502 错误
- `/api/v1/novels` - ❌ 超时
- `/docs` - ❌ 502 错误

---

## 🚨 根本原因分析

**502 Bad Gateway** 表示 Railway 无法连接到你的应用，可能原因：

### 1. **环境变量未设置** ⭐ 最可能
- `QIANFAN_API_KEY` 未设置
- `QIANFAN_API_URL` 未设置
- `QIANFAN_MODEL` 未设置
- 应用启动时找不到 API Key 导致失败

### 2. **应用启动失败**
- 依赖项安装失败
- 代码语法错误
- 导入模块失败

### 3. **端口配置错误**
- 应用监听的端口与 Railway 期望的不一致
- Railway 默认使用 `PORT` 环境变量

### 4. **启动命令问题**
- `railway.json` 中的启动命令不正确
- 应用启动脚本有误

---

## 🔧 解决步骤

### 步骤 1: 检查 Railway 日志

1. 打开 Railway Dashboard: https://railway.app/dashboard
2. 找到项目 `novel_make_v1`
3. 点击服务查看 **Deploy Logs**
4. 查看错误信息

**常见错误模式**：
```
ModuleNotFoundError: No module named 'xxx'
KeyError: 'QIANFAN_API_KEY'
Port 8000 is already in use
```

---

### 步骤 2: 设置环境变量 ⭐

在 Railway Dashboard 中设置以下环境变量：

```bash
# 必需变量
QIANFAN_API_KEY=bce-v3/ALTAK-vnASNnJZQkPchN6JShUdi/38e23c1484e3b2ab42e15dd596dc85fd4328caf4
QIANFAN_API_URL=https://qianfan.baidubce.com/v2/chat/completions
QIANFAN_MODEL=glm-5.1

# 服务配置
PORT=8000
ENVIRONMENT=production
API_HOST=0.0.0.0
API_PORT=8000

# 日志配置
LOG_LEVEL=INFO
```

**设置方法**：
1. Railway Dashboard → 项目 → 服务
2. 点击 "Variables" 标签
3. 点击 "Add Variable"
4. 逐个添加上述变量
5. 保存后自动触发重新部署

---

### 步骤 3: 检查启动命令

确认 `backend/railway.json` 配置正确：

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python main.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**验证**：
- ✅ 启动命令应为 `python main.py`（在 backend 目录下）
- ✅ 或者使用 `python backend/main.py`（如果在根目录）

---

### 步骤 4: 使用测试版本诊断

如果主应用启动失败，可以先部署测试版本：

**修改启动命令**：
```json
{
  "startCommand": "python main_railway_test.py"
}
```

测试版本是精简版，更容易启动成功。

---

### 步骤 5: 检查端口监听

应用必须监听 `PORT` 环境变量指定的端口：

```python
# backend/main.py 中应有：
port = int(os.getenv("PORT", "8000"))
uvicorn.run(app, host="0.0.0.0", port=port)
```

---

## 📋 快速检查清单

- [ ] 在 Railway 设置了所有必需环境变量
- [ ] 检查了 Railway 部署日志
- [ ] 确认启动命令正确
- [ ] 应用代码能正常启动（本地测试）
- [ ] 端口配置正确

---

## 🧪 本地测试

在本地测试应用是否能正常启动：

```bash
cd /home/gem/.openclaw/workspace/NOVEL_PLATFORM/backend

# 设置环境变量
export QIANFAN_API_KEY="bce-v3/ALTAK-vnASNnJZQkPchN6JShUdi/38e23c1484e3b2ab42e15dd596dc85fd4328caf4"
export QIANFAN_API_URL="https://qianfan.baidubce.com/v2/chat/completions"
export QIANFAN_MODEL="glm-5.1"
export PORT="8000"

# 启动应用
python main.py
```

预期输出：
```
╔═══════════════════════════════════════════╗
║    Novel Creation API v1.0.0              ║
║    AI 小说创作 + 短剧剧本转换               ║
║    Qianfan 版本                           ║
╚═══════════════════════════════════════════╝

🚀 服务启动中...
📍 地址: http://0.0.0.0:8000
📚 API文档: http://0.0.0.0:8000/docs
```

然后测试：
```bash
curl http://localhost:8000/health
```

---

## 🎯 下一步行动

### 立即执行（优先级 P0）：

[::button-group layout="flow"]
  [::button label="查看 Railway 日志" query_send="帮我分析 Railway 日志" style="primary"]
  [::button label="设置环境变量" query_send="生成环境变量配置" style="primary"]
  [::button label="本地测试启动" query_send="本地测试应用启动" style="primary"]
  [::button label="切换到测试版本" query_send="使用 main_railway_test.py 部署" style="primary"]
[::button-group/]

---

## 📞 获取帮助

如果以上步骤都无法解决问题，请提供：
1. Railway Deploy Logs 的完整输出
2. Railway Build Logs 的完整输出
3. 环境变量列表（隐藏敏感信息）

---

**测试结论**: API 无法访问，应用未正常启动。需要检查 Railway 配置和日志。
