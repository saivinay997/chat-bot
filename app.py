import streamlit as st
from streamlit_chat import message
import os
import asyncio
from services.llm_services import LLMService
from utils.env_manager import save_to_env, load_env_vars
from utils.ui_manager import apply_custom_css, display_sidebar, display_chat

# Load environment variables
load_env_vars()

# Configure Streamlit page
st.set_page_config(page_title="Multi-LLM Chatbot", layout="wide", initial_sidebar_state="expanded")

# Apply custom CSS
apply_custom_css()

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'show_config' not in st.session_state:
    st.session_state.show_config = False

# Display sidebar
display_sidebar()

# Main chat interface
st.header("Multi-LLM Chatbot")

# Display chat history
display_chat()

# Chat input form
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([6, 1])
    with col1:
        user_input = st.text_input("Message", placeholder="Type your message here...", label_visibility="collapsed", key="chat_input")
    with col2:
        submit_button = st.form_submit_button("Send")

if submit_button and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get AI response based on selected model
    with st.spinner("Thinking..."):
        try:
            # Initialize LLM service based on model selection
            use_azure = st.session_state.selected_model == "Azure OpenAI"
            llm_service = LLMService(use_azure=use_azure)
            
            # Get response based on model
            if st.session_state.selected_model in ["GPT-3.5", "Azure OpenAI"]:
                response = asyncio.run(llm_service.get_openai_response(st.session_state.messages))
            elif st.session_state.selected_model == "Gemini Flash":
                response = asyncio.run(llm_service.get_gemini_response(st.session_state.messages))
            else:  # Llama2
                response = llm_service.get_ollama_response(st.session_state.messages)

            st.session_state.messages.append({"role": "assistant", "content": response})

            # Save chat history
            if not st.session_state.chat_history or st.session_state.chat_history[-1] != st.session_state.messages:
                st.session_state.chat_history.append(st.session_state.messages.copy())

        except Exception as e:
            st.error(f"Error fetching response: {str(e)}")

    st.rerun()
