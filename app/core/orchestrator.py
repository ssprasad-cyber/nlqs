from app.core.intent import classify_intent
from app.core.translator import translate_to_sql
from app.core.executor import execute_sql
from app.rag.qa import answer_from_docs

def clean_sql(sql: str) -> str:
    if sql.startswith("```") and sql.endswith("```"):
        sql = sql.strip("`").strip()
    return sql.strip()

async def handle_query(question: str):
    intent = classify_intent(question)

    if intent == "sql":
        sql = await translate_to_sql(question)
        sql = clean_sql(sql)
        result = execute_sql(sql)
        return {
            "query_type": "sql",
            "sql_query": sql,
            "result": result,
        }

    elif intent == "rag":
        result = answer_from_docs(question)
        return {
            "query_type": "rag",
            "result": result,
        }

    else:
        return {
            "query_type": "error",
            "message": "Could not determine the query intent."
        }
