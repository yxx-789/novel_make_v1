"""
AI聊天页面 - 与AI模型进行对话
"""
import streamlit as st
from utils.api import api_client
from utils.config import Config
import time

st.set_page_config(

    page_title="AI聊天 - AI 小说创作平台",
    page_icon="◐",
    layout="wide"
)

# 应用全局样式和页面主题
from utils.global_styles import apply_global_styles, apply_page_theme
apply_global_styles()
apply_page_theme("AI聊天")

st.title("◐ AI 聊天")

# ==================== 初始化会话状态 ====================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

if "current_model" not in st.session_state:
    st.session_state.current_model = Config.DEFAULT_MODEL

# ==================== 侧边栏配置 ====================
with st.sidebar:
    st.markdown("## ⚙ 聊天设置")
    
    # 获取可用模型
    with st.spinner("加载模型列表..."):
        models_result = api_client.get_models()
    
    if "models" in models_result:
        model_options = []
        model_names = {}
        
        for model in models_result["models"]:
            model_id = model.get("id", "")
            model_name = model.get("name", model_id)
            model_options.append(model_id)
            model_names[model_id] = model_name
        
        # 模型选择
        selected_model = st.selectbox(
            "🤖 选择模型",
            model_options,
            format_func=lambda x: model_names.get(x, x),
            index=model_options.index(st.session_state.current_model) 
            if st.session_state.current_model in model_options else 0
        )
        
        if selected_model != st.session_state.current_model:
            st.session_state.current_model = selected_model
            st.info(f"✓ 已切换到: {model_names.get(selected_model, selected_model)}")
    
    st.markdown("---")
    
    # 聊天管理
    st.markdown("## 💾 聊天管理")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✦ 新对话", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.conversation_id = None
            st.rerun()
    
    with col2:
        if st.button("✕ 清空历史", use_container_width=True, type="secondary"):
            st.session_state.chat_history = []
            st.rerun()
    
    st.markdown("---")
    
    # 对话历史
    if st.session_state.chat_history:
        st.markdown("## ☰ 历史记录")
        
        for idx, message in enumerate(st.session_state.chat_history):
            if message["role"] == "user":
                st.caption(f"◆ 你: {message['content'][:50]}...")
            else:
                st.caption(f"🤖 AI: {message['content'][:50]}...")
    else:
        st.info("○ 还没有对话记录")

# ==================== 主聊天界面 ====================
# 聊天容器
chat_container = st.container()

