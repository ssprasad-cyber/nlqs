# app/core/translator.py
"""
This module translates natural language questions into SQL queries using an
LLM (Groq's hosted version of LLaMA3). It constructs a prompt based on the
current DB schema and calls the LLM API to generate a valid SQL query.
"""

import os
from openai import OpenAI, OpenAIError
from app.core.prompt import get_sql_prompt
from app.db.schema import get_schema_description

# Ensure the GROQ API key is set
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise EnvironmentError("GROQ_API_KEY not found in environment variables.")

# Initialize the OpenAI client for Groq
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

async def translate_to_sql(question: str) -> str:
    """
    Translates a user-provided natural language question into a SQL query.

    Parameters:
        question (str): The user's natural language question.

    Returns:
        str: A generated SQL query string.

    Raises:
        RuntimeError: If the LLM fails to return a usable response.
    """
    if not question or not question.strip():
        raise ValueError("Question is empty or invalid.")

    # Retrieve database schema and generate prompt
    schema = get_schema_description()
    prompt = get_sql_prompt(schema, question)

    try:
        # Send the prompt to Groq LLM via OpenAI-compatible API
        response = client.chat.completions.create(
            model="llama3-70b-8192",  # Groq-hosted LLaMA3 model
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )

        # Extract and return the SQL from the response
        return response.choices[0].message.content.strip()

    except OpenAIError as e:
        # Catch any issues with the OpenAI client or API response
        raise RuntimeError(f"Failed to translate to SQL: {str(e)}") from e
