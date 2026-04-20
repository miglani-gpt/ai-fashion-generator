import streamlit as st


def init_state():
    if "history" not in st.session_state:
        st.session_state.history = []

    if "current_prompt" not in st.session_state:
        st.session_state.current_prompt = ""

    if "versions" not in st.session_state:
        st.session_state.versions = []

    if "design_state" not in st.session_state:
        st.session_state.design_state = {
            "garment": None,
            "color": None,
            "fabric": None,
            "details": []
        }


def add_user_message(content):
    st.session_state.history.append({
        "role": "user",
        "content": content,
    })


def add_ai_message(prompt, image):
    # Safety: prevent None images from breaking UI
    if image is None:
        raise ValueError("Generated image is None — backend failed")

    st.session_state.history.append({
        "role": "assistant",
        "prompt": prompt,
        "image": image,
    })

    st.session_state.versions.append(image)


def reset_state():
    st.session_state.history = []
    st.session_state.current_prompt = ""
    st.session_state.versions = []
    st.session_state.design_state = {
        "garment": None,
        "color": None,
        "fabric": None,
        "details": []
    }