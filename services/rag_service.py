from services.embedding_service import embed
from services.vector_service import retrieve
from services.llm_service import generate
from config import TOP_K


def answer_question(query, chunks, index, chat_history=None):

    # 1️⃣ Embed user query
    query_embedding = embed([query])

    # 2️⃣ Retrieve top-k relevant chunks
    indices = retrieve(index, query_embedding, TOP_K)

    # 3️⃣ Build document context
    context = ""
    for idx in indices[0]:
        context += chunks[idx] + "\n"

    # 4️⃣ Add limited chat history (memory control)
    history_text = ""
    if chat_history:
        for msg in chat_history[-4:]:  # Only last 4 messages
            history_text += f"{msg['role']}: {msg['content']}\n"

    # 5️⃣ Create prompt
    prompt = f"""
You are a professional AI assistant.
Answer ONLY using the provided document context.
If the answer is not found, say "Answer not found in document."

Chat History:
{history_text}

Context:
{context}

Question:
{query}

Answer:
"""

    # 6️⃣ Generate response
    output = generate(prompt)

    # 7️⃣ Clean output if model repeats "Answer:"
    if "Answer:" in output:
        output = output.split("Answer:")[-1].strip()

    return output
