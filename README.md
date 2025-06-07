
# 🧠 NLQS: Natural Language Query System

NLQS (Natural Language Query System) allows users to query both structured and unstructured data using natural language. It intelligently determines whether a user query requires SQL translation or retrieval-augmented generation (RAG) and then returns a structured, formatted result.

---

## 📌 Project Goals

- Convert natural language questions into SQL queries or document answers.
- Provide seamless access to structured databases and unstructured documents.
- Deliver results in readable formats: tables, charts, and markdown.
- Support integration with UI frameworks and API layers.

---

## 🧩 Architecture Overview

### 📊 Components and Tools

![NLQS Architecture Diagram](./assets/architecture-diagram.png)

1. **User Interface**
   - Frontend built with **React** or **Streamlit**.
   - Allows users to input natural language queries.

2. **API Gateway Layer**
   - Powered by **FastAPI**, **LangServe**, or **Vercel Edge**.
   - Acts as the entry point for external requests.

3. **Query Validator & Executor**
   - Handles SQL execution and RAG-based answers.
   - Supports both **structured** (database) and **unstructured** (documents) queries.

4. **NLQS Orchestration Engine**
   - Responsible for:
     - Intent Classification
     - Prompt Construction
     - SQL Translation (LLM-based)
   - Acts as the decision-maker for which processing path to take.

5. **Response Formatter**
   - Converts query results into JSON, Markdown, or tabular formats.

6. **Final UI Renderer**
   - Displays final output using tables, CSV downloads, or chart components.

---

### 🧠 Orchestration Engine Flow

![NLQS Orchestration Flowchart](./assets/orchestration-flowchart.png)

1. **Intent Detection**: 
   - Identifies whether the query is SQL-based or document-based.
2. **SQL Path**:
   - Passes through SQL generator → executed on database → returns structured response.
3. **RAG Path**:
   - Passes through LLM + vector DBs like **LlamaIndex** or **LangChain** → returns contextual document answer.

---

## ⚙️ Tech Stack

| Layer                 | Technology           | Why Chosen                                       |
|----------------------|----------------------|--------------------------------------------------|
| Frontend             | React / Streamlit    | Fast rendering and interactive UX                |
| Backend              | FastAPI              | High performance and asynchronous API support    |
| Orchestration        | Python, LangChain    | Flexibility with LLM tools and RAG workflows     |
| Embeddings           | HuggingFace Models   | Local model control and cost efficiency          |
| LLM Translation      | Groq API             | Fast, affordable, and OpenAI-compatible          |
| PDF Processing       | PyMuPDF              | Lightweight and efficient for unstructured docs  |
| Database             | SQLite               | Simple for prototyping structured queries        |

---

## 🚀 How It Works

1. **User Inputs Question** (via UI)
2. **Intent is Classified** as either SQL or Document (RAG)
3. **SQL**:
   - Converts NL → SQL using Groq or OpenAI
   - Executes SQL query and returns rows
4. **RAG**:
   - Retrieves relevant chunks from embedded documents
   - Uses LangChain or LlamaIndex to generate the answer
5. **Formatter**: Output is presented as JSON / Markdown / Table

---

## 🛠️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/nlqs.git
cd nlqs
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

> Ensure Python 3.10+ is used.

### 3. Environment Variables

Create a `.env` file with the following:

```
OPENAI_API_KEY=your-api-key
GROQ_API_KEY=your-groq-api-key
```

### 4. Start Server

```bash
uvicorn app.main:app --reload
```

---

## 📡 API Endpoints

| Method | Endpoint       | Description                        |
|--------|----------------|------------------------------------|
| POST   | `/api/query`   | Accepts a natural language question |
| Body   | `{ "question": "..." }` | |

**Sample Request:**

```json
{
  "question": "List all customers from USA and India"
}
```

**Sample Response:**

```json
{
  "query_type": "sql",
  "sql_query": "SELECT * FROM customers WHERE country IN ('USA', 'India');",
  "result": {
    "columns": ["id", "name", "country", "age", "signup_date"],
    "rows": [[1, "Alice", "USA", 28, "2021-05-10"], [3, "Charlie", "India", 25, "2022-01-12"]],
    "summary": "2 rows returned."
  }
}
```

---

## 💡 Future Improvements

- ✅ Add support for multiple file types (PDF, DOCX, HTML).
- ✅ Use advanced LLMs (Groq, Claude, Gemini) as fallbacks.
- 🔄 Integrate user authentication and usage limits.
- 📊 Build dashboard to monitor and visualize query activity.
- 🔍 Improve intent classifier using a fine-tuned LLM model.
- 📚 Add document chunking and hybrid search scoring.

---

## 👨‍💻 Contributing

Contributions welcome! Please open issues or pull requests for improvements.

---

## 📄 License

MIT License © 2025

---
