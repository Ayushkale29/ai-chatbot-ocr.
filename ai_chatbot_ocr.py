import streamlit as st
import requests
import json
import easyocr
from PIL import Image
import numpy as np
import os

# ----------------------
# Paths and OCR Reader
# ----------------------
CHAT_HISTORY_FILE = "chat_sessions.json"
reader = easyocr.Reader(['en'], gpu=False)

st.set_page_config(page_title="AI Chatbot with OCR", page_icon="🤖")
st.title("🤖 AI Chatbot with Ollama + OCR")

# ----------------------
# Load all sessions
# ----------------------
if os.path.exists(CHAT_HISTORY_FILE):
    with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as f:
        all_sessions = json.load(f)
else:
    all_sessions = {"sessions": []}

# ----------------------
# Initialize current session
# ----------------------
if "current_session_id" not in st.session_state:
    if all_sessions["sessions"]:
        # Load last session by default
        st.session_state.current_session_id = all_sessions["sessions"][-1]["id"]
    else:
        st.session_state.current_session_id = 1

# Helper to get current session dict
def get_current_session():
    for s in all_sessions["sessions"]:
        if s["id"] == st.session_state.current_session_id:
            return s
    # If not found, create new
    new_session = {"id": st.session_state.current_session_id, "messages": []}
    all_sessions["sessions"].append(new_session)
    return new_session

current_session = get_current_session()

# ----------------------
# Sidebar - Previous Chats
# ----------------------
st.sidebar.header("Previous Chats")
if all_sessions["sessions"]:
    selected_session_index = st.sidebar.selectbox(
        "Select a session to load",
        range(len(all_sessions["sessions"])),
        format_func=lambda x: f"Session {all_sessions['sessions'][x]['id']}"
    )
    
    selected_id = all_sessions["sessions"][selected_session_index]["id"]
    if selected_id != st.session_state.current_session_id:
        st.session_state.current_session_id = selected_id
        st.session_state.messages = all_sessions["sessions"][selected_session_index]["messages"]

# ----------------------
# Sidebar - New Chat Button
# ----------------------
if st.sidebar.button("New Chat"):
    new_id = max([s["id"] for s in all_sessions["sessions"]], default=0) + 1
    # Create a new session
    new_session = {"id": new_id, "messages": []}
    all_sessions["sessions"].append(new_session)
    
    # Update session state
    st.session_state.current_session_id = new_id
    st.session_state.messages = new_session["messages"]
    
    # Save sessions
    with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(all_sessions, f, ensure_ascii=False, indent=4)

# ----------------------
# Initialize chat messages
# ----------------------
if "messages" not in st.session_state or not st.session_state.messages:
    st.session_state.messages = current_session["messages"]
    if not st.session_state.messages:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I’m your AI assistant, ready to help like ChatGPT. 👋"}
        ]

# ----------------------
# Display chat history
# ----------------------
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"], unsafe_allow_html=True)

# ----------------------
# Sidebar - Options
# ----------------------
st.sidebar.subheader("Options")
model_choice = st.sidebar.selectbox("Choose Model", ["llama3", "deepseek-coder"])

# ----------------------
# OCR Section
# ----------------------
st.sidebar.subheader("Upload Document/Image for OCR")
uploaded_file = st.sidebar.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

def save_sessions():
    """Save current messages into current session"""
    current_session = get_current_session()
    current_session["messages"] = st.session_state.messages
    with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(all_sessions, f, ensure_ascii=False, indent=4)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.sidebar.image(image, caption="Uploaded Image", use_column_width=True)
    img_array = np.array(image)
    
    # Extract text
    extracted_text = reader.readtext(img_array, detail=0)
    extracted_text = "\n".join(extracted_text)
    st.sidebar.write("Extracted Text:")
    st.sidebar.text(extracted_text)

    if st.sidebar.button("Send Extracted Text to Chatbot"):
        st.session_state.messages.append({"role": "user", "content": extracted_text})
        with st.chat_message("user"):
            st.markdown(extracted_text)

        # Send to Ollama
        conversation = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model_choice, "prompt": conversation},
            stream=True,
        )

        reply = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                if "response" in data:
                    reply += data["response"]

        with st.chat_message("assistant"):
            st.markdown(reply, unsafe_allow_html=True)

        st.session_state.messages.append({"role": "assistant", "content": reply})
        save_sessions()

# ----------------------
# Normal Chat Input
# ----------------------
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    conversation = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model_choice, "prompt": conversation},
        stream=True,
    )

    reply = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            if "response" in data:
                reply += data["response"]

    with st.chat_message("assistant"):
        st.markdown(reply, unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    save_sessions()
