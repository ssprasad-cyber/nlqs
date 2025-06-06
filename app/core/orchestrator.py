from app.core.intent import classify_intent
from app.core.translator import translate_to_sql
from app.rag.qa import answer_from_docs  # import your RAG function

async def handle_query(question: str) -> dict:
    intent = classify_intent(question)

    if intent == "sql":
        sql_query = await translate_to_sql(question)
        return {
            "intent": "sql",
            "natural_question": question,
            "generated_sql": sql_query
        }

    elif intent == "rag":
        # Run the RAG document question answering and return result
        # rag_answer = answer_from_docs(question)
        # return {
        #     "intent": "rag",
        #     "query": question,
        #     "answer": rag_answer
        # }
         return {
            "intent": "rag",
            "query": question,
            "note": "Next step: run RAG (vector search) on documents."
        }

    return {"error": "Intent detection failed."}
