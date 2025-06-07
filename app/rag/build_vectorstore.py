# app/rag/build_vectorstore.py

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
import os

PDF_PATH = "data/sample.pdf"
VECTORSTORE_PATH = "vectorstore/db_faiss"

def build_vectorstore():
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load_and_split()
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    db = FAISS.from_documents(documents, embeddings)
    db.save_local(VECTORSTORE_PATH)
    print("✅ Vectorstore built successfully!")

if __name__ == "__main__":
    build_vectorstore()
