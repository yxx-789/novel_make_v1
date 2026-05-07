# 🚀 Railway 后端部署完整检查清单

## 📋 部署前准备

### ✅ 已确认的信息

- [x] GitHub仓库：`https://github.com/yxx-789/novel_make_v1`
- [x] 千帆API Key：请在 Railway 控制台的 Environment Variables 中配置 `QIANFAN_API_KEY`
- [x] 千帆API URL：`https://qianfan.baidubce.com/v2`
- [x] 项目后端目录：`backend/`

---

## 第一步：注册Railway账号（2分钟）

### 操作步骤

1. **访问Railway**
   - 打开浏览器
   - 访问：https://railway.app/

2. **登录**
   - 点击右上角的 **"Login"** 按钮
   - 选择 **"Login with GitHub"**

3. **授权**
   - 点击 **"Authorize Railway"**
   - 允许Railway访问你的GitHub账号

4. **验证邮箱**
   - 检查邮箱
   - 点击验证链接

### ✅ 完成标志

看到Railway控制台页面，显示 **"New Project"** 按钮

---

## 第二步：创建新项目（1分钟）

### 操作步骤

1. **点击创建项目**
   - 在控制台页面
   - 点击 **"New Project"** 按钮（大的蓝色按钮）

2. **选择部署方式**
   - 选择 **"Deploy from GitHub repo"**
   - 如果提示授权，选择 **"All repositories"** 或 **"Only select repositories"**

3. **选择仓库**
   - 找到并选择：`yxx-789/novel_make_v1`
   - 点击仓库名称

### ✅ 完成标志

看到项目设置页面，显示 **"Configure"** 选项

---

## 第三步：配置项目（3分钟）⚠️ 重要！

### 1. 设置根目录

**非常重要！必须设置！**

1. 在项目页面，点击 **"Settings"** 标签
2. 向下滚动找到 **"Root Directory"**
3. 点击 **"Edit"**
4. 输入：`backend`
5. 点击 **"Save"**

**⚠️ 注意**：
- 必须设置为 `backend`
- 不是 `novel_make_v1/backend`
- 不是 `/backend`

### 2. 配置环境变量

**必须配置，否则部署失败！**

1. 点击 **"Variables"** 标签
2. 点击 **"New Variable"** 按钮
3. 逐个添加以下变量：

#### 必需的环境变量

```bash
# 千帆API配置
OPENAI_API_KEY = your_qianfan_api_key_here  # 替换为你的千帆 API Key（从环境变量读取）
OPENAI_BASE_URL = https://qianfan.baidubce.com/v2
LLM_MODEL = ernie-4.0-8k
LLM_TEMPERATURE = 0.7
LLM_MAX_TOKENS = 4096

# 服务配置
API_HOST = 0.0.0.0
API_PORT = 8000
ENVIRONMENT = production
```

#### 添加方法

**方式一：逐个添加**（推荐新手）
1. 点击 **"New Variable"**
2. 输入变量名：`OPENAI_API_KEY`
3. 输入值：`your_qianfan_api_key_here`（替换为你的真实 API Key）
4. 点击 **"Add"**
5. 重复以上步骤

**方式二：批量添加**（高级用户）
1. 点击 **"Raw Editor"**
2. 粘贴所有变量（每行一个，格式：`KEY=value`）
3. 点击 **"Save"**

### ✅ 完成标志

- Root Directory 显示为 `backend`
- Variables 页面显示所有环境变量

---

## 第四步：触发部署（1分钟）

### 操作步骤

1. **返回项目主页**
   - 点击项目名称（左上角）

2. **触发部署**
   - 配置保存后，Railway会自动开始部署
   - 或点击 **"Deploy"** 按钮

### ✅ 完成标志

看到部署进度，状态变为 **"Building"**

---

## 第五步：等待部署完成（3-5分钟）

### 监控部署进度

1. **查看部署状态**
   - 点击正在进行的部署
   - 查看 **"Build Logs"**

2. **正常流程**
   ```
   Installing dependencies...
   Collecting fastapi...
   Successfully installed...
   Starting deployment...
   Application startup complete.
   ```

3. **成功标志**
   - 状态显示：**"SUCCESS"** ✅
   - 日志显示：`Application startup complete`

### ❌ 如果失败

**常见错误及解决**：

| 错误信息 | 原因 | 解决方法 |
|---------|------|---------|
| `Module not found` | 依赖缺失 | 检查 `requirements.txt` |
| `API_KEY not set` | 环境变量未设置 | 检查 Variables 配置 |
| `Port 8000 not available` | 端口问题 | 确认 `API_PORT=8000` |

**查看日志**：
- 点击部署 → **"Deploy Logs"**
- 复制错误信息并告诉我

---

## 第六步：生成域名并测试（2分钟）

### 1. 生成域名

1. 部署成功后，点击 **"Settings"** 标签
2. 向下滚动到 **"Domains"** 部分
3. 点击 **"Generate Domain"**
4. 等待几秒钟，你会得到一个URL：
   ```
   https://novel-make-v1-production.up.railway.app
   ```
   或类似的地址

### 2. 测试API

#### 测试健康检查

在浏览器中访问：
```
https://你的域名.up.railway.app/health
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

#### 测试API文档

访问：
```
https://你的域名.up.railway.app/docs
```

**应该看到**：Swagger API 文档页面

#### 测试创建小说（可选）

使用浏览器或Postman测试：
```bash
POST https://你的域名.up.railway.app/api/v1/novels
Content-Type: application/json

{
  "title": "测试小说",
  "genre": "玄幻",
  "topic": "一个修仙故事",
  "total_chapters": 5
}
```

### ✅ 完成标志

- 成功访问 `/health` 端点
- 看到 Swagger API 文档
- 创建小说成功

---

## 第七步：记录后端URL

**重要！保存你的后端URL！**

你的后端地址格式：
```
https://novel-make-v1-production.up.railway.app
```

**复制并保存这个URL**，后面配置前端时会用到！

---

## 📊 部署状态检查清单

完成以下所有步骤后，部署成功：

- [ ] 注册Railway账号
- [ ] 创建新项目
- [ ] 设置 Root Directory 为 `backend`
- [ ] 添加所有环境变量
- [ ] 触发部署
- [ ] 等待部署成功（状态：SUCCESS）
- [ ] 生成域名
- [ ] 测试 `/health` 端点成功
- [ ] 记录后端URL

---

## 🐛 遇到问题？

### 常见问题快速解决

**问题1：看不到仓库**
- 解决：点击 "Configure GitHub App"，重新授权

**问题2：部署失败**
- 解决：查看 Deploy Logs，复制错误信息给我

**问题3：API返回错误**
- 解决：检查环境变量是否正确设置

**问题4：域名无法访问**
- 解决：等待1-2分钟DNS生效，或重新生成域名

---

## 📞 需要帮助？

- 📚 查看 `RAILWAY_DEPLOY.md` 详细文档
- 💬 随时告诉我遇到的问题
- 🔗 Railway文档：https://docs.railway.app/

---

## 🎯 下一步

部署成功后：

1. **保存后端URL**
2. **配置Streamlit Cloud前端**
3. **完整系统测试**

---

**🎉 恭喜！后端部署完成后，就可以配置前端了！**
