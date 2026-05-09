# 手动推送代码指南

## 🚨 当前问题

网络连接不稳定，无法从服务器自动推送到 GitHub。

**待推送的提交：**
```
790d59b - Chore: Clean up project structure
a9d49ce - Change start command to use Railway test application
```

---

## 📝 手动推送步骤

### 方法1：在本地机器推送

如果你在本地机器上有项目的克隆，可以直接推送：

```bash
# 1. 进入项目目录
cd path/to/novel_make_v1

# 2. 拉取最新代码
git pull origin main

# 3. 检查是否有待推送的提交
git log origin/main..HEAD --oneline

# 4. 推送代码
git push origin main
```

### 方法2：重新克隆并推送

```bash
# 1. 克隆仓库
git clone https://github.com/yxx-789/novel_make_v1.git
cd novel_make_v1

# 2. 配置 Git
git config user.name "xingyao"
git config user.email "xingyao@baidu.com"

# 3. 进行修改
# （参考下面的修改内容）

# 4. 提交并推送
git add .
git commit -m "Chore: Clean up project structure"
git push origin main
```

---

## 📋 需要推送的修改内容

### 1. 删除多余的 main 文件

删除以下文件：
- `backend/main_fixed.py`
- `backend/main_simple.py`

### 2. 删除所有测试文件

删除以下文件：
- `backend/test_*.py`（所有测试文件）
- `backend/quick_test.py`
- `backend/verify_integration.py`
- `backend/setup_workspace.py`
- `backend/mock_api.py`
- `backend/start.py`
- `backend/start_simple.py`

### 3. 删除过时的文档

删除以下文件：
- `ENGINE_FIX_REPORT.md`
- `FULL_CHAIN_TEST_REPORT.md`
- `FUNCTIONALITY_CHECK.md`
- `MIGRATION_PLAN.md`
- `PUSH_GUIDE.md`
- `RAILWAY_CHECKLIST.md`
- `SECURITY_FIX_SUMMARY.md`
- `TEST_REPORT.md`
- `design_comparison.md`

### 4. 修改 railway.json

将 `backend/railway.json` 修改为：

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python main_railway_test.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 5. 添加新文档

添加以下新文档：
- `DIAGNOSIS_REPORT.md`
- `RAILWAY_ENV_SETUP.md`
- `SYSTEM_ANALYSIS.md`

---

## 🚀 快速推送脚本

创建一个脚本 `push_changes.sh`：

```bash
#!/bin/bash

echo "开始清理项目..."

# 删除多余的 main 文件
rm -f backend/main_fixed.py backend/main_simple.py

# 删除测试文件
rm -f backend/test_*.py backend/quick_test.py backend/verify_integration.py
rm -f backend/setup_workspace.py backend/mock_api.py backend/start.py backend/start_simple.py

# 删除过时文档
rm -f ENGINE_FIX_REPORT.md FULL_CHAIN_TEST_REPORT.md FUNCTIONALITY_CHECK.md
rm -f MIGRATION_PLAN.md PUSH_GUIDE.md RAILWAY_CHECKLIST.md
rm -f SECURITY_FIX_SUMMARY.md TEST_REPORT.md design_comparison.md

# 删除其他临时文件
rm -f backend/requirements-minimal.txt backend/test_output_novel.md
rm -f backend/README_FULL.md

echo "清理完成！"

# 提交更改
git add -A
git commit -m "Chore: Clean up project structure

- Removed obsolete main files (main_fixed.py, main_simple.py)
- Removed all test files
- Removed outdated documentation
- Updated railway.json"

# 推送
echo "开始推送..."
git push origin main

echo "推送完成！"
```

运行脚本：
```bash
chmod +x push_changes.sh
./push_changes.sh
```

---

## 🔧 替代方案：直接在 Railway 修改

如果无法推送代码，可以直接在 Railway 控制台修改启动命令：

1. 登录 https://railway.app
2. 进入项目 `novelmakev1-production`
3. 点击 **Settings** → **Build & Deploy**
4. 在 **Custom Start Command** 中输入：
   ```
   cd backend && python main.py
   ```
5. 保存并重新部署

---

## ✅ 验证推送成功

推送成功后，检查：

1. **GitHub 仓库**
   https://github.com/yxx-789/novel_make_v1
   - 确认最新提交是 `790d59b`

2. **Railway 自动部署**
   - Railway 会自动检测到推送并重新部署
   - 查看部署日志确认成功

3. **应用访问**
   https://novelmakev1-production.up.railway.app/health
   - 应该返回 `{"status": "healthy", ...}`

---

## 📞 需要帮助？

如果遇到问题：
1. 检查网络连接
2. 确认 GitHub token 有效
3. 查看错误日志
4. 联系技术支持