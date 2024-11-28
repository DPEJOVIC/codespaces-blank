import streamlit as st 
from openai import OpenAI


st.title("Chat")


# Set up initial session state variables
def initialize():

    if "model" not in st.session_state:
        st.session_state["model"] = "gpt-4o-mini"

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    default_prompt = """Your role is to act as an AI tutor. You will try to help the user understand the topic(s) they wish to discuss."""
    if "system_prompt" not in st.session_state:
        st.session_state["system_prompt"] = default_prompt

    client = OpenAI(api_key = st.secrets["API_KEY"])

    return client, default_prompt
    
client, default_prompt = initialize()


# Display previous messages in the chat transcript on the screen
def write_chat_history():
    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

write_chat_history()


# Logic for sending the user's message to OpenAI and receiving a response
def chat_process():
    if prompt := st.chat_input("Message the chatbot here"): # If the user submits a chat message

        st.session_state["chat_history"].append({"role": "user", "content": prompt}) # Add the user's prompt to the chat transcript

        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):

            # Pass the chatbot the system prompt and the chat transcript
            messages = [
                {"role": "system", "content": st.session_state["system_prompt"]}
                ] + [
                {"role": m["role"], "content": m["content"]} for m in st.session_state["chat_history"]
            ]

            # Get a response from OpenAI, using the temperature setting specified by the user
            stream = client.chat.completions.create(
                model = st.session_state["model"],
                messages = messages,
                stream = True,
            )

            response = st.write_stream(stream) # Display the chatbot's response on the screen

        st.session_state["chat_history"].append({"role": "assistant", "content": response}) # Add the chatbot's response to the chat transcript

chat_process()