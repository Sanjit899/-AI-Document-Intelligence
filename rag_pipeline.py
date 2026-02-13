from transformers import pipeline
import numpy as np
from embeddings import get_embeddings
from vector_store import search

generator = pipeline(
    "text-generation",
    model="microsoft/phi-2",
    max_new_tokens=200
)

def generate_answer(query, text_chunks, index):
    query_embedding = get_embeddings([query])
    indices = search(index, np.array(query_embedding))

    context = ""
    for idx in indices[0]:
        context += text_chunks[idx] + "\n"

    prompt = f"""
Answer the question using the context below:

Context:
{context}

Question:
{query}

Answer:
"""

    result = generator(prompt)
    output = result[0]["generated_text"]

    # Extract only text after "Answer:"
    if "Answer:" in output:
        output = output.split("Answer:")[-1].strip()

    return output
