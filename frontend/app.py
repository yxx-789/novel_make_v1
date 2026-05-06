"""
AI 小说创作平台 - 主入口文件
"""
import streamlit as st
import os
from utils.config import Config
from utils.api import APIClient

# ==================== 加载环境配置 ====================
# 从 Streamlit Secrets 或环境变量加载配置
if 'API_BASE_URL' in st.secrets:
    Config.API_BASE_URL = st.secrets['API_BASE_URL']
elif 'API_BASE_URL' in os.environ:
    Config.API_BASE_URL = os.environ['API_BASE_URL']

# 更新 API 客户端的默认地址
from utils import api
api.Config.API_BASE_URL = Config.API_BASE_URL

# ==================== 页面配置 ====================
st.set_page_config(
    page_title=Config.PAGE_TITLE,
    page_icon=Config.PAGE_ICON,
    layout=Config.LAYOUT,
    initial_sidebar_state="expanded"
)

# ==================== 自定义样式 ====================
# 使用全局样式
from utils.global_styles import apply_global_styles
apply_global_styles()

# ==================== 侧边栏 ====================
with st.sidebar:
    # Logo和标题 - 文学感
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0 2rem 0;">
        <div style="
            font-size: 3.5rem;
            color: #2c2c2c;
            margin-bottom: 1.5rem;
            opacity: 0.8;
        ">⬡</div>
        <h1 style="
            font-family: 'Noto Serif SC', serif;
            font-size: 1.3rem;
            font-weight: 600;
            color: #2c2c2c;
            margin: 0 0 0.5rem 0;
            letter-spacing: 2px;
        ">小说创作</h1>
        <p style="
            color: #999;
            font-size: 0.85rem;
            margin: 0;
            font-style: italic;
        ">让故事自然生长</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1px; background: rgba(0,0,0,0.06); margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
    
    # 快速导航 - 章节感
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h3 style="
            font-family: 'Noto Serif SC', serif;
            font-size: 0.85rem;
            font-weight: 600;
            color: #999;
            margin: 0 0 1rem 0;
            letter-spacing: 1px;
        ">目 录</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.page_link("pages/1_🏠_首页.py", label="首页")
    st.page_link("pages/2_✍️_小说创作.py", label="小说创作")
    st.page_link("pages/3_📚_小说管理.py", label="小说管理")
    st.page_link("pages/4_🎬_剧本转换.py", label="剧本转换")
    st.page_link("pages/5_💬_AI聊天.py", label="AI对话")
    st.page_link("pages/6_⚙️_系统设置.py", label="系统设置")
    
    st.markdown("<div style='height: 1px; background: rgba(0,0,0,0.06); margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
    
    # 系统状态 - 简洁
    st.markdown("""
    <div style="margin-bottom: 1rem;">
        <h3 style="
            font-family: 'Noto Serif SC', serif;
            font-size: 0.85rem;
            font-weight: 600;
            color: #999;
            margin: 0 0 1rem 0;
            letter-spacing: 1px;
        ">状态</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("刷新", use_container_width=True):
        st.rerun()

# ==================== 主内容区 ====================
st.markdown('<h1 class="main-header">AI 小说创作平台</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">在这里，故事自然生长</p>', unsafe_allow_html=True)

# ==================== 功能介绍 ====================
st.markdown("## 创作空间")

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>小说创作</h3>
        <p>从第一个字开始，让故事流淌</p>
        <ul>
            <li>故事蓝图</li>
            <li>章节大纲</li>
            <li>内容生成</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>剧本转换</h3>
        <p>将小说化为影像的语言</p>
        <ul>
            <li>电影剧本</li>
            <li>电视剧本</li>
            <li>舞台剧本</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>AI 对话</h3>
        <p>与灵感对话，寻找故事的方向</p>
        <ul>
            <li>多模型支持</li>
            <li>流式输出</li>
            <li>对话历史</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==================== 快速开始 ====================
st.markdown("## 开始创作")

st.markdown("""
<div style="
    padding: 2.5rem 0;
    color: #666;
    line-height: 2;
    font-size: 1rem;
    letter-spacing: 0.5px;
">
    <p style="margin-bottom: 1.5rem;">创作是一个自然的过程：</p>
    <ol style="
        list-style: none;
        padding-left: 1.5rem;
        margin: 0;
    ">
        <li style="position: relative; padding: 0.8rem 0;">1. 在「小说创作」开启一个新的故事</li>
        <li style="position: relative; padding: 0.8rem 0;">2. 生成蓝图，勾勒故事的轮廓</li>
        <li style="position: relative; padding: 0.8rem 0;">3. 规划章节，搭建故事的骨架</li>
        <li style="position: relative; padding: 0.8rem 0;">4. 撰写内容，让故事自由生长</li>
        <li style="position: relative; padding: 0.8rem 0;">5. 如果需要，可将小说转换为剧本</li>
    </ol>
</div>
""", unsafe_allow_html=True)

# ==================== 技术特性 ====================
st.markdown("## 技术支持")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>AI 模型</h3>
        <p>多模型支持，灵活选择</p>
        <ul>
            <li>GLM-5.1</li>
            <li>Qwen3.5</li>
            <li>DeepSeek</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>平台架构</h3>
        <p>稳定可靠，快速响应</p>
        <ul>
            <li>FastAPI 后端</li>
            <li>Streamlit 前端</li>
            <li>百度千帆</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==================== 页脚 ====================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style="
    text-align: center;
    padding: 3rem 0 2rem 0;
    color: #999;
">
    <p style="
        font-family: 'Noto Serif SC', serif;
        font-size: 1rem;
        margin-bottom: 1rem;
        letter-spacing: 1px;
        font-style: italic;
    ">让故事自然生长</p>
    <p style="
        font-size: 0.85rem;
        margin-bottom: 0.5rem;
        letter-spacing: 0.5px;
    ">Powered by Streamlit & 百度千帆</p>
    <p style="
        font-size: 0.8rem;
        color: #bbb;
        margin: 0;
        letter-spacing: 0.5px;
    ">AI 小说创作平台 v1.0 | 2026</p>
</div>
""", unsafe_allow_html=True)
