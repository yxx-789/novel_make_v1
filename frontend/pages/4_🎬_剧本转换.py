"""
剧本转换页面 - 完全适配后端 API
"""
import streamlit as st
from utils.api import api_client

st.set_page_config(

    page_title="剧本转换 - AI 小说创作平台",
    page_icon="▣",
    layout="wide"
)

# 应用全局样式
from utils.global_styles import apply_global_styles
apply_global_styles()

st.title("▣ 剧本转换")

st.markdown("""
### ⬡ 功能说明
将小说转换为短视频剧本格式，适用于：
- 🎥 短视频平台（抖音、快手等）
- 📺 网剧剧本
- ◆ 舞台剧剧本
""")

# 加载小说列表
with st.spinner("加载小说列表..."):
    novels_result = api_client.get_novels()

# 解析小说列表
novels = []
if novels_result.get("success") or "novels" in novels_result:
    novels = novels_result.get("novels", [])

# 检查错误
if novels_result.get("error"):
    st.error(f"✕ 获取小说列表失败: {novels_result['error']}")
    st.info("○ 请检查：\n1. 后端服务是否启动\n2. API 地址是否正确（在系统设置页面配置）")

if novels:
    st.markdown("---")
    st.markdown("## ⬡ 选择要转换的小说")
    
    # 创建选择框
    novel_options = {}
    for n in novels:
        try:
            novel_id = n.get("novel_id") or n.get("id")
            title = n.get("title") or "未命名"
            genre = n.get("genre") or "未知类型"
            created_at = n.get("created_at") or "未知"
            
            label = f"⬡ {title} ({genre}) - {created_at[:10] if created_at else '未知'}"
            novel_options[label] = n
        except Exception as e:
            st.warning(f"△ 跳过一条数据: {e}")
    
    if novel_options:
        selected_label = st.selectbox(
            "❖ 选择小说",
            list(novel_options.keys()),
            help="选择一本已创建的小说进行转换"
        )
        
        selected_novel = novel_options[selected_label]
        novel_id = selected_novel.get("novel_id") or selected_novel.get("id")
        
        # 显示小说信息
        with st.expander("▤ 小说信息", expanded=True):
            st.markdown(f"**标题**: {selected_novel.get('title', '未知')}")
            st.markdown(f"**类型**: {selected_novel.get('genre', '未设置')}")
            st.markdown(f"**故事梗概**: {selected_novel.get('topic', '未设置')}")
            st.markdown(f"**核心主题**: {selected_novel.get('theme', '未设置')}")
            st.markdown(f"**ID**: `{novel_id}`")
            st.markdown(f"**总章节数**: {selected_novel.get('total_chapters', 0)}")
        
        st.markdown("---")
        
        # 转换配置
        st.markdown("## ⚙ 转换配置")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 章节范围
            total_chapters = selected_novel.get("total_chapters", 10)
            chapter_range = st.text_input(
                "⬡ 章节范围（可选）",
                placeholder="例如：1-3 或 all",
                value="all",
                help="指定要转换的章节范围，留空或 'all' 表示全部"
            )
            
            # 剧集编号
            episode_num = st.number_input(
                "▣ 剧集编号（可选）",
                min_value=1,
                value=1,
                help="指定剧集编号"
            )
        
        with col2:
            # 输出格式
            output_format = st.selectbox(
                "📄 输出格式",
                ["json", "markdown", "csv"],
                help="选择剧本的输出格式"
            )
            
            # 每集时长
            episode_duration = st.slider(
                "⏱️ 每集时长（秒）",
                min_value=60,
                max_value=180,
                value=90,
                step=15,
                help="短视频的时长（秒）"
            )
        
        st.markdown("---")
        
        # 开始转换
        st.markdown("## ▶ 开始转换")
        
        if st.button("▣ 开始转换", use_container_width=True, type="primary"):
            with st.spinner("正在将小说转换为剧本，AI 正在创作中（约30-60秒）..."):
                result = api_client.convert_to_drama(
                    novel_id=novel_id,
                    chapter_range=chapter_range if chapter_range else None,
                    episode_num=episode_num,
                    output_format=output_format
                )
                
                if result.get("success"):
                    st.success("✓ 剧本转换成功！")
                    
                    script_data = result.get("data", {})
                    
                    if script_data:
                        st.markdown("---")
                        st.markdown("## 📄 转换结果")
                        
                        # 基本信息卡片
                        st.markdown("### ▤ 剧本信息")
                        
                        col3, col4 = st.columns(2)
                        with col3:
                            st.markdown(f"**☰ 剧本标题**: {selected_novel.get('title', '未知')}")
                            st.markdown(f"**▣ 剧集编号**: {script_data.get('episode_num', 1)}")
                            st.markdown(f"**🆔 剧本ID**: `{script_data.get('script_id', '未知')}`")
                        
                        with col4:
                            st.markdown(f"**⏱️ 时长**: {script_data.get('total_duration', 0)} 秒")
                            st.markdown(f"**◆ 场景数**: {len(script_data.get('scenes', []))}")
                            st.markdown(f"**📹 总镜头数**: {script_data.get('total_shots', 0)}")
                        
                        st.markdown("---")
                        
                        # 显示剧本内容
                        st.markdown("### ⬡ 剧本内容预览")
                        
                        scenes = script_data.get("scenes", [])
                        
                        if scenes:
                            for scene in scenes[:5]:  # 只显示前5个场景
                                scene_num = scene.get("scene_num", "?")
                                location = scene.get("location", "未知")
                                time_of_day = scene.get("time_of_day", "日")
                                
                                st.markdown(f"""
                                <div style="
                                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                    padding: 1rem;
                                    border-radius: 10px;
                                    margin: 0.5rem 0;
                                    color: white;
                                ">
                                    <h4 style="margin: 0; color: white;">▣ 场景 {scene_num}: {location} ({time_of_day})</h4>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # 显示镜头
                                shots = scene.get("shots", [])
                                for shot in shots[:3]:  # 只显示前3个镜头
                                    shot_num = shot.get("shot_num", "?")
                                    shot_type = shot.get("shot_type", "中景")
                                    duration = shot.get("duration", 0)
                                    visual = shot.get("visual", "暂无描述")
                                    
                                    st.markdown(f"""
                                    <div style="
                                        background: #f8f9fa;
                                        padding: 0.8rem;
                                        border-radius: 5px;
                                        margin: 0.3rem 0;
                                        border-left: 3px solid #667eea;
                                    ">
                                        <strong>📹 镜头 {shot_num}</strong> ({shot_type}, {duration}秒)<br>
                                        <span style="color: #666;">{visual}</span>
                                    </div>
                                    """, unsafe_allow_html=True)
                        else:
                            st.warning("△ 剧本内容为空或格式不正确")
                        
                        st.markdown("---")
                        
                        # 导出选项
                        st.markdown("### ▥ 导出剧本")
                        
                        col5, col6 = st.columns(2)
                        
                        with col5:
                            # 导出 JSON
                            if st.button("▤ 导出 JSON", use_container_width=True):
                                import json
                                json_content = json.dumps(script_data, ensure_ascii=False, indent=2)
                                st.download_button(
                                    label="▥ 下载 JSON 文件",
                                    data=json_content,
                                    file_name=f"{selected_novel.get('title', '剧本')}_episode_{episode_num}.json",
                                    mime="application/json"
                                )
                        
                        with col6:
                            # 导出 Markdown
                            if st.button("☰ 导出 Markdown", use_container_width=True):
                                md_content = f"# {selected_novel.get('title', '剧本')}\n\n"
                                md_content += f"剧集编号: {episode_num}\n"
                                md_content += f"总时长: {script_data.get('total_duration', 0)}秒\n\n"
                                
                                for scene in scenes:
                                    md_content += f"## 场景 {scene.get('scene_num', '?')}: {scene.get('location', '未知')}\n\n"
                                    for shot in scene.get("shots", []):
                                        md_content += f"**镜头 {shot.get('shot_num', '?')}** ({shot.get('shot_type', '中景')}, {shot.get('duration', 0)}秒)\n"
                                        md_content += f"{shot.get('visual', '暂无描述')}\n\n"
                                
                                st.download_button(
                                    label="▥ 下载 Markdown 文件",
                                    data=md_content,
                                    file_name=f"{selected_novel.get('title', '剧本')}_episode_{episode_num}.md",
                                    mime="text/markdown"
                                )
                        
                        # 完整数据
                        with st.expander("◉ 查看完整数据"):
                            st.json(script_data)
                
                elif result.get("error"):
                    st.error(f"✕ 转换失败: {result['error']}")
                else:
                    st.error("✕ 转换失败: 未知错误")

else:
    st.warning("❖ 暂无小说")
    st.info("👆 请先创建小说后再进行剧本转换")

st.markdown("---")
st.markdown("## ⬡ 剧本格式说明")

tab1, tab2, tab3 = st.tabs(["▣ 短视频剧本", "📺 网剧剧本", "◆ 舞台剧本"])

with tab1:
    st.markdown("""
    ### ▣ 短视频剧本格式
    
    **适用场景**: 抖音、快手等短视频平台
    
    **特点**:
    - ⏱️ 时长: 60-180秒
    - 📹 镜头数: 10-30个
    - ◆ 节奏快，反转多
    - ○ 每个镜头都有明确的视觉描述
    
    **结构**:
    1. **钩子** (前3秒): 抓住观众注意力
    2. **故事发展** (中间): 情节推进
    3. **悬念结尾** (后5秒): 引导观众看下一集
    """)

with tab2:
    st.markdown("""
    ### 📺 网剧剧本格式
    
    **适用场景**: 网络剧集、系列短剧
    
    **特点**:
    - ⬡ 多集连续剧情
    - ◆ 完整的人物弧光
    - ⚡ 每集有独立的故事线
    
    **结构**:
    1. **剧集大纲**: 整体故事线
    2. **场景分解**: 详细场景描述
    3. **镜头脚本**: 具体拍摄指导
    """)

with tab3:
    st.markdown("""
    ### ◆ 舞台剧本格式
    
    **适用场景**: 舞台剧、话剧演出
    
    **特点**:
    - ◆ 强调对话和动作
    - ✦ 注重氛围营造
    - ⏱️ 连续时间流
    
    **结构**:
    1. **幕次分解**: 场景切换
    2. **人物对白**: 详细台词
    3. **舞台指示**: 动作和走位
    """)

st.markdown("---")
st.caption("○ 提示：剧本转换质量取决于小说的完整性和内容质量")
