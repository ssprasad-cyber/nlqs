# app/db/setup_db.py

import sqlite3
import os

DB_PATH = "data/sample.db"

def create_sample_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Drop old table
    cursor.execute("DROP TABLE IF EXISTS customers")

    # Create new table
    cursor.execute("""
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            country TEXT,
            age INTEGER,
            signup_date TEXT
        )
    """)

    # Insert sample data
    sample_data = [
        ("Alice", "USA", 28, "2021-05-10"),
        ("Bob", "France", 34, "2020-07-22"),
        ("Charlie", "India", 25, "2022-01-12"),
        ("Diana", "Germany", 30, "2019-03-18"),
    ]

    cursor.executemany("INSERT INTO customers (name, country, age, signup_date) VALUES (?, ?, ?, ?)", sample_data)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_sample_db()
