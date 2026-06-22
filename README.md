# Text-to-SQL Engine

A full-stack AI-powered web application that converts plain English questions/requests into SQL queries and executes them on a live MySQL database in real time.

---

## What it does

- Type a question/request in plain English
- The LLM generates the appropriate SQL query using live database schema
- The query executes on a MySQL database
- Results are displayed in a clean table

Supports SELECT, INSERT, and UPDATE queries.
DELETE and DROP are blocked for safety.

---

## Tech Stack

| Layer    | Technology                        |
|----------|-----------------------------------|
| Backend  | Python, FastAPI                   |
| AI / LLM | Groq API (llama-3.1-8b-instant)   |
| Database | MySQL                             |
| Frontend | HTML, CSS, JS                     |

---

## How it works

```
User question/request
↓
FastAPI receives the question/request
↓
database.py extracts live MySQL schema
↓
llm.py injects schema + question/request into Groq prompt
↓
LLM returns a SQL query
↓
Python executes the query on MySQL
↓
Result displayed as a table in the UI
```

---

## Project Structure

```
text-to-sql/
├── backend/
│   ├── main.py          # FastAPI app, routes, startup seeding
│   ├── database.py      # MySQL connection, schema extractor,
│   │                    # query runner, seed function
│   ├── llm.py           # Groq API call, SQL generator
│   ├── .env             # API keys and DB credentials (not committed)
│   └── requirements.txt
└── frontend/
├── index.html       # App structure
├── style.css        # Dark theme styling
└── script.js        # API calls, table rendering
```

---

## Setup and Installation

### Prerequisites
- Python 3.10+
- MySQL Community Server
- Groq API key (free at https://console.groq.com)

### 1. Clone the repository

```bash
git clone https://github.com/krishgoel20/text-to-sql.git
cd text-to-sql
```

### 2. Set up the backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file inside the `backend/` folder:

```
GROQ_API_KEY=your_groq_api_key_here
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=ecommerce_db
```

### 4. Run the backend

```bash
uvicorn main:app --reload
```

The database is created and seeded automatically on startup.
No manual SQL setup required.

### 5. Open the frontend

```bash
cd ../frontend
python -m http.server 5500
```

Visit **http://localhost:5500** in your browser.

---

## Sample Queries to Try

```
Show all customers from Mumbai.
Which products cost more than 10000?
Show all electronics products.
What is the total amount of all orders?
Which customer placed the most orders?
Add a new customer named John Doe from Delhi with email john@gmail.com.
Update Amit Sharma's city to Bengaluru.
```

---

## Key Concepts Demonstrated

- **Prompt engineering** — live schema is injected into every LLM prompt
  so the model always generates schema-aware SQL
- **Schema-aware querying** — the app reads the actual database structure
  at runtime, not hardcoded table names
- **Database seeding** — entire database builds itself from Python code
  on every server start, no manual setup needed
- **Full-stack integration** — FastAPI backend, MySQL database,
  and vanilla JS frontend working together
- **Safety guardrails** — DELETE and DROP statements are blocked
  at the prompt level

---

## Limitations

- Same question/request may produce different SQL queries on different runs
  due to LLM non-determinism
- No query history stored between sessions
- Not deployed (runs locally only)

---
