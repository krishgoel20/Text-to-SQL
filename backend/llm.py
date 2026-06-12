from groq import Groq
from dotenv import load_dotenv
import os
import re

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_sql(question: str, schema: str) -> str:
    prompt = f"""You are an expert SQL developer. A user has a MySQL database with the following schema:

{schema}

The user asks: "{question}"

Write a single valid MySQL SELECT query that answers the question.
Rules:
- Return ONLY the SQL query, nothing else
- Do not include any explanation or markdown
- Do not wrap it in backticks or code blocks
- You may generate SELECT, INSERT, or UPDATE statements only
- Never generate DELETE or DROP statements under any circumstances
- Use only the tables and columns that exist in the schema above
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    sql = response.choices[0].message.content.strip()
    sql = re.sub(r"```(?:sql)?", "", sql).strip()
    return sql