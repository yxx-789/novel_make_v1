# Streamlit 前端部署指南

## 部署到 Streamlit Cloud

### 1. 准备工作

确保前端代码已推送到 GitHub。

### 2. 设置环境变量

在 Streamlit Cloud 中设置以下环境变量：

```bash
API_BASE_URL=https://novelmakev1-production.up.railway.app
```

### 3. 部署步骤

#### 方式 A: 通过 Streamlit Cloud 界面

1. 访问 https://share.streamlit.io
2. 点击 "New app"
3. 填写信息：
   - **Repository**: `yxx-789/novel_make_v1`
   - **Branch**: `main`
   - **Main file path**: `frontend/app.py`
   - **App URL**: `novel-make-v1` (或其他名称)
4. 点击 "Advanced settings"
5. 在 "Environment variables" 中添加：
   - `API_BASE_URL=https://novelmakev1-production.up.railway.app`
6. 点击 "Deploy"

#### 方式 B: 通过配置文件

在项目根目录创建 `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = true
maxUploadSize = 200

[runner]
magicEnabled = true
```

---

## 本地开发

### 1. 安装依赖

```bash
cd frontend
pip install -r requirements.txt
```

### 2. 设置环境变量

```bash
# Linux/Mac
export API_BASE_URL=http://localhost:8000

# Windows
set API_BASE_URL=http://localhost:8000
```

### 3. 启动后端

```bash
cd backend
python main.py
```

### 4. 启动前端

```bash
cd frontend
streamlit run app.py
```

访问: http://localhost:8501

---

## 环境变量说明

| 变量名 | 说明 | 默认值 | 必需 |
|--------|------|--------|------|
| `API_BASE_URL` | 后端 API 地址 | `http://localhost:8000` | ✅ |
| `LLM_MODEL` | 默认 LLM 模型 | `glm-5.1` | ❌ |

---

## 自动检测环境

代码会自动检测运行环境：

```python
if os.environ.get('STREAMLIT_SERVER_HEADLESS') == 'true':
    # 生产环境 - Railway
    API_BASE_URL = os.environ.get('API_BASE_URL', 'https://novelmakev1-production.up.railway.app')
else:
    # 开发环境
    API_BASE_URL = os.environ.get('API_BASE_URL', 'http://localhost:8000')
```

这意味着：
- **本地开发**: 自动连接 `http://localhost:8000`
- **Streamlit Cloud**: 自动连接 Railway 后端

---

## 故障排查

### 问题 1: 前端无法连接后端

**症状**: 显示 "Connection refused" 或 "Network Error"

**解决方案**:
1. 确认后端已部署且健康检查通过
2. 检查环境变量 `API_BASE_URL` 是否正确
3. 在 Streamlit Cloud 中查看日志

### 问题 2: API 调用超时

**症状**: 显示 "Timeout after 600s"

**解决方案**:
1. 检查后端日志，确认 API 调用是否正常
2. 检查千帆 API 是否可用
3. 增加超时时间（在 `frontend/utils/api.py` 中修改）

### 问题 3: 页面样式异常

**症状**: CSS 样式不生效

**解决方案**:
1. 检查 `frontend/utils/global_styles.py` 是否正确导入
2. 清除浏览器缓存
3. 检查 Streamlit 版本是否兼容

---

## 性能优化

### 1. 缓存 API 响应

```python
@st.cache_data(ttl=300)  # 缓存 5 分钟
def get_novels_cached():
    return api_client.get_novels()
```

### 2. 使用会话状态

```python
if 'novels' not in st.session_state:
    st.session_state.novels = api_client.get_novels()
```

### 3. 异步加载

```python
with st.spinner('加载中...'):
    novels = api_client.get_novels()
```

---

## 更新部署

当代码更新后：

1. 推送到 GitHub
2. Streamlit Cloud 会自动检测到更新
3. 点击 "Deploy" 按钮重新部署
4. 等待部署完成（通常 1-2 分钟）

---

## 监控和日志

### 查看日志

在 Streamlit Cloud 中：
1. 进入应用页面
2. 点击 "Logs" 标签
3. 查看实时日志

### 设置日志级别

在 `.streamlit/config.toml` 中：

```toml
[logger]
level = "info"
```

---

## 安全建议

1. **不要在前端存储敏感信息**: API Key 应该在后端管理
2. **使用 HTTPS**: Streamlit Cloud 默认使用 HTTPS
3. **限制访问**: 可以设置密码保护（Streamlit Cloud 功能）
4. **定期更新依赖**: 保持 `requirements.txt` 中的包为最新版本
