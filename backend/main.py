# main.py
import os
import io
import re
import uuid
import numpy as np
import fitz  # PyMuPDF
import google.generativeai as genai
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Literal, Dict, Optional
from dotenv import load_dotenv

# =========================
# Load Environment Variables
# =========================
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Please set GEMINI_API_KEY environment variable.")
genai.configure(api_key=GEMINI_API_KEY)

EMBED_MODEL = "models/embedding-001"
GEN_MODEL = genai.GenerativeModel("gemini-1.5-flash")

# =========================
# FastAPI App Initialization
# =========================
app = FastAPI(default_response_class=JSONResponse)

# Allow frontend to connect (adjust allow_origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://fernechatbot.streamlit.app",
        "http://localhost:8501",
        "http://127.0.0.1:8501",
        "http://localhost",
        "http://127.0.0.1",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Backend is running! Try /api/upload, /api/chat or /api/chat/session."}

# =========================
# Helper Functions
# =========================
def read_pdf_from_bytes(pdf_bytes: bytes) -> str:
    """Reads the content of a PDF from in-memory bytes and extracts Unicode text."""
    text_content = ""
    try:
        pdf_stream = io.BytesIO(pdf_bytes)
        doc = fitz.open(stream=pdf_stream, filetype="pdf")
        for page in doc:
            # ensure text is normalized unicode
            text_content += page.get_text("text", flags=0)
        return text_content
    except Exception as e:
        return f"Error reading PDF from bytes: {e}"

def chunk_text(text: str, chunk_size: int = 1500, overlap: int = 200) -> List[str]:
    """Splits text into overlapping chunks to preserve context (Unicode safe)."""
    words = re.split(r"\s+", text)
    chunks, start = [], 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += max(1, chunk_size - overlap)
    return chunks

def get_embedding(text: str):
    """Get vector embedding for a text chunk."""
    try:
        result = genai.embed_content(model=EMBED_MODEL, content=text)
        return np.array(result["embedding"])
    except Exception as e:
        print(f"Embedding error: {e}")
        return None

def retrieve_relevant_chunks(doc_id: str, question: str, top_k: int = 3) -> List[str]:
    """Return the top_k most relevant chunks to the question."""
    if doc_id not in doc_embeddings or not doc_embeddings[doc_id]:
        return []
    q_emb = get_embedding(question)
    if q_emb is None:
        return doc_chunks.get(doc_id, [])[:top_k]

    # Filter out None embeddings
    emb_list = [e for e in doc_embeddings[doc_id] if e is not None]
    if not emb_list:
        return doc_chunks.get(doc_id, [])[:top_k]

    sims = cosine_similarity([q_emb], emb_list)[0]
    top_indices = sims.argsort()[-top_k:][::-1]

    valid_indices = [i for i, e in enumerate(doc_embeddings[doc_id]) if e is not None]
    mapped = [valid_indices[i] for i in top_indices if i < len(valid_indices)]
    return [doc_chunks[doc_id][i] for i in mapped]

# =========================
# Global stores (in-memory)
# =========================
documents: Dict[str, bytes] = {}
doc_chunks: Dict[str, List[str]] = {}
doc_embeddings: Dict[str, List[np.ndarray]] = {}

# ---------- Chat session store ----------
class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ChatSession(BaseModel):
    session_id: str
    doc_id: Optional[str] = None
    messages: List[ChatMessage] = []

chat_sessions: Dict[str, ChatSession] = {}

def get_or_create_session(session_id: str) -> ChatSession:
    sess = chat_sessions.get(session_id)
    if not sess:
        sess = ChatSession(session_id=session_id, doc_id=None, messages=[])
        chat_sessions[session_id] = sess
    return sess

# =========================
# Endpoints
# =========================
@app.post("/api/upload")
async def upload_pdf(file: UploadFile = File(...), session_id: Optional[str] = Query(None)):
    content = await file.read()
    doc_id = str(uuid.uuid4())

    documents[doc_id] = content
    document_text = read_pdf_from_bytes(content)
    chunks = chunk_text(document_text)
    embeddings = [get_embedding(c) for c in chunks]

    doc_chunks[doc_id] = chunks
    doc_embeddings[doc_id] = embeddings

    if session_id:
        sess = get_or_create_session(session_id)
        sess.doc_id = doc_id

    return JSONResponse({"doc_id": doc_id}, ensure_ascii=False)

@app.post("/api/chat")
async def query_doc(doc_id: str = Query(...), question: str = Query(...)):
    if doc_id not in documents:
        return JSONResponse({"error": "Document not found"}, status_code=404)

    relevant_chunks = retrieve_relevant_chunks(doc_id, question, top_k=3)
    context = "\n\n".join(relevant_chunks)
    prompt = (
        "Using only the following 10-K document excerpts, answer the question.\n"
        "If the excerpts do not contain the answer, say you do not have enough information.\n\n"
        f"{context}\n\nQuestion: {question}"
    )

    try:
        response = GEN_MODEL.generate_content(prompt)
        return JSONResponse({"answer": response.text}, ensure_ascii=False)
    except Exception as e:
        return JSONResponse({"answer": f"An error occurred: {e}"}, ensure_ascii=False)

@app.get("/api/chat/session")
async def get_chat_session(session_id: str = Query(...)):
    sess = get_or_create_session(session_id)
    return JSONResponse({
        "session_id": sess.session_id,
        "doc_id": sess.doc_id,
        "messages": [m.model_dump() for m in sess.messages],
    }, ensure_ascii=False)

@app.post("/api/chat/session")
async def save_chat_session(payload: ChatSession):
    chat_sessions[payload.session_id] = payload
    return JSONResponse({
        "ok": True,
        "session_id": payload.session_id,
        "count": len(payload.messages)
    }, ensure_ascii=False)

# =========================
# Run standalone
# =========================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")), reload=True)
