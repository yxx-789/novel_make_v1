# 🚀 Streamlit Cloud 部署指南

## 📋 前提条件

1. ✅ GitHub账号（已有）
2. ✅ Streamlit Cloud账号（使用GitHub登录）
3. ✅ 项目已上传到GitHub（已完成）

---

## 🎯 第一步：创建 Streamlit Cloud 账号

1. 访问 [Streamlit Cloud](https://streamlit.io/cloud)
2. 点击 **"Sign up"** 或 **"Log in with GitHub"**
3. 使用你的GitHub账号登录
4. 授权Streamlit访问你的GitHub仓库

---

## 🚀 第二步：部署应用到 Streamlit Cloud

### 方式一：通过网页控制台（推荐）

1. **登录 Streamlit Cloud**
   - 访问：https://share.streamlit.io/
   - 点击右上角的 **"Log in with GitHub"**

2. **创建新应用**
   - 点击 **"New app"** 按钮
   - 填写信息：
     - **Repository**: `yxx-789/novel_make_v1`
     - **Branch**: `main`
     - **Main file path**: `frontend/app.py`
     - **App name**: `novel-make-v1`（自定义）

3. **配置环境变量**（重要！）
   - 点击 **"Advanced settings"**
   - 添加环境变量：
     ```
     API_BASE_URL = https://your-backend-api.com
     OPENAI_API_KEY = sk-your-api-key-here
     LLM_MODEL = gpt-4o-mini
     ```

4. **点击 Deploy**
   - 等待3-5分钟
   - 看到绿色勾勾 ✅ 表示部署成功

5. **获取应用链接**
   - 格式：`https://novel-make-v1.streamlit.app`
   - 可以分享给其他人使用！

---

### 方式二：通过命令行（高级用户）

```bash
# 安装 Streamlit CLI
pip install streamlit-cli

# 登录
streamlit login

# 部署
streamlit deploy frontend/app.py --server.port 8501
```

---

## ⚙️ 第三步：配置后端API（重要！）

### 问题：Streamlit Cloud只能部署前端

**解决方案有两种：**

### **方案A：使用Streamlit Cloud + 独立后端**

1. **部署后端到云服务器**（二选一）：
   - [Railway](https://railway.app/)（推荐）
   - [Render](https://render.com/)
   - [Fly.io](https://fly.io/)
   - [Heroku](https://heroku.com/)

2. **修改前端配置**：
   ```python
   # frontend/utils/config.py
   class Config:
       API_BASE_URL = "https://your-backend-url.com"  # 改为你的后端地址
   ```

3. **在Streamlit Cloud设置环境变量**：
   ```
   API_BASE_URL = https://your-backend-url.com
   ```

---

### **方案B：使用Streamlit Cloud内置后端（简化版）**

修改 `app.py`，将后端逻辑集成到Streamlit应用中：

```python
import streamlit as st
from backend.main import app as fastapi_app
# ... 直接在Streamlit中调用后端函数
```

**优点**：一个应用包含前后端  
**缺点**：不适合高并发，适合演示和轻量使用

---

## 🔧 第四步：配置环境变量

### 在Streamlit Cloud控制台设置：

1. 进入你的应用页面
2. 点击右上角 **"Settings"** ⚙️
3. 点击 **"Secrets"** 标签
4. 添加环境变量（TOML格式）：
   ```toml
   API_BASE_URL = "https://your-backend-api.com"
   OPENAI_API_KEY = "sk-your-api-key-here"
   LLM_MODEL = "gpt-4o-mini"
   LLM_TEMPERATURE = 0.7
   ```
5. 点击 **"Save"**
6. 应用会自动重启

---

## 📊 第五步：验证部署

1. **访问应用链接**
   - 格式：`https://your-app-name.streamlit.app`

2. **检查功能**
   - ✅ 首页加载正常
   - ✅ 小说创作页面可以访问
   - ✅ API连接正常（系统设置页面）

3. **查看日志**
   - 在Streamlit Cloud控制台
   - 点击 **"Logs"** 查看运行日志

---

## 🐛 常见问题排查

### 问题1：应用启动失败

**原因**：依赖缺失  
**解决**：
```bash
# 检查 requirements.txt 是否包含所有依赖
cat frontend/requirements.txt
```

### 问题2：API连接失败

**原因**：后端未部署或地址错误  
**解决**：
1. 确认后端已部署到云服务器
2. 检查 `API_BASE_URL` 环境变量是否正确
3. 在"系统设置"页面测试连接

### 问题3：环境变量未生效

**原因**：Secrets格式错误  
**解决**：
```toml
# 正确格式
OPENAI_API_KEY = "sk-xxx"  # 注意引号
# 错误格式
OPENAI_API_KEY = sk-xxx    # 缺少引号
```

### 问题4：应用运行缓慢

**原因**：免费版资源有限  
**解决**：
1. 升级到Streamlit Cloud Pro
2. 优化代码（减少重复计算）
3. 使用缓存 `@st.cache_data`

---

## 💡 优化建议

### 1. 添加缓存提升性能

```python
import streamlit as st

@st.cache_data(ttl=3600)
def get_novels():
    # 缓存小说列表1小时
    return api_client.get_novels()
```

### 2. 添加错误处理

```python
try:
    result = api_client.create_novel(...)
    st.success("创建成功！")
except Exception as e:
    st.error(f"创建失败: {e}")
    st.info("请检查API配置")
```

### 3. 添加加载动画

```python
with st.spinner("正在生成..."):
    result = api_client.generate_blueprint(novel_id)
```

---

## 📈 监控和分析

### 1. 查看应用统计

在Streamlit Cloud控制台：
- **Views**: 访问次数
- **Uptime**: 在线时长
- **Memory**: 内存使用

### 2. 设置告警

- 应用崩溃时发送邮件通知
- 在 Settings → Notifications 中配置

---

## 🔄 更新部署

### 自动更新（推荐）

当你向GitHub推送新代码时，Streamlit Cloud会自动重新部署：

```bash
git add .
git commit -m "Update: 修复XXX问题"
git push origin main
```

### 手动更新

在Streamlit Cloud控制台：
1. 进入应用页面
2. 点击 **"Reboot"** 按钮

---

## 🎨 自定义域名（高级）

1. 在Streamlit Cloud控制台
2. Settings → Custom domain
3. 添加你的域名：`novel.yourdomain.com`
4. 配置DNS CNAME记录指向：`your-app.streamlit.app`

---

## 📞 获取帮助

- 📚 [Streamlit文档](https://docs.streamlit.io/)
- 💬 [Streamlit论坛](https://discuss.streamlit.io/)
- 🐛 [GitHub Issues](https://github.com/yxx-789/novel_make_v1/issues)

---

## ✅ 部署检查清单

- [ ] GitHub账号已登录Streamlit Cloud
- [ ] 仓库 `yxx-789/novel_make_v1` 已授权
- [ ] 创建新应用，选择 `frontend/app.py`
- [ ] 配置环境变量（API_BASE_URL等）
- [ ] 点击Deploy并等待成功
- [ ] 访问应用链接测试功能
- [ ] 在"系统设置"页面测试API连接
- [ ] 查看日志确认无错误

---

**🎉 部署成功后，你的AI小说创作平台就可以在线使用了！**
