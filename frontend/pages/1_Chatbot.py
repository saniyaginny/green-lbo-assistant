# pages/1_Chatbot.py
import os
import requests
import streamlit as st
from navbar import apply_page_chrome, render_navbar
apply_page_chrome()

# ---------- Config ----------
# Point this to your FastAPI server. Override by setting BACKEND_URL env var.
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Chatbot", layout="wide")
render_navbar()

# ---------- Title ----------
st.markdown(
    """
    <div style="text-align:center; margin-top: 36px;">
      <h2 style="color:#4d9019; margin-bottom: 8px;">Chatbot</h2>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Session state ----------
if "doc_id" not in st.session_state:
    st.session_state.doc_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []  # [{"role":"user"/"assistant","content":...}]

# ---------- Helpers ----------
def upload_pdf_to_backend(file) -> str | None:
    """Send the PDF to FastAPI and return the doc_id."""
    try:
        files = {"file": (file.name, file.getvalue(), file.type or "application/pdf")}
        r = requests.post(f"{BACKEND_URL}/api/upload", files=files, timeout=120)
        r.raise_for_status()
        return r.json().get("doc_id")
    except Exception as e:
        st.error(f"Upload failed: {e}")
        return None

def ask_backend(doc_id: str, question: str) -> str:
    """Ask the RAG endpoint a question and return the answer text."""
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

# ---------- UI: uploader ----------
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

# ---------- UI: chat ----------
st.subheader("2) Ask questions")
if not st.session_state.doc_id:
    st.info("Upload a PDF first to enable chat.")
else:
    # Render chat history
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    user_msg = st.chat_input("Ask something about the document...")
    if user_msg:
        # Show user message immediately
        st.session_state.messages.append({"role": "user", "content": user_msg})
        with st.chat_message("user"):
            st.markdown(user_msg)

        # Get answer
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = ask_backend(st.session_state.doc_id, user_msg)
            st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})
