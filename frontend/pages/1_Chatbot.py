import os
import requests
import streamlit as st
from navbar import render_navbar
from dotenv import load_dotenv

TEXT_ACCENT = "#748b4e"

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000").strip()

st.set_page_config(page_title="Chatbot", layout="wide")

# =================================================================
# Custom CSS to normalize font rendering
# =================================================================
st.markdown("""
    <style>
    .stChatMessageContent p,
    .stChatMessageContent div,
    .stChatMessageContent {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
        font-style: normal !important;
        font-weight: normal !important;
    }
    </style>
    """, unsafe_allow_html=True)

render_navbar()

st.write(f"<h3 style='color:{TEXT_ACCENT};'>Chatbot</h3>", unsafe_allow_html=True)
st.write("Ask questions about the preloaded 10-K document.")

if not BACKEND_URL:
    st.warning("Set BACKEND_URL in .env to use backend mode.")
else:
    st.info(f"📄 Document pre-loaded on backend: Clearway_Energy_2024_10K.pdf")

    st.divider()
    st.subheader("Ask a question")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Render previous messages
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.write(m["content"])

    # Input new question
    q = st.chat_input("Type a question")
    if q:
        st.session_state.messages.append({"role": "user", "content": q})
        with st.chat_message("user"):
            st.write(q)

        try:
            resp = requests.post(
                f"{BACKEND_URL}/api/chat",
                params={"question": q},
                timeout=120,
            )
            if resp.ok:
                data = resp.json()
                ans = data.get("answer", "(no answer)")

                # Escape $ so Streamlit doesn’t interpret LaTeX
                ans_escaped = ans.replace("$", "\\$")

                with st.chat_message("assistant"):
                    st.write(ans_escaped)

                st.session_state.messages.append(
                    {"role": "assistant", "content": ans_escaped}
                )
            else:
                st.error(f"Request failed: {resp.status_code} {resp.text}")
        except Exception as e:
            st.error(f"Error: {e}")
