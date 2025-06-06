# app/core/orchestrator.py

from app.core.intent import classify_intent
from app.core.translator import translate_to_sql

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
        return {
            "intent": "rag",
            "query": question,
            "note": "Next step: run RAG (vector search) on documents."
        }

    return {"error": "Intent detection failed."}
