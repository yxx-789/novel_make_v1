# 🚀 Railway 部署指南

## 📋 前提条件

- ✅ GitHub账号（已有）
- ✅ 项目已上传到GitHub（已完成）
- ✅ 千帆API Key（已有）

---

## 第一步：注册 Railway 账号

### 1. 访问 Railway

打开浏览器，访问：https://railway.app/

### 2. 使用 GitHub 登录

- 点击右上角的 **"Start a New Project"**
- 选择 **"Login with GitHub"**
- 授权 Railway 访问你的 GitHub

### 3. 验证账号

- Railway 可能需要验证邮箱
- 检查邮箱并点击验证链接

---

## 第二步：创建项目

### 1. 新建项目

登录后，点击 **"New Project"** 按钮

### 2. 选择部署方式

选择 **"Deploy from GitHub repo"**

### 3. 授权仓库

- 点击 **"Configure GitHub App"**
- 选择授权：
  - ✅ **All repositories**（推荐）
  - 或 **Only select repositories** → 选择 `novel_make_v1`

### 4. 选择仓库

- 选择：`yxx-789/novel_make_v1`
- 点击 **"Deploy Now"**

---

## 第三步：配置项目

### 1. 设置根目录

Railway 会自动检测，但需要确认：

- 点击项目名称（如：`novel_make_v1`）
- 点击 **"Settings"** 标签
- 找到 **"Root Directory"**
- 设置为：`backend`
- 点击 **"Save"**

### 2. 配置环境变量

在 **"Variables"** 标签页，添加以下变量：

```bash
# 千帆API配置
OPENAI_API_KEY = bce-v3/ALTAK-vnASNnJZQkPchN6JShUdi/38e23c1484e3b2ab42e15dd596dc85fd4328caf4
OPENAI_BASE_URL = https://qianfan.baidubce.com/v2
LLM_MODEL = ernie-4.0-8k

# 或者使用DeepSeek
# OPENAI_BASE_URL = https://api.deepseek.com/v1
# LLM_MODEL = deepseek-chat

# 其他配置
LLM_TEMPERATURE = 0.7
LLM_MAX_TOKENS = 4096
API_HOST = 0.0.0.0
API_PORT = 8000
ENVIRONMENT = production
```

**添加方式**：
1. 点击 **"New Variable"**
2. 输入变量名和值
3. 点击 **"Add"**
4. 重复以上步骤添加所有变量

或者点击 **"Raw Editor"**，一次性粘贴所有变量。

### 3. 保存配置

点击右上角的 **"Save"** 按钮

---

## 第四步：部署

### 1. 触发部署

配置保存后，Railway 会自动开始部署

### 2. 查看日志

- 点击 **"Deployments"** 标签
- 点击正在进行的部署
- 查看 **"Build Logs"** 和 **"Deploy Logs"**

### 3. 等待完成

⏳ 部署大约需要 2-5 分钟

**成功标志**：
- ✅ 看到 **"SUCCESS"** 标签
- ✅ 日志显示：`Application startup complete`

### 4. 查看应用URL

- 点击 **"Settings"** 标签
- 找到 **"Domains"** 部分
- 点击 **"Generate Domain"**
- 你会得到类似这样的URL：
  ```
  https://novel-make-v1-production.up.railway.app
  ```

---

## 第五步：测试后端API

### 1. 测试健康检查

在浏览器中访问：
```
https://your-app.up.railway.app/health
```

**预期返回**：
```json
{
  "status": "healthy",
  "timestamp": "2024-...",
  "engines": {
    "novel": true,
    "drama": true
  }
}
```

### 2. 测试API文档

访问：
```
https://your-app.up.railway.app/docs
```

**应该看到**：Swagger API 文档页面

### 3. 测试创建小说

使用 curl 或 Postman：

```bash
curl -X POST https://your-app.up.railway.app/api/v1/novels \
  -H "Content-Type: application/json" \
  -d '{
    "title": "测试小说",
    "genre": "玄幻",
    "topic": "一个修仙故事",
    "total_chapters": 5
  }'
```

