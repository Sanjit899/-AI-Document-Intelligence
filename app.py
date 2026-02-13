from flask import Flask, render_template, request
import logging
import os

# Config
from config import CHUNK_SIZE, CHUNK_OVERLAP

# Services
from services.pdf_service import PDFService
from services.embedding_service import embed
from services.vector_service import create_index
from services.rag_service import answer_question

# Utils
from utils.chunking import create_chunks

app = Flask(__name__)

# Logging setup
logging.basicConfig(level=logging.INFO)

# Global state (for now — later we can improve this)
text_chunks = []
vector_index = None


@app.route("/", methods=["GET", "POST"])
def index():
    global text_chunks, vector_index

    answer = ""

    if request.method == "POST":

        # =========================
        # PDF Upload Handling
        # =========================
        if "pdf" in request.files:
            file = request.files["pdf"]

            if file and PDFService.allowed_file(file.filename):
                try:
                    logging.info("Uploading PDF...")

                    file_path = PDFService.save_file(file, "uploads")
                    text = PDFService.extract_text(file_path)

                    logging.info("Creating chunks...")
                    text_chunks = create_chunks(text, CHUNK_SIZE, CHUNK_OVERLAP)

                    logging.info("Generating embeddings...")
                    embeddings = embed(text_chunks)

                    logging.info("Creating FAISS index...")
                    vector_index = create_index(embeddings)

                    answer = "PDF processed successfully!"

                except Exception as e:
                    logging.error(f"PDF Processing Error: {str(e)}")
                    answer = f"Error processing PDF: {str(e)}"

            else:
                answer = "Invalid file type. Please upload a PDF."

        # =========================
        # Question Handling
        # =========================
        elif "question" in request.form:
            question = request.form["question"]

            if vector_index is None:
                answer = "Please upload a PDF first."
            else:
                try:
                    logging.info(f"User Question: {question}")

                    answer = answer_question(
                        query=question,
                        chunks=text_chunks,
                        index=vector_index
                    )

                    logging.info(f"Model Answer: {answer}")

                except Exception as e:
                    logging.error(f"RAG Error: {str(e)}")
                    answer = f"Error generating answer: {str(e)}"

    return render_template("index.html", answer=answer)


if __name__ == "__main__":
    app.run(debug=True)
