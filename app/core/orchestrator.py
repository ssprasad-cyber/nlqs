# app/core/orchestrator.py
"""
Orchestrator module to route incoming natural language questions to the appropriate
handler — either an SQL translator+executor or a RAG (document-based) system.

This acts as the core logic of NLQS (Natural Language Query System).
"""

from app.core.intent import classify_intent
from app.core.translator import translate_to_sql
from app.core.executor import execute_sql
from app.rag.qa import answer_from_docs


def clean_sql(sql: str) -> str:
    """
    Cleans formatting characters from SQL strings (e.g., from markdown fences).

    Parameters:
        sql (str): SQL string that may be wrapped in markdown-style code blocks.

    Returns:
        str: Cleaned SQL string.
    """
    if not sql:
        return ""

    # Remove common markdown SQL code block formatting
    if sql.startswith("```") and sql.endswith("```"):
        sql = sql.strip("`").strip()
    
    return sql.strip()


async def handle_query(question: str) -> dict:
    """
    Handles a natural language query by classifying its intent and routing
    it to the appropriate execution pipeline.

    Parameters:
        question (str): The user's natural language query.

    Returns:
        dict: A structured response containing the query type and result.
    """
    if not question or not question.strip():
        return {
            "query_type": "error",
            "message": "Empty or invalid question provided."
        }

    try:
        # Step 1: Classify the type of question (SQL vs RAG)
        intent = classify_intent(question)

        # Step 2: Process SQL queries
        if intent == "sql":
            sql = await translate_to_sql(question)
            sql = clean_sql(sql)

            if not sql:
                return {
                    "query_type": "sql",
                    "sql_query": None,
                    "result": {
                        "query_type": "ERROR",
                        "summary": "Failed to generate SQL query."
                    }
                }

            result = execute_sql(sql)
            return {
                "query_type": "sql",
                "sql_query": sql,
                "result": result
            }

        # Step 3: Process RAG queries
        elif intent == "rag":
            result = answer_from_docs(question)
            return {
                "query_type": "rag",
                "result": result
            }

        # Step 4: Fallback for unexpected intent classification
        else:
            return {
                "query_type": "error",
                "message": "Could not determine the query intent."
            }

    except Exception as e:
        # Catch-all error handler to prevent internal crashes
        return {
            "query_type": "error",
            "message": f"Internal server error: {str(e)}"
        }
