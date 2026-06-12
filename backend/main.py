from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from database import get_schema, run_query, seed_database
from llm import generate_sql

load_dotenv()

app = FastAPI(title="Text-to-SQL API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
async def startup_event():
    seed_database()
    print("App is ready!")

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Text-to-SQL API is running"}

@app.get("/schema")
def fetch_schema():
    try:
        schema = get_schema()
        return {"schema": schema}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
def query(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    try:
        schema = get_schema()
        sql = generate_sql(request.question, schema)
        result = run_query(sql)
        if result["type"] == "select":
            return {
                "question": request.question,
                "sql": sql,
                "type": "select",
                "columns": result["columns"],
                "rows": result["rows"]
            }
        else:
            return {
                "question": request.question,
                "sql": sql,
                "type": "modify",
                "affected_rows": result["affected_rows"]
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))