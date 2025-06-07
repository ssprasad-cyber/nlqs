# app/rag/build_vector_index.py
"""
Builds and persists a FAISS vector index from documents loaded from given file paths.

This function:
- Loads documents using custom loader functions
- Splits documents into chunks suitable for embedding
- Creates embeddings via a custom embedder
- Builds and saves a FAISS vector store locally
"""

import os
from langchain.vectorstores import FAISS
from app.rag.loader import load_documents, split_documents
from app.rag.embedder import get_embedder

def build_vector_index(paths: list[str], persist_path: str = "data/faiss_index") -> FAISS:
    """
    Build and persist a FAISS vector store from documents loaded from provided paths.

    Parameters:
        paths (list[str]): List of file paths to load documents from.
        persist_path (str): Directory path where the FAISS index will be saved.

    Returns:
        FAISS: The built FAISS vector store instance.

    Raises:
        ValueError: If paths list is empty.
        FileNotFoundError: If any file in paths does not exist.
        Exception: For other failures during loading, embedding, or saving.
    """
    if not paths:
        raise ValueError("No document paths provided.")

    for p in paths:
        if not os.path.exists(p):
            raise FileNotFoundError(f"Document file not found: {p}")

    try:
        # Load documents from given paths
        documents = load_documents(paths)
        if not documents:
            raise ValueError("No documents loaded from the provided paths.")

        # Split documents into smaller chunks for embedding
        chunks = split_documents(documents)
        if not chunks:
            raise ValueError("Document splitting returned no chunks.")

        # Initialize embedding model
        embedder = get_embedder()

        # Create FAISS vector store from document chunks and embeddings
        vectorstore = FAISS.from_documents(chunks, embedder)

        # Ensure persistence directory exists
        os.makedirs(persist_path, exist_ok=True)

        # Save the vector store locally
        vectorstore.save_local(persist_path)

        return vectorstore

    except Exception as e:
        # Rethrow exception for upstream handling/logging
        raise RuntimeError(f"Failed to build vector index: {str(e)}") from e
