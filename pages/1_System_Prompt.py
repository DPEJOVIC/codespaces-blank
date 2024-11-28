import streamlit as st
from Chat import initialize


st.title("System Prompt")


client, default_prompt = initialize()


# Clears the chat transcript (used when the system prompt is changed)
def clear_history():
    st.session_state["chat_history"] = []


# Text box where the user can edit the system prompt
system_prompt_box = st.text_area(
    label = "Change the system prompt here:",
    value = st.session_state["system_prompt"],
    height = 400,
    on_change = clear_history
)


def change_system_prompt():
    st.session_state["system_prompt"] = system_prompt_box

change_system_prompt()


# Resets to the default value
def reset_system_prompt():
    st.session_state["system_prompt"] = default_prompt
    clear_history()

st.button("Reset prompt", on_click = reset_system_prompt)
