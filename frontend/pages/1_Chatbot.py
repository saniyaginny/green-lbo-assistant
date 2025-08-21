# pages/1_Chatbot.py
import os
import base64
import requests
import streamlit as st
from navbar import render_navbar

# ---------- Config ----------
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Chatbot", layout="wide")
render_navbar()

# =========================
# Base64 helper for title image
# =========================
def _img_to_data_uri(path: str) -> str:
    with open(path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:image/png;base64,{b64}"

# Resolve image path
base_dir = os.path.dirname(os.path.abspath(__file__))
candidates = [
    os.path.join(base_dir, "Chatbot.png"),
    os.path.join(os.path.dirname(base_dir), "Chatbot.png"),
    "/mnt/data/Chatbot.png",
]
title_img_path = next((p for p in candidates if os.path.exists(p)), None)

# =========================
# Global CSS for logo + CHAT FONT FIX + typing animation
# (font override copied from your second snippet)
# =========================
st.markdown("""
<style>
  /* Title/logo animation */
  @keyframes logoFadeDown {
    from { opacity: 0; transform: translateY(-12px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  .chatbot-logo {
    height: 85px;  /* same size as Ferne logo */
    animation: logoFadeDown 700ms ease-out 100ms both;
    transition: transform 300ms ease, filter 300ms ease;
  }
  .chatbot-logo:hover {
    transform: scale(1.08) rotate(-2deg);
    filter: drop-shadow(0 8px 18px rgba(77, 144, 25, 0.45));
  }

  /* --- FONT FIX (from your other file) --- */
  .stChatMessageContent p,
  .stChatMessageContent div,
  .stChatMessageContent {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
      font-style: normal !important;
      font-weight: normal !important;
  }

  /* --- Typing dots animation for assistant thinking --- */
  @keyframes dotPulse {
    0%   { transform: translateY(0); opacity: 0.35; }
    50%  { transform: translateY(-4px); opacity: 1; }
    100% { transform: translateY(0); opacity: 0.35; }
  }
  .typing-dots {
    display: inline-flex;
    gap: 6px;
    align-items: center;
    padding: 6px 2px;
  }
  .typing-dots span {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #4d9019; /* brand green */
    animation: dotPulse 1.1s ease-in-out infinite;
  }
  .typing-dots span:nth-child(2) { animation-delay: 0.15s; }
  .typing-dots span:nth-child(3) { animation-delay: 0.30s; }
</style>
""", unsafe_allow_html=True)

# =========================
# Title (image)
# =========================
if title_img_path:
    title_uri = _img_to_data_uri(title_img_path)
    st.markdown(
        f"""
        <div style="text-align:center; margin-top: 36px; margin-bottom: 8px;">
          <img src="{title_uri}" alt="Chatbot Logo" class="chatbot-logo" />
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <div style="text-align:center; margin-top: 36px; margin-bottom: 8px;">
          <h2 style="color:#4d9019;">Chatbot</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info("Title image not found. Place 'Chatbot.png' next to pages/1_Chatbot.py.")

# =========================
# Session state
# =========================
if "doc_id" not in st.session_state:
    st.session_state.doc_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []  # [{"role":"user"/"assistant","content":...}]

# =========================
# Helpers
# =========================
def upload_pdf_to_backend(file) -> str | None:
    try:
        files = {"file": (file.name, file.getvalue(), file.type or "application/pdf")}
        r = requests.post(f"{BACKEND_URL}/api/upload", files=files, timeout=120)
        r.raise_for_status()
        return r.json().get("doc_id")
    except Exception as e:
        st.error(f"Upload failed: {e}")
        return None

def ask_backend(doc_id: str, question: str) -> str:
    try:
        r = requests.post(
            f"{BACKEND_URL}/api/chat",
            params={"doc_id": doc_id, "question": question},
            timeout=120,
        )
        r.raise_for_status()
        data = r.json()
        return data.get("answer", "No answer returned.")
    except Exception as e:
        return f"An error occurred: {e}"

# =========================
# UI: uploader
# =========================
st.subheader("1) Upload a 10-K PDF")
pdf = st.file_uploader("Choose a PDF", type=["pdf"], accept_multiple_files=False)

cols = st.columns([1, 1, 6])
with cols[0]:
    if st.button("Upload", use_container_width=True, disabled=(pdf is None)):
        with st.spinner("Uploading and indexing..."):
            doc_id = upload_pdf_to_backend(pdf)
        if doc_id:
            st.session_state.doc_id = doc_id
            st.success("PDF indexed successfully.")
        else:
            st.session_state.doc_id = None

with cols[1]:
    if st.session_state.doc_id:
        st.success("Document loaded", icon="✅")
    else:
        st.info("No document loaded", icon="ℹ️")

st.markdown("---")

# =========================
# UI: chat
# =========================
st.subheader("2) Ask questions")
if not st.session_state.doc_id:
    st.info("Upload a PDF first to enable chat.")
else:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    user_msg = st.chat_input("Ask something about the document...")
    if user_msg:
        st.session_state.messages.append({"role": "user", "content": user_msg})
        with st.chat_message("user"):
            st.markdown(user_msg)

        # Assistant message with typing animation while thinking
        with st.chat_message("assistant"):
            # Show typing dots immediately
            typing_placeholder = st.empty()
            typing_placeholder.markdown(
                '<div class="typing-dots"><span></span><span></span><span></span></div>',
                unsafe_allow_html=True
            )

            # Do the work (backend call)
            answer = ask_backend(st.session_state.doc_id, user_msg)

            # Replace typing dots with the real answer
            typing_placeholder.empty()
            st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})
