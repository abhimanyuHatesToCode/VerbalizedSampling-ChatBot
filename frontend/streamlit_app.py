import streamlit as st
import requests
import time

BACKEND_URL = "http://localhost:8000/chat"

st.set_page_config(
    page_title="Verbalized Sampling Chat Bot",
    page_icon="🤹",
    layout="wide"
)
# --------------------------------------------------
# Dark Theme Styling (ChatGPT Style + Mode Glows)
# --------------------------------------------------

st.markdown("""
<style>

/* Main App Background */
.stApp {
    background-color: #2b2b2b;
    color: white;
}

/* Sidebar - Pure Black */
section[data-testid="stSidebar"] {
    background-color: #000000 !important;
    color: white;
}

/* Chat container background */
.block-container {
    background-color: #2b2b2b;
    padding: 2rem;
}

/* Chat input area */
div[data-testid="stChatInput"] {
    background-color: #000000 !important;
    border-top: 1px solid #333333;
}

/* Assistant & User chat bubbles */
div[data-testid="stChatMessage"] {
    background-color: #000000;
    border-radius: 12px;
    padding: 12px;
}

/* Valentine Glow */
@keyframes pinkGlow {
    0% { box-shadow: 0 0 8px rgba(255, 0, 120, 0.3); }
    50% { box-shadow: 0 0 20px rgba(255, 0, 150, 0.6); }
    100% { box-shadow: 0 0 8px rgba(255, 0, 120, 0.3); }
}

.valentine-glow {
    animation: pinkGlow 3s infinite ease-in-out;
    border-radius: 12px;
    padding: 12px;
}

/* Reasoning Aqua Glow */
@keyframes aquaGlow {
    0% { box-shadow: 0 0 8px rgba(0, 255, 255, 0.3); }
    50% { box-shadow: 0 0 20px rgba(0, 255, 255, 0.6); }
    100% { box-shadow: 0 0 8px rgba(0, 255, 255, 0.3); }
}

.reasoning-glow {
    animation: aquaGlow 3s infinite ease-in-out;
    border-radius: 12px;
    padding: 12px;
}

/* Buttons */
button {
    background-color: #111111 !important;
    color: white !important;
    border-radius: 8px;
}

/* Radio buttons */
div[role="radiogroup"] label {
    color: white !important;
}

/* Caption text */
.css-1v0mbdj {
    color: #aaaaaa !important;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.title("⚙️ Modes")

mode = st.sidebar.radio(
    "Select Mode",
    ["Normal 😊", "Reasoning 🤯", "Valentine 💘"]
)

if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("FastAPI • Gemini • Streamlit")

# --------------------------------------------------
# Session Memory
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------------------------------
# Token-Aware Trimming
# --------------------------------------------------

MAX_WORDS = 1200

def trim_messages(messages):
    total_words = 0
    trimmed = []

    for msg in reversed(messages):
        word_count = len(msg["content"].split())
        if total_words + word_count > MAX_WORDS:
            break
        trimmed.insert(0, msg)
        total_words += word_count

    return trimmed

def build_prompt(messages):
    prompt = ""
    for msg in messages:
        role = msg["role"].capitalize()
        prompt += f"{role}: {msg['content']}\n"
    return prompt

# --------------------------------------------------
# Main UI
# --------------------------------------------------

st.title("Verbalized Sampling Chat Bot")
st.caption("Session Memory 🧠 • Multi-Mode Reasoning 📲 • Valentine's Special 💝")

# Render chat history (Glow based on message mode)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):

        if msg["role"] == "assistant":
            message_mode = msg.get("mode", "normal")

            if message_mode == "valentine":
                st.markdown(
                    f'<div class="valentine-glow">{msg["content"]}</div>',
                    unsafe_allow_html=True
                )
            elif message_mode == "reasoning":
                st.markdown(
                    f'<div class="reasoning-glow">{msg["content"]}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(msg["content"])
        else:
            st.markdown(msg["content"])

# --------------------------------------------------
# User Input
# --------------------------------------------------

user_input = st.chat_input("Ask something...")

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    trimmed_messages = trim_messages(st.session_state.messages)
    conversation_prompt = build_prompt(trimmed_messages)

    if mode == "Normal 😊":
        selected_mode = "normal"
    elif mode == "Reasoning 🤯":
        selected_mode = "reasoning"
    else:
        selected_mode = "valentine"

    start_time = time.time()

    with st.chat_message("assistant"):
        placeholder = st.empty()

        with st.spinner("Thinking..."):
            response = requests.post(
                BACKEND_URL,
                json={
                    "prompt": conversation_prompt,
                    "mode": selected_mode
                },
                timeout=60
            )

        end_time = time.time()
        response_time = round(end_time - start_time, 2)

        if response.status_code == 200:
            reply = response.json()["response"]
        else:
            reply = "⚠️ Backend error"

        displayed_text = ""
        for char in reply:
            displayed_text += char
            placeholder.markdown(displayed_text)
            time.sleep(0.01)

        st.caption(f"⏱ Response time: {response_time}s")

    # IMPORTANT: store mode with message
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply,
        "mode": selected_mode
    })
