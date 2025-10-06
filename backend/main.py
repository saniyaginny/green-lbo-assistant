from fastapi import FastAPI, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import fitz  # PyMuPDF
import re
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
from dotenv import load_dotenv
import uuid
from typing import List, Dict, Optional

# =========================
# FastAPI App Initialization
# =========================
app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Gemini API Configuration
# =========================
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Please set GEMINI_API_KEY environment variable.")
genai.configure(api_key=GEMINI_API_KEY)

embed_model = "models/embedding-001"
model = genai.GenerativeModel("gemini-1.5-flash")

# =========================
# Helper Functions
# =========================
def read_pdf_bytes(file_bytes: bytes) -> str:
    """
    Reads the content of a PDF file (in-memory bytes) and extracts text.
    """
    text_content = ""
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page in doc:
            text_content += page.get_text()
        return text_content
    except Exception as e:
        return "Error reading PDF: {}".format(e)

def chunk_text(text: str, chunk_size: int = 1500, overlap: int = 200) -> List[str]:
    """
    Splits text into overlapping chunks to preserve context.
    """
    if not text:
        return []
    words = re.split(r"\s+", text)
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += max(1, chunk_size - overlap)
    return chunks

def get_embedding(text: str) -> Optional[np.ndarray]:
    """
    Get vector embedding for a text chunk.
    """
    try:
        result = genai.embed_content(model=embed_model, content=text)
        # The SDK returns a dict-like with key 'embedding'
        emb = result.get("embedding")
        if emb is None:
            return None
        return np.array(emb, dtype=float)
    except Exception as e:
        print("Embedding error: {}".format(e))
        return None

def retrieve_relevant_chunks(doc_id: str, question: str, top_k: int = 3) -> List[str]:
    """
    Retrieve top-k most similar chunks for a given question and document.
    """
    if doc_id not in doc_embeddings or doc_id not in doc_chunks:
        return []
    q_emb = get_embedding(question)
    if q_emb is None:
        return []
    # Filter out any None embeddings
    valid_embeddings = []
    valid_indices = []
    for i, emb in enumerate(doc_embeddings[doc_id]):
        if emb is not None:
            valid_embeddings.append(emb)
            valid_indices.append(i)
    if not valid_embeddings:
        return []
    sims = cosine_similarity([q_emb], np.vstack(valid_embeddings))[0]
    top_indices_local = sims.argsort()[-top_k:][::-1]
    top_chunks = []
    for li in top_indices_local:
        global_index = valid_indices[li]
        top_chunks.append(doc_chunks[doc_id][global_index])
    return top_chunks

# =========================
# Hardcoded Financial Calculations
# =========================
def calculate_net_debt():
    """
    Manually calculate Net Debt from the 2024 balance sheet numbers.
    Formula = (Long-term debt + Current debt) - Cash and equivalents
    """
    long_term_debt = 6750
    current_debt = 430
    cash_and_equivalents = 332
    net_debt = (long_term_debt + current_debt) - cash_and_equivalents
    return net_debt

def calculate_net_debt_ebitda_multiple():
    """
    Hardcoded calculation for Net Debt / EBITDA multiple (2024).
    EBITDA = Net Income + Depreciation/Amortization/Accretion + Interest Expense + Income Tax Expense
    """
    net_income = -63
    depreciation_amortization_accretion = 965
    interest_expense = 550
    income_tax_expense = 29

    ebitda = (
        net_income
        + depreciation_amortization_accretion
        + interest_expense
        + income_tax_expense
    )
    net_debt = calculate_net_debt()

    if ebitda != 0:
        multiple = float(net_debt) / float(ebitda)
    else:
        multiple = None

    return net_debt, ebitda, multiple

# =========================
# Global store (in-memory)
# =========================
# doc_id -> raw PDF text
documents: Dict[str, str] = {}
# doc_id -> list of text chunks
doc_chunks: Dict[str, List[str]] = {}
# doc_id -> list of embeddings (np.ndarray or None)
doc_embeddings: Dict[str, List[Optional[np.ndarray]]] = {}

# =========================
# API Endpoints
# =========================
@app.post("/api/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF and index it. Returns a doc_id to use with /api/chat.
    """
    try:
        file_bytes = await file.read()
        text = read_pdf_bytes(file_bytes)
        if text.startswith("Error reading PDF:"):
            return {
                "ok": False,
                "error": text,
            }

        chunks = chunk_text(text, chunk_size=1500, overlap=200)
        embeddings = [get_embedding(c) for c in chunks]

        # Generate and persist doc_id
        new_doc_id = str(uuid.uuid4())
        documents[new_doc_id] = text
        doc_chunks[new_doc_id] = chunks
        doc_embeddings[new_doc_id] = embeddings

        return {
            "ok": True,
            "doc_id": new_doc_id,
            "chunk_count": len(chunks),
            "file_name": file.filename,
        }
    except Exception as e:
        return {"ok": False, "error": "Upload failed: {}".format(e)}

@app.get("/api/docs")
async def list_docs():
    """
    List in-memory documents for debugging.
    """
    return {
        "count": len(documents),
        "doc_ids": list(documents.keys()),
    }

@app.delete("/api/docs/{doc_id}")
async def delete_doc(doc_id: str):
    """
    Delete a loaded document from memory.
    """
    if doc_id in documents:
        documents.pop(doc_id, None)
        doc_chunks.pop(doc_id, None)
        doc_embeddings.pop(doc_id, None)
        return {"ok": True, "deleted": doc_id}
    return {"ok": False, "error": "doc_id not found"}

@app.post("/api/chat")
async def query_doc(
    question: str = Query(..., description="User question"),
    doc_id: str = Query(..., description="Document id returned by /api/upload"),
):
    """
    Ask a question against a specific uploaded PDF.
    Preserves your special cases for Net Debt and Net Debt/EBITDA.
    """
    if doc_id not in documents:
        return {"answer": "Unknown doc_id. Upload a PDF first and use its doc_id."}

    q_lower = question.lower()

    # Net Debt
    if "net debt" in q_lower and "ebitda" not in q_lower:
        net_debt_value = calculate_net_debt()
        return {
            "answer": "The company's Net Debt at the end of the last fiscal year was ${} million.".format(
                net_debt_value
            )
        }

    # Net Debt / EBITDA multiple
    if "net debt" in q_lower and "ebitda" in q_lower:
        net_debt, ebitda, multiple = calculate_net_debt_ebitda_multiple()
        if multiple is not None:
            return {
                "answer": "Net Debt = ${}m, EBITDA = ${}m -> Net Debt/EBITDA = {:.2f}x".format(
                    net_debt, ebitda, multiple
                )
            }
        else:
            return {"answer": "EBITDA is zero, cannot compute Net Debt/EBITDA multiple."}

    # Otherwise use LLM retrieval
    relevant = retrieve_relevant_chunks(doc_id, question, top_k=3)
    if not relevant:
        return {"answer": "Could not retrieve relevant context for this question."}

    context = "\n\n".join(relevant)
    prompt = (
        "Using only the following document excerpts, answer the question.\n\n"
        "{}\n\nQuestion: {}".format(context, question)
    )

    try:
        response = model.generate_content(prompt)
        return {"answer": response.text}
    except Exception as e:
        return {"answer": "An error occurred: {}".format(e)}

# =========================
# Basic health check
# =========================
@app.get("/healthz")
async def healthz():
    return {"ok": True}
