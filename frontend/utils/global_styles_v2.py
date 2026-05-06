# -*- coding: utf-8 -*-
"""
全局样式 - 现代极简风主题（参考Linear/Notion）
层次分明，温暖舒适，不压抑
"""

GLOBAL_STYLES = """
<style>
    /* ==================== 字体引入 ==================== */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;600;700&family=Noto+Sans+SC:wght@300;400;500;600&display=swap');

    /* ==================== 全局样式 ==================== */
    * {
        font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* ==================== 方案A：现代极简风（推荐）==================== */
    /* 参考：Linear、Notion、Bear */

    /* 主背景 - 深灰黑，有呼吸感 */
    .stApp {
        background: #1a1a1a;
    }

    /* ==================== 标题样式 ==================== */
    .main-header {
        font-family: 'Noto Serif SC', serif;
        font-size: 2.8rem;
        font-weight: 400;
        text-align: center;
        padding: 3rem 0 1.5rem 0;
        color: #e8e8e8;
        letter-spacing: 2px;
        position: relative;
    }

    .main-header::after {
        content: '';
        display: block;
        width: 48px;
        height: 1px;
        background: linear-gradient(90deg, transparent, #6366f1, transparent);
        margin: 1.2rem auto 0;
        opacity: 0.4;
    }

    /* ==================== 副标题样式 ==================== */
    .sub-header {
        font-family: 'Noto Serif SC', serif;
        font-size: 1.1rem;
        color: #999;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 300;
        letter-spacing: 1px;
    }

    /* ==================== 卡片样式 - 分层设计 ==================== */
    .feature-card {
        background: #242424;
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.2);
        margin: 1.2rem 0;
        border: 1px solid #2a2a2a;
        transition: all 0.3s ease;
    }

    .feature-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        transform: translateY(-1px);
        border-color: #3a3a3a;
    }

    .feature-card h3 {
        font-family: 'Noto Serif SC', serif;
        color: #e8e8e8;
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
        color: #6366f1;
        font-weight: 500;
        font-size: 1.2rem;
    }

    /* ==================== 侧边栏样式 - 更深的层次 ==================== */
    [data-testid="stSidebar"] {
        background: #141414;
        border-right: 1px solid #2a2a2a;
    }

    [data-testid="stSidebar"] h1 {
        font-family: 'Noto Serif SC', serif;
        color: #e8e8e8;
        font-weight: 500;
        font-size: 1.3rem;
        letter-spacing: 1px;
    }

    [data-testid="stSidebar"] a {
        color: #888 !important;
        transition: all 0.2s ease;
    }

    [data-testid="stSidebar"] a:hover {
        color: #e8e8e8 !important;
    }

    /* ==================== 按钮样式 - 柔和的点缀 ==================== */
    .stButton > button {
        background: #6366f1;
        color: #fff;
        border: none;
        border-radius: 6px;
        padding: 0.6rem 1.8rem;
        font-weight: 500;
        transition: all 0.2s ease;
        font-size: 0.9rem;
        letter-spacing: 0.5px;
    }

    .stButton > button:hover {
        background: #818cf8;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
    }

    .stButton > button[kind="secondary"] {
        background: transparent;
        border: 1px solid #3a3a3a;
        color: #888;
    }

    .stButton > button[kind="secondary"]:hover {
        border-color: #6366f1;
        color: #e8e8e8;
    }

    /* ==================== 输入框样式 ==================== */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 6px;
        border: 1px solid #2a2a2a;
        background: #1e1e1e;
        color: #e8e8e8;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }

    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #666;
    }

    /* ==================== 选择框样式 ==================== */
    .stSelectbox > div > div,
    .stMultiselect > div > div {
        border-radius: 6px;
        border: 1px solid #2a2a2a;
        background: #1e1e1e;
        color: #e8e8e8;
    }

    /* ==================== 标题样式 ==================== */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Noto Serif SC', serif;
        color: #e8e8e8;
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
        border: 1px solid #2a2a2a;
        background: #1e1e1e;
        color: #e8e8e8;
    }

    /* ==================== 进度条样式 ==================== */
    .stProgress > div > div > div {
        background: #6366f1;
    }

    /* ==================== 分隔线样式 ==================== */
    hr {
        border: none;
        height: 1px;
        background: #2a2a2a;
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
        border: 1px solid #2a2a2a;
        background: #1e1e1e;
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
        background: #1e1e1e;
        color: #e8e8e8;
        border: 1px solid #2a2a2a;
    }

    /* ==================== 下载按钮 ==================== */
    .stDownloadButton > button {
        background: #6366f1;
        color: #fff;
        border-radius: 6px;
        padding: 0.6rem 1.8rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    .stDownloadButton > button:hover {
        background: #818cf8;
    }

    /* ==================== 标签页样式 ==================== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        color: #888;
    }

    .stTabs [aria-selected="true"] {
        color: #e8e8e8;
    }

    /* ==================== 表格样式 ==================== */
    .stDataFrame {
        background: #1e1e1e;
        color: #e8e8e8;
    }

    .stDataFrame th {
        background: #141414;
        color: #999;
    }

    /* ==================== 文件上传 ==================== */
    .stFileUploader > div > div {
        background: #1e1e1e;
        border: 2px dashed #2a2a2a;
        color: #888;
    }

    .stFileUploader > div > div:hover {
        border-color: #6366f1;
    }
</style>
"""


# 古典符号映射（替代emoji）
ICON_MAP = {
    # 页面标题
    "首页": "◈",
    "小说创作": "✦",
    "小说管理": "❖",
    "剧本转换": "▣",
    "AI聊天": "◐",
    "系统设置": "⚙",

    # 操作按钮
    "创建": "✦",
    "生成": "▶",
    "导出": "▤",
    "刷新": "↻",
    "删除": "✕",
    "查看": "◉",
    "复制": "⎘",
    "编辑": "✎",
    "保存": "▼",

    # 状态
    "成功": "✓",
    "错误": "✕",
    "警告": "△",
    "信息": "○",

    # 内容类型
    "小说": "⬡",
    "章节": "◇",
    "角色": "◆",
    "大纲": "☰",
    "蓝图": "☱",
}


def apply_global_styles():
    """应用全局样式"""
    import streamlit as st
    st.markdown(GLOBAL_STYLES, unsafe_allow_html=True)


def replace_emoji(text: str) -> str:
    """替换emoji为古典符号"""
    for emoji, symbol in ICON_MAP.items():
        text = text.replace(emoji, symbol)
    return text
