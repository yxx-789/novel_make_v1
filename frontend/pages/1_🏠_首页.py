"""
首页 - 系统状态和快速开始
"""
import streamlit as st
from utils.api import api_client
from utils.config import Config
from datetime import datetime

st.set_page_config(

    page_title="首页 - AI 小说创作平台",
    page_icon="🏠",
    layout="wide"
)

# 应用全局样式
from utils.global_styles import apply_global_styles
apply_global_styles()

st.title("🏠 首页")

# ==================== 系统状态检查 ====================
st.markdown("## 📊 系统状态")

col1, col2, col3 = st.columns(3)

# 检查后端连接
with col1:
    with st.spinner("检查后端连接..."):
        health = api_client.health_check()
    
    if "error" not in health:
        status = health.get("status", "unknown")
        if status == "healthy":
            st.success("✅ 后端服务正常")
            st.metric("状态", "在线", delta="健康")
        else:
            st.warning("⚠️ 后端服务异常")
            st.metric("状态", status)
    else:
        st.error("❌ 后端服务离线")
        st.metric("状态", "离线", delta="无法连接")
        st.error(f"错误信息: {health['error']}")

# 获取模型列表
with col2:
    with st.spinner("获取模型列表..."):
        models = api_client.get_models()
    
    if "models" in models:
        model_count = len(models["models"])
        st.success(f"✅ 可用模型: {model_count} 个")
        st.metric("模型数量", model_count)
    else:
        st.warning("⚠️ 无法获取模型列表")
        st.metric("模型数量", 0)

# 获取小说统计
with col3:
    with st.spinner("获取小说列表..."):
        novels = api_client.get_novels()
    
    if "novels" in novels:
        novel_count = len(novels["novels"])
        st.info(f"📚 已创建小说: {novel_count} 本")
        st.metric("小说数量", novel_count)
    else:
        st.info("📚 暂无小说")
        st.metric("小说数量", 0)

# ==================== 可用模型详情 ====================
st.markdown("---")
st.markdown("## 🤖 可用模型")

if "models" in models and models["models"]:
    cols = st.columns(len(models["models"]))
    
    for idx, model in enumerate(models["models"]):
        with cols[idx]:
            model_id = model.get("id", "unknown")
            model_name = model.get("name", "未知模型")
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 1.5rem;
                border-radius: 10px;
                color: white;
                text-align: center;
            ">
                <h3>{model_name}</h3>
                <p style="font-size: 0.9rem; opacity: 0.9;">{model_id}</p>
            </div>
            """, unsafe_allow_html=True)
else:
    st.warning("暂无可用模型")

# ==================== 快速开始指南 ====================
st.markdown("---")
st.markdown("## 🚀 快速开始指南")

tab1, tab2, tab3 = st.tabs(["📖 新手教程", "💡 创作技巧", "❓ 常见问题"])

with tab1:
    st.markdown("""
    ### 📝 第一步：创建小说
    
    1. 点击左侧导航栏的 **"✍️ 小说创作"**
    2. 填写小说基本信息：
       - 小说标题
       - 小说类型（玄幻、都市、科幻等）
       - 故事主题（成长、冒险、爱情等）
    3. 点击"创建小说"按钮
    
    ---
    
    ### 🎨 第二步：生成故事蓝图
    
    1. 选择刚创建的小说
    2. 点击"生成蓝图"按钮
    3. 系统将自动生成：
       - 核心冲突
       - 主要角色
       - 世界观设定
    
    ---
    
    ### 📋 第三步：生成章节大纲
    
    1. 在小说详情页面点击"生成大纲"
    2. 设置章节数量（建议 3-10 章）
    3. 系统将为每一章生成概要
    
    ---
    
    ### ✍️ 第四步：生成章节内容
    
    1. 点击"生成章节"按钮
    2. 选择要生成的章节编号
    3. 等待 AI 生成内容
    4. 可以多次生成以获得不同版本
    """)

with tab2:
    st.markdown("""
    ### 💡 提高创作质量的技巧
    
    #### 1️⃣ 明确故事主题
    - 选择清晰的主题词（如"成长"、"复仇"、"探险"）
    - 避免过于宽泛的主题
    
    #### 2️⃣ 合理设置章节数
    - 短篇小说：3-5 章
    - 中篇小说：5-10 章
    - 长篇小说：10-20 章（建议分多次创作）
    
    #### 3️⃣ 充分利用蓝图
    - 蓝图是故事的骨架
    - 可以多次生成蓝图，选择最满意的版本
    
    #### 4️⃣ 逐步生成内容
    - 不要一次性生成所有章节
    - 先生成前几章，评估质量后再继续
    
    #### 5️⃣ 剧本转换
    - 小说完成后可以转换为剧本格式
    - 适合影视改编或舞台剧创作
    """)

with tab3:
    st.markdown("""
    ### ❓ 常见问题解答
    
    **Q: 生成的内容质量不高怎么办？**
    
    A: 可以尝试以下方法：
    - 修改小说主题和类型
    - 重新生成蓝图
    - 多次生成章节内容，选择最佳版本
    
    ---
    
    **Q: 支持哪些小说类型？**
    
    A: 目前支持：
    - 玄幻、仙侠、武侠
    - 都市、言情、青春
    - 科幻、悬疑、推理
    - 历史、军事、游戏
    
    ---
    
    **Q: 如何保存我的小说？**
    
    A: 所有小说自动保存在后端数据库中，可以随时查看和编辑。
    
    ---
    
    **Q: 支持导出小说吗？**
    
    A: 目前支持：
    - 复制文本内容
    - 转换为剧本格式
    - 后续将支持导出 Word/PDF
    
    ---
    
    **Q: 如何切换不同的 AI 模型？**
    
    A: 在"系统设置"页面可以查看和切换可用模型。
    """)

# ==================== 最近活动 ====================
st.markdown("---")
st.markdown("## 📅 最近活动")

if "novels" in novels and novels["novels"]:
    st.markdown("### 最近创建的小说")
    
    for novel in novels["novels"][:5]:  # 显示最近 5 本
        with st.expander(
            f"📖 {novel.get('title', '未知标题')} - {novel.get('created_at', '未知时间')}",
            expanded=False
        ):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**类型**: {novel.get('genre', '未设置')}")
                st.markdown(f"**主题**: {novel.get('theme', '未设置')}")
            
            with col2:
                st.markdown(f"**创建时间**: {novel.get('created_at', '未知')}")
                st.markdown(f"**ID**: `{novel.get('id', '未知')}`")
else:
    st.info("暂无小说，去创建第一本吧！ 📝")

# ==================== 页脚 ====================
st.markdown("---")
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.caption(f"最后更新时间: {current_time}")
