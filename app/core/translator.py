# app/core/translator.py

import os
from openai import OpenAI
from app.core.prompt import get_sql_prompt
from app.db.schema import get_schema_description

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),  # Get this from https://console.groq.com/
    base_url="https://api.groq.com/openai/v1"  # Point to Groq API
)

async def translate_to_sql(question: str) -> str:
    schema = get_schema_description()
    prompt = get_sql_prompt(schema, question)

    response = client.chat.completions.create(
        model="llama3-70b-8192",  # Updated model
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )


    return response.choices[0].message.content.strip()
