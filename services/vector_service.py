import faiss
import numpy as np

def create_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    return index

def retrieve(index, query_embedding, top_k):
    distances, indices = index.search(np.array(query_embedding), top_k)
    return indices
