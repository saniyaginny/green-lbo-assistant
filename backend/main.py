# old main code
from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import fitz  # PyMuPDF
import re
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
import io
from dotenv import load_dotenv

# =========================
# Load Environment Variables
# =========================
load_dotenv()  # loads .env file in local development

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Please set GEMINI_API_KEY environment variable.")

genai.configure(api_key=GEMINI_API_KEY)

# Models
embed_model = "models/embedding-001"
model = genai.GenerativeModel("gemini-2.0-flash")

# =========================
# FastAPI App Initialization
# =========================
app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://fernechatbot.streamlit.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Backend is running! Try /api/upload or /api/chat."}

# =========================
# Helper Functions
# =========================
def read_pdf_from_bytes(pdf_bytes):
    """Reads the content of a PDF from in-memory bytes and extracts text."""
    text_content = ""
    try:
        pdf_stream = io.BytesIO(pdf_bytes)
        doc = fitz.open(stream=pdf_stream, filetype="pdf")
        for page in doc:
            text_content += page.get_text()
        return text_content
    except Exception as e:
        return f"Error reading PDF from bytes: {e}"

def chunk_text(text, chunk_size=1500, overlap=200):
    """Splits text into overlapping chunks to preserve context."""
    words = re.split(r"\s+", text)
    chunks, start = [], 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def get_embedding(text):
    """Get vector embedding for a text chunk."""
    try:
        result = genai.embed_content(model=embed_model, content=text)
        return np.array(result["embedding"])
    except Exception as e:
        print(f"Embedding error: {e}")
        return None

def retrieve_relevant_chunks(doc_id, question, top_k=3):
    """Return the top_k most relevant chunks to the question."""
    q_emb = get_embedding(question)
    sims = cosine_similarity([q_emb], doc_embeddings[doc_id])[0]
    top_indices = sims.argsort()[-top_k:][::-1]
    return [doc_chunks[doc_id][i] for i in top_indices]

# =========================
# Global store
# =========================
documents = {}         # doc_id -> raw PDF bytes
doc_chunks = {}        # doc_id -> list of text chunks
doc_embeddings = {}    # doc_id -> list of embeddings

# =========================
# Endpoints
# =========================
@app.post("/api/upload")
async def upload_pdf(file: UploadFile = File(...)):
    import uuid
    content = await file.read()
    doc_id = str(uuid.uuid4())

    documents[doc_id] = content

    # Preprocess
    document_text = read_pdf_from_bytes(content)
    chunks = chunk_text(document_text)
    embeddings = [get_embedding(c) for c in chunks]

    doc_chunks[doc_id] = chunks
    doc_embeddings[doc_id] = embeddings

    return JSONResponse({"doc_id": doc_id})


@app.post("/api/chat")
async def query_doc(doc_id: str = Query(...), question: str = Query(...)):
    if doc_id not in documents:
        return JSONResponse({"error": "Document not found"}, status_code=404)

    relevant_chunks = retrieve_relevant_chunks(doc_id, question, top_k=3)
    context = "\n\n".join(relevant_chunks)
    prompt = f"Using only the following 10-K document excerpts, answer the question:\n\n{context}\n\nQuestion: {question}"

    try:
        response = model.generate_content(prompt)
        return {"answer": response.text}
    except Exception as e:
        return {"answer": f"An error occurred: {e}"}
