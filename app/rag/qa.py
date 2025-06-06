from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os

DB_FAISS_PATH = "vectorstore/db_faiss"

def load_vectorstore():
    embeddings = HuggingFaceEmbeddings()
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    return db.as_retriever(search_kwargs={"k": 3})

def answer_from_docs(query: str) -> str:
    retriever = load_vectorstore()
    
    # LLM setup (replace with your active LLM provider)
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    # Optional: custom prompt
    prompt_template = """You are an expert assistant. Use the following context to answer the question:
    
    {context}

    Question: {question}

    Answer:"""

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

    response = chain.run(query)
    return response
