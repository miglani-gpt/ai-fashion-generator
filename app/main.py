import sys
import os
from io import BytesIO

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from app.state import init_state, add_user_message, add_ai_message, reset_state
from app.generator import generate_image, check_server_health
from app.fashion_brain import update_state, build_prompt, hex_to_color_name

st.set_page_config(page_title="AI Fashion Designer", layout="wide")

st.title("AI Fashion Designer")
st.caption("Interactive fashion concept generator")

init_state()


def image_to_png_bytes(image):
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
st.sidebar.header("Controls")

api_url = st.sidebar.text_input("Backend API URL")

if api_url:
    os.environ["FASHION_API_URL"] = api_url.rstrip("/")

if st.sidebar.button("Check Server"):
    if check_server_health():
        st.sidebar.success("Server is running ✅")
    else:
        st.sidebar.error("Cannot reach server ❌")

enhance = st.sidebar.checkbox("Enhance design", value=False)

# 🔥 FIXED COLOR PICKER
DEFAULT_COLOR = "#000000"
color = st.sidebar.color_picker("Color", value=DEFAULT_COLOR)

style = st.sidebar.selectbox("Style", ["None", "Casual", "Formal", "Streetwear", "Couture"])
fabric = st.sidebar.selectbox("Fabric", ["None", "Cotton", "Silk", "Denim", "Linen"])

st.sidebar.caption("Note: Picker overrides text only if changed.")

if st.sidebar.button("Reset Design"):
    reset_state()
    st.rerun()


# ─────────────────────────────────────────────
# CHAT
# ─────────────────────────────────────────────
st.subheader("Design Assistant")

if not st.session_state.history:
    st.info("Describe a fashion idea to begin.")

for i, item in enumerate(st.session_state.history):
    if item["role"] == "user":
        with st.chat_message("user"):
            st.write(item["content"])
    else:
        with st.chat_message("assistant"):

            if item.get("image") is None:
                st.write("Generating...")
                continue

            st.image(item["image"], use_container_width=True)

            st.caption("Generated design")

            with st.expander("Prompt"):
                st.write(item["prompt"])

            st.download_button(
                label="Download",
                data=image_to_png_bytes(item["image"]),
                file_name=f"design_{i}.png",
                mime="image/png",
                key=f"download_{i}"
            )


# ─────────────────────────────────────────────
# INPUT (CORE LOGIC)
# ─────────────────────────────────────────────
user_input = st.chat_input("Describe your fashion design...")

if user_input:
    add_user_message(user_input)

    state = st.session_state.design_state

    # 🔥 Step 1: Update from user input (highest priority)
    state = update_state(state, user_input)

    # 🔥 Step 2: Apply UI overrides ONLY if explicitly changed

    if style != "None":
        if f"{style} style" not in state["details"]:
            state["details"].append(f"{style} style")

    if fabric != "None":
        state["fabric"] = fabric.lower()

    # ✅ CRITICAL FIX — only override color if user changed picker
    if color != DEFAULT_COLOR:
        state["color"] = hex_to_color_name(color)

    # Save updated state
    st.session_state.design_state = state

    # Build prompt
    new_prompt = build_prompt(state, enhance=enhance)
    st.session_state.current_prompt = new_prompt

    try:
        with st.spinner("Generating..."):
            image = generate_image(new_prompt)

        add_ai_message(new_prompt, image)
        st.session_state.history[-1]["enhanced"] = enhance

    except Exception as e:
        st.error(f"Error: {e}")

    st.rerun()


# ─────────────────────────────────────────────
# VERSION GALLERY
# ─────────────────────────────────────────────
st.markdown("---")
st.subheader("Versions")

if not st.session_state.versions:
    st.info("No designs yet.")
else:
    cols = st.columns(3)

    for i, img in enumerate(st.session_state.versions):
        with cols[i % 3]:
            st.image(img, caption=f"Version {i + 1}")


# ─────────────────────────────────────────────
# COMPARE
# ─────────────────────────────────────────────
st.markdown("---")
st.subheader("Compare")

if len(st.session_state.versions) >= 2:
    idx1 = st.selectbox("First", range(len(st.session_state.versions)))
    idx2 = st.selectbox(
        "Second",
        range(len(st.session_state.versions)),
        index=len(st.session_state.versions) - 1
    )

    col1, col2 = st.columns(2)

    with col1:
        st.image(st.session_state.versions[idx1])

    with col2:
        st.image(st.session_state.versions[idx2])
else:
    st.info("Generate at least 2 designs to compare.")