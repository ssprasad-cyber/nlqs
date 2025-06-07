# app/core/executor.py
"""
This module handles execution of raw SQL queries against a SQLite database.
It distinguishes between SELECT (read) and MODIFY (write) operations,
returns structured results for SELECT queries, and reports the outcome
or error for other query types. Designed for secure and robust database interaction.
"""

import sqlite3
from typing import Any, Dict

# Path to the SQLite database file
DB_PATH = "data/sample.db"

def execute_sql(sql: str) -> Dict[str, Any]:
    """
    Executes a given SQL query on the SQLite database.

    Parameters:
        sql (str): The SQL query to execute.

    Returns:
        dict: A structured dictionary containing query results or error info.
    """
    if not sql or not sql.strip():
        return {
            "query_type": "ERROR",
            "summary": "Empty SQL query provided."
        }

    try:
        # Automatically handles connection closing
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Determine the type of SQL operation (e.g., SELECT, INSERT)
            query_type = sql.strip().split()[0].lower()

            # Execute the SQL query
            cursor.execute(sql)

            # Handle SELECT queries separately
            if query_type == "select":
                rows = cursor.fetchall()

                if not rows:
                    return {
                        "query_type": "SELECT",
                        "columns": [],
                        "rows": [],
                        "summary": "No results found."
                    }

                # Extract column names and convert rows to lists
                columns = rows[0].keys()
                data = [list(row) for row in rows]

                return {
                    "query_type": "SELECT",
                    "columns": list(columns),
                    "rows": data,
                    "summary": f"{len(rows)} rows returned."
                }
            else:
                # For non-SELECT queries (INSERT, UPDATE, DELETE, etc.)
                conn.commit()
                return {
                    "query_type": "MODIFY",
                    "summary": f"{cursor.rowcount} rows affected."
                }

    except sqlite3.OperationalError as e:
        # Catch common DB issues like bad SQL syntax
        return {
            "query_type": "ERROR",
            "summary": f"OperationalError: {str(e)}"
        }
    except sqlite3.DatabaseError as e:
        # Catch broader DB errors
        return {
            "query_type": "ERROR",
            "summary": f"DatabaseError: {str(e)}"
        }
    except Exception as e:
        # Catch any other unexpected errors
        return {
            "query_type": "ERROR",
            "summary": f"UnexpectedError: {str(e)}"
        }