**预期返回**：
```json
{
  "success": true,
  "message": "小说创建成功",
  "data": { ... }
}
```

---

## 第六步：配置前端

### 1. 获取后端URL

从 Railway 复制你的应用 URL，例如：
```
https://novel-make-v1-production.up.railway.app
```

### 2. 在 Streamlit Cloud 配置环境变量

登录 Streamlit Cloud：
1. 进入你的应用页面
2. 点击 **"Settings"** ⚙️
3. 点击 **"Secrets"** 标签
4. 修改 `API_BASE_URL`：

```toml
API_BASE_URL = "https://novel-make-v1-production.up.railway.app"
OPENAI_API_KEY = "bce-v3/ALTAK-vnASNnJZQkPchN6JShUdi/38e23c1484e3b2ab42e15dd596dc85fd4328caf4"
LLM_MODEL = "ernie-4.0-8k"
```

5. 点击 **"Save"**

### 3. 重启前端

在 Streamlit Cloud 点击 **"Reboot"** 按钮

---

## 第七步：完整测试

### 1. 访问前端

```
https://novel-make-v1.streamlit.app
```

### 2. 测试系统设置

- 进入 **⚙️ 系统设置** 页面
- 点击 **"测试连接"**
- 应该显示：✅ 连接成功

### 3. 测试创建小说

- 进入 **✍️ 小说创作** 页面
- 创建一本小说
- 生成蓝图
- 生成章节

---

## 🐛 常见问题

### 问题1：部署失败

**原因**：依赖缺失或配置错误

**解决**：
1. 查看 Build Logs
2. 检查 `requirements.txt` 是否完整
3. 确认 Python 版本（需要 3.10+）

### 问题2：API连接失败

**原因**：环境变量未设置或错误

**解决**：
1. 检查 Railway 的 Variables 配置
2. 确认 `OPENAI_API_KEY` 正确
3. 查看日志中的错误信息

### 问题3：千帆API调用失败

**原因**：API Key 或 URL 配置错误

**解决**：
```bash
# 正确的千帆配置
OPENAI_BASE_URL = https://qianfan.baidubce.com/v2  # 注意：不是 /chat/completions
LLM_MODEL = ernie-4.0-8k  # 或其他支持的模型
```

### 问题4：前端无法连接后端

**原因**：CORS 配置或 URL 错误

**解决**：
1. 确认后端 URL 正确（包含 https://）
2. 检查后端 CORS 配置（已默认允许所有来源）
3. 在 Streamlit Cloud 重新配置 `API_BASE_URL`

---

## 💰 费用说明

### Railway 免费额度

- **$5 免费额度/月**
- 约 500 小时运行时间
- 对于测试和小规模使用足够

### 付费套餐

- **Hobby**: $5/月
- **Pro**: $20/月
- 如需更多资源，可以升级

---

## 📊 监控和维护

### 查看日志

在 Railway 控制台：
- 点击部署 → **"Deploy Logs"**
- 实时查看运行日志

### 监控性能

- **Metrics** 标签：CPU、内存使用
- **Usage** 标签：费用统计

### 自动部署

每次向 GitHub 推送代码，Railway 会自动重新部署

---

## 🎯 完整部署清单

- [ ] 注册 Railway 账号
- [ ] 创建新项目
- [ ] 选择 GitHub 仓库 `yxx-789/novel_make_v1`
- [ ] 设置 Root Directory 为 `backend`
- [ ] 配置环境变量（千帆 API Key）
- [ ] 等待部署完成
- [ ] 生成应用域名
- [ ] 测试健康检查 `/health`
- [ ] 在 Streamlit Cloud 配置 `API_BASE_URL`
- [ ] 重启前端应用
- [ ] 完整功能测试

---

## 📞 获取帮助

- 📚 [Railway 文档](https://docs.railway.app/)
- 💬 [Railway Discord](https://discord.gg/railway)
- 🐛 项目 Issues: https://github.com/yxx-789/novel_make_v1/issues

---

**🎉 部署成功后，你的AI小说创作平台就可以在线使用了！**
