"""
AI 小说创作平台 - 主入口文件
"""
import streamlit as st
from utils.config import Config

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
    /* 主标题样式 */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* 副标题样式 */
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* 卡片样式 */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    /* 状态指示器 */
    .status-online {
        color: #28a745;
        font-weight: bold;
    }
    
    .status-offline {
        color: #dc3545;
        font-weight: bold;
    }
    
    /* 隐藏 Streamlit 默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==================== 侧边栏 ====================
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/000000/book.png", width=100)
    st.title("📚 AI 小说创作平台")
    st.markdown("---")
    
    # 快速导航
    st.markdown("### 🎯 快速导航")
    st.page_link("pages/1_🏠_首页.py", label="🏠 首页", icon="🏠")
    st.page_link("pages/2_✍️_小说创作.py", label="✍️ 小说创作", icon="✍️")
    st.page_link("pages/3_📚_小说管理.py", label="📚 小说管理", icon="📚")
    st.page_link("pages/4_🎬_剧本转换.py", label="🎬 剧本转换", icon="🎬")
    st.page_link("pages/5_💬_AI聊天.py", label="💬 AI聊天", icon="💬")
    st.page_link("pages/6_⚙️_系统设置.py", label="⚙️ 系统设置", icon="⚙️")
    
    st.markdown("---")
    
    # 系统状态
    st.markdown("### 📊 系统状态")
    if st.button("🔄 刷新状态", use_container_width=True):
        st.rerun()

# ==================== 主内容区 ====================
st.markdown('<h1 class="main-header">AI 小说创作平台</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">基于大语言模型的智能小说创作工具</p>', unsafe_allow_html=True)

# ==================== 功能介绍 ====================
st.markdown("## ✨ 核心功能")

col1, col2, col3 = st.columns(3)

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
<div style="text-align: center; color: #999; padding: 2rem 0;">
    <p>🎨 Made with ❤️ by AI | Powered by Streamlit & 百度千帆</p>
    <p>📖 AI 小说创作平台 v1.0 | 2026</p>
</div>
""", unsafe_allow_html=True)
