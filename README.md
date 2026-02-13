📄 AI Document Intelligence
Multi-PDF Conversational RAG System using FastAPI

An AI-powered document question-answering system that allows users to upload multiple PDFs and interact with them using conversational AI. The system uses Retrieval-Augmented Generation (RAG) with embeddings and vector search for accurate contextual answers.

🚀 Features

📂 Upload multiple PDF documents

✂️ Intelligent text chunking

🧠 Sentence-transformer embeddings

🔎 FAISS vector similarity search

💬 Session-based conversational memory

⚡ FastAPI backend

📖 Auto Swagger API docs

🌍 CORS enabled (frontend ready)


🏗️ Tech Stack

Backend: FastAPI

Embeddings: sentence-transformers (all-MiniLM-L6-v2)

Vector Store: FAISS

LLM: HuggingFace Transformers

PDF Processing: PyPDF

Language: Python 3.12.


🧠 Architecture Overview

User Uploads PDFs
↓
Text Extraction
↓
Text Chunking
↓
Embedding Generation
↓
FAISS Vector Index
↓
User Query
↓
Relevant Chunk Retrieval
↓
LLM Response Generation
↓
Session Memory Stored

📁 Project Structure
AI_Document_Intelligence/
│
├── main.py
├── config.py
├── requirements.txt
│
├── services/
│   ├── pdf_service.py
│   ├── embedding_service.py
│   ├── vector_service.py
│   ├── rag_service.py
│
├── utils/
│   └── chunking.py
│
└── uploads/

⚙️ Installation & Setup
2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate     # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt
You  will find  the  requirements  on the file .

4️⃣ Run Server
uvicorn main:app --reload

🌐 API Access

After running:

Main API:- http://127.0.0.1:8000/

Swagger Docs:- http://127.0.0.1:8000/docs

📤 API Endpoints
Upload PDFs

POST /upload

Form-data:

files → multiple PDF files

Chat with Documents

POST /chat

Form-data:

question → user query

session_id (optional)

Response:{
  "session_id": "uuid",
  "answer": "Generated answer..."
}


🛠️ Future Improvements

Persist FAISS index to disk

Streaming responses

Authentication

Database-backed session storage

Cloud deployment (Render / Railway / AWS)

🎯 Use Cases

Research document analysis

Academic paper QA

Legal document assistant

Company knowledge base chatbot

AI-powered PDF assistant


👨‍💻 Author

S K
BCA Student | AI & Backend Developer


