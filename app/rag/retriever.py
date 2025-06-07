# app/rag/retriever.py
"""
Module to load FAISS vector index and perform question answering using
Groq's ChatGroq LLM integrated with LangChain's RetrievalQA chain.
"""

import os
from langchain.vectorstores import FAISS
from app.rag.embedder import get_embedder
from langchain.chains import RetrievalQA
from groq import ChatGroq

def load_vector_index(persist_path: str = "data/faiss_index") -> FAISS:
    """
    Load the FAISS vector index from local storage.

    Args:
        persist_path (str): Path where the FAISS index is stored.

    Returns:
        FAISS: Loaded FAISS vector store instance.

    Raises:
        RuntimeError: If loading the vector index fails.
    """
    try:
        embedder = get_embedder()
        vector_index = FAISS.load_local(persist_path, embedder, allow_dangerous_deserialization=True)
        return vector_index
    except Exception as e:
        raise RuntimeError(f"Failed to load vector index from {persist_path}: {e}") from e

def ask_doc_question(query: str, index: FAISS) -> str:
    """
    Ask a question against the document index using Groq's ChatGroq model.

    Args:
        query (str): The user's query.
        index (FAISS): The FAISS vector index retriever.

    Returns:
        str: The generated answer.

    Raises:
        RuntimeError: If the QA chain execution fails.
    """
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY environment variable is not set.")

        llm = ChatGroq(model="mixtral-8x7b-32768", api_key=api_key)

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=index.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True,
        )

        return qa_chain.run(query)

    except Exception as e:
        raise RuntimeError(f"Failed to run QA chain: {e}") from e
