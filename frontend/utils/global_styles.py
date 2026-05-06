# -*- coding: utf-8 -*-
"""
全局样式 - 浅色玻璃拟态主题（方案A）
参考：瞬息重启、Linear、Notion
温柔舒适，现代极简，适合文学创作
"""

GLOBAL_STYLES = """
<style>
    /* ==================== 字体引入 ==================== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Noto+Serif+SC:wght@300;400;500;600&display=swap');

    /* ==================== CSS 变量定义 ==================== */
    :root {
        --bg-primary: #f1f5f9;
        --bg-secondary: #e2e8f0;
        --text-primary: #1e293b;
        --text-secondary: #334155;
        --text-tertiary: #64748b;
        --accent-color: #38bdf8;
        --glass-bg: rgba(255, 255, 255, 0.6);
        --glass-border: rgba(255, 255, 255, 0.8);
        --shadow-sm: 0 4px 20px rgba(0, 0, 0, 0.03);
        --shadow-md: 0 15px 30px -10px rgba(0, 0, 0, 0.1);
        --radius-lg: 24px;
        --radius-xl: 32px;
    }

    /* ==================== 防止页面闪烁 - 立即应用背景色 ==================== */
    html, body, [class*="css"] {
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%) !important;
    }

    /* ==================== 全局样式 ==================== */
    * {
        font-family: 'Inter', 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 300;  /* 极细字体 */
    }

    /* 主背景 - 淡雅的灰白渐变 */
    .stApp {
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
    }

    /* ==================== 文本样式 ==================== */
    p, span, div {
        color: #475569;  /* 提高对比度，更深 */
        line-height: 1.8;
        font-weight: 400;  /* 常规字重，更清晰 */
    }

    /* ==================== 主标题样式 - 极简优雅 ==================== */
    .main-header {
        font-family: 'Noto Serif SC', serif;
        font-size: 3rem;
        font-weight: 400;
        text-align: center;
        padding: 3rem 0 1.5rem 0;
        color: #334155;
        letter-spacing: 3px;
        position: relative;
    }

    .main-header::after {
        content: '';
        display: block;
        width: 64px;
        height: 1px;
        background: linear-gradient(90deg, transparent, #38bdf8, transparent);
        margin: 1.5rem auto 0;
        opacity: 0.5;
    }

    /* ==================== 副标题样式 ==================== */
    .sub-header {
        font-family: 'Noto Serif SC', serif;
        font-size: 1.1rem;
        color: #94a3b8;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 300;
        letter-spacing: 1px;
    }

    /* ==================== 卡片样式 - 玻璃拟态 ==================== */
    .feature-card {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.8);
        padding: 2rem;
        border-radius: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
        margin: 1.5rem 0;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    .feature-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.8);
        box-shadow: 0 15px 30px -10px rgba(0, 0, 0, 0.1);
    }

    .feature-card h3 {
        font-family: 'Noto Serif SC', serif;
        color: #334155;
        font-size: 1.4rem;
        font-weight: 400;
        margin-bottom: 1rem;
        letter-spacing: 1px;
    }

    .feature-card p {
        color: #475569;
        line-height: 1.8;
        margin-bottom: 1rem;
        font-weight: 400;
    }

    .feature-card ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }

    .feature-card ul li {
        color: #475569;
        padding: 0.6rem 0;
        padding-left: 1.5rem;
        position: relative;
        font-weight: 400;
    }

    .feature-card ul li::before {
        content: '›';
        position: absolute;
        left: 0;
        color: #38bdf8;
        font-weight: 500;
        font-size: 1.3rem;
    }

    /* ==================== 侧边栏样式 ==================== */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.4);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.8);
    }

    [data-testid="stSidebar"] h1 {
        font-family: 'Noto Serif SC', serif;
        color: #334155;
        font-weight: 400;
        font-size: 1.4rem;
        letter-spacing: 1px;
    }

    [data-testid="stSidebar"] a {
        color: #475569 !important;
        transition: all 0.3s ease;
        font-weight: 400;
    }

    [data-testid="stSidebar"] a:hover {
        color: #38bdf8 !important;
    }

    /* ==================== 按钮样式 - 大圆角 ==================== */
    .stButton > button {
        background: #334155;
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.7rem 2rem;
        font-weight: 500;
        transition: all 0.3s ease;
        font-size: 0.9rem;
        letter-spacing: 1px;
    }

    .stButton > button:hover {
        background: #1e293b;
        transform: translateY(-2px);
        box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.15);
    }

    .stButton > button[kind="secondary"] {
        background: transparent;
        border: 1px solid #cbd5e1;
        color: #64748b;
    }

    .stButton > button[kind="secondary"]:hover {
        border-color: #38bdf8;
        color: #38bdf8;
        background: rgba(56, 189, 248, 0.05);
    }

    /* ==================== 输入框样式 - 玻璃拟态 ==================== */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.8);
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(10px);
        color: #334155;
        font-weight: 300;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #38bdf8;
        box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.1);
        background: rgba(255, 255, 255, 0.8);
    }

    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #94a3b8;
        font-weight: 400;
    }

    /* ==================== 选择框样式 ==================== */
    .stSelectbox > div > div,
    .stMultiselect > div > div {
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.8);
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(10px);
        color: #334155;
    }

    /* ==================== 标题样式 - 极细字体 ==================== */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Noto Serif SC', serif;
        color: #334155;
        font-weight: 400;
    }

    h2 {
        font-weight: 400;
        font-size: 1.6rem;
        letter-spacing: 1px;
        margin-bottom: 1.5rem;
    }

    /* ==================== 信息框样式 - 玻璃拟态 ==================== */
    .stAlert {
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.8);
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(10px);
        color: #334155;
    }

    /* ==================== 进度条样式 ==================== */
    .stProgress > div > div > div {
        background: #38bdf8;
        border-radius: 10px;
    }

    /* ==================== 分隔线样式 ==================== */
    hr {
        border: none;
        height: 1px;
        background: rgba(148, 163, 184, 0.3);
        margin: 2.5rem 0;
    }

    /* ==================== 隐藏 Streamlit 默认元素 ==================== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ==================== 页面容器样式 ==================== */
    .main .block-container {
        padding: 2.5rem 3.5rem;
        max-width: 1200px;
    }

    /* ==================== 表单样式 - 玻璃拟态 ==================== */
    .stForm {
        border: 1px solid rgba(255, 255, 255, 0.8);
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(20px);
        padding: 2rem;
        border-radius: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
    }

    /* ==================== 复选框和单选框 ==================== */
    .stCheckbox > label,
    .stRadio > label {
        color: #475569;
        font-weight: 400;
    }

    /* ==================== 数字输入框 ==================== */
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(10px);
        color: #334155;
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-radius: 16px;
        font-weight: 300;
    }

    /* ==================== 下载按钮 ==================== */
    .stDownloadButton > button {
        background: #334155;
        color: white;
        border-radius: 20px;
        padding: 0.7rem 2rem;
        font-weight: 500;
        transition: all 0.3s ease;
        letter-spacing: 1px;
    }

    .stDownloadButton > button:hover {
        background: #1e293b;
        transform: translateY(-2px);
    }

    /* ==================== 标签页样式 ==================== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: rgba(255, 255, 255, 0.4);
        padding: 0.5rem;
        border-radius: 20px;
    }

    .stTabs [data-baseweb="tab"] {
        color: #475569;
        font-weight: 400;
        border-radius: 16px;
        padding: 0.5rem 1.5rem;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        color: #334155;
        background: rgba(255, 255, 255, 0.8);
        font-weight: 400;
    }

    /* ==================== 表格样式 ==================== */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(10px);
        color: #334155;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.8);
    }

    .stDataFrame th {
        background: rgba(255, 255, 255, 0.8);
        color: #334155;
        font-weight: 500;
    }

    /* ==================== 文件上传 ==================== */
    .stFileUploader > div > div {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(10px);
        border: 2px dashed #cbd5e1;
        color: #475569;
        border-radius: 16px;
        transition: all 0.3s ease;
    }

    .stFileUploader > div > div:hover {
        border-color: #38bdf8;
        background: rgba(255, 255, 255, 0.8);
    }

    /* ==================== 状态色 ==================== */
    .stAlert[data-baseweb="notification"][kind="positive"] {
        background: rgba(134, 239, 172, 0.2);
        border-color: rgba(134, 239, 172, 0.5);
    }

    .stAlert[data-baseweb="notification"][kind="negative"] {
        background: rgba(252, 165, 165, 0.2);
        border-color: rgba(252, 165, 165, 0.5);
    }

    .stAlert[data-baseweb="notification"][kind="warning"] {
        background: rgba(253, 224, 71, 0.2);
        border-color: rgba(253, 224, 71, 0.5);
    }

    /* ==================== 滚动条样式 ==================== */
    ::-webkit-scrollbar {
        width: 4px;
        height: 4px;
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(100, 116, 139, 0.3);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: rgba(100, 116, 139, 0.5);
    }

    /* ==================== 加载动画 ==================== */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(5px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .stApp {
        animation: fadeIn 0.3s ease;
    }
</style>
"""


def apply_global_styles():
    """应用全局样式"""
    import streamlit as st
    st.markdown(GLOBAL_STYLES, unsafe_allow_html=True)
