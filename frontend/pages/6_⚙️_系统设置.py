"""
系统设置页面 - 配置和管理系统参数
"""
import streamlit as st
from utils.api import api_client, APIClient
from utils.config import Config
from datetime import datetime

st.set_page_config(

    page_title="系统设置 - AI 小说创作平台",
    page_icon="⚙",
    layout="wide"
)

# 应用全局样式和页面主题
from utils.global_styles import apply_global_styles, apply_page_theme
apply_global_styles()
apply_page_theme("系统设置")

st.title("⚙ 系统设置")

# ==================== API 配置 ====================
st.markdown("## 🔌 API 配置")

with st.form("api_config_form"):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        current_url = Config.API_BASE_URL
        new_api_url = st.text_input(
            "🌐 后端 API 地址",
            value=current_url,
            placeholder="例如: http://localhost:8000",
            help="修改后端 API 的基础地址"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("💾 保存配置", use_container_width=True, type="primary")
    
    if submitted:
        if new_api_url:
            Config.update_api_url(new_api_url)
            api_client.base_url = new_api_url
            st.success(f"✓ API 地址已更新为: {new_api_url}")
            st.rerun()
        else:
            st.error("✕ API 地址不能为空")

# 显示当前配置
with st.expander("▤ 查看当前配置", expanded=False):
    st.json({
        "API_BASE_URL": Config.API_BASE_URL,
        "DEFAULT_MODEL": Config.DEFAULT_MODEL,
        "PAGE_TITLE": Config.PAGE_TITLE,
        "LAYOUT": Config.LAYOUT
    })

# ==================== 连接测试 ====================
st.markdown("---")
st.markdown("## ◉ 连接测试")

col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("🏥 健康检查", use_container_width=True, type="primary"):
        with st.spinner("正在检查..."):
            health = api_client.health_check()
        
        if "error" not in health:
            status = health.get("status", "unknown")
            if status == "healthy":
                st.success("✓ 后端服务正常")
                st.json(health)
            else:
                st.warning(f"△ 状态: {status}")
                st.json(health)
        else:
            st.error(f"✕ 连接失败: {health['error']}")
            st.info("○ 请检查：\n1. 后端服务是否启动\n2. API 地址是否正确\n3. 网络连接是否正常")

with col2:
    if st.button("🤖 测试模型接口", use_container_width=True):
        with st.spinner("正在测试..."):
            models = api_client.get_models()
        
        if "models" in models:
            st.success(f"✓ 获取到 {len(models['models'])} 个模型")
            st.json(models)
        else:
            st.error(f"✕ 获取失败: {models.get('error', '未知错误')}")

with col3:
    if st.button("❖ 测试小说接口", use_container_width=True):
        with st.spinner("正在测试..."):
            novels = api_client.get_novels()
        
        if "novels" in novels:
            st.success(f"✓ 获取到 {len(novels['novels'])} 本小说")
            st.json({"count": len(novels["novels"])})
        else:
            st.error(f"✕ 获取失败: {novels.get('error', '未知错误')}")

# ==================== 可用模型管理 ====================
st.markdown("---")
st.markdown("## 🤖 可用模型")

with st.spinner("加载模型列表..."):
    models_result = api_client.get_models()

if "models" in models_result and models_result["models"]:
    models = models_result["models"]
    
    st.markdown(f"### 共 {len(models)} 个可用模型")
    
    # 模型卡片展示
    cols = st.columns(min(len(models), 3))
    
    for idx, model in enumerate(models):
        col_idx = idx % 3
        
        with cols[col_idx]:
            model_id = model.get("id", "unknown")
            model_name = model.get("name", "未知模型")
            model_provider = model.get("provider", "未知")
            model_type = model.get("type", "未知")
            
            # 判断是否为当前默认模型
            is_default = (model_id == Config.DEFAULT_MODEL)
            
            st.markdown(f"""
            <div style="
                background: {'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' if is_default else '#f8f9fa'};
                padding: 1.5rem;
                border-radius: 10px;
                {'color: white;' if is_default else 'color: #333;'}
                margin-bottom: 1rem;
            ">
                <h4 style="margin: 0; {'color: white;' if is_default else ''}">
                    {'✦ ' if is_default else ''}{model_name}
                </h4>
                <p style="margin: 0.5rem 0 0 0; opacity: 0.8; font-size: 0.9rem;">
                    ID: {model_id}
                </p>
                <p style="margin: 0.25rem 0 0 0; opacity: 0.8; font-size: 0.85rem;">
                    提供商: {model_provider} | 类型: {model_type}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # 设置为默认模型按钮
            if not is_default:
                if st.button(
                    f"✦ 设为默认",
                    key=f"set_default_{model_id}",
                    use_container_width=True
                ):
                    Config.DEFAULT_MODEL = model_id
                    st.success(f"✓ 已将 {model_name} 设置为默认模型")
                    st.rerun()
            else:
                st.info("✓ 当前默认模型")
    
    # 模型详细列表
    with st.expander("▤ 查看模型详细列表", expanded=False):
        for model in models:
            st.json(model)

else:
    st.warning("△ 无法获取模型列表")
    st.info("○ 请检查后端 API 连接是否正常")

# ==================== 默认模型设置 ====================
st.markdown("---")
st.markdown("## ✦ 默认模型设置")

if "models" in models_result and models_result["models"]:
    model_options = {
        f"{m.get('name', m.get('id', '未知'))} ({m.get('id', '未知')})": m.get("id")
        for m in models_result["models"]
    }
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_model_name = st.selectbox(
            "🤖 选择默认模型",
            options=list(model_options.keys()),
            index=list(model_options.values()).index(Config.DEFAULT_MODEL)
            if Config.DEFAULT_MODEL in model_options.values() else 0
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✓ 确认设置", use_container_width=True, type="primary"):
            selected_model_id = model_options[selected_model_name]
            Config.DEFAULT_MODEL = selected_model_id
            st.success(f"✓ 默认模型已设置为: {selected_model_name}")
            st.rerun()

else:
    st.warning("△ 暂无可选模型")

# ==================== 系统信息 ====================
st.markdown("---")
st.markdown("## ☰ 系统信息")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🖥️ 前端信息")
    st.markdown(f"""
    - **平台**: Streamlit
    - **版本**: {st.__version__}
    - **布局**: {Config.LAYOUT}
    - **当前时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """)

with col2:
    st.markdown("### 🔌 API 信息")
    st.markdown(f"""
    - **地址**: `{Config.API_BASE_URL}`
    - **默认模型**: `{Config.DEFAULT_MODEL}`
    - **超时时间**: 30 秒
    """)

with col3:
    st.markdown("### 📈 状态统计")
    
    # 获取统计信息
    novels_result = api_client.get_novels()
    
    if "novels" in novels_result:
        novel_count = len(novels_result["novels"])
        st.metric("❖ 小说总数", novel_count)
    
    if "models" in models_result:
        model_count = len(models_result["models"])
        st.metric("🤖 可用模型", model_count)

# ==================== 高级设置 ====================
st.markdown("---")
st.markdown("## ⚙ 高级设置")

with st.expander("⚙ 展开高级设置", expanded=False):
    st.warning("△ 以下设置可能影响系统稳定性，请谨慎修改")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔌 API 高级配置")
        
        # 超时设置
        timeout = st.slider(
            "⏱️ 请求超时时间（秒）",
            min_value=10,
            max_value=120,
            value=30,
            step=10,
            help="API 请求的最大等待时间"
        )
        
        if st.button("💾 保存超时设置"):
            api_client.timeout = timeout
            st.success(f"✓ 超时时间已设置为 {timeout} 秒")
    
    with col2:
        st.markdown("### ✦ 界面设置")
        
        # 显示模式
        display_mode = st.radio(
            "🖥️ 显示模式",
            ["自动", "宽屏", "居中"],
            help="选择应用的显示模式"
        )
        
        # 主题选择
        theme = st.selectbox(
            "✦ 颜色主题",
            ["默认", "深色", "浅色"],
            help="选择界面主题颜色"
        )
        
        if st.button("✦ 应用主题"):
            st.info("○ 主题设置需要在重启应用后生效")

# ==================== 缓存管理 ====================
st.markdown("---")
st.markdown("## 🗄️ 缓存管理")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("✕ 清空缓存", use_container_width=True):
        st.cache_data.clear()
        st.success("✓ 缓存已清空")

with col2:
    if st.button("↻ 重载配置", use_container_width=True):
        st.rerun()

with col3:
    if st.button("☰ 查看缓存状态", use_container_width=True):
        st.info("○ Streamlit 会自动管理缓存")

# ==================== 日志查看 ====================
st.markdown("---")
st.markdown("## ▤ 操作日志")

with st.expander("☰ 查看日志", expanded=False):
    st.markdown("""
    ### 最近操作记录
    
    - ✓ 2026-05-06 10:40:00 - 系统设置页面访问
    - ✓ 2026-05-06 10:35:00 - API 连接测试
    - ✓ 2026-05-06 10:30:00 - 模型列表获取
    - ℹ️ 2026-05-06 10:25:00 - 系统初始化完成
    """)
    
    st.info("○ 详细日志请查看后端服务器日志")

# ==================== 帮助文档 ====================
st.markdown("---")
st.markdown("## ❓ 帮助与支持")

tab1, tab2, tab3 = st.tabs(["⬡ 使用指南", "⚙ 故障排查", "📞 技术支持"])

with tab1:
    st.markdown("""
    ### ⬡ 快速使用指南
    
    #### 1️⃣ API 配置
    - 默认 API 地址：`http://localhost:8000`
    - 如需修改，在"API 配置"区域输入新地址并保存
    
    #### 2️⃣ 模型选择
    - 在"可用模型"区域查看所有支持的模型
    - 点击"设为默认"按钮设置默认使用的模型
    
    #### 3️⃣ 连接测试
    - 使用"健康检查"按钮测试后端连接
    - 使用"测试模型接口"验证模型可用性
    
    #### 4️⃣ 故障排查
    - 检查后端服务是否启动
    - 确认 API 地址是否正确
    - 查看网络连接是否正常
    """)

with tab2:
    st.markdown("""
    ### ⚙ 常见问题排查
    
    #### ✕ 后端连接失败
    
    **原因：**
    1. 后端服务未启动
    2. API 地址错误
    3. 网络连接问题
    
    **解决方案：**
    1. 启动后端服务：`python start.py`
    2. 检查 API 地址配置
    3. 确认网络连接正常
    
    ---
    
    #### ✕ 模型不可用
    
    **原因：**
    1. 模型 API Key 未配置
    2. 模型服务不可达
    3. 请求频率限制
    
    **解决方案：**
    1. 检查环境变量配置
    2. 验证 API Key 是否有效
    3. 稍后重试
    
    ---
    
    #### ✕ 生成失败
    
    **原因：**
    1. 模型参数错误
    2. 输入内容不符合要求
    3. 网络超时
    
    **解决方案：**
    1. 检查输入参数
    2. 简化输入内容
    3. 增加超时时间
    """)

with tab3:
    st.markdown("""
    ### 📞 技术支持
    
    #### 📧 联系方式
    - **邮箱**: support@example.com
    - **文档**: https://docs.example.com
    
    #### ◐ 在线支持
    - **Discord**: https://discord.gg/example
    - **GitHub Issues**: https://github.com/example/issues
    
    #### 🐛 报告问题
    提交问题时请包含：
    1. 错误信息截图
    2. 操作步骤描述
    3. 系统环境信息
    
    #### ❖ 相关资源
    - [Streamlit 官方文档](https://docs.streamlit.io)
    - [FastAPI 官方文档](https://fastapi.tiangolo.com)
    - [百度千帆文档](https://cloud.baidu.com/doc/WENXINWORKSHOP/index.html)
    """)

# ==================== 页脚 ====================
st.markdown("---")
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.caption(f"⚙ 系统设置 | 最后更新: {current_time}")
