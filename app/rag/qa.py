# app/rag/qa.py
"""
Module for retrieving answers from a FAISS vectorstore augmented with
a retrieval-augmented generation (RAG) chain using LangChain.

It loads vectorstore embeddings and uses a ChatOpenAI LLM with a
custom prompt to answer user queries based on relevant documents.
"""

import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

DB_FAISS_PATH = "vectorstore/db_faiss"

def load_vectorstore() -> FAISS:
    """
    Loads the FAISS vectorstore with embeddings from local storage.

    Returns:
        FAISS retriever: Retriever object to fetch relevant documents.

    Raises:
        RuntimeError: If loading the vectorstore or embeddings fails.
    """
    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        # Load the FAISS index from local directory with embeddings
        db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
        # Return retriever with top-k=3 documents for each query
        return db.as_retriever(search_kwargs={"k": 3})
    except Exception as e:
        raise RuntimeError(f"Failed to load vectorstore: {e}") from e


def answer_from_docs(query: str) -> str:
    """
    Answers a user query by retrieving relevant documents and generating
    a response using a retrieval-augmented generation chain.

    Args:
        query (str): The natural language query from the user.

    Returns:
        str: The generated answer based on retrieved documents.

    Raises:
        RuntimeError: If the RAG chain execution fails.
    """
    try:
        retriever = load_vectorstore()

        llm = ChatOpenAI(
            model="llama3-70b-8192",
            temperature=0,
            openai_api_key=os.getenv("GROQ_API_KEY"),
            openai_api_base="https://api.groq.com/openai/v1"
        )

        prompt_template = (
            "You are an expert assistant. Use the following context to answer the question:\n\n"
            "{context}\n\n"
            "Question: {question}\n\n"
            "Answer:"
        )

        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )

        chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff",
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=False,
        )

        response = chain.invoke({"query": query})
        return response

    except Exception as e:
        raise RuntimeError(f"Failed to answer from documents: {e}") from e
