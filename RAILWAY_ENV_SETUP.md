# Railway 环境变量配置指南

## 🔑 必需设置的环境变量

在 Railway 控制台设置以下环境变量：

### 百度千帆 API 配置

```bash
QIANFAN_API_KEY=bce-v3/ALTAK-vnASNnJZQkPchN6JShUdi/38e23c1484e3b2ab42e15dd596dc85fd4328caf4
QIANFAN_API_URL=https://qianfan.baidubce.com/v2/chat/completions
QIANFAN_MODEL=glm-5.1
```

### 可选配置

```bash
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=4096
EMBEDDING_MODEL=embedding-v1
ENVIRONMENT=production
LOG_LEVEL=INFO
```

---

## 📝 在 Railway 设置环境变量的步骤

### 方法1：通过 Railway 控制台

1. 登录 Railway：https://railway.app
2. 进入项目：`novelmakev1-production`
3. 点击 **Settings** 标签
4. 找到 **Environment Variables** 部分
5. 点击 **Add Variable** 或 **New Variable**
6. 逐个添加以下变量：

| 变量名 | 值 |
|--------|---|
| QIANFAN_API_KEY | `bce-v3/ALTAK-vnASNnJZQkPchN6JShUdi/38e23c1484e3b2ab42e15dd596dc85fd4328caf4` |
| QIANFAN_API_URL | `https://qianfan.baidubce.com/v2/chat/completions` |
| QIANFAN_MODEL | `glm-5.1` |

7. 点击 **Save** 或 **Apply**
8. Railway 会自动重新部署应用

### 方法2：通过 Railway CLI

如果安装了 Railway CLI，可以使用命令行设置：

```bash
# 登录 Railway
railway login

# 链接到项目
railway link

# 设置环境变量
railway variables set QIANFAN_API_KEY=bce-v3/ALTAK-vnASNnJZQkPchN6JShUdi/38e23c1484e3b2ab42e15dd596dc85fd4328caf4
railway variables set QIANFAN_API_URL=https://qianfan.baidubce.com/v2/chat/completions
railway variables set QIANFAN_MODEL=glm-5.1

# 重新部署
railway up
```

### 方法3：通过 railway.json 配置文件

在 `railway.json` 中添加环境变量（不推荐，因为会暴露 API key）：

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python main.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10,
    "env": {
      "QIANFAN_API_KEY": "your_api_key_here",
      "QIANFAN_API_URL": "https://qianfan.baidubce.com/v2/chat/completions",
      "QIANFAN_MODEL": "glm-5.1"
    }
  }
}
```

⚠️ **注意：** 不推荐在 `railway.json` 中直接写 API key，因为这会被提交到 GitHub 公开仓库。

---

## ✅ 验证环境变量是否设置成功

设置完成后，应用启动日志应该显示：

```
✅ 引擎初始化成功 - 平台: Qianfan
🤖 模型: glm-5.1 (Qianfan)
```

如果看到：

```
⚠️ 引擎初始化失败: ...
```

说明环境变量未正确设置。

---

## 🔍 常见问题

### 问题1：环境变量设置后仍显示 "Qianfan (no API key)"

**原因：** 环境变量名称错误或未生效

**解决方案：**
1. 确认变量名是 `QIANFAN_API_KEY`（不是 `API_KEY`）
2. 确认没有多余的空格或引号
3. 重新部署应用

### 问题2：应用启动后 API 调用失败

**原因：** API key 格式错误或过期

**解决方案：**
1. 检查 API key 是否正确
2. 登录百度千帆控制台验证 API key 是否有效
3. 检查 API URL 是否正确

### 问题3：Railway 部署后无法访问

**原因：** 健康检查失败或应用崩溃

**解决方案：**
1. 查看 Railway 部署日志
2. 确认应用监听的端口正确（应该是 `PORT` 环境变量）
3. 检查是否有未捕获的异常

---

## 📚 相关文档

- [Railway 环境变量文档](https://docs.railway.app/develop/variables)
- [百度千帆 API 文档](https://cloud.baidu.com/doc/WENXINWORKSHOP/index.html)
- [项目系统分析报告](./SYSTEM_ANALYSIS.md)