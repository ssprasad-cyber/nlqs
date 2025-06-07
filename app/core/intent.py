# app/core/intent.py
"""
This module defines a simple keyword-based intent classifier that determines
whether a natural language question should be processed as a structured SQL
query or passed to a Retrieval-Augmented Generation (RAG) pipeline.

Currently based on keyword matching but can be upgraded to a machine learning
or LLM-based classifier for more nuanced detection.
"""

from typing import Literal

def classify_intent(question: str) -> Literal["sql", "rag"]:
    """
    Classifies the intent of a natural language question.

    Parameters:
        question (str): The input question from the user.

    Returns:
        Literal["sql", "rag"]: 
            - "sql" if the question matches typical SQL-related patterns.
            - "rag" if it's more suitable for a document-based QA model.
    """

    if not question or not question.strip():
        # Default to RAG if the question is empty or invalid
        return "rag"

    # Keywords that typically indicate SQL-based structured data queries
    keywords_sql = [
        "show", "list", "count", "top", "group by", "from", "where", "order by",
        "most", "least", "total", "average", "sum", "max", "min"
    ]

    # Normalize question to lowercase and pad spaces for accurate matching
    question_lower = f" {question.lower()} "

    # If any SQL keyword is present, classify as SQL
    for keyword in keywords_sql:
        if f" {keyword} " in question_lower:
            return "sql"

    # Default to RAG for anything that doesn't appear SQL-related
    return "rag"
