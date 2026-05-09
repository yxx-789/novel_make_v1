"""
小说创作页面 - 完全适配后端 API（优化版：支持查看已生成的蓝图和大纲）
"""
import streamlit as st
from utils.api import api_client
from utils.config import Config

st.set_page_config(
    page_title="小说创作 - AI 小说创作平台",
    page_icon="✦",
    layout="wide"
)

# 应用全局样式和页面主题
from utils.global_styles import apply_global_styles, apply_page_theme
apply_global_styles()
apply_page_theme("小说创作")

st.title("✦ 小说创作")

# ==================== 创建新小说 ====================
st.markdown("## ☰ 创建新小说")
st.caption("○ 提示：带 * 的为必填项")

with st.form("create_novel_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        novel_title = st.text_input(
            "⬡ 小说标题 *",
            placeholder="例如：修仙之路",
            max_chars=50,
            help="给你的小说起一个吸引人的标题"
        )
        
        # 后端支持的类型（枚举值）
        novel_genre = st.selectbox(
            "❖ 小说类型 *",
            [
                "玄幻", "仙侠", "武侠", "都市", 
                "言情", "科幻", "悬疑", "历史", "其他"
            ],
            help="选择适合你小说的类型"
        )
    
    with col2:
        # topic 是必填项（后端要求）
        novel_topic = st.text_area(
            "◇ 故事梗概 *",
            placeholder="例如：一个少年在修仙世界中不断成长，最终成为强者的故事",
            max_chars=500,
            height=100,
            help="简要描述故事的主要内容和发展方向"
        )
        
        # theme 是可选项
        novel_theme = st.text_input(
            "💭 核心主题（可选）",
            placeholder="例如：成长、友情、坚持",
            max_chars=100,
            help="小说想要表达的核心思想"
        )
    
    # 高级选项
    with st.expander("⚙ 高级选项"):
        novel_style = st.text_area(
            "✦ 写作风格（可选）",
            placeholder="例如：轻松幽默、热血激昂、温馨治愈",
            max_chars=200,
            height=80,
            help="指导 AI 的写作风格"
        )
        
        col3, col4 = st.columns(2)
        with col3:
            total_chapters = st.number_input(
                "⬡ 总章节数",
                min_value=1,
                max_value=1000,
                value=10,
                help="计划创作的总章节数"
            )
        
        with col4:
            target_word_count = st.number_input(
                "☰ 每章目标字数",
                min_value=500,
                max_value=10000,
                value=3000,
                step=500,
                help="每章的目标字数"
            )
    
    # 提交按钮
    submitted = st.form_submit_button("▶ 创建小说", use_container_width=True, type="primary")
    
    if submitted:
        if not novel_title or not novel_genre or not novel_topic:
            st.error("请填写所有必填项（标题、类型、故事梗概）")
        else:
            with st.spinner("正在创建小说..."):
                # 调用后端 API（参数映射）
                result = api_client.create_novel(
                    title=novel_title,
                    genre=novel_genre,
                    topic=novel_topic,  # 后端参数名是 topic
                    theme=novel_theme if novel_theme else None,
                    style_guide=novel_style if novel_style else None,
                    total_chapters=total_chapters,
                    target_word_count=target_word_count
                )
                
                if result.get("success"):
                    # 后端返回格式：{"success": true, "message": "...", "data": NovelProject}
                    novel_data = result.get("data", {})
                    novel_id = novel_data.get("novel_id")
                    
                    st.success(f"✓ 小说创建成功！")
                    
                    if novel_id:
                        st.info(f"▤ 小说 ID: `{novel_id}`")
                        
                        # 保存到 session_state
                        if "current_novel" not in st.session_state:
                            st.session_state.current_novel = {}
                        st.session_state.current_novel = {
                            "id": novel_id,
                            "title": novel_title,
                            "genre": novel_genre,
                            "topic": novel_topic
                        }
                        
                        st.info("👇 小说创建成功！请在下方选择刚创建的小说，开始生成蓝图")
                    
                elif result.get("error"):
                    st.error(f"✕ 创建失败: {result['error']}")
                else:
                    st.error("✕ 创建失败: 未知错误")

