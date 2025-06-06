# app/core/prompt.py

def get_sql_prompt(schema: str, question: str) -> str:
    return f"""
You are an expert SQL generator.

Here is the database schema:
{schema}

Convert the following natural language request into a valid SQL query:

Question: {question}

Only return the SQL query. Do not explain anything.
"""
