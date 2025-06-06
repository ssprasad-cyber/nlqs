from app.rag.indexer import build_vector_index

if __name__ == "__main__":
    paths = ["data/sample.pdf"]  # Add your file(s)
    build_vector_index(paths)
    print("✅ Indexed successfully!")
