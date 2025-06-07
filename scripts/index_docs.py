# scripts/index_docs.py
"""
Script to build and persist a FAISS vector index from document files.

Usage:
    python index_docs.py
"""

import logging
from app.rag.indexer import build_vector_index

def main():
    paths = ["data/sample.pdf"]  # List your document files here

    try:
        build_vector_index(paths)
        print("✅ Indexed successfully!")
    except Exception as e:
        logging.error(f"Failed to build vector index: {e}", exc_info=True)
        print("❌ Indexing failed. See logs for details.")

if __name__ == "__main__":
    main()
