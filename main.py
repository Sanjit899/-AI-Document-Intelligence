from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uuid
import logging

from config import CHUNK_SIZE, CHUNK_OVERLAP
from services.pdf_service import PDFService
from services.embedding_service import embed
from services.vector_service import create_index
from services.rag_service import answer_question
from utils.chunking import create_chunks


# =========================
# App Initialization
# =========================
app = FastAPI()

logging.basicConfig(level=logging.INFO)

# =========================
# CORS Middleware
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Global State
# =========================
all_chunks = []
vector_index = None
chat_sessions = {}


# =========================
# Health Check
# =========================
@app.get("/")
def home():
    return {"message": "AI Document Intelligence API Running 🚀"}


# =========================
# Upload Multiple PDFs
# =========================
@app.post("/upload")
async def upload_pdfs(files: List[UploadFile] = File(...)):

    global all_chunks, vector_index

    try:
        for file in files:

            if not PDFService.allowed_file(file.filename):
                return {"error": "Only PDF files allowed"}

            contents = await file.read()
            path = PDFService.save_raw_file(contents, file.filename, "uploads")

            text = PDFService.extract_text(path)
            chunks = create_chunks(text, CHUNK_SIZE, CHUNK_OVERLAP)

            all_chunks.extend(chunks)

        embeddings = embed(all_chunks)
        vector_index = create_index(embeddings)

        return {"message": "All PDFs processed successfully"}

    except Exception as e:
        logging.exception("PDF processing failed")
        return {"error": str(e)}


# =========================
# Chat Endpoint (RAG)
# =========================
@app.post("/chat")
async def chat(
    question: str = Form(...),
    session_id: str = Form(None)
):

    global vector_index, all_chunks, chat_sessions

    if vector_index is None:
        return {"error": "Upload PDFs first"}

    # Create session
    if not session_id:
        session_id = str(uuid.uuid4())
        chat_sessions[session_id] = []

    if session_id not in chat_sessions:
        chat_sessions[session_id] = []

    # Store user message
    chat_sessions[session_id].append({
        "role": "user",
        "content": question
    })

    # Generate answer
    answer = answer_question(
        query=question,
        chunks=all_chunks,
        index=vector_index,
        chat_history=chat_sessions[session_id]
    )

    # Store assistant reply
    chat_sessions[session_id].append({
        "role": "assistant",
        "content": answer
    })

    return {
        "session_id": session_id,
        "answer": answer
    }
