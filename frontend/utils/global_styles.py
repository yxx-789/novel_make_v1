# -*- coding: utf-8 -*-
"""
全局样式 - 温暖夜色风主题（方案B）
参考：Typora、Bear Dark
温暖舒适，适合长时间阅读，文学感强
"""

GLOBAL_STYLES = """
<style>
    /* ==================== 字体引入 ==================== */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;600;700&family=Noto+Sans+SC:wght@300;400;500;600&display=swap');

    /* ==================== 防止页面闪烁 - 立即应用背景色 ==================== */
    html, body, [class*="css"] {
        background-color: #1e1e1e !important;
    }
    
    /* 强制立即渲染背景 */
    .stApp {
        background: #1e1e1e !important;
    }

    /* ==================== 全局样式 - 增大字体提高清晰度 ==================== */
    * {
        font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 16px;  /* 基础字体大小 */
    }

    /* 主背景 - 温暖的深灰 */
    .stApp {
        background: #1e1e1e;
    }

    /* ==================== 文本清晰度优化 ==================== */
    p, span, div {
        color: #b8b8b8;  /* 提高对比度 */
        line-height: 1.6;  /* 增加行高 */
    }

    /* 标题更大更清晰 */
    h1 { font-size: 2.5rem !important; }
    h2 { font-size: 1.8rem !important; }
    h3 { font-size: 1.4rem !important; }
    h4 { font-size: 1.2rem !important; }

    /* ==================== 主标题样式 ==================== */
    .main-header {
        font-family: 'Noto Serif SC', serif;
        font-size: 2.8rem;
        font-weight: 400;
        text-align: center;
        padding: 3rem 0 1.5rem 0;
        color: #d4d4d4;
        letter-spacing: 2px;
        position: relative;
    }

    .main-header::after {
        content: '';
        display: block;
        width: 48px;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e8c47c, transparent);
        margin: 1.2rem auto 0;
        opacity: 0.4;
    }

    /* ==================== 副标题样式 ==================== */
    .sub-header {
        font-family: 'Noto Serif SC', serif;
        font-size: 1.1rem;
        color: #808080;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 300;
        letter-spacing: 1px;
    }

    /* ==================== 卡片样式 - 三层次设计 ==================== */
    .feature-card {
        background: #282828;
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2);
        margin: 1.2rem 0;
        border: 1px solid #333;
        transition: all 0.3s ease;
    }

    .feature-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        transform: translateY(-1px);
        border-color: #444;
    }

    .feature-card h3 {
        font-family: 'Noto Serif SC', serif;
        color: #d4d4d4;
        font-size: 1.3rem;
        font-weight: 500;
        margin-bottom: 0.8rem;
        letter-spacing: 0.5px;
    }

    .feature-card p {
        color: #999;
        line-height: 1.7;
        margin-bottom: 1rem;
        font-weight: 400;
    }

    .feature-card ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }

    .feature-card ul li {
        color: #888;
        padding: 0.5rem 0;
        padding-left: 1.2rem;
        position: relative;
        font-weight: 400;
    }

    .feature-card ul li::before {
        content: '›';
        position: absolute;
        left: 0;
        color: #e8c47c;
        font-weight: 500;
        font-size: 1.2rem;
    }

    /* ==================== 侧边栏样式 - 最深层次 ==================== */
    [data-testid="stSidebar"] {
        background: #181818;
        border-right: 1px solid #2a2a2a;
    }

    [data-testid="stSidebar"] h1 {
        font-family: 'Noto Serif SC', serif;
        color: #d4d4d4;
        font-weight: 500;
        font-size: 1.3rem;
        letter-spacing: 1px;
    }

    [data-testid="stSidebar"] a {
        color: #888 !important;
        transition: all 0.2s ease;
    }

    [data-testid="stSidebar"] a:hover {
        color: #e8c47c !important;
    }

    /* ==================== 按钮样式 - 温暖的点缀 ==================== */
    .stButton > button {
        background: #e8c47c;
        color: #1e1e1e;
        border: none;
        border-radius: 6px;
        padding: 0.6rem 1.8rem;
        font-weight: 500;
        transition: all 0.2s ease;
        font-size: 0.9rem;
        letter-spacing: 0.5px;
    }

    .stButton > button:hover {
        background: #d4a85c;
        box-shadow: 0 2px 8px rgba(232, 196, 124, 0.3);
    }

    .stButton > button[kind="secondary"] {
        background: transparent;
        border: 1px solid #444;
        color: #888;
    }

    .stButton > button[kind="secondary"]:hover {
        border-color: #e8c47c;
        color: #e8c47c;
    }

    /* ==================== 输入框样式 ==================== */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 6px;
        border: 1px solid #333;
        background: #282828;
        color: #d4d4d4;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #e8c47c;
        box-shadow: 0 0 0 3px rgba(232, 196, 124, 0.1);
    }

    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #666;
    }

    /* ==================== 选择框样式 ==================== */
    .stSelectbox > div > div,
    .stMultiselect > div > div {
        border-radius: 6px;
        border: 1px solid #333;
        background: #282828;
        color: #d4d4d4;
    }

    /* ==================== 标题样式 ==================== */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Noto Serif SC', serif;
        color: #d4d4d4;
    }

    h2 {
        font-weight: 500;
        font-size: 1.5rem;
        letter-spacing: 0.5px;
        margin-bottom: 1.5rem;
    }

    /* ==================== 文本样式 ==================== */
    p, span, div {
        color: #999;
    }

    /* ==================== 信息框样式 ==================== */
    .stAlert {
        border-radius: 6px;
        border: 1px solid #333;
        background: #282828;
        color: #d4d4d4;
    }

    /* ==================== 进度条样式 ==================== */
    .stProgress > div > div > div {
        background: #e8c47c;
    }

    /* ==================== 分隔线样式 ==================== */
    hr {
        border: none;
        height: 1px;
        background: #333;
        margin: 2rem 0;
    }

    /* ==================== 隐藏 Streamlit 默认元素 ==================== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ==================== 页面容器样式 ==================== */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1200px;
    }

    /* ==================== 表单样式 ==================== */
    .stForm {
        border: 1px solid #333;
        background: #282828;
        padding: 1.5rem;
        border-radius: 8px;
    }

    /* ==================== 复选框和单选框 ==================== */
    .stCheckbox > label,
    .stRadio > label {
        color: #999;
    }

    /* ==================== 数字输入框 ==================== */
    .stNumberInput > div > div > input {
        background: #282828;
        color: #d4d4d4;
        border: 1px solid #333;
    }

    /* ==================== 下载按钮 ==================== */
    .stDownloadButton > button {
        background: #e8c47c;
        color: #1e1e1e;
        border-radius: 6px;
        padding: 0.6rem 1.8rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    .stDownloadButton > button:hover {
        background: #d4a85c;
    }

    /* ==================== 标签页样式 ==================== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        color: #888;
    }

    .stTabs [aria-selected="true"] {
        color: #e8c47c;
    }

    /* ==================== 表格样式 ==================== */
    .stDataFrame {
        background: #282828;
        color: #d4d4d4;
    }

    .stDataFrame th {
        background: #181818;
        color: #e8c47c;
    }

    /* ==================== 文件上传 ==================== */
    .stFileUploader > div > div {
        background: #282828;
        border: 2px dashed #444;
        color: #888;
    }

    .stFileUploader > div > div:hover {
        border-color: #e8c47c;
    }

    /* ==================== 状态色（莫兰迪色调）==================== */
    .stAlert[data-baseweb="notification"][kind="positive"] {
        background: #2d3d2e;
        border-color: #4a5d4b;
    }

    .stAlert[data-baseweb="notification"][kind="negative"] {
        background: #4d2e2e;
        border-color: #6d3d3d;
    }

    .stAlert[data-baseweb="notification"][kind="warning"] {
        background: #4d3d2e;
        border-color: #6d5d3d;
    }
</style>
"""


def apply_global_styles():
    """应用全局样式"""
    import streamlit as st
    st.markdown(GLOBAL_STYLES, unsafe_allow_html=True)
