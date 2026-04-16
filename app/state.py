import streamlit as st

def init_state():
    if "history" not in st.session_state:
        st.session_state.history = []
    if "current_prompt" not in st.session_state:
        st.session_state.current_prompt = ""

def add_user_message(content):
    st.session_state.history.append({
        "role": "user",
        "content": content
    })

def add_ai_message(prompt, image):
    st.session_state.history.append({
        "role": "assistant",
        "prompt": prompt,
        "image": image
    })

def reset_state():
    st.session_state.history = []
    st.session_state.current_prompt = ""