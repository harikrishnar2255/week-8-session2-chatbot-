import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# Page configuration
st.set_page_config(page_title="Groq Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 AI Assistant")
st.caption("Powered by Groq & `openai/gpt-oss-120b`")

# Fetch API key stored under variable 'x'
groq_api_key = os.getenv("x")

if not groq_api_key:
    st.error("API key 'x' not found in .env file. Please check your setup.")
    st.stop()

# Initialize OpenAI client with Groq's endpoint
client = OpenAI(
    api_key=groq_api_key,
    base_url="https://api.groq.com/openai/v1"
)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Display prior chat messages (excluding system prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User prompt input
if prompt := st.chat_input("Ask something..."):
    # Append and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=st.session_state.messages
                )
                bot_reply = response.choices[0].message.content
                st.markdown(bot_reply)
                
                # Append assistant reply to session state
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            except Exception as e:
                st.error(f"Error generating response: {e}")