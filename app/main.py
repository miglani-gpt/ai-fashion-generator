import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from app.state import init_state, add_user_message, add_ai_message, reset_state
from app.prompt_engine import refine_prompt
from app.generator import generate_image

st.title("👗 AI Fashion Designer")

# Init state
init_state()

# Reset button
if st.button("Reset Design"):
    reset_state()
    st.rerun()

# Display history
for item in st.session_state.history:
    if item["role"] == "user":
        st.markdown(f"**You:** {item['content']}")
    else:
        st.markdown(f"**AI Prompt:** {item['prompt']}")
        st.image(item["image"])

# Input
user_input = st.text_input("Describe your design...")

if st.button("Generate") and user_input:
    add_user_message(user_input)

    # Prompt refinement
    new_prompt = refine_prompt(
        st.session_state.current_prompt,
        user_input
    )

    st.session_state.current_prompt = new_prompt

    # Generate image
    image = generate_image(new_prompt)

    add_ai_message(new_prompt, image)

    st.rerun()