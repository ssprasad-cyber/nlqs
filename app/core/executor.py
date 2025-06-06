# app/core/executor.py

import sqlite3

DB_PATH = "data/sample.db"

def execute_sql(sql: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        query_type = sql.strip().split()[0].lower()
        cursor.execute(sql)

        if query_type == "select":
            rows = cursor.fetchall()
            if not rows:
                result = {
                    "query_type": "SELECT",
                    "columns": [],
                    "rows": [],
                    "summary": "No results found."
                }
            else:
                columns = rows[0].keys()
                data = [list(row) for row in rows]  # or [dict(row) for row in rows] for key-based
                result = {
                    "query_type": "SELECT",
                    "columns": list(columns),
                    "rows": data,
                    "summary": f"{len(rows)} rows returned."
                }
        else:
            conn.commit()
            result = {
                "query_type": "MODIFY",
                "summary": f"{cursor.rowcount} rows affected."
            }

        conn.close()
        return result

    except Exception as e:
        return {
            "query_type": "ERROR",
            "summary": str(e)
        }
