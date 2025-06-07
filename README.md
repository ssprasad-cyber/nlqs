# NLQS (Natural Language Query System)

A FastAPI-based backend service that allows users to query structured data via natural language questions. The system intelligently routes questions to either a SQL translator or a retrieval-augmented generation (RAG) module for document-based QA.

---

## Features

- **Intent classification:** Automatically classify a question as SQL-based or document-based.
- **SQL translation:** Convert natural language questions into SQL queries using a large language model (Groq API).
- **SQL execution:** Execute generated SQL on a predefined database schema with sample data.
- **Document QA:** Answer questions using retrieval-augmented generation on vectorized documents.
- **Clean SQL output:** Removes markdown formatting (like backticks) from generated SQL queries.
- **Error handling:** Detect invalid SQL or unsupported queries and provide meaningful error messages.

---

## Architecture Overview
![NLQS Architecture Diagram](https://github.com/ssprasad-cyber/nlqs/blob/main/architecture%20/_-%20visual%20selection.png)
![NLQS orchestratory engine](https://github.com/ssprasad-cyber/nlqs/blob/main/architecture%20/_-%20visual%20selection%20(1).png)
---

## Key Modules

### 1. API Routes (`app/routes/query.py`)

- Endpoint: `POST /api/query`
- Accepts JSON: `{ "question": "string", "source": "db" | "docs" }`
- Calls orchestrator to handle query and returns structured JSON response.

### 2. Orchestrator (`app/core/orchestrator.py`)

- Coordinates flow based on source (db or docs).
- Cleans generated SQL (removes markdown backticks).
- Calls SQL translator and executor for database queries.
- Calls RAG module for document question answering.

### 3. Intent Classifier (`app/core/intent.py`)

- Simple keyword-based intent detection.
- Classifies queries as `"sql"` or `"rag"`.

### 4. SQL Translator (`app/core/translator.py`)

- Uses Groq OpenAI-compatible API with a LLM (`llama3-70b-8192`).
- Generates SQL from natural language question.
- Incorporates database schema context in prompt.

### 5. Document QA (`app/rag/qa.py`)

- Loads vector store using FAISS and HuggingFace embeddings.
- Runs RetrievalQA chain with OpenAI GPT-3.5-turbo LLM.
- Answers questions based on sample documents (e.g., PDF vector store).

---

## Sample Database Schema & Data

```sql
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    country TEXT,
    age INTEGER,
    signup_date TEXT
);

INSERT INTO customers (name, country, age, signup_date) VALUES
("Alice", "USA", 28, "2021-05-10"),
("Bob", "France", 34, "2020-07-22"),
("Charlie", "India", 25, "2022-01-12"),
("Diana", "Germany", 30, "2019-03-18");
```
## Example Requests
### SQL Query
### Request:

json
```
{
  "question": "Show me all customers from USA and India.",
  "source": "db"
}
```
### Response:

json
```
{
  "intent": "sql",
  "natural_question": "Show me all customers from USA and India.",
  "generated_sql": "SELECT * FROM customers WHERE country IN ('USA', 'India');"
}
```
## Document Query
### Request:

json
```
{
  "question": "What is the main topic of the sample PDF?",
  "source": "docs"
}
```
### Response:

json
```
{
  "intent": "rag",
  "query": "What is the main topic of the sample PDF?",
  "answer": "The main topic of the sample PDF is ..."
}
```

### Setup & Installation
## Clone the repository:

bash

```
git clone https://github.com/ssprasad-cyber/nlqs.git
cd nlqs
```
## Create and activate a virtual environment:

bash
```
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
Install dependencies:
```
bash
```
pip install -r requirements.txt
Set environment variables:
```
bash
```
export GROQ_API_KEY="your_groq_api_key"
# or for Windows PowerShell
$env:GROQ_API_KEY="your_groq_api_key"
Run the FastAPI server:
```

bash
```
uvicorn app.main:app --reload
```
Access the interactive API docs at http://localhost:8000/docs

## Notes
- The SQL translation relies on a Groq LLM API key and endpoint.

- Document QA requires a pre-built vector store with documents indexed.

- Intent classification is keyword-based and can be improved with an LLM classifier.

- SQL queries are cleaned to remove formatting artifacts before execution.

- Error handling is implemented for invalid SQL and unsupported queries.

## Future Work
- Improve intent classification using an LLM.

- Enhance error handling and feedback.

- Support more complex database schemas.

- Add user authentication and request logging.

- Integrate asynchronous execution for database and vector queries.

- Expand document vector store with more diverse data.

## License
MIT License

