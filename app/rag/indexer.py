import os
from langchain.vectorstores import FAISS
from app.rag.loader import load_documents, split_documents
from app.rag.embedder import get_embedder

def build_vector_index(paths: list, persist_path="data/faiss_index"):
    documents = load_documents(paths)
    chunks = split_documents(documents)
    embedder = get_embedder()

    vectorstore = FAISS.from_documents(chunks, embedder)
    os.makedirs(persist_path, exist_ok=True)
    vectorstore.save_local(persist_path)
    return vectorstore
