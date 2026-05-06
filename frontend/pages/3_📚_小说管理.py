"""
小说管理页面 - 完全适配后端 API
"""
import streamlit as st
from utils.api import api_client

st.set_page_config(

    page_title="小说管理 - AI 小说创作平台",
    page_icon="📚",
    layout="wide"
)

# 应用全局样式
from utils.global_styles import apply_global_styles
apply_global_styles()

st.title("📚 小说管理")

# 加载小说列表
with st.spinner("加载小说列表..."):
    novels_result = api_client.get_novels()

# 解析小说列表
novels = []
if novels_result.get("success") or "novels" in novels_result:
    novels = novels_result.get("novels", [])

# 检查错误
if novels_result.get("error"):
    st.error(f"❌ 获取小说列表失败: {novels_result['error']}")
    st.info("💡 请检查：\n1. 后端服务是否启动\n2. API 地址是否正确（在系统设置页面配置）")

if novels:
    # 统计信息
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📖 总小说数", len(novels))
    
    with col2:
        # 类型分布
        genre_count = {}
        for novel in novels:
            genre = novel.get("genre") or "未分类"
            genre_count[genre] = genre_count.get(genre, 0) + 1
        st.metric("📚 类型数", len(genre_count))
    
    with col3:
        # 最新创建
        latest = novels[0].get("created_at") if novels else "无"
        st.metric("📅 最新创建", latest[:10] if latest else "无")
    
    st.markdown("---")
    
    # 搜索和筛选
    col4, col5 = st.columns([2, 1])
    
    with col4:
        search_query = st.text_input(
            "🔍 搜索小说",
            placeholder="输入标题或类型...",
            help="支持模糊搜索"
        )
    
    with col5:
        filter_genre = st.selectbox(
            "📚 按类型筛选",
            ["全部"] + list(genre_count.keys())
        )
    
    # 筛选逻辑
    filtered_novels = novels
    if search_query:
        filtered_novels = [
            n for n in filtered_novels
            if search_query.lower() in (n.get("title") or "").lower()
            or search_query.lower() in (n.get("genre") or "").lower()
            or search_query.lower() in (n.get("topic") or "").lower()
        ]
    
    if filter_genre != "全部":
        filtered_novels = [
            n for n in filtered_novels
            if n.get("genre") == filter_genre
        ]
    
    st.markdown(f"### 📚 小说列表 ({len(filtered_novels)} 本)")
    
    # 显示小说列表
    for idx, novel in enumerate(filtered_novels):
        novel_id = novel.get("novel_id") or novel.get("id")
        title = novel.get("title") or "未命名"
        genre = novel.get("genre") or "未知类型"
        topic = novel.get("topic", "")[:100] + "..." if len(novel.get("topic", "")) > 100 else novel.get("topic", "")
        theme = novel.get("theme") or "未设置"
        style_guide = novel.get("style_guide") or "未设置"
        created_at = novel.get("created_at") or "未知"
        total_chapters = novel.get("total_chapters", 0)
        generated_count = len(novel.get("generated_chapters", []))
        
        with st.expander(f"📖 {title} - {created_at[:10] if created_at else '未知'}"):
            col6, col7 = st.columns([3, 1])
            
            with col6:
                st.markdown(f"**📝 标题**: {title}")
                st.markdown(f"**📚 类型**: {genre}")
                st.markdown(f"**🎯 故事梗概**: {topic}")
                st.markdown(f"**💭 核心主题**: {theme}")
                st.markdown(f"**🎨 写作风格**: {style_guide}")
                st.markdown(f"**📅 创建时间**: {created_at}")
                st.markdown(f"**🆔 ID**: `{novel_id}`")
                st.markdown(f"**📖 总章节**: {total_chapters} | **已生成**: {generated_count}")
            
            with col7:
                st.markdown("### ⚙️ 操作")
                
                # 查看详情按钮
                if st.button("👁️ 查看详情", key=f"view_{novel_id}_{idx}"):
                    st.session_state.view_novel_id = novel_id
                    st.rerun()
                
                # 复制 ID 按钮
                if st.button("📋 复制 ID", key=f"copy_{novel_id}_{idx}"):
                    st.success(f"✅ ID: `{novel_id}`")
                
                # 导出按钮
                if st.button("📤 导出小说", key=f"export_{novel_id}_{idx}"):
                    with st.spinner("正在导出..."):
                        result = api_client.export_novel(novel_id, "markdown")
                        if result.get("success"):
                            content = result.get("data", {}).get("content", "")
                            if content:
                                st.download_button(
                                    label="📥 下载 Markdown",
                                    data=content,
                                    file_name=f"{title}.md",
                                    mime="text/markdown"
                                )
                        else:
                            st.error(f"导出失败: {result.get('error', '未知错误')}")
    
    # 查看小说详情
    if "view_novel_id" in st.session_state and st.session_state.view_novel_id:
        st.markdown("---")
        st.markdown("## 📖 小说详情")
        
        if st.button("← 返回列表"):
            st.session_state.view_novel_id = None
            st.rerun()
        
        with st.spinner("加载小说详情..."):
            detail_result = api_client.get_novel(st.session_state.view_novel_id)
            
            if detail_result.get("success"):
                detail = detail_result.get("data", {})
                
                st.markdown("---")
                
                # 基本信息
                st.markdown("### 📋 基本信息")
                col8, col9 = st.columns(2)
                with col8:
                    st.markdown(f"**标题**: {detail.get('title')}")
                    st.markdown(f"**类型**: {detail.get('genre')}")
                    st.markdown(f"**故事梗概**: {detail.get('topic')}")
                with col9:
                    st.markdown(f"**核心主题**: {detail.get('theme') or '未设置'}")
                    st.markdown(f"**写作风格**: {detail.get('style_guide') or '未设置'}")
                    st.markdown(f"**状态**: {detail.get('status') or '草稿'}")
                
                # 创作进度
                st.markdown("### 📊 创作进度")
                progress_col1, progress_col2, progress_col3 = st.columns(3)
                
                with progress_col1:
                    has_blueprint = detail.get("plot_blueprint") is not None
                    st.markdown(f"{'✅' if has_blueprint else '⭕'} 故事蓝图")
                
                with progress_col2:
                    has_outline = detail.get("chapters") and len(detail.get("chapters", [])) > 0
                    st.markdown(f"{'✅' if has_outline else '⭕'} 章节大纲")
                
                with progress_col3:
                    generated_chapters = detail.get("generated_chapters", [])
                    st.markdown(f"{'✅' if generated_chapters else '⭕'} 章节内容 ({len(generated_chapters)} 章)")
                
                # 世界观设定
                if detail.get("world_setting"):
                    st.markdown("---")
                    st.markdown("### 🌍 世界观设定")
                    world = detail.get("world_setting", {})
                    st.markdown(f"**时代**: {world.get('era', '未设置')}")
                    st.markdown(f"**地点**: {world.get('location', '未设置')}")
                    st.markdown(f"**力量体系**: {world.get('power_system', '未设置')}")
                
                # 角色档案
                if detail.get("characters"):
                    st.markdown("---")
                    st.markdown("### 👥 角色档案")
                    for char in detail.get("characters", [])[:5]:
                        st.markdown(f"**{char.get('name', '未知')}** ({char.get('role', '未知')})")
                        st.caption(f"性格: {', '.join(char.get('personality', []))}")
                
                # 情节蓝图
                if detail.get("plot_blueprint"):
                    st.markdown("---")
                    st.markdown("### 📖 情节蓝图")
                    plot = detail.get("plot_blueprint", {})
                    st.markdown(f"**核心冲突**: {plot.get('main_conflict', '未设置')}")
                    st.markdown(f"**高潮**: {plot.get('climax', '未设置')}")
                    st.markdown(f"**结局**: {plot.get('resolution', '未设置')}")
                
                # 章节大纲
                if detail.get("chapters"):
                    st.markdown("---")
                    st.markdown("### 📚 章节大纲")
                    for chapter in detail.get("chapters", [])[:10]:
                        chapter_num = chapter.get("chapter_num", "?")
                        chapter_title = chapter.get("title", "未命名")
                        summary = chapter.get("summary", "暂无概要")
                        
                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            padding: 1rem;
                            border-radius: 10px;
                            margin: 0.5rem 0;
                            color: white;
                        ">
                            <h4 style="margin: 0; color: white;">📖 第 {chapter_num} 章: {chapter_title}</h4>
                            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">{summary}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # 已生成章节
                if detail.get("generated_chapters"):
                    st.markdown("---")
                    st.markdown("### 📖 已生成章节")
                    for chapter in detail.get("generated_chapters", []):
                        chapter_num = chapter.get("chapter_num", "?")
                        chapter_title = chapter.get("title", "未命名")
                        word_count = chapter.get("word_count", 0)
                        
                        with st.expander(f"第 {chapter_num} 章: {chapter_title} ({word_count} 字)"):
                            st.text_area("", chapter.get("content", ""), height=200, key=f"content_{chapter_num}")
            
            elif detail_result.get("error"):
                st.error(f"❌ 加载失败: {detail_result.get('error')}")

else:
    st.warning("📚 暂无小说")
    st.info("👆 请前往小说创作页面创建第一本小说")

st.markdown("---")
st.markdown("## 🔧 批量操作")

col10, col11, col12 = st.columns(3)

with col10:
    if st.button("🔄 刷新列表", use_container_width=True):
        st.rerun()

with col11:
    if st.button("📊 导出统计", use_container_width=True):
        stats = {
            "总数": len(novels),
            "类型分布": genre_count
        }
        st.json(stats)

with col12:
    st.button("🗑️ 清空所有", use_container_width=True, type="secondary", disabled=True)
    st.caption("⚠️ 为安全起见，此功能已禁用")
