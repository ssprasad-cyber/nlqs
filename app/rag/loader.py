# app/rag/loader.py
"""
Module to load documents from multiple file paths and split them into
smaller chunks for downstream embedding and indexing.

Supports PDF and text files using LangChain community loaders.
"""

from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_documents(paths: List[str]) -> List:
    """
    Loads documents from the specified file paths.

    Args:
        paths (List[str]): List of file paths to load documents from.

    Returns:
        List: A list of loaded Document objects.

    Raises:
        FileNotFoundError: If any file path does not exist.
        ValueError: If the paths list is empty.
        Exception: For other loading failures.
    """
    if not paths:
        raise ValueError("No document paths provided.")

    documents = []
    for path in paths:
        if not path:
            continue
        if not isinstance(path, str):
            raise TypeError(f"Expected string file path, got {type(path)}")

        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        try:
            if path.lower().endswith(".pdf"):
                loader = PyPDFLoader(path)
            else:
                loader = TextLoader(path)
            loaded_docs = loader.load()
            if not loaded_docs:
                print(f"Warning: No documents loaded from {path}")
            documents.extend(loaded_docs)
        except Exception as e:
            raise RuntimeError(f"Failed to load document {path}: {str(e)}") from e

    return documents


def split_documents(documents: List, chunk_size: int = 500, chunk_overlap: int = 50) -> List:
    """
    Splits documents into smaller text chunks using a recursive character splitter.

    Args:
        documents (List): List of Document objects to split.
        chunk_size (int): Maximum size of each chunk.
        chunk_overlap (int): Number of overlapping characters between chunks.

    Returns:
        List: List of chunked Document objects.

    Raises:
        ValueError: If documents list is empty.
    """
    if not documents:
        raise ValueError("No documents provided for splitting.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    try:
        chunks = splitter.split_documents(documents)
        if not chunks:
            print("Warning: Document splitting resulted in zero chunks.")
        return chunks
    except Exception as e:
        raise RuntimeError(f"Failed to split documents: {str(e)}") from e
