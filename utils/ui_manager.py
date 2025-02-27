import streamlit as st
import os
from utils.env_manager import save_to_env

def apply_custom_css():
    """Apply custom CSS styling for Streamlit app"""
    st.markdown("""
    <style>
        .main { background-color: #202123; }
        .stTextInput > div > div > input { background-color: #40414f; color: white; border-radius: 20px; }
        .stButton > button { border-radius: 20px; padding: 10px 20px; background-color: transparent; border: 1px solid #565869; color: white; }
        .sidebar .sidebar-content { background-color: #202123; }
    </style>
    """, unsafe_allow_html=True)

def display_sidebar():
    """Display sidebar UI elements"""
    with st.sidebar:
        st.title("Multi-LLM Chat")

        if st.button("⚙️ Configure API Keys"):
            st.session_state.show_config = not st.session_state.show_config

        if st.session_state.show_config:
            st.subheader("API Configuration")
            api_configs = {
                "OpenAI": "OPENAI_API_KEY",
                "Azure OpenAI": ["AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT", "AZURE_DEPLOYMENT_NAME"],
                "Google AI": "GOOGLE_API_KEY",
                "Ollama": "OLLAMA_BASE_URL"
            }

            for provider, keys in api_configs.items():
                st.markdown(f"### {provider}")
                if isinstance(keys, list):
                    for key in keys:
                        value = st.text_input(f"{provider} {key}", value=os.getenv(key, ""), type="password" if "KEY" in key else "text")
                        if value:
                            save_to_env(key, value)
                else:
                    value = st.text_input(f"{provider} API Key", value=os.getenv(keys, ""), type="password")
                    if value:
                        save_to_env(keys, value)

            if st.button("Save Configuration"):
                st.success("Configuration saved successfully!")
                st.session_state.show_config = False

        st.markdown("### Model Selection")
        st.session_state.selected_model = st.selectbox("Choose Model", ["GPT-3.5", "Azure OpenAI", "Gemini Flash", "Llama2 (Ollama)"])

        st.markdown("### Chat History")
        for idx, chat in enumerate(st.session_state.chat_history):
            if st.button(f"Chat {idx + 1}", key=f"chat_{idx}"):
                st.session_state.messages = chat

def display_chat():
    """Display chat messages"""
    message_container = st.container()
    with message_container:
        for idx, msg in enumerate(st.session_state.messages):
            message(msg["content"], is_user=msg["role"] == "user", key=f"msg_{idx}")
