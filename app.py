# app.py (full code combining all steps)

import os
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
import PyPDF2

load_dotenv()


client = OpenAI()

def extract_file_text(file):
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    elif file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    else:
        return ""

def generate_response(user_prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": user_prompt}]
    )
    message_text = response.choices[0].message.content
    return message_text

st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 AI Chatbot Assistant")
st.markdown("**Welcome!** Ask anything or upload a file for the bot to analyze.")

uploaded_file = st.sidebar.file_uploader("Upload a file (optional):", type=["txt", "pdf"])
if uploaded_file is not None:
    st.sidebar.write("Uploaded file:", f"**{uploaded_file.name}** ({uploaded_file.size} bytes)")

if "messages" not in st.session_state:
    st.session_state.messages = []
if not st.session_state.messages:
    st.session_state.messages.append({"role": "assistant", "content": "Hello! I'm here to help. Feel free to ask me anything or upload a file."})

# Display existing chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input widget for new messages
# Chat input widget for new messages
if user_msg := st.chat_input("Type your message here..."):
    # Extract file content if available
    file_text = extract_file_text(uploaded_file) if uploaded_file else ""
    full_prompt = f"{file_text}\n\nUser: {user_msg}" if file_text else user_msg

    # Add user message to history and display it
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"):
        st.markdown(user_msg)

    # Generate assistant response with spinner
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            assistant_msg = generate_response(full_prompt)
            st.markdown(assistant_msg)

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": assistant_msg})
