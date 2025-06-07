# app/core/intent.py

from typing import Literal

# For now, a simple keyword-based classifier (can upgrade to LLM later)
def classify_intent(question: str) -> Literal["sql", "rag"]:
    keywords_sql = [
        "show", "list", "count", "top", "group by", "from", "where", "order by",
        "most", "least", "total", "average", "sum"
    ]

    question_lower = question.lower()
    for keyword in keywords_sql:
        if f" {keyword} " in f" {question_lower} ":
            return "sql"

    # Default to RAG for non-structured queries

    return "rag"
