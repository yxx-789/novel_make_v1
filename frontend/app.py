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
st.markdown("""
<style>
    /* ==================== 全局样式 ==================== */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
    
    * {
        font-family: 'Noto Sans SC', sans-serif;
    }
    
    /* ==================== 主标题样式 ==================== */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        padding: 3rem 0 1.5rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradient-shift 8s ease infinite;
        background-size: 200% 200%;
        letter-spacing: 2px;
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* ==================== 副标题样式 ==================== */
    .sub-header {
        font-size: 1.4rem;
        color: #6b7280;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 300;
        letter-spacing: 1px;
    }
    
    /* ==================== 卡片样式 ==================== */
    .feature-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 
            0 4px 6px -1px rgba(0, 0, 0, 0.1),
            0 2px 4px -1px rgba(0, 0, 0, 0.06),
            inset 0 1px 0 rgba(255, 255, 255, 0.8);
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.8);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 
            0 20px 25px -5px rgba(0, 0, 0, 0.1),
            0 10px 10px -5px rgba(0, 0, 0, 0.04),
            inset 0 1px 0 rgba(255, 255, 255, 0.8);
    }
    
    .feature-card:hover::before {
        opacity: 1;
    }
    
    .feature-card h3 {
        color: #1f2937;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .feature-card p {
        color: #6b7280;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    
    .feature-card ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .feature-card ul li {
        color: #4b5563;
        padding: 0.5rem 0;
        padding-left: 1.5rem;
        position: relative;
        transition: all 0.2s;
    }
    
    .feature-card ul li::before {
        content: '▸';
        position: absolute;
        left: 0;
        color: #667eea;
        font-weight: bold;
    }
    
    .feature-card ul li:hover {
        padding-left: 2rem;
        color: #667eea;
    }
    
    /* ==================== 状态指示器 ==================== */
    .status-online {
        color: #10b981;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .status-online::before {
        content: '●';
        animation: pulse 2s infinite;
    }
    
    .status-offline {
        color: #ef4444;
        font-weight: 600;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* ==================== 按钮样式 ==================== */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 6px -1px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 12px -2px rgba(102, 126, 234, 0.5);
    }
    
    /* ==================== 侧边栏样式 ==================== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    [data-testid="stSidebar"] .element-container {
        margin: 0.5rem 0;
    }
    
    [data-testid="stSidebar"] h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
    }
    
    /* ==================== 隐藏 Streamlit 默认元素 ==================== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ==================== 页面容器样式 ==================== */
    .main .block-container {
        padding: 2rem 3rem;
    }
    
    /* ==================== 标题样式 ==================== */
    h2 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        border-bottom: 2px solid transparent;
        background-image: linear-gradient(135deg, #667eea 0%, #764ba2 100%), linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-size: 0% 2px, 100% 0%;
        background-position: 0 100%, 0 100%;
        background-repeat: no-repeat;
        padding-bottom: 0.5rem;
    }
    
    /* ==================== 信息框样式 ==================== */
    .stAlert {
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* ==================== 进度条样式 ==================== */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* ==================== 分隔线样式 ==================== */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, #764ba2, transparent);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 侧边栏 ====================
with st.sidebar:
    # Logo和标题
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <div style="
            font-size: 4rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 1rem;
        ">📖</div>
        <h1 style="
            font-size: 1.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0;
        ">AI 小说创作平台</h1>
        <p style="
            color: #6b7280;
            font-size: 0.875rem;
            margin: 0.5rem 0 0 0;
        ">Powered by 百度千帆</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 快速导航
    st.markdown("""
    <div style="margin-bottom: 1rem;">
        <h3 style="
            font-size: 0.875rem;
            font-weight: 700;
            color: #374151;
            margin: 0 0 1rem 0;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        ">🎯 快速导航</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.page_link("pages/1_🏠_首页.py", label="🏠 首页", icon="🏠")
    st.page_link("pages/2_✍️_小说创作.py", label="✍️ 小说创作", icon="✍️")
    st.page_link("pages/3_📚_小说管理.py", label="📚 小说管理", icon="📚")
    st.page_link("pages/4_🎬_剧本转换.py", label="🎬 剧本转换", icon="🎬")
    st.page_link("pages/5_💬_AI聊天.py", label="💬 AI聊天", icon="💬")
    st.page_link("pages/6_⚙️_系统设置.py", label="⚙️ 系统设置", icon="⚙️")
    
    st.markdown("---")
    
    # 系统状态
    st.markdown("""
    <div style="margin-bottom: 1rem;">
        <h3 style="
            font-size: 0.875rem;
            font-weight: 700;
            color: #374151;
            margin: 0 0 1rem 0;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        ">📊 系统状态</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 刷新状态", use_container_width=True):
        st.rerun()

# ==================== 主内容区 ====================
st.markdown('<h1 class="main-header">AI 小说创作平台</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">基于大语言模型的智能小说创作工具</p>', unsafe_allow_html=True)

# ==================== 功能介绍 ====================
st.markdown("## ✨ 核心功能")

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>✍️ 小说创作</h3>
        <p>从零开始创作小说，支持蓝图生成、大纲规划、章节撰写全流程</p>
        <ul>
            <li>智能蓝图生成</li>
            <li>自动大纲规划</li>
            <li>章节内容生成</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>🎬 剧本转换</h3>
        <p>将小说自动转换为剧本格式，支持多种剧本风格</p>
        <ul>
            <li>电影剧本</li>
            <li>电视剧剧本</li>
            <li>舞台剧剧本</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>💬 AI 聊天</h3>
        <p>与 AI 进行实时对话，获取创作灵感和建议</p>
        <ul>
            <li>多模型支持</li>
            <li>流式输出</li>
            <li>对话历史</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==================== 快速开始 ====================
st.markdown("---")
st.markdown("## 🚀 快速开始")

st.markdown("""
### 使用流程

1. **📝 创建小说** - 在"小说创作"页面创建新的小说项目
2. **🎨 生成蓝图** - 系统自动生成故事蓝图和核心元素
3. **📋 规划大纲** - 生成章节大纲，确定故事结构
4. **✍️ 生成章节** - 逐章生成小说内容
5. **🎬 剧本转换** - 可选：将小说转换为剧本格式
""")

# ==================== 技术特性 ====================
st.markdown("---")
st.markdown("## 🛠️ 技术特性")

col1, col2 = st.columns(2)

with col1:
    st.info("""
    **🎯 支持的大模型**
    - GLM-5.1 (智谱 AI)
    - Qwen3.5-397B (通义千问)
    - DeepSeek-V3.2
    """)
    
with col2:
    st.success("""
    **💡 技术栈**
    - 后端：FastAPI + 百度千帆
    - 前端：Streamlit
    - AI 引擎：大语言模型
    """)

# ==================== 页脚 ====================
st.markdown("---")
st.markdown("""
<div style="
    text-align: center;
    padding: 3rem 0 2rem 0;
    background: linear-gradient(180deg, transparent 0%, rgba(102, 126, 234, 0.05) 100%);
    border-radius: 16px;
    margin-top: 2rem;
">
    <p style="
        font-size: 1.1rem;
        color: #6b7280;
        margin-bottom: 0.5rem;
        font-weight: 500;
    ">🎨 Made with ❤️ by AI</p>
    <p style="
        font-size: 0.875rem;
        color: #9ca3af;
        margin-bottom: 0.75rem;
    ">Powered by Streamlit & 百度千帆</p>
    <div style="
        display: inline-block;
        padding: 0.5rem 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
        box-shadow: 0 4px 6px -1px rgba(102, 126, 234, 0.3);
    ">
        📖 AI 小说创作平台 v1.0 | 2026
    </div>
</div>
""", unsafe_allow_html=True)
