# app/rag/build_vectorstore.py
"""
This script loads a PDF document, splits it into chunks, embeds them using a
HuggingFace model, and saves the resulting FAISS vector store locally.

Used for Retrieval-Augmented Generation (RAG) pipelines.
"""

import os
import sys
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader

# Configuration paths
PDF_PATH = "data/sample.pdf"
VECTORSTORE_PATH = "vectorstore/db_faiss"

def build_vectorstore():
    """
    Builds and saves a FAISS vector store from a PDF using HuggingFace embeddings.
    
    Raises:
        FileNotFoundError: If the source PDF file is missing.
        Exception: For other failures in processing or saving.
    """
    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(f"PDF file not found at: {PDF_PATH}")

    try:
        # Step 1: Load and split the document
        loader = PyPDFLoader(PDF_PATH)
        documents = loader.load_and_split()

        if not documents:
            raise ValueError("No content loaded from PDF.")

        # Step 2: Load sentence-transformer embeddings
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # Step 3: Build vector database from embedded documents
        db = FAISS.from_documents(documents, embeddings)

        # Ensure target folder exists
        os.makedirs(VECTORSTORE_PATH, exist_ok=True)

        # Step 4: Save vector store locally
        db.save_local(VECTORSTORE_PATH)

        print("✅ Vectorstore built successfully and saved to:", VECTORSTORE_PATH)

    except Exception as e:
        print(f"❌ Failed to build vectorstore: {str(e)}", file=sys.stderr)
        raise

# Allow script to be run standalone
if __name__ == "__main__":
    build_vectorstore()
