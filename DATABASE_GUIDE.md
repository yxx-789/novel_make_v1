# 🗄️ 数据库集成指南

## 📋 概述

本次更新添加了 SQLite 数据库支持，解决了以下问题：

- ✅ 数据持久化存储（Railway 重启后数据不丢失）
- ✅ 切换页面后数据保留
- ✅ 支持数据查询和管理
- ✅ 为未来多用户支持做准备

---

## 🔧 技术架构

### 数据库选择

**SQLite**（当前使用）
- ✅ 无需额外服务
- ✅ 部署简单
- ✅ Railway 直接支持
- ✅ 适合单用户/小团队

**PostgreSQL**（未来可选）
- ✅ Railway 原生支持
- ✅ 高性能
- ✅ 支持多用户
- ✅ 数据可靠

### 数据库模型

#### 1. 小说项目表 (`novel_projects`)

| 字段 | 类型 | 说明 |
|------|------|------|
| novel_id | String | 小说 ID（主键）|
| title | String | 小说标题 |
| genre | String | 小说类型 |
| topic | Text | 故事梗概 |
| theme | Text | 核心主题 |
| world_setting | JSON | 世界观设定 |
| characters | JSON | 角色设定 |
| plot_blueprint | JSON | 情节蓝图 |
| chapter_outlines | JSON | 章节大纲 |
| created_at | DateTime | 创建时间 |

#### 2. 章节内容表 (`chapter_contents`)

| 字段 | 类型 | 说明 |
|------|------|------|
| chapter_id | String | 章节 ID（主键）|
| novel_id | String | 小说 ID（外键）|
| chapter_num | Integer | 章节号 |
| title | String | 章节标题 |
| content | Text | 章节内容 |
| word_count | Integer | 字数 |
| created_at | DateTime | 创建时间 |

---

## 🚀 使用方法

### 本地开发

1. **初始化数据库**

```bash
cd backend
python database/migrate.py
```

2. **启动后端**

```bash
python main.py
```

数据库文件会自动创建在 `backend/novels.db`

### Railway 部署

Railway 会自动：
- ✅ 创建 SQLite 数据库文件
- ✅ 持久化存储数据
- ✅ 重启后数据保留

**数据持久化原理**：
- Railway 的文件系统会保留 SQLite 数据库文件
- 重启后文件仍然存在
- 数据不会丢失

---

## 📊 数据迁移

### 从内存版本迁移

如果你之前使用的是内存版本，数据无法自动迁移。需要：

1. 导出旧数据（如果有）
2. 重新创建小说项目
3. 重新生成蓝图和大纲

### 数据备份

**本地备份**：
```bash
cp backend/novels.db backend/novels_backup.db
```

**Railway 备份**：
- Railway 会自动备份文件系统
- 也可以通过 API 导出数据

---

## 🔍 验证数据库

### 检查数据库状态

```bash
cd backend
python database/migrate.py
```

输出示例：
```
📊 检查数据库状态...
   小说项目数量: 3
   章节数量: 15

   📚 已有小说项目:
      - 修仙之路 (ID: a1b2c3d4)
      - 都市传说 (ID: e5f6g7h8)
```

### 直接查询数据库

```bash
sqlite3 backend/novels.db
sqlite> SELECT title, genre FROM novel_projects;
```

---

## 🐛 故障排除

### 问题 1: 数据库连接失败

**错误信息**: `no such table: novel_projects`

**解决方案**:
```bash
cd backend
python database/migrate.py
```

### 问题 2: 数据丢失

**可能原因**:
- Railway 重启时数据卷未挂载
- 使用了临时文件系统

**解决方案**:
- Railway 会自动持久化文件
- 检查 Railway 日志确认

### 问题 3: 权限错误

**错误信息**: `Permission denied: novels.db`

**解决方案**:
```bash
chmod 666 backend/novels.db
```

---

## 📈 性能优化

### 索引优化

数据库已自动创建索引：
- `novel_id` (主键索引)
- `novel_projects.novel_id` (普通索引)
- `chapter_contents.novel_id` (普通索引)

### 查询优化

- ✅ 使用分页查询（`page`, `page_size`）
- ✅ 避免 N+1 查询
- ✅ JSON 字段按需查询

---

## 🔮 未来计划

### 短期（1-2周）

- [ ] 添加数据导出功能（JSON/CSV）
- [ ] 添加数据备份功能
- [ ] 优化查询性能

### 中期（1个月）

- [ ] 支持用户系统（多用户）
- [ ] 支持协作编辑
- [ ] 迁移到 PostgreSQL

### 长期（3个月）

- [ ] 数据分析和统计
- [ ] 版本控制
- [ ] 数据同步

---

## 📝 API 变更

### 新增 API

```python
# 获取小说详情（包含蓝图和大纲）
GET /api/v1/novels/{novel_id}

# 返回格式
{
    "success": true,
    "data": {
        "novel_id": "a1b2c3d4",
        "title": "修仙之路",
        "world_setting": {...},  # 世界观
        "characters": [...],      # 角色
        "plot_blueprint": {...},  # 蓝图
        "chapter_outlines": [...] # 大纲
    }
}
```

### 修改 API

所有 API 行为不变，但数据现在持久化存储。

---

## ⚠️ 注意事项

1. **首次部署**
   - 数据库会自动初始化
   - 无需手动创建表

2. **数据安全**
   - API Key 等敏感信息仍通过环境变量传递
   - 数据库文件不包含敏感信息

3. **Railway 配置**
   - 无需额外配置
   - SQLite 文件自动持久化

4. **并发访问**
   - SQLite 支持多个读取，单个写入
   - 适合单用户/小团队
   - 高并发场景建议使用 PostgreSQL

---

## 🎉 总结

数据库集成已完成，现在你可以：

- ✅ 创建小说项目，数据永久保存
- ✅ 生成蓝图和大纲，刷新页面后仍然存在
- ✅ 切换页面或重启服务，数据不丢失
- ✅ 随时查看已生成的内容

**立即体验**：
1. 推送代码到 GitHub
2. Railway 自动重新部署
3. 创建新小说项目
4. 生成蓝图和大纲
5. 刷新页面，数据仍然存在！

---

## 📞 支持

如有问题，请查看：
- Railway 日志
- 数据库日志
- API 响应信息

或联系开发团队。