with chat_container:
    # 显示欢迎信息
    if not st.session_state.chat_history:
        st.markdown("""
        <div style="
            text-align: center;
            padding: 3rem 1rem;
            color: #666;
        ">
            <h2>◐ 欢迎使用 AI 聊天</h2>
            <p>选择模型后，开始与 AI 对话吧！</p>
            <p>○ 你可以询问：创作建议、故事灵感、写作技巧等</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 显示聊天历史
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # 聊天输入
    if prompt := st.chat_input("请输入你的问题..."):
        # 添加用户消息到历史
        user_message = {"role": "user", "content": prompt}
        st.session_state.chat_history.append(user_message)
        
        # 显示用户消息
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 显示AI响应
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            # 模拟流式输出
            full_response = ""
            
            # 调用API
            try:
                result = api_client.chat(
                    message=prompt,
                    model=st.session_state.current_model,
                    conversation_id=st.session_state.conversation_id
                )
                
                if "response" in result:
                    response_text = result["response"]
                    
                    # 流式显示
                    for chunk in response_text.split():
                        full_response += chunk + " "
                        time.sleep(0.05)  # 模拟打字效果
                        message_placeholder.markdown(full_response + "▌")
                    
                    message_placeholder.markdown(full_response)
                    
                    # 保存AI响应到历史
                    ai_message = {"role": "assistant", "content": full_response}
                    st.session_state.chat_history.append(ai_message)
                    
                    # 保存会话ID
                    if "conversation_id" in result:
                        st.session_state.conversation_id = result["conversation_id"]
                
                elif "error" in result:
                    error_msg = f"✕ 错误: {result['error']}"
                    message_placeholder.markdown(error_msg)
                    st.session_state.chat_history.append({
                        "role": "assistant", 
                        "content": error_msg
                    })
                else:
                    error_msg = "✕ 未知错误"
                    message_placeholder.markdown(error_msg)
                    st.session_state.chat_history.append({
                        "role": "assistant", 
                        "content": error_msg
                    })
            
            except Exception as e:
                error_msg = f"✕ 请求失败: {str(e)}"
                message_placeholder.markdown(error_msg)
                st.session_state.chat_history.append({
                    "role": "assistant", 
                    "content": error_msg
                })

# ==================== 预设问题 ====================
st.markdown("---")
st.markdown("## ○ 预设问题")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⬡ 小说创作建议", use_container_width=True):
        st.session_state.preset_question = "请给我一些小说创作的实用建议"
        st.rerun()

with col2:
    if st.button("◆ 角色塑造技巧", use_container_width=True):
        st.session_state.preset_question = "如何塑造生动的小说角色？"
        st.rerun()

with col3:
    if st.button("☰ 写作风格指导", use_container_width=True):
        st.session_state.preset_question = "如何形成独特的写作风格？"
        st.rerun()

# ==================== 创意灵感 ====================
st.markdown("---")
st.markdown("## ✦ 创意灵感生成")

with st.form("inspiration_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        genre = st.selectbox(
            "❖ 小说类型",
            ["玄幻", "仙侠", "武侠", "都市", "科幻", "悬疑", "历史", "奇幻"]
        )
        
        theme = st.text_input(
            "◇ 故事主题",
            placeholder="例如：成长、复仇、爱情"
        )
    
    with col2:
        setting = st.text_input(
            "◉ 故事背景",
            placeholder="例如：未来都市、古代江湖、异世界"
        )
        
        character = st.text_input(
            "◆ 主角设定",
            placeholder="例如：落魄剑客、天才科学家"
        )
    
    submitted = st.form_submit_button("✦ 生成创意灵感", use_container_width=True)
    
    if submitted:
        if not all([genre, theme, setting, character]):
            st.error("请填写所有字段")
        else:
            prompt = f"""
            请为一部小说生成创意灵感：
            类型：{genre}
            主题：{theme}
            背景：{setting}
            主角：{character}
            
            请提供：
            1. 故事梗概
            2. 核心冲突
            3. 主要角色关系
            4. 关键情节转折点
            """
            
            st.session_state.preset_question = prompt
            st.rerun()

# ==================== 处理预设问题 ====================
if "preset_question" in st.session_state:
    # 清空聊天历史
    st.session_state.chat_history = []
    
    # 添加预设问题到输入
    st.chat_input(st.session_state.preset_question)
    
    # 清空预设问题
    del st.session_state.preset_question

# ==================== 聊天统计 ====================
if st.session_state.chat_history:
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        user_messages = len([m for m in st.session_state.chat_history if m["role"] == "user"])
        st.metric("◆ 用户消息", user_messages)
    
    with col2:
        ai_messages = len([m for m in st.session_state.chat_history if m["role"] == "assistant"])
        st.metric("🤖 AI 回复", ai_messages)
    
    with col3:
        total_words = sum(len(m["content"]) for m in st.session_state.chat_history)
        st.metric("☰ 总字数", total_words)

# ==================== 聊天导出 ====================
if st.session_state.chat_history:
    st.markdown("---")
    st.markdown("## ▤ 导出对话")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 显示对话内容
        with st.expander("▤ 查看完整对话", expanded=False):
            for message in st.session_state.chat_history:
                role_icon = "◆" if message["role"] == "user" else "🤖"
                st.markdown(f"**{role_icon} {message['role'].title()}:**")
                st.markdown(message["content"])
                st.markdown("---")
    
    with col2:
        # 生成可复制的文本
        chat_text = ""
        for message in st.session_state.chat_history:
            role = "用户" if message["role"] == "user" else "AI助手"
            chat_text += f"{role}: {message['content']}\n\n"
        
        st.code(chat_text, language=None)
        
        if st.button("▤ 复制对话", use_container_width=True):
            st.success("✓ 对话内容已显示在上方，可手动复制")

# ==================== 页脚 ====================
st.markdown("---")
st.caption(f"◐ 当前模型: {st.session_state.current_model}")
