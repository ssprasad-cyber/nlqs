# app/db/schema.py
"""
    Return a string describing your database schema,
    e.g., tables, columns, types, relationships...
    This is used by your SQL translation prompt."""

def get_schema_description() -> str:
    return """
Table: customers
- id (integer)
- name (text)
- country (text)
- signup_date (date)

Table: orders
- id (integer)
- customer_id (integer)
- total_amount (float)
- order_date (date)
"""