st.markdown("---")

# ==================== 选择小说并创作 ====================
st.markdown("## ❖ 选择小说进行创作")

with st.spinner("加载小说列表..."):
    novels_result = api_client.get_novels()

# 解析小说列表
novels = []
if novels_result.get("success") or "novels" in novels_result:
    # 后端返回格式：{"novels": [...], "total": 10, "page": 1, "page_size": 100}
    novels = novels_result.get("novels", [])
elif novels_result.get("data"):
    # 另一种可能的格式
    novels = novels_result["data"]

# 检查错误
if novels_result.get("error"):
    st.error(f"✕ 获取小说列表失败: {novels_result['error']}")
    st.info("○ 请检查：\n1. 后端服务是否启动\n2. API 地址是否正确（在系统设置页面配置）")

if novels:
    # 创建选择框
    novel_options = {}
    for n in novels:
        try:
            # 后端返回的字段名
            novel_id = n.get("novel_id") or n.get("id") or str(n)
            title = n.get("title") or "未命名"
            genre = n.get("genre") or "未知类型"
            topic = n.get("topic", "")[:50] + "..." if len(n.get("topic", "")) > 50 else n.get("topic", "")
            
            label = f"⬡ {title} ({genre}) - ID: {novel_id}"
            if topic:
                label += f" | {topic}"
            
            novel_options[label] = n
        except Exception as e:
            st.warning(f"△ 跳过一条数据: {e}")
    
    if novel_options:
        selected_label = st.selectbox(
            "选择要操作的小说",
            list(novel_options.keys()),
            help="选择一本小说开始创作"
        )
        
        selected_novel = novel_options[selected_label]
        novel_id = selected_novel.get("novel_id") or selected_novel.get("id")
        
        # 显示小说信息
        with st.expander("⬡ 小说详情", expanded=True):
            st.markdown(f"**标题**: {selected_novel.get('title', '未知')}")
            st.markdown(f"**类型**: {selected_novel.get('genre', '未设置')}")
            st.markdown(f"**故事梗概**: {selected_novel.get('topic', '未设置')}")
            st.markdown(f"**核心主题**: {selected_novel.get('theme', '未设置')}")
            st.markdown(f"**写作风格**: {selected_novel.get('style_guide', '未设置')}")
            st.markdown(f"**ID**: `{novel_id}`")
            st.markdown(f"**总章节数**: {selected_novel.get('total_chapters', 0)}")
            st.markdown(f"**每章字数**: {selected_novel.get('target_word_count', 0)}")
            st.markdown(f"**创建时间**: {selected_novel.get('created_at', '未知')}")
        
        st.markdown("---")
        
        # ==================== 新增：查看已生成的内容 ====================
        st.markdown("### 📊 创作进度总览")
        
        # 获取小说完整信息
        with st.spinner("加载创作进度..."):
            novel_detail = api_client.get_novel(novel_id)
        
        # 解析蓝图和大纲数据
        blueprint_data = None
        outline_data = None
        chapters_data = []
        
        if novel_detail.get("success"):
            data = novel_detail.get("data", {})
            blueprint_data = data.get("blueprint") or data.get("plot_blueprint")
            outline_data = data.get("chapter_outlines") or data.get("outlines")
            chapters_data = data.get("chapters") or []
        
        # 显示进度
        col_p1, col_p2, col_p3 = st.columns(3)
        
        with col_p1:
            blueprint_status = "✅ 已生成" if blueprint_data else "⏳ 未生成"
            st.metric("📋 蓝图", blueprint_status)
        
        with col_p2:
            outline_count = len(outline_data) if outline_data else 0
            outline_status = f"✅ {outline_count} 章" if outline_count > 0 else "⏳ 未生成"
            st.metric("📝 大纲", outline_status)
        
        with col_p3:
            chapter_count = len(chapters_data)
            chapter_status = f"✅ {chapter_count} 章" if chapter_count > 0 else "⏳ 未生成"
            st.metric("📖 章节", chapter_status)
        
        st.markdown("---")
        
        # ==================== 已生成的蓝图内容（新增）====================
        if blueprint_data:
            st.markdown("### 📋 已生成的蓝图")
            
            with st.expander("👁️ 查看蓝图内容", expanded=False):
                # 显示蓝图结构
                st.markdown("#### ◉ 世界观设定")
                world = blueprint_data.get("world_setting", {}) or blueprint_data.get("worldSetting", {})
                if world:
                    col_w1, col_w2 = st.columns(2)
                    with col_w1:
                        st.markdown(f"- **时代**: {world.get('era', '未设置')}")
                        st.markdown(f"- **地点**: {world.get('location', '未设置')}")
                    with col_w2:
                        st.markdown(f"- **力量体系**: {world.get('power_system', '未设置')}")
                        st.markdown(f"- **社会结构**: {world.get('social_structure', '未设置')}")
                
                st.markdown("#### 👥 角色档案")
                characters = blueprint_data.get("characters", [])
                if characters:
                    for i, char in enumerate(characters[:10], 1):  # 显示前10个
                        with st.container():
                            st.markdown(f"**{i}. {char.get('name', '未知')}** ({char.get('role', '未知角色')})")
                            if char.get('personality'):
                                st.caption(f"性格: {char.get('personality')}")
                            if char.get('background'):
                                st.caption(f"背景: {char.get('background')}")
                
                st.markdown("#### ⬡ 情节蓝图")
                plot = blueprint_data.get("plot_blueprint", {}) or blueprint_data.get("plotBlueprint", {})
                if plot:
                    col_p1, col_p2 = st.columns(2)
                    with col_p1:
                        st.markdown(f"- **核心冲突**: {plot.get('main_conflict', '未设置')}")
                        st.markdown(f"- **高潮**: {plot.get('climax', '未设置')}")
                    with col_p2:
                        st.markdown(f"- **结局**: {plot.get('resolution', '未设置')}")
                        st.markdown(f"- **主题**: {plot.get('theme', '未设置')}")
                
                # 完整数据
                with st.expander("◉ 查看完整蓝图数据（JSON）"):
                    st.json(blueprint_data)
            
            st.markdown("---")
        
        # ==================== 已生成的大纲内容（新增）====================
        if outline_data and len(outline_data) > 0:
            st.markdown("### 📝 已生成的章节大纲")
            
            with st.expander("👁️ 查看大纲内容", expanded=False):
                # 显示前10章大纲
                for outline in outline_data[:10]:
                    chapter_num = outline.get("chapter_num") or outline.get("chapterNum", "?")
                    title = outline.get("title", "未命名")
                    summary = outline.get("summary", "暂无概要")
                    
                    with st.container():
                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            padding: 1rem;
                            border-radius: 10px;
                            margin: 0.5rem 0;
                            color: white;
                        ">
                            <h4 style="margin: 0; color: white;">⬡ 第 {chapter_num} 章: {title}</h4>
                            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">{summary}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                if len(outline_data) > 10:
                    st.info(f"还有 {len(outline_data) - 10} 章未显示...")
            
            st.markdown("---")
        
        # ==================== 步骤一：生成蓝图 ====================
        st.markdown("### ✦ 步骤一：生成故事蓝图")
        
        if blueprint_data:
            st.info("✅ 蓝图已生成，可以重新生成覆盖现有蓝图")
        
        st.info("""
        ▤ **蓝图包含**：
        - ◉ 世界观设定（时代背景、地点、力量体系等）
        - 👥 角色档案（主角、配角、反派的详细信息）
        - ⬡ 情节蓝图（核心冲突、高潮、结局等）
        """)
        
        if st.button("◇ 生成蓝图" if not blueprint_data else "🔄 重新生成蓝图", use_container_width=True, type="primary"):
            with st.spinner("正在生成蓝图，AI 正在创作中，请稍候..."):
                result = api_client.generate_blueprint(novel_id)
                
                if result.get("success"):
                    st.success("✓ 蓝图生成成功！")
                    st.rerun()  # 刷新页面显示新蓝图
                    
                elif result.get("error"):
                    st.error(f"✕ 生成失败: {result['error']}")
                else:
                    st.error("✕ 生成失败: 未知错误")
        
        st.markdown("---")
        
        # ==================== 步骤二：生成章节大纲 ====================
        st.markdown("### ▤ 步骤二：生成章节大纲")
        
        if outline_data and len(outline_data) > 0:
            st.info(f"✅ 已生成 {len(outline_data)} 章大纲，可以重新生成覆盖现有大纲")
        
        if st.button("☰ 生成大纲" if not (outline_data and len(outline_data) > 0) else "🔄 重新生成大纲", use_container_width=True, type="primary"):
            with st.spinner("正在生成章节大纲，AI 正在创作中..."):
                result = api_client.generate_outline(novel_id)
                
                if result.get("success"):
                    st.success("✓ 大纲生成成功！")
                    st.rerun()  # 刷新页面显示新大纲
                    
                elif result.get("error"):
                    st.error(f"✕ 生成失败: {result['error']}")
        
        st.markdown("---")
        
        # ==================== 步骤三：生成章节内容 ====================
        st.markdown("### ✦ 步骤三：生成章节内容")
        
        col5, col6 = st.columns([2, 3])
        with col5:
            chapter_num = st.number_input(
                "章节编号",
                min_value=1,
                max_value=selected_novel.get("total_chapters", 100),
                value=1,
                help="输入要生成的章节编号"
            )
        
        with col6:
            additional_guidance = st.text_area(
                "○ 额外创作指导（可选）",
                placeholder="例如：这一章要突出主角的内心挣扎...",
                height=100,
                help="给 AI 一些特殊的创作建议"
            )
        
        st.markdown("#### ○ 提示")
        st.caption("每次生成一章内容，生成时间较长（约30-60秒），请耐心等待")
        
        if st.button("▶ 生成章节", use_container_width=True, type="primary"):
            with st.spinner(f"正在生成第 {chapter_num} 章，AI 正在创作中（约30-60秒）..."):
                result = api_client.generate_chapter(
                    novel_id,
                    chapter_num,
                    additional_guidance if additional_guidance else None
                )
                
                if result.get("success"):
                    st.success(f"✓ 第 {chapter_num} 章生成成功！")
                    
                    chapter_data = result.get("data", {})
                    
                    if chapter_data:
                        st.markdown("#### ⬡ 章节内容")
                        
                        chapter_title = chapter_data.get("title", f"第 {chapter_num} 章")
                        chapter_content = chapter_data.get("content", "")
                        word_count = chapter_data.get("word_count", 0)
                        
                        st.markdown(f"""
                        <div style="
                            background: white;
                            padding: 2rem;
                            border-radius: 10px;
                            border: 2px solid #667eea;
                            margin: 1rem 0;
                        ">
                            <h2 style="color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 0.5rem;">
                                {chapter_title}
                            </h2>
                            <div style="line-height: 1.8; color: #333; margin-top: 1rem; white-space: pre-wrap;">
                                {chapter_content[:2000]}{'...' if len(chapter_content) > 2000 else ''}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.info(f"☰ 本章字数: {word_count} 字")
                        
                        # 完整内容
                        with st.expander("⬡ 查看完整章节"):
                            st.text_area("", chapter_content, height=400)
                    
                elif result.get("error"):
                    st.error(f"✕ 生成失败: {result['error']}")

else:
    st.warning("❖ 暂无小说，请先创建一本小说")
    st.info("👆 请在页面上方创建第一本小说")

# 调试信息
if novels_result and not novels_result.get("error"):
    with st.expander("◉ 调试信息"):
        st.json(novels_result)

st.markdown("---")
st.caption("○ 提示：建议按顺序完成蓝图 → 大纲 → 章节的创作流程")
