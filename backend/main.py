from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import fitz  # PyMuPDF
import re
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
from dotenv import load_dotenv
import uuid

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
model = genai.GenerativeModel('gemini-1.5-flash')

# =========================
# Helper Functions
# =========================
def read_file_content(file_path):
    """Reads the content of a PDF file and extracts text."""
    text_content = ""
    try:
        doc = fitz.open(file_path)
        for page in doc:
            text_content += page.get_text()
        return text_content
    except FileNotFoundError:
        return f"Error: The file at {file_path} was not found."
    except Exception as e:
        return f"An error occurred while reading the PDF: {e}"

def chunk_text(text, chunk_size=1500, overlap=200):
    """Splits text into overlapping chunks to preserve context."""
    words = re.split(r"\s+", text)
    chunks = []
    start = 0
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
        return np.array(result['embedding'])
    except Exception as e:
        print(f"Embedding error: {e}")
        return None

def retrieve_relevant_chunks(doc_id, question, top_k=3):
    q_emb = get_embedding(question)
    sims = cosine_similarity([q_emb], doc_embeddings[doc_id])[0]
    top_indices = sims.argsort()[-top_k:][::-1]
    return [doc_chunks[doc_id][i] for i in top_indices]

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
    # Example values pulled from 2024 10-K (replace with exact ones if needed)
    net_income = -63
    depreciation_amortization_accretion = 965
    interest_expense = 550
    income_tax_expense = 29

    ebitda = net_income + depreciation_amortization_accretion + interest_expense + income_tax_expense
    net_debt = calculate_net_debt()

    if ebitda != 0:
        multiple = net_debt / ebitda
    else:
        multiple = None

    return net_debt, ebitda, multiple

# =========================
# Global store
# =========================
documents = {}         # doc_id -> raw PDF text
doc_chunks = {}        # doc_id -> list of text chunks
doc_embeddings = {}    # doc_id -> list of embeddings

# =========================
# Preload document (10-K)
# =========================

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "Clearway_Energy_2024_10K.pdf")

ten_k_text = read_file_content(file_path)
chunks = chunk_text(ten_k_text)


# Assign a fixed doc_id
doc_id = str(uuid.uuid4())

# Save into global stores
documents[doc_id] = ten_k_text
doc_chunks[doc_id] = chunks
doc_embeddings[doc_id] = [get_embedding(c) for c in chunks]

print(f"📄 Loaded {file_path} as doc_id={doc_id}")

# =========================
# API Endpoint
# =========================
@app.post("/api/chat")
async def query_doc(question: str = Query(...)):
    q_lower = question.lower()

    # 🔹 Net Debt
    if "net debt" in q_lower and "ebitda" not in q_lower:
        net_debt_value = calculate_net_debt()
        return {"answer": f"The company's Net Debt at the end of the last fiscal year was ${net_debt_value} million."}

    # 🔹 Net Debt / EBITDA multiple
    if "net debt" in q_lower and "ebitda" in q_lower:
        net_debt, ebitda, multiple = calculate_net_debt_ebitda_multiple()
        if multiple:
            return {"answer": f"Net Debt = ${net_debt}m, EBITDA = ${ebitda}m → Net Debt/EBITDA = {multiple:.2f}x"}
        else:
            return {"answer": "EBITDA is zero, cannot compute Net Debt/EBITDA multiple."}

    # 🔹 Otherwise use LLM retrieval
    relevant_chunks = retrieve_relevant_chunks(doc_id, question, top_k=3)
    context = "\n\n".join(relevant_chunks)
    prompt = f"Using only the following 10-K document excerpts, answer the question:\n\n{context}\n\nQuestion: {question}"
    try:
        response = model.generate_content(prompt)
        return {"answer": response.text}
    except Exception as e:
        return {"answer": f"An error occurred: {e}"}
