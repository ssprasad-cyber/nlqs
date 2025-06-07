# app/rag/embedder.py
"""
Provides a reusable embedding model instance for transforming text into vector embeddings
using a HuggingFace sentence-transformer model.
"""

from langchain.embeddings import HuggingFaceEmbeddings

def get_embedder() -> HuggingFaceEmbeddings:
    """
    Initializes and returns a HuggingFaceEmbeddings instance
    using the 'sentence-transformers/all-MiniLM-L6-v2' model.

    Returns:
        HuggingFaceEmbeddings: The embedding model instance.

    Raises:
        RuntimeError: If the embedding model fails to initialize.
    """
    try:
        embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        return embedder
    except Exception as e:
        raise RuntimeError(f"Failed to initialize embedder: {e}") from e
