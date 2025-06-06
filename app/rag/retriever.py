from langchain.vectorstores import FAISS
from app.rag.embedder import get_embedder
from langchain.chains import RetrievalQA
from groq import ChatGroq  # Or use ChatOpenAI, Claude, etc.

def load_vector_index(persist_path="data/faiss_index"):
    return FAISS.load_local(persist_path, get_embedder(), allow_dangerous_deserialization=True)

def ask_doc_question(query: str, index):
    llm = ChatGroq(model="mixtral-8x7b-32768", api_key="your_key")
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=index.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )
    return qa_chain.run(query)
