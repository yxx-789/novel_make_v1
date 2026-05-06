# -*- coding: utf-8 -*-
"""
全局样式 - 夜色叙事风主题
深蓝夜色 + 暗金点缀
"""

GLOBAL_STYLES = """
<style>
    /* ==================== 字体引入 ==================== */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;600;700&family=Noto+Sans+SC:wght@300;400;500;600&display=swap');

    /* ==================== 全局样式 ==================== */
    * {
        font-family: 'Noto Sans SC', sans-serif;
    }

    /* 全局背景 - 夜色深蓝 */
    .stApp {
        background: linear-gradient(180deg, #2c3e50 0%, #1c2833 100%);
    }

    /* ==================== 主标题样式 ==================== */
    .main-header {
        font-family: 'Noto Serif SC', serif;
        font-size: 3rem;
        font-weight: 400;
        text-align: center;
        padding: 4rem 0 1.5rem 0;
        color: #F4F1EA;
        letter-spacing: 4px;
        position: relative;
    }

    .main-header::after {
        content: '';
        display: block;
        width: 60px;
        height: 2px;
        background: #d4af37;
        margin: 1.5rem auto 0;
        opacity: 0.6;
    }

    /* ==================== 副标题样式 ==================== */
    .sub-header {
        font-family: 'Noto Serif SC', serif;
        font-size: 1.2rem;
        color: #bdc3c7;
        text-align: center;
        margin-bottom: 4rem;
        font-weight: 300;
        letter-spacing: 2px;
        font-style: italic;
    }

    /* ==================== 卡片样式 - 夜色质感 ==================== */
    .feature-card {
        background: #34495e;
        padding: 2.5rem;
        border-radius: 4px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.3);
        margin: 1.5rem 0;
        border: 1px solid rgba(212, 175, 55, 0.1);
        transition: all 0.4s ease;
        position: relative;
    }

    .feature-card::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 3px;
        background: #d4af37;
        opacity: 0.3;
        transition: opacity 0.3s;
    }

    .feature-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        transform: translateY(-2px);
        border-color: rgba(212, 175, 55, 0.3);
    }

    .feature-card:hover::before {
        opacity: 0.6;
    }

    .feature-card h3 {
        font-family: 'Noto Serif SC', serif;
        color: #F4F1EA;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 1rem;
        letter-spacing: 1px;
    }

    .feature-card p {
        color: #95a5a6;
        line-height: 1.8;
        margin-bottom: 1.2rem;
        font-weight: 300;
    }

    .feature-card ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }

    .feature-card ul li {
        color: #7f8c8d;
        padding: 0.6rem 0;
        padding-left: 1.5rem;
        position: relative;
        font-weight: 400;
        letter-spacing: 0.5px;
    }

    .feature-card ul li::before {
        content: '·';
        position: absolute;
        left: 0;
        color: #d4af37;
        font-weight: bold;
        font-size: 1.5rem;
        line-height: 1;
    }

    /* ==================== 状态指示器 ==================== */
    .status-online {
        color: #4A7C59;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.9rem;
    }

    .status-online::before {
        content: '●';
        font-size: 0.5rem;
    }

    .status-offline {
        color: #9E3D2D;
        font-weight: 500;
        font-size: 0.9rem;
    }

    /* ==================== 按钮样式 ==================== */
    .stButton > button {
        background: #d4af37;
        color: #1c2833;
        border: none;
        border-radius: 2px;
        padding: 0.7rem 2rem;
        font-weight: 500;
        transition: all 0.3s ease;
        font-size: 0.9rem;
        letter-spacing: 1px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
    }

    .stButton > button:hover {
        background: #E5C974;
        box-shadow: 0 2px 6px rgba(212, 175, 55, 0.4);
    }

    .stButton > button[kind="secondary"] {
        background: transparent;
        border: 1px solid #d4af37;
        color: #d4af37;
    }

    .stButton > button[kind="secondary"]:hover {
        background: rgba(212, 175, 55, 0.1);
    }

    /* ==================== 侧边栏样式 ==================== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1c2833 0%, #17202a 100%);
        border-right: 1px solid rgba(212, 175, 55, 0.1);
    }

    [data-testid="stSidebar"] .element-container {
        margin: 0.3rem 0;
    }

    [data-testid="stSidebar"] h1 {
        font-family: 'Noto Serif SC', serif;
        color: #F4F1EA;
        font-weight: 600;
        font-size: 1.5rem;
        letter-spacing: 2px;
    }

    /* ==================== 页面链接样式 ==================== */
    [data-testid="stSidebar"] a {
        color: #95a5a6 !important;
        transition: all 0.3s ease;
    }

    [data-testid="stSidebar"] a:hover {
        color: #E5C974 !important;
    }

    /* ==================== 隐藏 Streamlit 默认元素 ==================== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ==================== 页面容器样式 ==================== */
    .main .block-container {
        padding: 3rem 4rem;
        max-width: 1200px;
    }

    /* ==================== 标题样式 ==================== */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Noto Serif SC', serif;
        color: #F4F1EA;
    }

    h2 {
        font-weight: 600;
        font-size: 1.6rem;
        letter-spacing: 1px;
        border-bottom: 1px solid rgba(212, 175, 55, 0.2);
        padding-bottom: 1rem;
        margin-bottom: 2rem;
    }

    /* ==================== 信息框样式 ==================== */
    .stAlert {
        border-radius: 2px;
        border: 1px solid rgba(212, 175, 55, 0.2);
        box-shadow: 0 1px 3px rgba(0,0,0,0.3);
        background: #34495e;
        color: #F4F1EA;
    }

    /* ==================== 进度条样式 ==================== */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #d4af37 0%, #E5C974 100%);
    }

    /* ==================== 分隔线样式 ==================== */
    hr {
        border: none;
        height: 1px;
        background: rgba(212, 175, 55, 0.1);
        margin: 3rem 0;
    }

    /* ==================== 文本输入框样式 ==================== */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 2px;
        border: 1px solid rgba(212, 175, 55, 0.2);
        background: #34495e;
        color: #F4F1EA;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #d4af37;
        box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.1);
    }

    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #7f8c8d;
    }

    /* ==================== 选择框样式 ==================== */
    .stSelectbox > div > div,
    .stMultiselect > div > div {
        border-radius: 2px;
        border: 1px solid rgba(212, 175, 55, 0.2);
        background: #34495e;
        color: #F4F1EA;
    }

    .stSelectbox > div > div:focus,
    .stMultiselect > div > div:focus {
        border-color: #d4af37;
        box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.1);
    }

    /* ==================== 滑块样式 ==================== */
    .stSlider > div > div > div {
        background: #d4af37;
    }

    /* ==================== 复选框样式 ==================== */
    .stCheckbox > label {
        color: #F4F1EA;
    }

    /* ==================== 单选框样式 ==================== */
    .stRadio > label {
        color: #F4F1EA;
    }

    /* ==================== 文本样式 ==================== */
    p, span, div {
        color: #95a5a6;
    }

    .stMarkdown {
        color: #95a5a6;
    }

    /* ==================== 代码块样式 ==================== */
    .stCodeBlock {
        background: #1c2833;
        border: 1px solid rgba(212, 175, 55, 0.2);
    }

    /* ==================== 表格样式 ==================== */
    .stDataFrame {
        background: #34495e;
        color: #F4F1EA;
    }

    .stDataFrame th {
        background: #1c2833;
        color: #E5C974;
    }

    /* ==================== 下载按钮样式 ==================== */
    .stDownloadButton > button {
        background: #d4af37;
        color: #1c2833;
        border: none;
        border-radius: 2px;
        padding: 0.7rem 2rem;
        font-weight: 500;
        transition: all 0.3s ease;
        font-size: 0.9rem;
        letter-spacing: 1px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
    }

    .stDownloadButton > button:hover {
        background: #E5C974;
        box-shadow: 0 2px 6px rgba(212, 175, 55, 0.4);
    }

    /* ==================== 表单样式 ==================== */
    .stForm {
        border: 1px solid rgba(212, 175, 55, 0.1);
        background: #34495e;
        padding: 2rem;
        border-radius: 4px;
    }

    /* ==================== 标签页样式 ==================== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }

    .stTabs [data-baseweb="tab"] {
        color: #95a5a6;
    }

    .stTabs [aria-selected="true"] {
        color: #E5C974;
    }

    /* ==================== 指数器样式 ==================== */
    .stNumberInput > div > div > input {
        background: #34495e;
        color: #F4F1EA;
        border: 1px solid rgba(212, 175, 55, 0.2);
    }

    .stNumberInput > div > div > input:focus {
        border-color: #d4af37;
        box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.1);
    }

    /* ==================== 日期选择器样式 ==================== */
    .stDateInput > div > div > input {
        background: #34495e;
        color: #F4F1EA;
        border: 1px solid rgba(212, 175, 55, 0.2);
    }

    .stDateInput > div > div > input:focus {
        border-color: #d4af37;
        box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.1);
    }

    /* ==================== 文件上传样式 ==================== */
    .stFileUploader > div > div {
        background: #34495e;
        border: 2px dashed rgba(212, 175, 55, 0.3);
        color: #95a5a6;
    }

    .stFileUploader > div > div:hover {
        border-color: #d4af37;
        background: rgba(52, 73, 94, 0.8);
    }
</style>
"""


def apply_global_styles():
    """应用全局样式"""
    import streamlit as st
    st.markdown(GLOBAL_STYLES, unsafe_allow_html=True)
