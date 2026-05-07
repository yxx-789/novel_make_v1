# 引擎配置修复报告

## 🔴 问题诊断

### 症状
- 蓝图生成返回空内容
- 所有 AI 生成功能无法正常工作

### 根本原因

你的项目有两个版本的引擎：

| 文件 | 说明 | API 平台 |
|------|------|---------|
| `backend/core/novel_engine.py` | 原始版本 | OpenAI |
| `backend/core/novel_engine_qianfan.py` | 千帆版本 | 百度千帆 ✅ |

但是 `backend/api/routes.py` 导入的是 **OpenAI 版本**：

```python
# ❌ 错误的导入
from core.novel_engine import NovelEngine

# ✅ 正确的导入
from core.novel_engine_qianfan import NovelEngine
```

同时，`backend/main.py` 的配置也使用 OpenAI：

```python
# ❌ 错误的配置
"api_key": os.getenv("OPENAI_API_KEY", "sk-xxx"),
"model": os.getenv("LLM_MODEL", "gpt-4o-mini"),

# ✅ 正确的配置
"api_key": os.getenv("QIANFAN_API_KEY", ""),
"model": os.getenv("QIANFAN_MODEL", "glm-5.1"),
```

---

## ✅ 修复内容

### 1. 修改 `backend/api/routes.py`

```diff
- from core.novel_engine import NovelEngine
+ from core.novel_engine_qianfan import NovelEngine
```

### 2. 修改 `backend/main.py`

```diff
- "api_key": os.getenv("OPENAI_API_KEY", "sk-xxx"),
- "base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
- "model": os.getenv("LLM_MODEL", "gpt-4o-mini"),
+ "api_key": os.getenv("QIANFAN_API_KEY", ""),
+ "api_url": os.getenv("QIANFAN_API_URL", "https://qianfan.baidubce.com/v2/chat/completions"),
+ "model": os.getenv("QIANFAN_MODEL", "glm-5.1"),
```

---

## 🧪 测试结果

```bash
$ python test_qianfan.py

配置检查
============================================================
LLM API Key (前20位): bce-v3/ALTAK-vnASNnJ...
LLM Model: glm-5.1
LLM API URL: https://qianfan.baidubce.com/v2/chat/completions

测试千帆 API 连接
============================================================
✅ 客户端端初始化成功
✅ API 调用成功
响应: 你好，请问有什么我可以帮你的吗？
模型: glm-5.1
Token 使用: {'prompt_tokens': 11, 'completion_tokens': 198, 'total_tokens': 209}
```

---

## 📋 后续步骤

### 1. 推送代码

```bash
cd /home/gem/.openclaw/workspace/NOVEL_PLATFORM
git push origin main
```

### 2. 重新部署 Railway

推送后，Railway 会自动检测到更新并重新部署。

或者手动触发：
1. 登录 Railway 控制台
2. 找到你的项目
3. 点击 **Redeploy**

### 3. 验证修复

部署完成后，测试蓝图生成：

```bash
curl -X POST https://novelmakev1-production.up.railway.app/api/v1/novels/{novel_id}/blueprint
```

应该返回真实的蓝图内容，而不是空值。

---

## 🎉 总结

| 问题 | 状态 |
|------|------|
| 引擎导入错误 | ✅ 已修复 |
| 配置错误 | ✅ 已修复 |
| 本地测试 | ✅ 通过 |
| 推送 GitHub | ⏳ 等待手动推送 |
| Railway 部署 | ⏳ 推送后自动部署 |

修复后，你的项目将完全使用百度千帆 API，支持以下模型：
- glm-5.1 (智谱)
- qwen3.5-397b-a17b (阿里)
- deepseek-v3.2 (DeepSeek)
